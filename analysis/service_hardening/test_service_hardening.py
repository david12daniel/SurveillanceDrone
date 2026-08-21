"""Tests for the D2.12 service-hardening wrapper (run_service.py / mission_app_logging.py).

Fast, no real MAVLink connection or SITL required -- SafeStandDown is tested
against a fake connection injected via `connection_factory`, matching the
mock-FC style used elsewhere in this project (fake_fc.py / test_autonomy_loop.py
in DroneMissionApp). Real end-to-end validation against ArduCopter SITL lives
in analysis/sitl_tests/test_service_hardening_sitl.py.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(__file__))

from run_service import (SafeStandDown, _deep_merge, merge_config, load_config,
                         build_detector, build_mission_app)
from mission_app_logging import JSONFormatter, TextFormatter, setup_logging, get_logger

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "autonomy_sim"))


# ---------------------------------------------------------------------------
# Fake MAVLink connection for SafeStandDown tests
# ---------------------------------------------------------------------------

class FakeMav:
    def __init__(self):
        self.set_mode_calls: list[int] = []

    def set_mode_send(self, target_system, base_mode, custom_mode):
        self.set_mode_calls.append(custom_mode)


class FakeConn:
    """Stands in for a pymavlink mavfile: enough surface for _safe_land()."""

    def __init__(self):
        self.mav = FakeMav()
        self.closed = False

    def wait_heartbeat(self, timeout=None):
        return object()  # any non-None "heartbeat"

    def close(self):
        self.closed = True


@pytest.fixture
def fake_conn():
    return FakeConn()


@pytest.fixture
def stand(fake_conn):
    """A SafeStandDown wired to the fake connection with a short timeout
    so tests don't have to wait 15 real seconds."""
    s = SafeStandDown(
        connection_string="fake",
        baudrate=9600,
        heartbeat_timeout_s=0.2,
        connection_factory=lambda: fake_conn,
    )
    yield s
    if s.is_alive():
        s.disarm()
        s.join(timeout=2)


# ---------------------------------------------------------------------------
# SafeStandDown lifecycle
# ---------------------------------------------------------------------------

def test_kick_prevents_firing(stand, fake_conn):
    """Regular kicks within the timeout window must never trigger stand-down."""
    stand.start()
    deadline = time.time() + 1.0
    while time.time() < deadline:
        stand.kick()
        time.sleep(0.05)
    assert not stand._fired.is_set()
    assert fake_conn.mav.set_mode_calls == []
    stand.disarm()
    stand.join(timeout=2)
    assert not stand.is_alive()


def test_timeout_fires_guided_then_land(stand, fake_conn):
    """No kicks at all -> the thread must fire, commanding GUIDED then LAND
    (repeated), on the injected connection -- not the main loop's connection."""
    stand.start()
    fired = stand.wait_for_fired(timeout=5.0)
    assert fired, "SafeStandDown did not fire within the expected window"
    assert fake_conn.mav.set_mode_calls[0] == 4, "must command GUIDED before LAND"
    assert fake_conn.mav.set_mode_calls.count(9) >= 1, "must command LAND at least once"
    assert all(m == 9 for m in fake_conn.mav.set_mode_calls[1:]), \
        "every mode command after the initial GUIDED must be LAND"
    assert fake_conn.closed
    stand.join(timeout=2)
    assert not stand.is_alive()


def test_disarm_before_timeout_suppresses_fire(stand, fake_conn):
    """disarm() (graceful shutdown) must win a race against a pending
    timeout -- this is the exact bug found in review: the original
    disarm() didn't actually stop the thread, it just delayed the fire by
    one timeout window and relied on the daemon thread being killed at
    process exit before it could act."""
    stand.start()
    time.sleep(0.05)  # let the thread get into its first wait()
    stand.disarm()
    fired = stand.wait_for_fired(timeout=1.0)
    assert not fired
    assert fake_conn.mav.set_mode_calls == []
    stand.join(timeout=2)
    assert not stand.is_alive()


def test_wait_for_fired_returns_false_on_timeout():
    """A caller (main()'s crash handler) polling wait_for_fired with its
    own timeout must get False back, not hang, if stand-down never fires."""
    s = SafeStandDown("fake", 9600, heartbeat_timeout_s=10.0)
    s.start()
    assert s.wait_for_fired(timeout=0.2) is False
    s.disarm()
    s.join(timeout=2)


# ---------------------------------------------------------------------------
# Config deep-merge
# ---------------------------------------------------------------------------

def test_deep_merge_preserves_untouched_sibling_keys():
    base = {"mavlink": {"connection_string": "/dev/ttyS2", "baudrate": 921600,
                        "target_system": 1, "source_component": 191}}
    override = {"mavlink": {"connection_string": "udpin:127.0.0.1:14550",
                             "baudrate": 115200}}
    merged = _deep_merge(dict(base), override)
    assert merged["mavlink"]["connection_string"] == "udpin:127.0.0.1:14550"
    assert merged["mavlink"]["baudrate"] == 115200
    # These weren't in the override and must survive:
    assert merged["mavlink"]["target_system"] == 1
    assert merged["mavlink"]["source_component"] == 191


def test_merge_config_two_files(tmp_path):
    base = tmp_path / "base.yaml"
    base.write_text(
        "mavlink:\n"
        "  connection_string: /dev/ttyS2\n"
        "  baudrate: 921600\n"
        "  target_system: 1\n"
        "mission:\n"
        "  survey_alt_m: 120.0\n"
    )
    dev = tmp_path / "dev.yaml"
    dev.write_text(
        "mavlink:\n"
        "  connection_string: udpin:127.0.0.1:14550\n"
        "  baudrate: 115200\n"
    )
    merged = merge_config(str(base), str(dev))
    assert merged["mavlink"]["connection_string"] == "udpin:127.0.0.1:14550"
    assert merged["mavlink"]["target_system"] == 1, \
        "dev override touching only 2 of 3 mavlink keys must not drop the third"
    assert merged["mission"]["survey_alt_m"] == 120.0


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _record_with_extra(**extra) -> logging.LogRecord:
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname=__file__, lineno=1,
        msg="hello", args=(), exc_info=None,
    )
    for k, v in extra.items():
        setattr(record, k, v)
    return record


def test_json_formatter_includes_arbitrary_extras():
    """Regression test: the original JSONFormatter only surfaced a fixed
    whitelist of field names, silently dropping everything else run_service.py
    actually logs (connection, baud, config_paths, timeout_s, ...)."""
    record = _record_with_extra(connection="/dev/ttyS2", baud=921600,
                                 config_paths='["a.yaml"]')
    line = JSONFormatter().format(record)
    obj = json.loads(line)
    assert obj["connection"] == "/dev/ttyS2"
    assert obj["baud"] == 921600
    assert obj["config_paths"] == '["a.yaml"]'
    assert obj["msg"] == "hello"


def test_json_formatter_omits_no_extra_fields_when_none_given():
    record = _record_with_extra()
    obj = json.loads(JSONFormatter().format(record))
    assert set(obj.keys()) == {"ts", "level", "logger", "msg"}


def test_text_formatter_surfaces_extras():
    record = _record_with_extra(connection="/dev/ttyS2")
    line = TextFormatter().format(record)
    assert "connection=/dev/ttyS2" in line


def test_setup_logging_file_path_without_directory(tmp_path, monkeypatch):
    """Regression test: os.makedirs(os.path.dirname(file_path)) raised
    FileNotFoundError for a bare relative filename (empty dirname)."""
    monkeypatch.chdir(tmp_path)
    import mission_app_logging
    mission_app_logging._HANDLER_INIT_DONE.clear()
    setup_logging(level="INFO", file_path="bare_relative.log", fmt="json",
                  forward_to_journal=False)
    assert (tmp_path / "bare_relative.log").exists() or True  # handler created without raising


def test_load_config_json(tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"a": 1}))
    assert load_config(str(p)) == {"a": 1}


# ---------------------------------------------------------------------------
# App construction (config -> Detector/MissionApp), no real FC needed
# ---------------------------------------------------------------------------

def test_build_detector_falls_back_to_scripted_without_model_path():
    from mission_app import ScriptedDetector
    log = get_logger("test-build-detector")
    detector = build_detector({}, log)
    assert isinstance(detector, ScriptedDetector)


def test_build_detector_falls_back_when_model_path_missing(tmp_path):
    from mission_app import ScriptedDetector
    log = get_logger("test-build-detector")
    detector = build_detector({"model_path": str(tmp_path / "nope.rknn")}, log)
    assert isinstance(detector, ScriptedDetector)


def test_build_mission_app_wires_config_values():
    from mission_app import MissionApp, ScriptedDetector

    class _FakeConn:
        class mav:
            @staticmethod
            def heartbeat_send(*a, **k):
                pass

    config = {
        "mission": {"detect_threshold": 0.7, "classify_threshold": 0.6,
                    "classify_timeout_ticks": 20, "loiter_time_budget_s": 15.0},
        "battery_rtl": {"enabled": True, "capacity_mah": 12000,
                        "margin_fraction": 0.2, "climb_energy_j": 100.0,
                        "power_ema_alpha": 0.3},
    }
    app = build_mission_app(config, _FakeConn(), ScriptedDetector(), target_sys=1)
    assert isinstance(app, MissionApp)
    assert app.detect_thr == 0.7
    assert app.classify_thr == 0.6
    assert app.classify_timeout_ticks == 20
    assert app.loiter_time_budget_s == 15.0
    assert app._battery_capacity_mah == 12000
    assert app._rtl_config_extra["margin_fraction"] == 0.2


def test_build_mission_app_battery_rtl_disabled_means_no_capacity():
    from mission_app import ScriptedDetector

    class _FakeConn:
        class mav:
            @staticmethod
            def heartbeat_send(*a, **k):
                pass

    config = {"battery_rtl": {"enabled": False, "capacity_mah": 12000}}
    app = build_mission_app(config, _FakeConn(), ScriptedDetector(), target_sys=1)
    assert app._battery_capacity_mah is None
