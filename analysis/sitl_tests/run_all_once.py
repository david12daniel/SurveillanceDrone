#!/usr/bin/env python3
"""Run ALL SITL tests in one shot and print results."""
import sys, os, time, subprocess, traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pymavlink import mavutil
from helpers import (
    set_mode_via_command, arm_and_check, guided_takeoff,
    send_position_target, wait_position, wait_mode, MODE,
    set_param, get_param,
)

PASS, FAIL, SKIP = range(3)
results = []

def test(name, fn):
    try:
        fn()
        results.append((name, PASS, ""))
        print(f"  [PASS] {name}")
    except Exception as e:
        results.append((name, FAIL, str(e)))
        print(f"  [FAIL] {name}: {e}")

# --- Mode ACK tests ---
def mode_ack_tests(conn):
    for mode_name in ("AUTO", "GUIDED", "RTL", "LAND", "STABILIZE"):
        ok = set_mode_via_command(conn, mode_name)
        assert ok, f"{mode_name} mode command was not accepted"
        hb_ok = wait_mode(conn, MODE[mode_name])
        assert hb_ok, f"HEARTBEAT did not report {mode_name}"
    # Invalid mode should be rejected
    conn.mav.set_mode_send(conn.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 99)
    deadline = time.time() + 10
    acked = False
    while time.time() < deadline:
        ack = conn.recv_match(type="COMMAND_ACK", blocking=False)
        if ack is not None and ack.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
            assert ack.result != mavutil.mavlink.MAV_RESULT_ACCEPTED, "Invalid mode 99 should NOT be accepted"
            acked = True; break
        time.sleep(0.05)
    assert acked, "No COMMAND_ACK for invalid mode"

# --- Arming gate tests ---
def arming_tests(conn):
    set_mode_via_command(conn, "STABILIZE"); time.sleep(0.5)
    arm_result = arm_and_check(conn, timeout=5.0)
    print(f"    Arm at boot: {'OK' if arm_result else 'rejected (expected)'}")
    deadline = time.time() + 20
    ekf_ok = False
    while time.time() < deadline:
        ekf = conn.recv_match(type="EKF_STATUS_REPORT", blocking=False)
        if ekf is not None and (ekf.flags & 0x0F):
            ekf_ok = True; break
        msg = conn.recv_match(type="STATUSTEXT", blocking=False)
        time.sleep(0.5)
    if ekf_ok:
        set_mode_via_command(conn, "GUIDED"); time.sleep(0.5)
        armed = arm_and_check(conn, timeout=10)
        assert armed, "Arm in GUIDED after EKF should succeed"
        print("    ARM after EKF convergence: OK")
    else:
        print("    SKIP: EKF did not converge within 20s")
        raise Exception("EKF did not converge")

# --- GUIDED nav tests ---
def guided_nav_tests(conn):
    ok = guided_takeoff(conn, alt_m=20.0)
    assert ok, "Guided takeoff failed"; print("    Takeoff to 20m: OK")
    lat, lon = 42_3000000, -83_7000000
    send_position_target(conn, lat, lon, 10.0)
    deadline = time.time() + 20
    reached = False
    while time.time() < deadline:
        msg = conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg and (msg.relative_alt / 1000.0) <= 11.0:
            reached = True; break
        time.sleep(0.2)
    assert reached, "Did not descend to 10m"; print("    Descent to 10m: OK")
    offset_lat, offset_lon = 42_3000500, -83_6999500
    send_position_target(conn, offset_lat, offset_lon, 15.0)
    converged = wait_position(conn, offset_lat, offset_lon, pos_tolerance_m=10.0, timeout=30)
    assert converged, "Did not converge to position"; print("    Position convergence: OK")

# --- Failsafe param tests ---
def failsafe_tests(conn):
    for pname in ("FS_BATT_VOLTAGE", "BATT_LOW_VOLT", "FS_THR_ENABLE", "BATT_FS_LOW_ACT"):
        val = get_param(conn, pname)
        assert val is not None, f"Could not read {pname}"
        print(f"    {pname} = {val}")
    ok = set_param(conn, "FS_BATT_VOLTAGE", 10.0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
    assert ok, "Could not set FS_BATT_VOLTAGE"
    readback = get_param(conn, "FS_BATT_VOLTAGE")
    assert readback is not None and abs(readback - 10.0) < 0.01, f"Mismatch: {readback}"
    print("    Param set+readback: OK")

# --- MAIN ---
binary = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", "arducopter")
if not os.path.isfile(binary):
    print(f"ERROR: binary not found at {binary}")
    sys.exit(1)

inst = 14
serial0_port = 5760 + inst * 10
home = "42.3000,-83.7000,180,0"

print(f"Starting SITL (instance {inst}, SERIAL0 tcp:{serial0_port})...")
cmd = [binary, "--home", home, "--model", "+", "--speedup", "3", "--instance", str(inst)]
proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"  SITL PID={proc.pid}")
time.sleep(8)

conn_str = f"tcp:127.0.0.1:{serial0_port}"
print(f"Connecting to {conn_str}...")
conn = mavutil.mavlink_connection(conn_str, dialect="ardupilotmega", source_system=255, source_component=191)
deadline = time.time() + 20
connected = False
while time.time() < deadline:
    if conn.wait_heartbeat(blocking=False) is not None:
        connected = True; break
    time.sleep(0.5)
if not connected:
    print("FAIL: Could not connect to SITL"); proc.terminate(); sys.exit(1)
print(f"  Connected. sys={conn.target_system} comp={conn.target_component}")
time.sleep(0.5)
while conn.recv_match(blocking=False) is not None: pass

print("\n--- Mode ACK tests ---")
test("Mode ACK - all modes", lambda c=conn: mode_ack_tests(c))

print("\n--- Arming gate tests ---")
test("Arming - pre-arm checks", lambda c=conn: arming_tests(c))

print("\n--- GUIDED navigation tests ---")
test("GUIDED nav - takeoff+nav", lambda c=conn: guided_nav_tests(c))

print("\n--- Failsafe parameter tests ---")
test("Failsafe params - read/write", lambda c=conn: failsafe_tests(c))

# Summary
print("\n" + "=" * 60)
passed = sum(1 for _, s, _ in results if s == PASS)
failed = sum(1 for _, s, _ in results if s == FAIL)
print(f"RESULTS: {passed} passed, {failed} failed")
for name, status, msg in results:
    label = {PASS: "PASS", FAIL: "FAIL", SKIP: "SKIP"}[status]
    print(f"  [{label}] {name}")
    if msg: print(f"         {msg}")

conn.close()
print("Shutting down SITL...")
proc.terminate()
try: proc.wait(timeout=10)
except subprocess.TimeoutExpired: proc.kill()
print("Done.")

sys.exit(0 if failed == 0 else 1)