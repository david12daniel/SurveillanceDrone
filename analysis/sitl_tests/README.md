# ArduPilot SITL Integration Suite (D2.13)

Runs the onboard mission app (`mission_app.py`) against a **real ArduPilot SITL**
instance to validate behaviors the mock FC cannot exercise:

- **Mode-ACK handling** — SITL returns `COMMAND_ACK` for `SET_MODE`; the app must
  wait for and verify the ACK before proceeding.
- **EKF/arming gates** — SITL enforces GPS lock, EKF convergence, and pre-arm checks
  before accepting `ARM_DISARM`. The app should handle these gracefully.
- **GUIDED navigation tracking** — SITL actually navigates to position targets instead
  of snapping; tests validate that the app waits for meaningful position convergence.
- **Real failsafe behavior** — inject `FS_*` / `BATT_*` conditions via SITL parameters
  and verify the app stands down correctly.

## Prerequisites

```bash
# ArduPilot SITL (any of the following approaches)
pip install ardupilot-sitl          # binary install (easiest)
# or: git clone https://github.com/ArduPilot/ardupilot.git
#     cd ardupilot && ./waf configure --board sitl && ./waf copter

# Python dependencies
pip install pymavlink pytest
```

## Quick start

```bash
cd analysis/sitl_tests
pytest -v --sitl-binary=arducopter   # autodetect if in PATH
```

For a manual walk-through:

```bash
# Terminal 1 — start SITL
sim_vehicle.py -v ArduCopter --out=udp:127.0.0.1:14555

# Terminal 2 — run the full suite
python -m pytest analysis/sitl_tests/ -v \
  --sitl-connection=udpin:127.0.0.1:14555
```

## Test groups

| Module | Tests | What it validates |
|---|---|---|
| `test_arming_gates.py` | 3 | Pre-arm checks, EKF convergence wait, arm/disarm sequence |
| `test_mode_ack.py` | 4 | SET_MODE → COMMAND_ACK correctness, retry on timeout |
| `test_guided_nav.py` | 3 | GUIDED position target → position reached within tolerance |
| `test_failsafe_params.py` | 2 | FS_THR_ENABLE / BATT_FS_LOW_ACT injection → mode change observed |
| `test_full_mission.py` | 1 | End-to-end: arm → takeoff → AUTO → detect → GUIDED descend → classify → resume |

## Architecture

```
sitl_tests/
├── README.md          ← this file
├── conftest.py        ← pytest fixtures (SITL process lifecycle, MAVLink connections)
├── helpers.py         ← shared utilities (arm, takeoff, set_param, wait_mode, etc.)
├── params_sets.py     ← canonical parameter values for the two §3.7 failsafe requirements
├── test_arming_gates.py
├── test_mode_ack.py
├── test_guided_nav.py
├── test_failsafe_params.py
└── test_full_mission.py
```

## Relation to mock tests

The autonomy_sim/ tests validate that the *app's internal state machine* produces the
correct MAVLink messages. The SITL tests validate that *ArduPilot accepts and acts on*
those messages — two different failure modes. Both should pass before field deployment.

## Common failure modes

| Symptom | Likely cause |
|---|---|
| `EKF check fails` at arm | SITL needs GPS lock; add `--gps=ublox` or wait 15 s |
| `COMMAND_ACK` has `result=4 (FAILED)` | Mode not available in current flight mode/state |
| GUIDED target never converges | `WPNAV_LOIT_SPEED`/`WPNAV_SPEED` defaults too slow; test tolerance needs adjustment |
| Failsafe not triggering | Parameter not save; call `PARAM_SET` with the right type |

---
*Part of the Surveillance Drone project, D2.13. See TASKS.md for the full work breakdown.*