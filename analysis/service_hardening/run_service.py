"""Service wrapper for the onboard mission application (D2.12).

Loads configuration, initializes logging, manages the systemd watchdog,
handles graceful shutdown (SIGTERM/SIGINT → LAND), and provides a safe
stand-down thread for crash recovery.

Designed to be invoked by systemd as ``ExecStart``::

    ExecStart=/usr/bin/python3 /opt/mission_app/run_service.py

Usage from command line (testing / SITL)::

    python3 run_service.py --config /path/to/config.yaml

"""

from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import threading
import time
import traceback
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Try sd_notify (optional — systemd 229+).  Falls back to a no-op on
# platforms where ctypes can't load libsystemd (e.g. macOS/Windows).
# ---------------------------------------------------------------------------
_HAS_SD_NOTIFY = False
try:
    import ctypes
    import ctypes.util

    _lib = ctypes.util.find_library("systemd")
    if _lib is not None:
        _sd = ctypes.CDLL(_lib, use_errno=True)
        _sd.sd_notify.argtypes = [ctypes.c_int, ctypes.c_char_p]
        _sd.sd_notify.restype = ctypes.c_int
        _HAS_SD_NOTIFY = True
except Exception:
    pass


def sd_notify(state: str) -> None:
    if _HAS_SD_NOTIFY:
        _sd.sd_notify(0, state.encode("utf-8"))


# ---------------------------------------------------------------------------
# Import the mission application and logging module (sibling files)
# ---------------------------------------------------------------------------
# We add the `analysis/service_hardening/` directory to sys.path so the
# service can import its siblings even when launched from a different cwd.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

# Also add the autonomy_sim directory so we can import MissionApp
_AUTONOMY_DIR = _HERE.parent / "autonomy_sim"

from mission_app_logging import get_logger, setup_logging

# ---------------------------------------------------------------------------
# Config loader
# ---------------------------------------------------------------------------

def load_config(path: str) -> dict[str, Any]:
    """Load a YAML or JSON config file.

    YAML is preferred (supports comments).  Falls back to JSON if PyYAML
    is not installed or the file is `.json`.
    """
    p = Path(path)
    raw = p.read_text(encoding="utf-8")

    if p.suffix in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore[import-untyped]
            cfg = yaml.safe_load(raw)
        except ImportError:
            # Fallback: parse as JSON.  YAML-on-JSON-safe is limited but
            # works for simple dicts.
            import json as _json
            cfg = _json.loads(raw)
    elif p.suffix == ".json":
        cfg = json.loads(raw)
    else:
        raise ValueError(f"Unknown config format: {p.suffix}")

    if not isinstance(cfg, dict):
        raise ValueError("Config must be a top-level mapping")

    return cfg


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge `override` into `base` (mutates and returns `base`).

    A nested-dict value merges key-by-key instead of replacing the whole
    dict, so a dev/SITL override that touches one key of e.g. `mavlink`
    (exactly the pattern shown in mission_app_config.yaml's own SITL
    example) doesn't silently drop its untouched sibling keys.
    """
    for key, val in override.items():
        if isinstance(val, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], val)
        else:
            base[key] = val
    return base


def merge_config(*paths: str) -> dict[str, Any]:
    """Load multiple config files and deep-merge them.

    Later files override earlier ones, key-by-key (recursively for nested
    mappings). The last file is typically ``/etc/mission_app/config.dev.yaml``
    for SITL / development overrides.
    """
    merged: dict[str, Any] = {}
    for p in paths:
        part = load_config(p)
        _deep_merge(merged, part)
    return merged


# ---------------------------------------------------------------------------
# Safe stand-down thread
# ---------------------------------------------------------------------------

class SafeStandDown(threading.Thread):
    """Daemon thread that drives the aircraft to LAND if the main loop dies.

    The main loop signals ``_alive`` every tick.  If the timeout elapses
    without a pulse, this thread opens a *separate* MAVLink connection to
    the FC and sends:
      1. GUIDED mode
      2. LAND mode, repeated a few times a second apart

    There is no ACK verification on this link (contrast with
    ``MissionApp._service_mode``'s ACK+retry loop on the primary link) --
    repeating LAND a few times is a cheap best-effort hedge against losing
    a single command on what may itself be a degraded link, not a
    guarantee of delivery.

    ``_alive`` uses a :class:`threading.Event` with a ``wait()`` timeout so
    this thread is not busy-waiting::

        heartbeat: wait(heartbeat_timeout_s) → timeout → fire stand-down

    If the main loop exits normally (success or graceful shutdown), it sets
    ``_alive`` permanently so this thread never fires.
    """

    def __init__(
        self,
        connection_string: str,
        baudrate: int,
        target_system: int = 1,
        heartbeat_timeout_s: float = 15.0,
        source_component: int = 191,
        connection_factory: Optional[Any] = None,
    ):
        super().__init__(daemon=True, name="safe-stand-down")
        self._conn_str = connection_string
        self._baud = baudrate
        self._target = target_system
        self.timeout_s = heartbeat_timeout_s
        self._src_comp = source_component
        # Injectable for tests; defaults to a real pymavlink connection.
        self._connection_factory = connection_factory
        self._alive = threading.Event()
        self._alive.set()  # starts "alive"; cleared → fire stand-down
        self._stopped = threading.Event()   # set by disarm(): stop before firing
        self._fired = threading.Event()     # set once a stand-down attempt is done
        self._log: Optional[Any] = None

    def set_logger(self, log: Any) -> None:
        self._log = log

    def kick(self) -> None:
        """Signal that the main loop is still alive."""
        self._alive.set()

    def disarm(self) -> None:
        """Permanently disable stand-down (used on graceful exit).

        Sets both flags: ``_stopped`` so the run loop exits instead of
        firing, and ``_alive`` so a thread currently blocked in ``wait()``
        wakes immediately to observe ``_stopped`` rather than sitting out
        the rest of the timeout window.
        """
        self._stopped.set()
        self._alive.set()

    def wait_for_fired(self, timeout: Optional[float] = None) -> bool:
        """Block until a stand-down attempt has completed (or `timeout`)."""
        return self._fired.wait(timeout=timeout)

    def run(self) -> None:
        log = self._log or get_logger("safe-stand-down")

        while not self._stopped.is_set():
            pulsed = self._alive.wait(timeout=self.timeout_s)
            self._alive.clear()

            if self._stopped.is_set():
                # disarm() raced with (or preempted) a real timeout -- a
                # graceful shutdown always wins over a false-positive fire.
                return

            if pulsed:
                continue  # got a pulse before the timeout; keep watching

            # Timeout — main loop appears dead
            log.critical("Main loop heartbeat timeout — initiating safe stand-down")
            try:
                self._safe_land(log)
            except Exception:
                log.critical("Safe-stand-down failed",
                             extra={"error": str(traceback.format_exc())})
            finally:
                self._fired.set()
            return

    def _safe_land(self, log: Any) -> None:
        from pymavlink import mavutil

        if self._connection_factory is not None:
            conn = self._connection_factory()
        else:
            # Open a fresh MAVLink connection (don't touch the possibly-
            # corrupt main loop's connection).
            conn = mavutil.mavlink_connection(
                self._conn_str,
                baud=self._baud,
                source_system=self._target,
                source_component=self._src_comp,
                dialect="ardupilotmega",
            )
        # Wait up to 5 s for a heartbeat from the FC
        conn.wait_heartbeat(timeout=5)
        log.critical("Stand-down FC heartbeat received — sending LAND sequence")

        # GUIDED first, then LAND via set_mode_send -- the same mechanism
        # already proven against real SITL elsewhere in this codebase
        # (MissionApp._set_mode / analysis/sitl_tests). Commanding LAND via a
        # MAV_CMD_NAV_LAND COMMAND_LONG from an arbitrary prior mode is not
        # the path this project has validated, so this thread deliberately
        # uses the same mechanism as everything else instead of a novel one.
        conn.mav.set_mode_send(
            self._target,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            4,  # GUIDED
        )
        time.sleep(1)
        # No ACK verification on this link -- repeat LAND a few times a
        # second apart as a best-effort hedge against losing a single
        # command (see the class docstring).
        for _ in range(3):
            conn.mav.set_mode_send(
                self._target,
                mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                9,  # LAND
            )
            time.sleep(1)
        log.critical("Stand-down LAND mode commanded")
        conn.close()


# ---------------------------------------------------------------------------
# Signal handling
# ---------------------------------------------------------------------------

_shutdown_requested = threading.Event()


def _signal_handler(signum: int, _frame) -> None:
    _shutdown_requested.set()


# ---------------------------------------------------------------------------
# App construction (pulled out of main() so it's unit-testable without a
# real FC connection or systemd environment)
# ---------------------------------------------------------------------------

def build_detector(inference_cfg: dict[str, Any], log: Any):
    """Build the Detector the mission app will use, from the `inference:`
    config section. Falls back to ScriptedDetector (dev/SITL) if no model
    path is configured, the path doesn't exist, or the RKNN wrapper (D2.6)
    isn't importable yet."""
    from mission_app import ScriptedDetector

    detector_path = inference_cfg.get("model_path", "")
    if detector_path and os.path.exists(detector_path):
        # D2.6 RKNN wrapper — import it dynamically so the service doesn't
        # crash if the wrapper module doesn't exist yet.
        try:
            from mission_app_rknn import RK2288Detector  # type: ignore[import-untyped]
            detector = RK2288Detector(
                model_path=detector_path,
                conf_threshold=inference_cfg.get("confidence_threshold", 0.45),
                iou_threshold=inference_cfg.get("iou_threshold", 0.50),
            )
            log.info("RKNN detector loaded", extra={"model_path": detector_path})
            return detector
        except ImportError:
            log.warning("RKNN wrapper not available; using ScriptedDetector")
            return ScriptedDetector()

    act = f"Path '{detector_path}' not found" if detector_path else "No model_path configured"
    log.info(f"Using ScriptedDetector ({act})")
    return ScriptedDetector()


def build_mission_app(config: dict[str, Any], conn: Any, detector: Any, target_sys: int):
    """Construct the MissionApp from the merged config + an open connection."""
    from mission_app import MissionApp

    mission_cfg = config.get("mission", {})
    battery_cfg = config.get("battery_rtl", {})
    battery_capacity_mah = battery_cfg.get("capacity_mah") if battery_cfg.get("enabled", True) else None

    return MissionApp(
        conn=conn,
        detector=detector,
        target_system=target_sys,
        detect_thr=mission_cfg.get("detect_threshold", 0.90),
        classify_thr=mission_cfg.get("classify_threshold", 0.80),
        classify_timeout_ticks=mission_cfg.get("classify_timeout_ticks", 40),
        loiter_time_budget_s=mission_cfg.get("loiter_time_budget_s", 30.0),
        battery_capacity_mah=battery_capacity_mah,
        rtl_margin_fraction=battery_cfg.get("margin_fraction", 0.10),
        rtl_climb_energy_j=battery_cfg.get("climb_energy_j", 0.0),
        rtl_power_ema_alpha=battery_cfg.get("power_ema_alpha", 0.1),
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Mission App Service Wrapper")
    parser.add_argument(
        "--config", "-c",
        default="/etc/mission_app/config.yaml",
        help="Path to the config file (default: /etc/mission_app/config.yaml)",
    )
    parser.add_argument(
        "--dev-config",
        help="Optional dev-override config file (loaded second, keys override main)",
    )
    parser.add_argument(
        "--sitl",
        action="store_true",
        help="Shortcut: equivalent to --dev-config pointing at sitl_config.yaml",
    )
    args = parser.parse_args()

    # ---- Load config ------------------------------------------------------
    config_paths = [args.config]
    if args.sitl:
        sitl_path = str(_HERE / "sitl_config.yaml")
        if os.path.exists(sitl_path):
            config_paths.append(sitl_path)
        else:
            print(f"[warn] SITL flag set but {sitl_path} not found; using defaults",
                  file=sys.stderr)
    if args.dev_config:
        config_paths.append(args.dev_config)

    config = merge_config(*config_paths)

    # ---- Logging ----------------------------------------------------------
    log_cfg = config.get("logging", {})
    setup_logging(
        level=log_cfg.get("level", "INFO"),
        file_path=log_cfg.get("file_path"),
        max_bytes=log_cfg.get("max_bytes", 10 * 1024 * 1024),
        backup_count=log_cfg.get("backup_count", 5),
        fmt=log_cfg.get("format", "json"),
        forward_to_journal=log_cfg.get("forward_to_journal", True),
    )
    log = get_logger("service")

    # ---- Signal handlers --------------------------------------------------
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)
    log.info("Signal handlers registered")

    # ---- Notify systemd: starting -----------------------------------------
    sd_notify("STATUS=Starting mission app")
    log.info("Loading configuration complete",
             extra={"config_paths": json.dumps(config_paths)})

    # ---- MAVLink connection -----------------------------------------------
    mav_cfg = config.get("mavlink", {})
    conn_str = mav_cfg.get("connection_string", "/dev/ttyS2")
    baud = mav_cfg.get("baudrate", 921600)
    target_sys = mav_cfg.get("target_system", 1)
    src_comp = mav_cfg.get("source_component", 191)

    # Startup delay (let the FC boot before we connect)
    startup_delay = config.get("system", {}).get("startup_delay_s", 5)
    if startup_delay > 0:
        log.info(f"Waiting {startup_delay}s for FC to boot", extra={"delay_s": startup_delay})
        time.sleep(startup_delay)

    try:
        from pymavlink import mavutil
        conn = mavutil.mavlink_connection(
            conn_str,
            baud=baud,
            source_system=target_sys,
            source_component=src_comp,
            dialect="ardupilotmega",
        )
        log.info("MAVLink connection opened",
                 extra={"connection": conn_str, "baud": baud})

        # Wait for a first heartbeat from the FC (timeout = 10 s)
        if conn.wait_heartbeat(timeout=10) is None:
            log.warning("No FC heartbeat received within 10 s — continuing anyway")
        else:
            log.info("FC heartbeat received",
                     extra={"src_system": conn.target_system,
                            "src_component": conn.target_component})
    except Exception as exc:
        log.critical("Failed to open MAVLink connection",
                     extra={"error": str(exc), "traceback": traceback.format_exc()})
        sd_notify("STATUS=MAVLink connect failed")
        sys.exit(1)

    # ---- Build the mission app ---------------------------------------------
    inference_cfg = config.get("inference", {})
    system_cfg = config.get("system", {})

    # Import the core MissionApp here (after logging is ready). This also
    # allows the module to be imported even if the RKNN detector isn't
    # available yet — build_detector() falls back to ScriptedDetector.
    sys.path.insert(0, str(_AUTONOMY_DIR))

    detector = build_detector(inference_cfg, log)
    app = build_mission_app(config, conn, detector, target_sys)
    log.info("MissionApp instantiated")

    # ---- Safe stand-down thread -------------------------------------------
    stand_cfg = system_cfg.get("safe_standdown", {})
    stand = SafeStandDown(
        connection_string=stand_cfg.get(
            "connection_string",
            system_cfg.get("safe_standdown_connection_string", conn_str)),
        baudrate=stand_cfg.get(
            "baud",
            system_cfg.get("safe_standdown_baud", 9600)),
        target_system=target_sys,
        heartbeat_timeout_s=stand_cfg.get("heartbeat_timeout_s", 15.0),
        source_component=src_comp,
    )
    stand.set_logger(log)
    stand.start()
    log.info("Safe stand-down thread started",
             extra={"timeout_s": stand.timeout_s})

    # ---- Notify systemd: ready --------------------------------------------
    sd_notify("READY=1")
    sd_notify("STATUS=Running sweep-and-detect loop")
    log.info("Entering main loop")

    # ---- Main loop --------------------------------------------------------
    tick_hz = 50.0
    dt = 1.0 / tick_hz
    watchdog_interval = system_cfg.get("watchdog_interval_s", 10)
    # Guard against a misconfigured 0 (or negative) interval turning into a
    # `_tick % 0` ZeroDivisionError every tick.
    watchdog_ticks = max(1, int(tick_hz * watchdog_interval))
    _tick = 0

    try:
        # Initial heartbeat
        app.send_heartbeat()
        log.info(f"Initial heartbeat sent (src={src_comp})")

        while not _shutdown_requested.is_set():
            _tick += 1

            app.send_heartbeat() if _tick % int(tick_hz) == 0 else None
            app.step()

            # systemd watchdog: pulse every `watchdog_interval_s` seconds
            if _tick % watchdog_ticks == 0:
                sd_notify("WATCHDOG=1")
                sd_notify(f"STATUS=state={app.state} mode={app.fc_mode}")

            # Safe stand-down heartbeat
            stand.kick()

            if app.state == app.PASSIVE:
                log.info("Passive state — FC has taken over (failsafe or RTL)")
                # Sleep longer when passive to reduce CPU
                time.sleep(1.0)
            else:
                time.sleep(dt)

        # ---- Graceful shutdown --------------------------------------------
        log.info("Shutdown requested — initiating graceful descent")
        sd_notify("STATUS=Shutting down")

        # Stand down: return to LAND (or RTL) before exiting
        try:
            # `is not None` matters here: STABILIZE is mode 0, which is
            # falsy in Python -- a bare `if app.fc_mode` would silently skip
            # commanding LAND whenever the FC happened to be in STABILIZE.
            if app.fc_mode is not None and app.fc_mode not in (6, 9):  # not already RTL/LAND
                app._alert("Shutdown requested, returning to land")
                app._set_mode("LAND")
                # Give the FC time to process
                for _ in range(20):
                    app.step()
                    time.sleep(0.1)
        except Exception as exc:
            log.warning("Shutdown mode-set failed, exiting anyway",
                        extra={"error": str(exc)})

        # Disarm safe-stand-down so it doesn't fire while we exit
        stand.disarm()
        conn.close()
        log.info("Graceful shutdown complete")
        sd_notify("STOPPING=1")

    except Exception as exc:
        log.critical("Unhandled exception in main loop",
                     extra={
                         "error": str(exc),
                         "traceback": traceback.format_exc(),
                         "state": app.state if app else "N/A",
                         "fc_mode": app.fc_mode if app else "N/A",
                     })
        sd_notify("STATUS=Crash — safe stand-down active")
        # The safe-stand-down thread will handle landing, but it is a daemon
        # thread: the interpreter kills daemon threads outright at process
        # exit without waiting for them. Block until it reports the stand-
        # down attempt finished (bounded by its own heartbeat timeout plus a
        # margin for the LAND command round-trip) instead of a fixed short
        # sleep, or `sys.exit()` here would race the very thread this
        # handler exists to give time to.
        fired = stand.wait_for_fired(timeout=stand.timeout_s + 10)
        if not fired:
            log.critical("Safe stand-down did not complete before exit timeout",
                         extra={"timeout_s": stand.timeout_s + 10})
        sys.exit(1)


if __name__ == "__main__":
    main()
