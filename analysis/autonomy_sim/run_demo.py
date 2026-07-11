"""Narrated run of the autonomy loop against the mock FC — 'watch it work'.

    python run_demo.py

Runs one nominal detect->investigate->classify->resume cycle and prints the
MAVLink control contract as it happens, annotated with the behavior.sysml
element each step realizes. No ArduPilot install required.
"""
from pymavlink import mavutil

from mission_app import MissionApp, ScriptedDetector, MODE, MODE_NAME
from fake_fc import FakeFC

ANNOT = {
    "statustext": "STATUSTEXT to GCS (operator alert; committed no-downlink path, C20)",
    "set_mode":   "MAV_CMD DO_SET_MODE",
    "position_target": "SET_POSITION_TARGET_GLOBAL_INT (GUIDED descend)",
    "failsafe_observed": "observed FC failsafe -> stand down",
}
MODEL = {
    ("set_mode", "GUIDED"): "  <- send TargetDetected  (SweepAndDetect end; cruise->loiter)",
    ("set_mode", "AUTO"):   "  <- send InvestigationComplete (InvestigateAndClassify end; loiter->cruise)",
}


def main():
    fc_conn = mavutil.mavlink_connection("udpin:127.0.0.1:14572", dialect="ardupilotmega",
                                         source_system=1, source_component=1)
    app_conn = mavutil.mavlink_connection("udpout:127.0.0.1:14572", dialect="ardupilotmega",
                                          source_system=1, source_component=191)
    fc = FakeFC(fc_conn, start_mode="AUTO", start_alt_m=120.0)
    fc.start()
    print("=" * 68)
    print("Autonomy loop demo - mission app  <->  mock ArduPilot FC (MAVLink)")
    print("FC boots in AUTO @ 120 m, flying the surveillance route.")
    print("=" * 68)
    app = MissionApp(app_conn, ScriptedDetector(detect_after_calls=10, classify_success_on_call=3))
    app.run(max_ticks=200, tick_hz=50.0)
    fc.stop(); fc.join(timeout=2)
    fc_conn.close(); app_conn.close()

    print("\n--- App actions on the wire (in order) ---")
    for kind, detail in app.events:
        line = f"  {kind:16s} {detail:24s} {ANNOT.get(kind,'')}"
        print(line)
        tag = MODEL.get((kind, detail))
        if tag:
            print(tag)

    print("\n--- What the FC received (verifies the contract) ---")
    print(f"  mode commands : {[MODE_NAME[m] for m in fc.mode_cmds]}   (expect ['GUIDED','AUTO'])")
    print(f"  descent target: {[f'{a:.0f}m' for *_, a in fc.position_targets]}   (expect ['90m'])")
    print(f"  alerts        : {fc.statustexts}")
    ok = fc.mode_cmds == [MODE["GUIDED"], MODE["AUTO"]] and app.state == MissionApp.SWEEP
    print(f"\nRESULT: {'PASS - AUTO->GUIDED->AUTO loop closed, resumed route' if ok else 'FAIL'}")


if __name__ == "__main__":
    main()
