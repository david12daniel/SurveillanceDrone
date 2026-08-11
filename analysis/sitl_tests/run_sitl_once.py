#!/usr/bin/env python3
"""Run all SITL tests with an auto-managed arducopter process (Copter 3.3)."""
import sys, os, time, subprocess, signal

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pymavlink import mavutil
from helpers import (
    set_mode_via_command, arm_and_check, guided_takeoff,
    send_position_target, wait_position, wait_mode, MODE,
    set_param, get_param,
)

PASS, FAIL = 0, 1
results = []

def test(name, fn):
    try:
        fn()
        results.append((name, PASS, ""))
        print(f"  [PASS] {name}")
    except Exception as e:
        results.append((name, FAIL, str(e)))
        print(f"  [FAIL] {name}: {e}")

binary = os.path.join(HERE, "bin", "arducopter")
assert os.path.isfile(binary), f"Binary not found: {binary}"

# Kill any leftover arducopter processes
os.system("killall -9 arducopter 2>/dev/null")
time.sleep(2)

inst = 0
home = "42.3000,-83.7000,180,0"

print("Starting Copter 3.3 SITL (UDP-based)...")
proc = subprocess.Popen(
    [binary, "--home", home, "--model", "+", "--instance", str(inst)],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"  PID={proc.pid}")

# Old SITL (3.3) uses UDP on 5760+inst*10 (SERIAL0)
serial0_port = 5760 + inst * 10  # 5760
time.sleep(6)

# Check it's alive
if proc.poll() is not None:
    print(f"FAIL: SITL exited with code {proc.returncode}")
    sys.exit(1)

# Connect via UDP
conn = mavutil.mavlink_connection(f"udp:127.0.0.1:{serial0_port}",
                                   dialect="ardupilotmega",
                                   source_system=255, source_component=191,
                                   input=False)
deadline = time.time() + 25
while time.time() < deadline:
    if conn.wait_heartbeat(blocking=False) is not None:
        break
    time.sleep(0.5)
else:
    print("FAIL: no HEARTBEAT (tried UDP)")
    proc.terminate()
    sys.exit(1)

print(f"  Connected. sys={conn.target_system} comp={conn.target_component} mode={conn.flightmode}")
time.sleep(1)
# Drain pre-boot messages
while conn.recv_match(blocking=False) is not None:
    pass

# --- Mode ACK tests ---
print("\n--- [1] Mode ACK ---")
def mode_ack():
    for mode_name in ("AUTO", "GUIDED", "RTL", "LAND", "STABILIZE"):
        ok = set_mode_via_command(conn, mode_name)
        assert ok, f"{mode_name} mode command was not accepted"
        hb_ok = wait_mode(conn, MODE[mode_name])
        assert hb_ok, f"HEARTBEAT did not report {mode_name}"
        print(f"    {mode_name}: OK")
test("Mode ACK", mode_ack)

# --- Arming gates ---
print("\n--- [2] Arming gates ---")
def arming():
    set_mode_via_command(conn, "STABILIZE")
    time.sleep(1)
    # Send arm command (EKF not converged yet - that's OK, try anyway)
    conn.mav.command_long_send(
        conn.target_system, conn.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, 1, 0, 0, 0, 0, 0, 0)
    time.sleep(2)
    # Wait for EKF convergence
    print("    Waiting for EKF convergence...")
    deadline = time.time() + 30
    ekf_ok = False
    while time.time() < deadline:
        ekf = conn.recv_match(type="EKF_STATUS_REPORT", blocking=False)
        if ekf and (ekf.flags & 0x0F):
            ekf_ok = True
            break
        time.sleep(0.5)
    assert ekf_ok, "EKF did not converge within 30s"
    print("    EKF converged")
    # Now arm in GUIDED
    set_mode_via_command(conn, "GUIDED")
    time.sleep(1)
    armed = arm_and_check(conn, timeout=15)
    assert armed, "Arm in GUIDED after EKF convergence failed"
    print("    ARM in GUIDED: OK")
test("Arming gates", arming)

# --- GUIDED nav ---
print("\n--- [3] GUIDED nav ---")
def guided_nav():
    ok = guided_takeoff(conn, alt_m=15.0)
    assert ok, "Guided takeoff failed"
    print("    Takeoff to 15m: OK")
    # Descend to 10m
    lat, lon = 42_3000000, -83_7000000
    send_position_target(conn, lat, lon, 10.0)
    deadline = time.time() + 25
    reached = False
    while time.time() < deadline:
        msg = conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg and (msg.relative_alt / 1000.0) <= 11.0:
            reached = True
            break
        time.sleep(0.2)
    assert reached, "Did not descend to 10m"
    print("    Descent to 10m: OK")
    # Move to offset position
    olat, olon = 42_3000500, -83_6999500
    send_position_target(conn, olat, olon, 15.0)
    converged = wait_position(conn, olat, olon, pos_tolerance_m=10.0, timeout=30)
    assert converged, "Did not converge to position target"
    print("    Position convergence: OK")
test("Guided nav", guided_nav)

# --- Failsafe params ---
print("\n--- [4] Failsafe params ---")
def failsafe():
    for pname in ("FS_BATT_VOLTAGE", "BATT_LOW_VOLT", "FS_THR_ENABLE", "BATT_FS_LOW_ACT"):
        val = get_param(conn, pname)
        assert val is not None, f"Could not read {pname}"
        print(f"    {pname} = {val}")
    ok = set_param(conn, "FS_BATT_VOLTAGE", 10.0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
    assert ok, "Could not set FS_BATT_VOLTAGE"
    readback = get_param(conn, "FS_BATT_VOLTAGE")
    assert readback is not None and abs(readback - 10.0) < 0.01, f"Mismatch: {readback}"
    print("    Param set+readback: OK")
test("Failsafe params", failsafe)

# --- Summary ---
print("\n" + "="*60)
print("RESULTS")
print("="*60)
passed = sum(1 for _, s, _ in results if s == PASS)
failed = sum(1 for _, s, _ in results if s == FAIL)
for name, status, msg in results:
    label = {PASS: "PASS", FAIL: "FAIL"}[status]
    print(f"  [{label}] {name}")
    if msg:
        print(f"         {msg}")
print(f"\n{passed} passed, {failed} failed")

conn.close()
proc.terminate()
try: proc.wait(timeout=10)
except subprocess.TimeoutExpired: proc.kill()

sys.exit(0 if failed == 0 else 1)
