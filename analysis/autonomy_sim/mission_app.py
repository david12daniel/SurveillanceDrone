"""Onboard mission application skeleton — the SBC autonomy loop.

This is the executable counterpart of the two UC-5 halves in behavior.sysml
(SweepAndDetect / InvestigateAndClassify) and the FlightMode state machine.
It drives an ArduPilot flight controller over MAVLink; the thermal detector is
injected (mock now, RKNN model later), so this file validates the *control
contract* (the AUTO->GUIDED->AUTO loop) independently of the CV model.

Model traceability (behavior.sysml / MODEL_ISSUES.md §C25):
  state SWEEP        <-> FlightMode.flying.cruise, do = SweepAndDetect
  state INVESTIGATE  <-> FlightMode.flying.loiter, do = InvestigateAndClassify
  detect >= 0.90     <-> SweepAndDetect `decide detected` (R3_1)
  send TargetDetected        <-> mode AUTO->GUIDED  (this file: _set_mode GUIDED)
  classify >= 0.80   <-> InvestigateAndClassify `decide classified` (R3_2)
  send InvestigationComplete <-> mode GUIDED->AUTO  (this file: _set_mode AUTO)
  FC-commanded RTL   <-> FlightMode flying->returnToLaunch (external trigger)
"""
from __future__ import annotations
import time
from typing import Protocol
from pymavlink import mavutil

from battery_rtl_trigger import BatteryRTLMonitor, RTLTriggerConfig
from energy_model import pack_voltage_v

# ArduCopter custom flight-mode numbers (verify against your firmware build).
MODE = {"STABILIZE": 0, "AUTO": 3, "GUIDED": 4, "LOITER": 5, "RTL": 6, "LAND": 9}
MODE_NAME = {v: k for k, v in MODE.items()}
_FAILSAFE_MODES = {MODE["RTL"], MODE["LAND"]}

# D2.17 fallbacks, used only until the real PARAM_VALUE arrives from the FC
# (see MissionApp._pump()'s PARAM_VALUE handling) -- ArduCopter's own stock
# defaults, not project-specific numbers.
_DEFAULT_RETURN_SPEED_MPS = 5.0   # stock WPNAV_SPEED = 500 cm/s
_DEFAULT_RTL_ALT_M = 15.0         # stock RTL_ALT = 1500 cm

SURVEY_ALT_M = 120.0      # R1 sweep altitude
CLASSIFY_ALT_M = 90.0     # R3_2 recognition altitude


class Detector(Protocol):
    """Thermal-inference interface. Mock in tests; RKNN-backed in the real build."""
    def detect(self) -> float: ...                 # SweepAndDetect: detection confidence 0..1
    def classify(self) -> tuple[str, float]: ...   # InvestigateAndClassify: (species, confidence)


class MissionApp:
    SWEEP, INVESTIGATE, PASSIVE = "SWEEP", "INVESTIGATE", "PASSIVE"

    def __init__(self, conn, detector: Detector, *, target_system: int = 1,
                 detect_thr: float = 0.90, classify_thr: float = 0.80,
                 classify_timeout_ticks: int = 40,
                 loiter_time_budget_s: float = 30.0,
                 battery_capacity_mah: float | None = None,
                 rtl_margin_fraction: float = 0.10,
                 rtl_climb_energy_j: float = 0.0,
                 rtl_power_ema_alpha: float = 0.1):
        self.conn = conn
        self.detector = detector
        self.target_system = target_system
        self.detect_thr = detect_thr            # R3_1
        self.classify_thr = classify_thr        # R3_2
        self.classify_timeout_ticks = classify_timeout_ticks
        self.loiter_time_budget_s = loiter_time_budget_s   # D2.9: 30 s loiter budget (task 0.4)
        self._investigate_start: float | None = None         # wall-clock entry time of INVESTIGATE
        self.state = self.SWEEP
        self.fc_mode: int | None = None
        self.position: tuple[int, int, float] | None = None  # lat_e7, lon_e7, rel_alt_m
        self._classify_ticks = 0
        self.events: list[tuple[str, str]] = []               # (kind, detail) — for logging/assertions
        self._boot = time.time()

        # D2.17: distance-adaptive low-battery RTL trigger (a tighter, earlier
        # layer in front of the FC's own static BATT_CRT_MAH backstop -- see
        # battery_rtl_trigger.py). battery_capacity_mah is the feature flag:
        # leave it None (default) to disable, matching every existing caller/
        # test that doesn't configure a pack and doesn't drive HOME_POSITION/
        # BATTERY_STATUS through FakeFC.
        self._battery_capacity_mah = battery_capacity_mah
        self._rtl_config_extra = dict(
            margin_fraction=rtl_margin_fraction,
            climb_energy_j=rtl_climb_energy_j,
            power_ema_alpha=rtl_power_ema_alpha,
        )
        self._home: tuple[float, float] | None = None          # (lat_deg, lon_deg)
        self._battery: tuple[float, float, float] | None = None  # (current_a, voltage_v, consumed_mah)
        self._return_speed_mps = _DEFAULT_RETURN_SPEED_MPS     # overridden by RTL_SPEED/WPNAV_SPEED PARAM_VALUE
        self._rtl_alt_m = _DEFAULT_RTL_ALT_M                    # overridden by RTL_ALT PARAM_VALUE
        self._rtl_monitor: BatteryRTLMonitor | None = None
        self._requested_rtl_params = False

    # ---- MAVLink out ------------------------------------------------------
    def _ms(self) -> int:
        return int((time.time() - self._boot) * 1000)

    def send_heartbeat(self):
        # Companion computer heartbeat so the FC (or mock) learns our address.
        self.conn.mav.heartbeat_send(
            mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER,
            mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)

    def _set_mode(self, mode_name: str):
        self.conn.mav.set_mode_send(
            self.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            MODE[mode_name])
        self.events.append(("set_mode", mode_name))

    def _alert(self, text: str, severity: int = mavutil.mavlink.MAV_SEVERITY_NOTICE):
        self.conn.mav.statustext_send(severity, text.encode("utf-8")[:50])
        self.events.append(("statustext", text))

    def _command_descent(self, lat_e7: int, lon_e7: int, alt_m: float):
        # GUIDED position target: hold lat/lon, command target altitude (descend).
        # type_mask = 3576 (0b0000110111111000): x/y/z used, vel/accel ignored,
        # yaw/yaw_rate ignored -- ArduPilot's own documented "position only"
        # mask. An earlier version of this mask also set bit 9
        # (POSITION_TARGET_TYPEMASK_FORCE_SET, giving 4088/0b0000111111111000)
        # -- a common copy-paste artifact from example offboard-control code
        # where that bit isn't actually one of the "ignore" bits. Confirmed
        # against real ArduCopter 4.7.0 SITL (task D2.13/D2.15, 2026-08-11):
        # with bit 9 set, a same-lat/lon lower-altitude target never moved the
        # vehicle in Z at all -- this is the exact descend-to-classify call
        # this function exists for, so that bit being set would have silently
        # broken UC-5/InvestigateAndClassify's altitude change on real
        # hardware. See analysis/sitl_tests/helpers.py's send_position_target
        # for the same fix and the full investigation notes.
        type_mask = 0b0000110111111000
        self.conn.mav.set_position_target_global_int_send(
            self._ms(), self.target_system, 1,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            type_mask, lat_e7, lon_e7, alt_m,
            0, 0, 0, 0, 0, 0, 0, 0)
        self.events.append(("position_target", f"{alt_m:.0f}m"))

    def _request_param(self, param_id: str):
        self.conn.mav.param_request_read_send(
            self.target_system, 1, param_id.encode("utf-8"), -1)

    # ---- MAVLink in -------------------------------------------------------
    def _pump(self):
        while True:
            msg = self.conn.recv_match(blocking=False)
            if msg is None:
                return
            t = msg.get_type()
            if t == "HEARTBEAT" and msg.get_srcComponent() == mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1:
                self.fc_mode = msg.custom_mode
            elif t == "GLOBAL_POSITION_INT":
                self.position = (msg.lat, msg.lon, msg.relative_alt / 1000.0)
            elif t == "HOME_POSITION":
                self._home = (msg.latitude / 1e7, msg.longitude / 1e7)
            elif t == "BATTERY_STATUS":
                # D2.17 telemetry: current_battery (cA), current_consumed (mAh) are
                # -1 when the FC doesn't know yet -- ignore the sample until both
                # are populated rather than feeding the RTL monitor a bogus draw.
                if msg.current_battery >= 0 and msg.current_consumed >= 0:
                    voltage_v = pack_voltage_v(list(msg.voltages))
                    self._battery = (msg.current_battery / 100.0, voltage_v, float(msg.current_consumed))
            elif t == "PARAM_VALUE":
                param_id = msg.param_id if isinstance(msg.param_id, str) else msg.param_id.decode("utf-8")
                param_id = param_id.rstrip("\x00")
                # RTL_SPEED was renamed RTL_SPEED_MS on modern ArduCopter
                # (confirmed via a full PARAM_REQUEST_LIST dump against
                # 4.7.0, task D2.13, 2026-08-10 -- see
                # analysis/sitl_tests/params_sets.py's RTL_CRUISE). Accept
                # either name so this works across firmware versions.
                if param_id in ("RTL_SPEED", "RTL_SPEED_MS") and msg.param_value > 0:
                    self._return_speed_mps = msg.param_value / 100.0
                elif param_id == "WPNAV_SPEED":
                    # Fallback only -- ArduPilot uses WPNAV_SPEED for RTL when
                    # RTL_SPEED == 0. Don't let this overwrite an already-live
                    # nonzero RTL_SPEED/RTL_SPEED_MS that arrived first.
                    if self._return_speed_mps == _DEFAULT_RETURN_SPEED_MPS:
                        self._return_speed_mps = msg.param_value / 100.0
                elif param_id == "RTL_ALT":
                    self._rtl_alt_m = msg.param_value / 100.0

    # ---- state machine ----------------------------------------------------
    def step(self):
        self._pump()

        if self._battery_capacity_mah is not None and not self._requested_rtl_params:
            self._request_param("RTL_SPEED")
            self._request_param("RTL_SPEED_MS")
            self._request_param("WPNAV_SPEED")
            self._request_param("RTL_ALT")
            self._requested_rtl_params = True

        # External failsafe (LinkLossDetected / LowBatteryReached): the FC owns the
        # decision and switches to RTL/LAND on its own. We observe and stand down.
        if self.fc_mode in _FAILSAFE_MODES and self.state != self.PASSIVE:
            self.state = self.PASSIVE
            self.events.append(("failsafe_observed", MODE_NAME.get(self.fc_mode, "?")))
            return
        if self.state == self.PASSIVE:
            return

        # Need telemetry before acting (validates the FC link is live).
        if self.fc_mode is None or self.position is None:
            return

        # D2.17: distance-adaptive low-battery RTL trigger -- a second opinion
        # in front of the FC's static BATT_CRT_MAH backstop, recomputed every
        # tick from live distance-to-home + measured cruise power rather than
        # a fixed worst-case-distance reserve (see battery_rtl_trigger.py).
        # Cross-cutting like the failsafe check above: applies in SWEEP and
        # INVESTIGATE alike, so it runs before the state-specific branches.
        if self._battery_capacity_mah is not None and self._battery is not None:
            if self._rtl_monitor is None and self._home is not None:
                self._rtl_monitor = BatteryRTLMonitor(
                    self._home[0], self._home[1],
                    RTLTriggerConfig(
                        capacity_mah=self._battery_capacity_mah,
                        return_speed_mps=self._return_speed_mps,
                        **self._rtl_config_extra,
                    ),
                )
            if self._rtl_monitor is not None:
                lat, lon, alt = self.position
                current_a, voltage_v, consumed_mah = self._battery
                fired = self._rtl_monitor.update(
                    lat=lat / 1e7, lon=lon / 1e7,
                    below_rtl_alt=alt < self._rtl_alt_m,
                    current_a=current_a, voltage_v=voltage_v, consumed_mah=consumed_mah,
                )
                if fired:
                    d = self._rtl_monitor.last_diagnostics
                    self._alert(f"BATTERY_RTL dist={d['distance_to_home_m']:.0f}m "
                                f"need={d['energy_needed_j'] / 3600:.0f}Wh "
                                f"have={d['remaining_energy_j'] / 3600:.0f}Wh")
                    self._set_mode("RTL")
                    self.state = self.PASSIVE
                    self.events.append(("battery_rtl_triggered", f"{d['distance_to_home_m']:.0f}m"))
                    return

        if self.state == self.SWEEP:
            if self.fc_mode != MODE["AUTO"]:
                return  # only sweep while flying the route
            if self.detector.detect() >= self.detect_thr:            # R3_1
                lat, lon, _ = self.position
                self._alert(f"DETECT {lat/1e7:.5f},{lon/1e7:.5f}")   # geotag POI alert
                self._set_mode("GUIDED")                              # send TargetDetected
                self._command_descent(lat, lon, CLASSIFY_ALT_M)      # descend 120->90 m
                self._classify_ticks = 0
                self._investigate_start = time.time()                # D2.9: start the loiter budget clock
                self.state = self.INVESTIGATE

        elif self.state == self.INVESTIGATE:
            self._classify_ticks += 1
            species, conf = self.detector.classify()                 # R3_2
            if conf >= self.classify_thr:
                self._alert(f"CLASSIFY {species} {conf:.2f}")
                self._set_mode("AUTO")                                # send InvestigationComplete
                self.state = self.SWEEP
            # D2.9: outer loiter time budget (task 0.4) — 30 s wall-clock per
            # investigation, then log-as-unclassified and resume. The inner
            # classify_timeout_ticks (0.8 s) still bounds per-aspect sampling.
            loiter_elapsed = time.time() - (self._investigate_start or time.time())
            if loiter_elapsed >= self.loiter_time_budget_s:
                self._alert("UNCLASSIFIED loiter-budget-timeout")     # log POI & resume
                self._set_mode("AUTO")                                # send InvestigationComplete
                self.state = self.SWEEP
            elif self._classify_ticks >= self.classify_timeout_ticks:
                self._alert("UNCLASSIFIED timeout")
                self._set_mode("AUTO")
                self.state = self.SWEEP

    def run(self, max_ticks: int = 400, tick_hz: float = 50.0):
        self.send_heartbeat()
        dt = 1.0 / tick_hz
        for i in range(max_ticks):
            if i % int(tick_hz) == 0:
                self.send_heartbeat()   # ~1 Hz companion heartbeat
            self.step()
            if self.state == self.PASSIVE:
                return   # FC has taken over (failsafe); nothing left to command
            time.sleep(dt)


class ScriptedDetector:
    """Deterministic mock detector — stands in for the RKNN thermal model so the
    control loop can be tested without CV. Fires exactly one detection, and
    succeeds classification after a few retries (exercising the adjustOrbit loop)."""
    def __init__(self, detect_after_calls: int = 10, species: str = "deer",
                 classify_success_on_call: int = 3, classify_conf: float = 0.87):
        self._d = self._c = 0
        self._fired = False
        self.detect_after = detect_after_calls
        self.species = species
        self.classify_success_on = classify_success_on_call
        self.classify_conf = classify_conf

    def detect(self) -> float:
        self._d += 1
        if not self._fired and self._d >= self.detect_after:
            self._fired = True
            return 0.95                      # one-shot detection >= R3_1 threshold
        return 0.10

    def classify(self) -> tuple[str, float]:
        self._c += 1
        conf = self.classify_conf if self._c >= self.classify_success_on else 0.40
        return self.species, conf
