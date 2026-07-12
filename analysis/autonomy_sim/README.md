# Autonomy loop — SITL/mock validation harness

> **Live development moved to its own repo: [`../../../DroneMissionApp`](../../../DroneMissionApp)** (capability **D-2**, `github.com/david12daniel/DroneMissionApp`). This directory is the **frozen de-risking prototype** that proved the AUTO→GUIDED→AUTO control contract; ongoing mission-app work happens in that repo. (2026-07-12)

De-risks the **UC-5 control contract** (the AUTO→GUIDED→AUTO mission loop) from
[`behavior.sysml`](../../behavior.sysml) *before* any computer-vision work, and
gives the onboard mission app a home. The thermal detector is injected, so this
harness validates the flight-control loop independently of the CV model — the
single biggest software risk (see [`../software_gap_analysis.md`](../software_gap_analysis.md)).

## Files
| File | Role | Model element |
|---|---|---|
| `mission_app.py` | The onboard mission app skeleton (SBC). `MissionApp` state machine + `Detector` interface + `ScriptedDetector` mock. | `SweepAndDetect`, `InvestigateAndClassify`, `DetectInvestigateClassify`, `FlightMode` |
| `fake_fc.py` | Minimal MAVLink FC simulator so the loop runs without ArduPilot. Records what it receives. | stands in for `drone.platform` (ArduPilot) |
| `test_autonomy_loop.py` | pytest: asserts the on-the-wire contract (mode sequence, descent target, alerts, failsafe stand-down). | UC-5 + failsafe transitions |
| `run_demo.py` | Narrated single-cycle run — "watch it work". | — |

## Run (offline — no ArduPilot needed)
```
pip install pymavlink pytest
cd analysis/autonomy_sim
python -m pytest -v      # 2 passing contract tests (~8 s)
python run_demo.py       # narrated AUTO->GUIDED->AUTO cycle
```
`run_demo.py` prints each MAVLink action the app puts on the wire, annotated with
the `behavior.sysml` element it realizes, then the FC's received record as proof:
```
mode commands : ['GUIDED', 'AUTO']
descent target: ['90m']
alerts        : ['DETECT 42.30000,-83.70000', 'CLASSIFY deer 0.87']
RESULT: PASS
```

## What this proves (and what it doesn't)
**Proves:** the mission app's MAVLink contract is correct — it commands the mode
switches, GUIDED descent to the R3_2 altitude, and operator alerts in the right
order, and it stands down when the FC declares a failsafe. The two model `send`s
(`TargetDetected`/`InvestigationComplete`) map cleanly to real mode changes.

**Does NOT prove:** real vehicle dynamics, EKF/GPS/arming preconditions, actual
GUIDED navigation, or the detector's accuracy. `fake_fc.py` is a contract stub,
not a flight model, and `ScriptedDetector` is not the thermal model.

## Next: run against real ArduPilot SITL
The same `mission_app.py` runs unchanged against SITL — swap the connection
string. Install ArduPilot SITL (WSL/Linux recommended on Windows), then:
```
# terminal 1 — start the simulator (ArduCopter)
sim_vehicle.py -v ArduCopter --console --map --out=udp:127.0.0.1:14550

# terminal 2 — point a thin runner at SITL instead of the mock
#   conn = mavutil.mavlink_connection('udp:127.0.0.1:14550')
#   app  = MissionApp(conn, ScriptedDetector());  app.run()
```
Against SITL you additionally validate: mode-change acceptance (ACKs), GUIDED
waypoint tracking, arming/EKF gates, and failsafe behavior from real parameters
(`FS_*`, `BATT_*`) — i.e. the two failsafe requirements the gap analysis
recommends formalizing. Then replace `ScriptedDetector` with the RKNN-backed
detector to close the last loop.

> ArduCopter mode numbers (AUTO=3, GUIDED=4, RTL=6, LAND=9) are defined in
> `mission_app.py`; verify against your firmware build before flight.
