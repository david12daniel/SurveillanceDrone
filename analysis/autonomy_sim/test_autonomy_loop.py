"""Contract tests for the autonomy loop against the mock FC.

De-risks the UC-5 control contract BEFORE any CV work: asserts the app drives
the real MAVLink AUTO->GUIDED->AUTO sequence, commands a descent to the R3_2
altitude, alerts the operator, and stands down on an FC-commanded failsafe.
Run: pytest -v   (from analysis/autonomy_sim/)
"""
import threading
import time

from pymavlink import mavutil

from mission_app import MissionApp, ScriptedDetector, MODE


def _pair(port):
    fc = mavutil.mavlink_connection(f"udpin:127.0.0.1:{port}", dialect="ardupilotmega",
                                    source_system=1, source_component=1)
    app = mavutil.mavlink_connection(f"udpout:127.0.0.1:{port}", dialect="ardupilotmega",
                                     source_system=1, source_component=191)
    return fc, app


def test_nominal_detection_cycle():
    from fake_fc import FakeFC
    fc_conn, app_conn = _pair(14570)
    fc = FakeFC(fc_conn, start_mode="AUTO", start_alt_m=120.0)
    fc.start()
    try:
        app = MissionApp(app_conn, ScriptedDetector(detect_after_calls=10,
                                                    classify_success_on_call=3))
        app.run(max_ticks=200, tick_hz=50.0)   # ~4 s budget
    finally:
        fc.stop(); fc.join(timeout=2)
        fc_conn.close(); app_conn.close()

    # The contract, verified on the wire (what the FC actually received):
    assert fc.mode_cmds == [MODE["GUIDED"], MODE["AUTO"]], fc.mode_cmds
    assert fc.position_targets, "expected a GUIDED descent target"
    assert any(abs(alt - 90.0) < 1.0 for *_, alt in fc.position_targets), "descend to 90 m (R3_2)"
    assert any(s.startswith("DETECT") for s in fc.statustexts), fc.statustexts
    assert any(s.startswith("CLASSIFY deer") for s in fc.statustexts), fc.statustexts
    assert app.state == MissionApp.SWEEP   # returned to route


def test_failsafe_rtl_stands_down():
    from fake_fc import FakeFC
    fc_conn, app_conn = _pair(14571)
    fc = FakeFC(fc_conn, start_mode="AUTO", start_alt_m=120.0)
    fc.start()
    # Detector that never fires — the only mode change will be the FC's failsafe.
    app = MissionApp(app_conn, ScriptedDetector(detect_after_calls=10_000))
    runner = threading.Thread(target=app.run, kwargs={"max_ticks": 250, "tick_hz": 50.0})
    runner.start()
    try:
        time.sleep(1.0)
        fc.force_mode("RTL")     # simulate link-loss / low-battery failsafe (FC-owned)
        runner.join(timeout=6)
    finally:
        fc.stop(); fc.join(timeout=2)
        fc_conn.close(); app_conn.close()

    assert app.state == MissionApp.PASSIVE
    assert ("failsafe_observed", "RTL") in app.events
    assert MODE["GUIDED"] not in fc.mode_cmds   # app issued no autonomy commands


def test_position_target_mask_never_sets_force_set():
    # Regression (D2.15): the original mask (0b0000111111111000) set bit 9
    # (FORCE_SET), which makes ArduCopter silently drop GUIDED altitude-only
    # position targets -- the vehicle never descends to the R3_2 classify
    # altitude, with no error surfaced. See MODEL_ISSUES.md's type_mask entry.
    from fake_fc import FakeFC
    force_set = 0b0000001000000000
    fc_conn, app_conn = _pair(14572)
    fc = FakeFC(fc_conn, start_mode="AUTO", start_alt_m=120.0)
    fc.start()
    try:
        app = MissionApp(app_conn, ScriptedDetector(detect_after_calls=10,
                                                    classify_success_on_call=3))
        app.run(max_ticks=200, tick_hz=50.0)
    finally:
        fc.stop(); fc.join(timeout=2)
        fc_conn.close(); app_conn.close()

    assert fc.position_target_masks, "expected a GUIDED position target"
    for mask in fc.position_target_masks:
        assert not mask & force_set, f"FORCE_SET must stay clear (mask {mask:#016b})"
        assert not mask & 0b111, "position bits 0-2 must stay ENABLED (not ignored)"


# D2.17: distance-adaptive low-battery RTL trigger. Same HOME_LAT/HOME_LON and
# battery-drain scenario as test_battery_rtl_trigger.py's BatteryRTLMonitorTests
# (far_from_home_low_battery_triggers / close_to_home_same_battery_does_not_trigger)
# -- those tests prove the pure-math decision; these prove it's actually wired
# through MissionApp/FakeFC's real MAVLink messages (HOME_POSITION,
# BATTERY_STATUS, PARAM_REQUEST_READ/PARAM_VALUE) rather than just imported.
_RTL_HOME_LAT, _RTL_HOME_LON = 42.30000, -83.70000


def test_battery_rtl_triggers_when_far_from_home_and_low():
    from fake_fc import FakeFC
    fc_conn, app_conn = _pair(14573)
    # ~2.8 km out (the R7 worst-case leg), 250 W steady draw, only ~5% of a
    # 12 Ah pack left -- clearly not enough to make it home. rtl_speed_mps=12
    # exercises the real RTL_SPEED=0 -> WPNAV_SPEED PARAM_VALUE fallback (see
    # FakeFC._handle's PARAM_REQUEST_READ branch), not just a hardcoded default.
    fc = FakeFC(fc_conn, start_mode="AUTO", start_alt_m=120.0,
                lat=_RTL_HOME_LAT + 0.0252, lon=_RTL_HOME_LON,
                home_lat=_RTL_HOME_LAT, home_lon=_RTL_HOME_LON,
                battery_capacity_mah=12000.0, battery_voltage_v=22.2,
                battery_current_a=250.0 / 22.2, battery_consumed_mah=11400.0,
                rtl_speed_mps=12.0)
    fc.start()
    try:
        # detect_after_calls huge: only the battery monitor should command anything.
        app = MissionApp(app_conn, ScriptedDetector(detect_after_calls=10_000),
                          battery_capacity_mah=12000.0)
        app.run(max_ticks=200, tick_hz=50.0)
        # run() returns the instant state goes PASSIVE -- the RTL mode_send is
        # already on the wire, but FakeFC's background thread may not have
        # drained its socket yet. Bounded wait rather than a bare sleep: no
        # tuning to the FC's exact 2 ms poll interval, no fixed slop either.
        deadline = time.time() + 1.0
        while not fc.mode_cmds and time.time() < deadline:
            time.sleep(0.01)
    finally:
        fc.stop(); fc.join(timeout=2)
        fc_conn.close(); app_conn.close()

    assert app.state == MissionApp.PASSIVE
    assert MODE["RTL"] in fc.mode_cmds, fc.mode_cmds
    assert any(k == "battery_rtl_triggered" for k, _ in app.events), app.events
    assert any(s.startswith("BATTERY_RTL") for s in fc.statustexts), fc.statustexts


def test_battery_rtl_does_not_trigger_when_near_home_with_reserve():
    """The whole point of D2.17, proven end-to-end: same battery state and
    draw as the far-from-home case above, only the distance differs (~55 m,
    not ~2.8 km) -- the static R6_FS_BATT threshold would treat both
    identically, but this adaptive trigger should not fire here."""
    from fake_fc import FakeFC
    fc_conn, app_conn = _pair(14574)
    fc = FakeFC(fc_conn, start_mode="AUTO", start_alt_m=120.0,
                lat=_RTL_HOME_LAT + 0.0005, lon=_RTL_HOME_LON,
                home_lat=_RTL_HOME_LAT, home_lon=_RTL_HOME_LON,
                battery_capacity_mah=12000.0, battery_voltage_v=22.2,
                battery_current_a=250.0 / 22.2, battery_consumed_mah=11400.0,
                rtl_speed_mps=12.0)
    fc.start()
    try:
        app = MissionApp(app_conn, ScriptedDetector(detect_after_calls=10_000),
                          battery_capacity_mah=12000.0)
        app.run(max_ticks=200, tick_hz=50.0)
    finally:
        fc.stop(); fc.join(timeout=2)
        fc_conn.close(); app_conn.close()

    assert app.state == MissionApp.SWEEP
    assert MODE["RTL"] not in fc.mode_cmds, fc.mode_cmds
    assert not any(k == "battery_rtl_triggered" for k, _ in app.events), app.events
