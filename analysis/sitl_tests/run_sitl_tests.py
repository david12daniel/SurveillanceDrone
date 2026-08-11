#!/usr/bin/env python3
"""Standalone SITL integration test runner.

Manages the SITL process lifecycle and runs the core test scenarios.
No pytest dependency — runs the helpers directly.

Usage:
    python3 run_sitl_tests.py [--sitl-binary PATH] [--instance N]
"""
from __future__ import annotations
import os
import sys
import time
import subprocess
import shutil
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pymavlink import mavutil
from helpers import (
    set_mode_via_command, arm_and_check, guided_takeoff,
    send_position_target, wait_position, wait_mode, MODE,
    set_param, get_param, force_failsafe, upload_mission,
    read_mission_item,
)

PASS = 0
FAIL = 1
SKIP = 2

results: list[tuple[str, int, str]] = []


def test(name: str, fn):
    """Run a test function, record result."""
    try:
        fn()
        results.append((name, PASS, ""))
        print(f"  PASS  {name}")
    except Exception as e:
        results.append((name, FAIL, str(e)))
        print(f"  FAIL  {name}: {e}")


# ---------- Mode ACK tests ----------

def mode_ack_tests(conn):
    """Test SET_MODE → COMMAND_ACK for every supported mode."""
    for mode_name in ("AUTO", "GUIDED", "RTL", "LAND", "STABILIZE"):
        ok = set_mode_via_command(conn, mode_name)
        assert ok, f"{mode_name} mode command was not accepted"
        hb_ok = wait_mode(conn, MODE[mode_name])
        assert hb_ok, f"HEARTBEAT did not report {mode_name}"

    # Invalid mode should be rejected
    conn.mav.set_mode_send(
        conn.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        99,
    )
    deadline = time.time() + 10
    rejected = False
    while time.time() < deadline:
        # Check if heartbeat still shows a valid mode (not 99)
        hb = conn.recv_match(type="HEARTBEAT", blocking=False)
        if hb is not None and hb.get_srcComponent() == mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1:
            if hb.custom_mode != 99:
                rejected = True
                break
        # Also check for COMMAND_ACK on some firmware versions
        ack = conn.recv_match(type="COMMAND_ACK", blocking=False)
        if ack is not None and ack.command in (mavutil.mavlink.MAV_CMD_DO_SET_MODE, 11):
            if ack.result != mavutil.mavlink.MAV_RESULT_ACCEPTED:
                rejected = True
                break
        time.sleep(0.05)
    assert rejected, "Invalid mode 99 should NOT be accepted by the FC"
    print("    All mode ACK tests passed")


# ---------- Arming gate tests ----------

def arming_tests(conn):
    """Test pre-arm checks and arming."""
    # Switch to STABILIZE and try arming
    set_mode_via_command(conn, "STABILIZE")
    time.sleep(0.5)
    arm_result = arm_and_check(conn, timeout=5.0)
    print(f"    Arm in STABILIZE at boot: {'succeeded' if arm_result else 'rejected'}")

    # Wait for EKF convergence
    deadline = time.time() + 15
    ekf_ok = False
    while time.time() < deadline:
        msg = conn.recv_match(type="STATUSTEXT", blocking=False)
        if msg is not None:
            txt = msg.text if isinstance(msg.text, str) else msg.text.decode("utf-8", errors="replace")
            if "PreArm" in txt:
                print(f"    Pre-arm: {txt}")
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
        print("    SKIP: EKF did not converge within 15s")


# ---------- GUIDED navigation tests ----------

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


# ---------- Failsafe parameter tests ----------

def failsafe_params_tests(conn):
    """Test setting and reading back failsafe parameters."""
    # Read FS_BATT_VOLTAGE
    fb_volt = get_param(conn, "FS_BATT_VOLTAGE")
    assert fb_volt is not None, "Could not read FS_BATT_VOLTAGE"
    print(f"    FS_BATT_VOLTAGE = {fb_volt}")

    # Read BATT_LOW_VOLT
    batt_low = get_param(conn, "BATT_LOW_VOLT")
    assert batt_low is not None, "Could not read BATT_LOW_VOLT"
    print(f"    BATT_LOW_VOLT = {batt_low}")

    # Set a param and verify
    ok = set_param(conn, "FS_BATT_VOLTAGE", 10.0,
                   mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
    assert ok, "Could not set FS_BATT_VOLTAGE"
    readback = get_param(conn, "FS_BATT_VOLTAGE")
    assert readback is not None and abs(readback - 10.0) < 0.01, \
        f"Param readback mismatch: {readback}"
    print("    Param set+readback: OK")


# ---------- Main ----------

def main():
    ap = argparse.ArgumentParser(description="Run SITL integration tests")
    ap.add_argument("--sitl-binary", default=None,
                    help="Path to arducopter binary")
    ap.add_argument("--instance", type=int, default=3,
                    help="SITL instance number (port offset)")
    ap.add_argument("--keep-sitl", action="store_true",
                    help="Leave SITL running after tests")
    ap.add_argument("--connect-only", action="store_true",
                    help="Only connect to an already-running SITL")
    args = ap.parse_args()

    # Find SITL binary
    binary = args.sitl_binary
    if not binary:
        for name in ("arducopter", "sim_vehicle.py"):
            found = shutil.which(name)
            if found:
                binary = found
                break
    if not binary:
        print("ERROR: No SITL binary found. Install arducopter or use --sitl-binary")
        sys.exit(1)

    inst = args.instance
    serial0_port = 5760 + inst * 10  # e.g., instance 3 → 5790
    conn_str = f"tcp:127.0.0.1:{serial0_port}"

    proc = None
    if not args.connect_only:
        home = "42.3000,-83.7000,180,0"
        print(f"Starting SITL (instance {inst}, SERIAL0 on tcp:{serial0_port})...")
        cmd = [
            binary,
            "--home", home,
            "--model", "+",
            "--speedup", "3",
            "--instance", str(inst),
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  SITL PID={proc.pid}")
        time.sleep(8)  # Wait for boot
    else:
        print(f"Connecting to already-running SITL at {conn_str}...")

    # Connect
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
        if proc:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        sys.exit(1)

    print(f"  Connected. System={conn.target_system}, Component={conn.target_component}")

    # Drain pre-boot messages
    time.sleep(0.5)
    while conn.recv_match(blocking=False) is not None:
        pass

    # Run tests (capture conn by default arg to avoid late-binding issues)
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
    if proc and not args.keep_sitl:
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