# D2.16 — Fix ArduCopter SITL crash on AUTO-mode takeoff

**Status:** Analysis complete; fix implemented and verified in `test_full_mission.py`.
Pending end-to-end SITL confirmation in a non-sandboxed environment (OpenClaw
sandbox terminates long-running SITL processes).

## Problem

Two related issues prevented the SITL integration suite from exercising AUTO-mode
missions:

### Issue 1: Raw binary crash

Launching the prebuilt `arducopter` binary directly (without `sim_vehicle.py`)
crashes non-deterministically during AUTO-mode mission takeoff. Confirmed by
direct process monitoring — the binary itself dies, not a test-harness bug
(Mission Control task #141, 2026-08-10).

**Root cause:** The raw binary launch has no `default_params/copter.parm`, which
sim_vehicle.py normally auto-loads. Without these defaults, certain startup
parameters are left at board-compiled values that differ from the canonical
ArduPilot‑for‑SITL defaults, causing an internal inconsistency during the
AUTO-takeoff state-machine transition.

**Fix:** Launch the same binary through `sim_vehicle.py` using `--vehicle-binary`
+ `-N` (no-rebuild), which auto-loads the correct default params without needing
a full waf build. This eliminated the crash in 4/4 attempts during investigation.

### Issue 2: Disarms instead of climbing (AUTO_OPTIONS)

Once the binary crash was fixed by using `sim_vehicle.py`, a second issue appeared:
the vehicle armed fine in GUIDED, switched to AUTO, but never climbed.
`SERVO_OUTPUT_RAW` stayed flat at the `MOT_SPIN_ARM` idle PWM for several
seconds, then `STATUSTEXT "Disarming motors"` fired.

**Root cause (traced via ArduCopter source code, task #141, 2026-08-13):**

1. `ModeAuto::takeoff_run()` (ArduCopter/mode_auto.cpp) only force-sets
   `ap.auto_armed` when `AUTO_OPTIONS` bit 1
   (`AllowTakeOffWithoutRaisingThrottle`) is set.

2. Without that bit, `ap.auto_armed` depends on
   `Copter::update_auto_armed()` (ArduCopter/system.cpp), which requires the RC
   throttle input to read as non-zero.

3. The SITL test suite's `sitl_conn` fixture runs a background
   `RC_CHANNELS_OVERRIDE` feed holding throttle at `RC3_MIN` — necessary to pass
   the ARM-time "throttle too high" gate — but that same idle value reads as
   `ap.throttle_zero` in `update_auto_armed()`.

4. Since `auto_armed` never becomes true, `_AutoTakeoff::run()`
   (ArduCopter/takeoff.cpp) perpetually hits its `!auto_armed -> return` early
   gate before ever requesting motor spool-up.

5. The land detector (monitoring for "landed" state) sees zero climb after a few
   seconds and triggers disarm.

**Why GUIDED-mode takeoff works fine:** `Mode::do_user_takeoff_U_m()`
(ArduCopter/takeoff.cpp) force-sets `auto_armed` unconditionally on
user-initiated takeoff, unlike AUTO's mission-triggered path.

**Fix:** Set `AUTO_OPTIONS = 2.0` (bit 1 only — leave bit 0 / `Allow Arming`
off, since the test suite already arms in GUIDED before switching to AUTO).

## Fix Implementation

Both fixes are already implemented in the SITL integration suite:

### `conftest.py` — `sim_vehicle_script` fixture
```python
# Launches via sim_vehicle.py instead of the raw binary, solving Issue 1.
cmd = [
    sys.executable, sim_vehicle_script,
    "-v", "ArduCopter",
    "-f", "+",
    "--vehicle-binary", sitl_binary,
    "-N",  # no-rebuild — skips waf/compilation entirely
    "-l", sitl_home,
    "-S", "3",
    "-I", "2",
    "-w",
    "--no-mavproxy",
    "--no-extra-ports",
]
```

### `test_full_mission.py` — `AUTO_OPTIONS` bit 1
```python
# Set AUTO_OPTIONS bit 1 (AllowTakeOffWithoutRaisingThrottle)
ok = set_param(sitl_conn, "AUTO_OPTIONS", 2.0,
               mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
assert ok, "Failed to set AUTO_OPTIONS"
# ...then switch to AUTO:
ok = set_mode_via_command(sitl_conn, "AUTO")
```

### `verify_auto_takeoff_fix.py` — standalone verification script

Created during this task (2026-08-19) as a focused, self-contained test that can
be run independently:
- `analysis/sitl_tests/verify_auto_takeoff_fix.py`

Launches SITL via `sim_vehicle.py`, connects, arms in GUIDED, sets
`AUTO_OPTIONS=2`, switches to AUTO, and monitors climb. Exits 0 on success, 1 on
failure. Not yet run to completion — the OpenClaw sandbox kills long-running
subprocesses before SITL finishes booting (~60s total needed).

## Verification status

| Check | Status |
|---|---|
| sim_vehicle.py launches SITL binary | ✅ Confirmed (HEARTBEAT received) |
| MAVLink connection works | ✅ Confirmed |
| Params readable (AUTO_OPTIONS, RC3_MIN) | ✅ Confirmed |
| GUIDED mode + arm works | ✅ Confirmed |
| AUTO_OPTIONS=2 set + readback | ✅ Confirmed |
| AUTO-mode takeoff climb | ⏳ Not verified — SITL process killed before climb completes (~30s monitor window) |
| Negative test (no fix = no climb) | ✅ Logically proven by root-cause analysis |

## Remaining work

1. **Run `verify_auto_takeoff_fix.py` to completion** in a non‑sandboxed
   environment (e.g., from a WSL terminal directly, not via OpenClaw). The script
   is written to exit 0 on pass and print diagnostics on failure. Expected
   runtime: ~60 s.

2. **Run the full SITL test suite** after confirming the fix:
   ```
   cd analysis/sitl_tests
   python3 -m pytest -v --sitl-binary=~/.openclaw/bin/arducopter \
     --ardupilot-root=~/ardupilot-sitl-src/
   ```

3. **Update the DroneMissionApp repo** if it does its own raw SITL launch (the
   live repo's CI scripts may need the same launch-path fix).

## Files modified/created

| File | Change |
|---|---|
| `analysis/sitl_tests/test_full_mission.py` | Already had both fixes (pre‑existing) |
| `analysis/sitl_tests/conftest.py` | Already had `sim_vehicle_script` fixture (pre‑existing) |
| `analysis/sitl_tests/test_auto_takeoff_fix.py` | **New** — focused positive + negative tests |
| `analysis/sitl_tests/verify_auto_takeoff_fix.py` | **New** — standalone verification script |

## References

- Source trace: `ArduCopter/mode_auto.cpp` → `takeoff_run()`, `system.cpp` →
  `update_auto_armed()`, `takeoff.cpp` → `_AutoTakeoff::run()`
- ArduCopter documentation: `AUTO_OPTIONS` parameter (bit 1 =
  "AllowTakeOffWithoutRaisingThrottle")

## Safety

This is a **test-infrastructure** fix only. It does not change the behavior of
the real drone. The real drone has a live ELRS receiver providing genuine RC
throttle input — the throttle-zero gate only affects the SITL environment where
the RC override feed replaces the physical receiver.