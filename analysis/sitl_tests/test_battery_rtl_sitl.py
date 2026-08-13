"""D2.17 SITL validation: fly a scripted low-battery-far-from-home scenario
against real ArduPilot and confirm the actual MissionApp/BatteryRTLMonitor
code (imported for real, not reimplemented) decides to trigger AND that
ArduPilot accepts the resulting RTL command; plus a near-home scenario
proving the same battery-drain profile does NOT trigger early.

This is the "SITL validation pass" the reference doc
(Mission-Control's projects/surveillance-drone-d2-17-rtl-trigger/README.md,
"Integration point" step 6) called out as the load-bearing check before this
goes anywhere near a real battery pack -- the autonomy_sim/ mock-FC tests
prove the trigger decision is correct; this proves ArduPilot itself accepts
and acts on what MissionApp sends, the same distinction test_full_mission.py
draws for the rest of the control loop. Was blocked on task #141's SITL
AUTO-takeoff-crash finding; unblocked once that closed (2026-08-13).

Facts below confirmed by direct SITL probing (task D2.17/#142, 2026-08-13),
not guessed -- see this module's own comments and Mission Control task #142
notes for the probe transcript:

- BATT_CAPACITY defaults to 3300 mAh and drains for real (ArduCopter's own
  AP_BattMonitor integrates simulated current draw over time, same code as
  real hardware) -- a physically-realistic 12 Ah pack would take too long to
  deplete meaningfully in a short test even at this suite's -S 3 speedup, so
  these tests shrink it to 500 mAh, which reaches ~0% by ~22s of hover.
  Voltage (SIM_BATT_VOLTAGE) stays a fixed 12.6 V throughout -- it doesn't
  decay with consumption in this SITL model, which is fine: the trigger's
  remaining-energy calc is driven by capacity minus current_consumed, not
  voltage sag.
- MAV_CMD_DO_SET_HOME only succeeded once the vehicle was armed (and in
  GUIDED) -- called disarmed, even ~25s after connecting (well past this
  suite's documented EKF/GPS convergence time), it came back
  MAV_RESULT_FAILED and HOME_POSITION never moved. Armed+GUIDED, it
  succeeded immediately and HOME_POSITION relocated correctly. Reordering
  around that (arm+takeoff first, DO_SET_HOME right after) avoids the
  alternative of physically flying 2.8 km in-test, which isn't practical
  alongside a battery drain in one short SITL session.
"""
from __future__ import annotations
import os
import sys
import time

import pytest
from pymavlink import mavutil
from helpers import set_mode_via_command, arm_and_check, set_param, get_param, wait_mode

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "autonomy_sim"))
from mission_app import MissionApp, MODE  # noqa: E402

HOME_LAT, HOME_LON = 42.30000, -83.70000
_TEST_CAPACITY_MAH = 500.0


@pytest.fixture(scope="module", autouse=True)
def _restore_batt_capacity(sitl_process):
    """This module shrinks BATT_CAPACITY (see the module docstring) so a
    pack depletes in a practical test timeframe, and never resets it --
    which leaks into every LATER test file's arm attempts when the full
    suite runs together, the exact same class of bug
    test_failsafe_params.py's own _restore_arming_safe_defaults fixture
    exists to prevent (confirmed: this module's own tests AND
    test_full_mission.py failing to arm right after, task D2.17/#142,
    2026-08-13). Capture the real pre-test value and restore it, rather than
    hand-maintaining a hardcoded assumed default.

    Uses two short-lived connections (capture, close; later reconnect,
    restore, close) rather than one held open across the whole `yield` --
    SITL's SERIAL0 TCP port only accepts one client at a time, and a
    connection left open for the module's entire duration collides with
    each test's own sitl_conn (this exact bug, first found in
    test_failsafe_params.py's equivalent fixture, made every test in that
    module hang/ERROR when the suite ran together; same fix applied here).
    """
    def _connect():
        _, conn_str = sitl_process
        conn = mavutil.mavlink_connection(conn_str, dialect="ardupilotmega",
                                          source_system=255, source_component=191)
        conn.wait_heartbeat(timeout=15)
        conn.target_component = mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1
        return conn

    conn = _connect()
    original = get_param(conn, "BATT_CAPACITY", timeout=5.0)
    conn.close()

    yield

    if original is not None:
        conn = _connect()
        set_param(conn, "BATT_CAPACITY", original, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
        conn.close()


class _NeverDetects:
    """Stand-in Detector: the RTL check runs independently of SWEEP/
    INVESTIGATE state, so what this reports never matters for these tests --
    it exists only because MissionApp.__init__ requires a Detector."""
    def detect(self) -> float:
        return 0.0

    def classify(self) -> tuple[str, float]:
        return "unknown", 0.0


def _arm_guided_and_takeoff(conn, alt_m: float = 15.0):
    assert set_mode_via_command(conn, "GUIDED"), "GUIDED mode failed"
    assert arm_and_check(conn), "Arm in GUIDED failed"
    conn.mav.command_long_send(
        conn.target_system, conn.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, alt_m)


def test_battery_rtl_triggers_against_real_sitl(sitl_conn):
    conn = sitl_conn
    assert set_param(conn, "BATT_CAPACITY", _TEST_CAPACITY_MAH,
                      mavutil.mavlink.MAV_PARAM_TYPE_REAL32), "Failed to set BATT_CAPACITY"

    _arm_guided_and_takeoff(conn)

    # ~2.8 km north -- the same R7 worst-case leg used elsewhere in this
    # project (autonomy_sim's mock test, the original unit tests). See this
    # module's docstring for why DO_SET_HOME is issued here, post-arm.
    far_lat = HOME_LAT + 0.0252
    conn.mav.command_long_send(
        conn.target_system, conn.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_HOME, 0,
        0, 0, 0, 0, far_lat, HOME_LON, 180.0)

    app = MissionApp(conn, _NeverDetects(), target_system=conn.target_system,
                      battery_capacity_mah=_TEST_CAPACITY_MAH)
    triggered = False
    deadline = time.time() + 20.0
    while time.time() < deadline and not triggered:
        app.step()
        triggered = app.state == MissionApp.PASSIVE
        time.sleep(0.05)

    assert triggered, "BatteryRTLMonitor never triggered within 20s against real SITL"
    assert any(k == "battery_rtl_triggered" for k, _ in app.events), app.events

    # The load-bearing check: not just that MissionApp *decided* to command
    # RTL, but that real ArduPilot actually accepted it.
    assert wait_mode(conn, MODE["RTL"], timeout=5.0), \
        "SITL never entered RTL after MissionApp commanded it"


def test_battery_rtl_does_not_trigger_near_home_against_real_sitl(sitl_conn):
    """Same battery-drain profile as the test above -- the point of D2.17,
    proven against real SITL telemetry this time, not just the mock FC:
    home is left at the vehicle's actual takeoff position (no DO_SET_HOME),
    so distance-to-home stays ~0 throughout."""
    conn = sitl_conn
    assert set_param(conn, "BATT_CAPACITY", _TEST_CAPACITY_MAH,
                      mavutil.mavlink.MAV_PARAM_TYPE_REAL32), "Failed to set BATT_CAPACITY"

    _arm_guided_and_takeoff(conn)

    app = MissionApp(conn, _NeverDetects(), target_system=conn.target_system,
                      battery_capacity_mah=_TEST_CAPACITY_MAH)
    # Bounded window, stopped well before the pack is fully exhausted (probe
    # data: ~500 mAh reaches ~0% by ~t=22s under this throttle/capacity).
    # Once remaining energy hits exactly zero, a near-zero-distance "needed"
    # energy is also ~zero and the comparison stops meaningfully testing the
    # *adaptive* (distance-aware) behavior this task exists to prove.
    deadline = time.time() + 15.0
    while time.time() < deadline:
        app.step()
        assert app.state != MissionApp.PASSIVE, (
            "triggered near home (should not have): "
            f"{app._rtl_monitor.last_diagnostics if app._rtl_monitor else None}"
        )
        time.sleep(0.05)
