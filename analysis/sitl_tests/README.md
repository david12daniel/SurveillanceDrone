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

All of the below were confirmed by direct probing against the two real SITL
binaries in this environment (task D2.13/D2.14, 2026-08-10), not guessed --
see `conftest.py`/`helpers.py` docstrings and the `test_*.py` files' own
comments for the full reasoning behind each fix.

| Symptom | Likely cause |
|---|---|
| `PreArm: Motors: Check frame class and type` | `FRAME_CLASS` defaults to 0 (undefined) on a fresh EEPROM when launching the raw binary directly. `conftest.py` sets it (and the legacy `FRAME` param for Copter 3.3). |
| `PreArm: 3D Accel calibration needed`, never clears | Fresh EEPROM, never ran the interactive accelcal wizard. `conftest.py` sets `ARMING_SKIPCHK`/legacy `ARMING_CHECK` to skip just the INS check. |
| `Arm: Check FS_THR_VALUE` / `Arm: Throttle too high` | No RC hardware means ArduPilot never sees RC_CHANNELS at all, reading as a permanent throttle failsafe. `conftest.py`'s `sitl_conn` fixture runs a background `RC_CHANNELS_OVERRIDE` feed (idle throttle) for the life of each connection. |
| `MISSION_REQUEST`/`RC_CHANNELS_OVERRIDE` seem to be silently dropped | `target_component` defaults to 0 (broadcast) in pymavlink -- it does NOT auto-populate from the first HEARTBEAT the way `target_system` does. `COMMAND_LONG`-based commands tolerate broadcast targeting; several message types (notably `RC_CHANNELS_OVERRIDE`) don't. Set `conn.target_component` explicitly. |
| `EKF check fails` at arm / arm command times out once | A single arm attempt doesn't retry itself, and GPS/home genuinely takes ~20-25 s wall-clock after boot (not sped up by `--speedup`). `arm_and_check` resends every 2 s instead of asking once. |
| `struct.error: 'I' format requires 0 <= number...` sending a position target | `time_boot_ms` must be milliseconds since the FC's own boot, not `time.time()*1000` -- a Unix-epoch ms value overflows the field's uint32 range. Pass `0`. |
| No `GLOBAL_POSITION_INT`/`EKF_STATUS_REPORT`/etc at all, only `HEARTBEAT`/`TIMESYNC` | SITL doesn't stream anything beyond the bare minimum until a client requests it, same as any real GCS would on connect. Send `REQUEST_DATA_STREAM(MAV_DATA_STREAM_ALL, ...)` once connected. |
| A wait loop that checks several different message types per iteration (e.g. STATUSTEXT, then EKF_STATUS_REPORT, then HEARTBEAT) reports the wrong thing, or never sees an event you can independently confirm happened | `recv_match(type=X, blocking=False)` internally discards every non-matching message while hunting for X. Under this suite's full-rate telemetry stream, an earlier type-filtered poll in the same loop can eat a message a later one needed. Poll only one type per loop, or pass a list of types to a single `recv_match` call. |
| A `while` loop with a computed `deadline` that never actually checks it | Easy to introduce by only checking a different loop condition (e.g. `received_seq < n`). Always include the deadline in the loop condition, not just compute it. |
| ArduPilot requests mission items via `MISSION_REQUEST`, not `MISSION_REQUEST_INT` | Firmware-dependent; listen for both. |
| `Auto: Missing Takeoff Cmd`, mission has a takeoff command | Mission item seq 0 is a conventional home/reference placeholder ArduPilot expects, not a real command -- real commands start at seq 1, matching QGroundControl/Mission Planner. |
| `Arm: Auto mode not armable` | `AUTO_OPTIONS` bit 0 ("Allow Arming") is off by default -- a deliberate safety gate against arming directly in AUTO. Arm in GUIDED/STABILIZE first, then switch to AUTO, matching standard ArduCopter practice, rather than loosening that gate. |
| GUIDED target never converges (lateral) | `WPNAV_*` parameters no longer exist on modern ArduCopter (renamed to `PSC_D_*`/`PSC_NE_*` under the position-controller rewrite); this doesn't block lateral GUIDED targets, which work fine once the above are fixed. |
| GUIDED target never converges (**altitude-only**, same lat/lon as current position) | Fixed (task D2.15, 2026-08-11): `type_mask` had bit 9 (`POSITION_TARGET_TYPEMASK_FORCE_SET`) unintentionally set (4088 / `0b0000111111111000`, a common copy-paste artifact) -- clearing it (3576 / `0b0000110111111000`, ArduPilot's own documented "position only" mask) produced a clean, monotonic descent. Same bug and fix in the real mission app's `_command_descent()` (`analysis/autonomy_sim/mission_app.py`); see `test_guided_altitude_change`'s docstring for the full investigation, including why alternative commands (`MAV_CMD_GUIDED_CHANGE_ALTITUDE`, `MAV_CMD_DO_REPOSITION`) are NOT viable substitutes on this firmware. |
| SITL binary exits mid-test ("Closed connection on SERIAL0" is the last line in its own log, then the process is gone) | Confirmed real crash, not a test-harness bug: observed during an AUTO-mode takeoff sequence, and independently the shared SITL process appears to become less reliable the more mission-upload/arm/disarm/mode-change cycles it's put through in one session. `conftest.py`'s `sitl_conn` fixture checks `sitl_process.poll()` and skips cleanly instead of every remaining test independently timing out, but the crash itself isn't fixed. **Tracked as D2.15 (Mission Control, project "Surveillance Drone") -- launching via ArduPilot's official `sim_vehicle.py` orchestrator instead of the raw binary was confirmed (2026-08-11) to eliminate the crash in 4/4 attempts, at the cost of surfacing a new "disarms instead of climbing" issue; see the task notes for the full writeup and a ready-to-use launch command.** |

---
*Part of the Surveillance Drone project, D2.13. See TASKS.md for the full work breakdown.*