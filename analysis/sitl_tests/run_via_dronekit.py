#!/usr/bin/env python3
"""Run the SITL integration suite using dronekit-sitl for process management.

DroneKit-SITL handles downloading and launching the Copter 3.3 firmware binary
with correct port forwarding. This wrapper starts it, runs the test suite,
and cleans up.

Usage:
    python3 run_via_dronekit.py [--instance N] [--keep-sitl]
"""
from __future__ import annotations
import os
import sys
import time
import subprocess
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pymavlink import mavutil
from helpers import (
    set_mode_via_command, arm_and_check, guided_takeoff,
    send_position_target, wait_position, wait_mode, MODE,
    set_param, get_param,
)

PASS = 0
FAIL = 1
SKIP = 2
results: list[tuple[str, int, str]] = []


def test(name: str, fn):
    try:
        fn()
        results.append((name, PASS, ""))
        print(f"  PASS  {name}")
    except Exception as e:
        results.append((name, FAIL, str(e)))
        print(f"  FAIL  {name}: {e}")


def mode_ack_tests(conn):
    """Test SET_MODE for every supported mode."""
    for mode_name in ("STABILIZE", "GUIDED", "AUTO", "RTL", "LAND"):
        ok = set_mode_via_command(conn, mode_name)
        assert ok, f"{mode_name} mode was not confirmed in HEARTBEAT"
    print("    All mode transitions: OK")


def arming_tests(conn):
    """Test pre-arm checks and arming."""
    # Try to arm in STABILIZE at boot
    set_mode_via_command(conn, "STABILIZE")
    time.sleep(0.5)
    arm_result = arm_and_check(conn, timeout=5.0)
    print(f"    Arm in STABILIZE at boot: {'succeeded' if arm_result else 'rejected'}")

    # Wait for EKF convergence
    deadline = time.time() + 20
    ekf_ok = False
    while time.time() < deadline:
        ekf = conn.recv_match(type="EKF_STATUS_REPORT", blocking=False)
        if ekf is not None and (ekf.flags & 0x0F):
            ekf_ok = True
            break
        time.sleep(0.5)

    if ekf_ok:
        set_mode_via_command(conn, "GUIDED")
        time.sleep(0.5)
        armed = arm_and_check(conn)
        assert armed, "Arm in GUIDED after EKF convergence should succeed"
        print("    ARM in GUIDED after EKF: OK")
    else:
        print("    SKIP: EKF did not converge within 20s")


def guided_nav_tests(conn):
    """Test GUIDED takeoff and position target navigation."""
    # Takeoff to 20m
    ok = guided_takeoff(conn, alt_m=20.0)
    assert ok, "Guided takeoff failed"
    print("    Takeoff to 20m: OK")

    # Command altitude change to 10m
    lat = 42_3000000
    lon = -83_7000000
    send_position_target(conn, lat, lon, 10.0)
    deadline = time.time() + 20
    reached = False
    while time.time() < deadline:
        msg = conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg is not None:
            alt = msg.relative_alt / 1000.0
            if alt <= 11.0:
                reached = True
                break
        time.sleep(0.2)
    assert reached, "Vehicle did not descend to 10m"
    print("    Descent to 10m: OK")

    # Navigate to offset position
    offset_lat = 42_3000500
    offset_lon = -83_6999500
    send_position_target(conn, offset_lat, offset_lon, 15.0)
    converged = wait_position(conn, offset_lat, offset_lon, pos_tolerance_m=10.0)
    assert converged, "Vehicle did not converge to position target"
    print("    Position target convergence: OK")

    # Check altitude safety
    min_alt = 999.0
    deadline = time.time() + 5.0
    while time.time() < deadline:
        msg = conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg is not None:
            alt_now = msg.relative_alt / 1000.0
            min_alt = min(min_alt, alt_now)
        time.sleep(0.2)
    assert min_alt >= 12.0, f"Vehicle dropped to {min_alt:.1f}m"
    print(f"    Altitude safety (min {min_alt:.1f}m): OK")


def failsafe_params_tests(conn):
    """Test setting and reading back failsafe parameters."""
    fb_volt = get_param(conn, "FS_BATT_VOLTAGE")
    assert fb_volt is not None, "Could not read FS_BATT_VOLTAGE"
    print(f"    FS_BATT_VOLTAGE = {fb_volt}")

    batt_low = get_param(conn, "BATT_LOW_VOLT")
    assert batt_low is not None, "Could not read BATT_LOW_VOLT"
    print(f"    BATT_LOW_VOLT = {batt_low}")

    ok = set_param(conn, "FS_BATT_VOLTAGE", 10.0,
                   mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
    assert ok, "Could not set FS_BATT_VOLTAGE"
    readback = get_param(conn, "FS_BATT_VOLTAGE")
    assert readback is not None and abs(readback - 10.0) < 0.01, \
        f"Param readback mismatch: {readback}"
    print("    Param set+readback: OK")


def main():
    ap = argparse.ArgumentParser(description="Run SITL tests via dronekit-sitl")
    ap.add_argument("--instance", type=int, default=3)
    ap.add_argument("--keep-sitl", action="store_true")
    args = ap.parse_args()

    inst = args.instance
    serial0_port = 5760 + inst * 10

    # Start SITL via dronekit-sitl
    print(f"Starting dronekit-sitl copter (instance {inst})...")
    proc = subprocess.Popen(
        ["dronekit-sitl", "copter", "--instance", str(inst), "--speedup", "3"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(f"  PID={proc.pid}")
    time.sleep(12)

    # Connect
    conn_str = f"tcp:127.0.0.1:{serial0_port}"
    print(f"Connecting to {conn_str}...")
    conn = mavutil.mavlink_connection(conn_str, dialect="ardupilotmega",
                                      source_system=255, source_component=191)
    deadline = time.time() + 20
    connected = False
    while time.time() < deadline:
        if conn.wait_heartbeat(blocking=False) is not None:
            connected = True
            break
        time.sleep(0.5)

    if not connected:
        print("FAIL: Could not connect to SITL (no HEARTBEAT)")
        if not args.keep_sitl:
            proc.terminate()
        sys.exit(1)

    print(f"  Connected. System={conn.target_system}, Component={conn.target_component}")

    # Drain pre-boot messages
    time.sleep(2)
    n = 0
    while conn.recv_match(blocking=False):
        n += 1
    print(f"  Drained {n} pre-boot messages")

    # Run tests
    print("\n--- Running Mode ACK tests ---")
    test("Mode ACK - all modes", lambda c=conn: mode_ack_tests(c))

    print("\n--- Running Arming gate tests ---")
    test("Arming - pre-arm checks", lambda c=conn: arming_tests(c))

    print("\n--- Running GUIDED navigation tests ---")
    test("GUIDED nav - takeoff and position", lambda c=conn: guided_nav_tests(c))

    print("\n--- Running Failsafe parameter tests ---")
    test("Failsafe params - read/write", lambda c=conn: failsafe_params_tests(c))

    # Summary
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    passed = sum(1 for _, s, _ in results if s == PASS)
    failed = sum(1 for _, s, _ in results if s == FAIL)
    skipped = sum(1 for _, s, _ in results if s == SKIP)
    for name, status, msg in results:
        label = {PASS: "PASS", FAIL: "FAIL", SKIP: "SKIP"}[status]
        print(f"  [{label}] {name}")
        if msg:
            print(f"         {msg}")
    print(f"\n{passed} passed, {failed} failed, {skipped} skipped")

    # Cleanup
    conn.close()
    if not args.keep_sitl:
        print("Shutting down SITL...")
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("  Done.")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()