"""Focused test for D2.16: AUTO-mode takeoff with the AUTO_OPTIONS bit-1 fix.

Issue (from task D2.13/#70, D2.16/#141):
  The raw arducopter SITL binary crashes non-deterministically during an
  AUTO-mode mission takeoff. Launching the same binary through
  sim_vehicle.py eliminates the crash (sim_vehicle.py auto-loads
  default_params/copter.parm which the raw-binary launch never had).

  Once the crash is gone, a second issue surfaces: the vehicle arms fine in
  GUIDED, switches to AUTO, but never climbs — SERVO_OUTPUT_RAW stays flat
  at MOT_SPIN_ARM idle PWM, then STATUSTEXT "Disarming motors" fires.

Root cause of the climb failure:
  ModeAuto::takeoff_run() (ArduCopter/mode_auto.cpp) only force-sets
  ap.auto_armed when AUTO_OPTIONS bit 1 (AllowTakeOffWithoutRaisingThrottle)
  is set. Without it, ap.auto_armed depends on
  Copter::update_auto_armed(), which checks for non-zero RC throttle input.
  Since this suite holds throttle at RC3_MIN to satisfy the arm gate, the
  value reads as ap.throttle_zero → auto_armed stays false →
  _AutoTakeoff::run() hits its !auto_armed → return early gate → no
  spool-up → land detector triggers → disarmed.

Fix:
  Set AUTO_OPTIONS = 2.0 (bit 1 only, leaving bit 0 = Allow Arming off
  since we arm in GUIDED first per standard practice) before switching to
  AUTO.

This test verifies the full end-to-end sequence works.
"""
import time
import pytest
from pymavlink import mavutil
from helpers import (
    set_mode_via_command, arm_and_check, set_param, wait_mode, MODE,
    upload_mission, get_param,
)


HOME_LAT = 42_3000000
HOME_LON = -83_7000000


def _make_test_mission():
    """Build a minimal mission: home placeholder → TAKEOFF → WAYPOINT → RTL."""
    return [
        # seq 0: home placeholder (not executed)
        {"frame": 0, "command": 16, "current": 1, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": HOME_LAT, "y": HOME_LON, "z": 180.0},
        # seq 1: TAKEOFF to 15 m
        {"frame": 3, "command": 22, "current": 0, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": HOME_LAT, "y": HOME_LON, "z": 15.0},
        # seq 2: WAYPOINT 30 m north
        {"frame": 3, "command": 16, "current": 0, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": HOME_LAT + 30, "y": HOME_LON, "z": 15.0},
        # seq 3: RTL
        {"frame": 3, "command": 20, "current": 0, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": 0, "y": 0, "z": 0},
    ]


def test_auto_takeoff_with_fix(sitl_conn):
    """D2.16: Verify AUTO-mode takeoff succeeds with AUTO_OPTIONS bit 1.

    This replicates exactly the scenario that crashed/stranded the vehicle
    during D2.13 debugging, with the documented fix applied.
    """
    # ── Diagnostics: log key parameters to understand what we're working with ─
    rc3_min = get_param(sitl_conn, "RC3_MIN", timeout=5.0)
    rc3_max = get_param(sitl_conn, "RC3_MAX", timeout=5.0)
    auto_options = get_param(sitl_conn, "AUTO_OPTIONS", timeout=5.0)
    print(f"\n[D2.16] Baseline params: RC3_MIN={rc3_min}, RC3_MAX={rc3_max}, "
          f"AUTO_OPTIONS={auto_options}")

    # ── 1. Upload a minimal mission ────────────────────────────────────────
    items = _make_test_mission()
    ok = upload_mission(sitl_conn, items)
    assert ok, "Mission upload failed"

    # ── 2. Arm in GUIDED ───────────────────────────────────────────────────
    ok = set_mode_via_command(sitl_conn, "GUIDED")
    assert ok, "GUIDED mode command failed"

    ok = arm_and_check(sitl_conn)
    assert ok, "Arm in GUIDED failed"

    # ── 3. Set AUTO_OPTIONS bit 1 (AllowTakeOffWithoutRaisingThrottle) ────
    ok = set_param(sitl_conn, "AUTO_OPTIONS", 2.0,
                   mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
    assert ok, "Failed to set AUTO_OPTIONS"

    auto_options = get_param(sitl_conn, "AUTO_OPTIONS", timeout=5.0)
    print(f"[D2.16] AUTO_OPTIONS after set: {auto_options}")
    assert auto_options is not None and abs(auto_options - 2.0) < 0.1, \
        f"AUTO_OPTIONS readback mismatch: {auto_options}"

    # ── 4. Switch to AUTO ──────────────────────────────────────────────────
    ok = set_mode_via_command(sitl_conn, "AUTO")
    assert ok, "AUTO mode command failed"

    ok = wait_mode(sitl_conn, MODE["AUTO"])
    assert ok, "Vehicle did not enter AUTO mode"

    # ── 5. Monitor takeoff ─────────────────────────────────────────────────
    # Watch for climb. With the fix, the vehicle should spool up and climb
    # to the 15 m takeoff altitude within ~30 s.
    deadline = time.time() + 45.0
    reached_alt = False
    max_alt_seen = 0.0

    while time.time() < deadline:
        msg = sitl_conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg is not None:
            alt = msg.relative_alt / 1000.0
            if alt > max_alt_seen:
                max_alt_seen = alt
            if alt >= 13.0:  # within 2 m of the 15 m target
                reached_alt = True
                break
        time.sleep(0.2)

    print(f"[D2.16] Max altitude reached: {max_alt_seen:.1f} m / "
          f"target 15.0 m")

    # Also check if the process crashed (poll returns None if alive)
    # sitl_process is session-scoped; we don't have direct access here,
    # but if SITL crashed all SIMSTATE would stop and GLOBAL_POSITION_INT
    # would cease — we'd hit the deadline.
    if not reached_alt:
        # Check if we got any HEARTBEAT recently
        hb = sitl_conn.recv_match(type="HEARTBEAT", blocking=False)
        if hb is None:
            pytest.fail("No HEARTBEAT — SITL likely crashed. "
                        "See test_full_mission.py's docstring for details.")
        pytest.fail(f"Vehicle did not take off in AUTO within 45 s. "
                    f"Max altitude: {max_alt_seen:.1f} m. "
                    f"Armed: {'ARMED' if hb and (hb.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED) else 'DISARMED'}")

    assert reached_alt, f"Takeoff failed: max alt {max_alt_seen:.1f} m"

    # ── 6. Verify the mission continues (reach waypoint) ───────────────────
    deadline = time.time() + 30.0
    reached_wp = False
    while time.time() < deadline:
        msg = sitl_conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg is not None:
            # Check if we moved north: lat should change by ~30*1e-7 deg
            lat_diff = abs(msg.lat - (HOME_LAT + 30))
            if lat_diff < 20 and msg.relative_alt / 1000.0 > 12.0:
                reached_wp = True
                break
        time.sleep(0.2)

    assert reached_wp, "Vehicle did not reach waypoint after takeoff"
    print(f"[D2.16] Waypoint reached — AUTO takeoff + navigation "
          f"confirmed working with the AUTO_OPTIONS fix")


def test_auto_takeoff_fails_without_fix(sitl_conn):
    """Negative test: verify that WITHOUT the AUTO_OPTIONS fix, takeoff fails.

    This confirms the root cause analysis is correct by reproducing the
    failure mode. If this test unexpectedly passes, it means something else
    in the environment already enables takeoff (e.g., sim_vehicle.py's
    bundled copter.parm sets AUTO_OPTIONS to a non-zero value).

    Run this with `--override-ini` to exclude it from CI if the base
    environment already includes the fix (which would make this test
    permanently fail).
    """
    # ── 1. Upload the minimal mission ──────────────────────────────────────
    items = _make_test_mission()
    ok = upload_mission(sitl_conn, items)
    assert ok, "Mission upload failed"

    # ── 2. Arm in GUIDED ───────────────────────────────────────────────────
    ok = set_mode_via_command(sitl_conn, "GUIDED")
    assert ok, "GUIDED mode command failed"

    ok = arm_and_check(sitl_conn)
    assert ok, "Arm in GUIDED failed"

    # ── 3. Verify AUTO_OPTIONS is 0 (no bits set) ──────────────────────────
    auto_options = get_param(sitl_conn, "AUTO_OPTIONS", timeout=5.0)
    print(f"[D2.16-negative] AUTO_OPTIONS = {auto_options}")

    # If AUTO_OPTIONS is already non-zero, this test can't reproduce the
    # failure — skip instead of asserting.
    if auto_options is not None and auto_options > 0.5:
        pytest.skip(f"AUTO_OPTIONS is already {auto_options} — "
                    f"the failure cannot be reproduced in this environment")

    # ── 4. Switch to AUTO WITHOUT setting AUTO_OPTIONS bit 1 ────────────────
    ok = set_mode_via_command(sitl_conn, "AUTO")
    assert ok, "AUTO mode command failed"

    ok = wait_mode(sitl_conn, MODE["AUTO"])
    assert ok, "Vehicle did not enter AUTO mode"

    # ── 5. Monitor — expect NO climb ───────────────────────────────────────
    deadline = time.time() + 20.0
    max_alt = 0.0
    while time.time() < deadline:
        msg = sitl_conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg is not None:
            alt = msg.relative_alt / 1000.0
            if alt > max_alt:
                max_alt = alt
        time.sleep(0.2)

    print(f"[D2.16-negative] Max altitude without fix: {max_alt:.2f} m")

    # The vehicle should stay essentially on the ground. Allow 1 m of
    # altitude noise from GPS drift.
    assert max_alt < 1.5, (
        f"Vehicle climbed to {max_alt:.2f} m WITHOUT the AUTO_OPTIONS fix! "
        f"Either the root cause analysis is wrong or the environment "
        f"(sim_vehicle.py bundled params?) already enables takeoff."
    )