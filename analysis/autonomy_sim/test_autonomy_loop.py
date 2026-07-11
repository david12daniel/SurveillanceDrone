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
