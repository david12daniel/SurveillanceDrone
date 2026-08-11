#!/usr/bin/env python3
"""Quick SITL validation: launches SITL, runs mode ACK test, reports."""
import os, sys, time, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pymavlink import mavutil
from helpers import set_mode_via_command, wait_mode, MODE

SITL_BIN = os.path.expanduser("~/.dronekit/sitl/copter-3.3/apm")
INSTANCE = 5
PORT = 5760 + INSTANCE * 10  # 5810

# Start SITL
cmd = [
    SITL_BIN,
    "--home=42.3000,-83.7000,180,0",
    "--model=quad",
    "--speedup=3",
    f"-I{INSTANCE}",
]
proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"SITL PID={proc.pid}, waiting 8s for boot...")
time.sleep(8)

# Connect
conn_str = f"tcp:127.0.0.1:{PORT}"
print(f"Connecting to {conn_str}...")
conn = mavutil.mavlink_connection(conn_str, dialect="ardupilotmega",
                                  source_system=255, source_component=191)
deadline = time.time() + 15
connected = False
while time.time() < deadline:
    if conn.wait_heartbeat(blocking=False) is not None:
        connected = True
        break
    time.sleep(0.5)

if not connected:
    print("FAIL: Could not connect to SITL")
    proc.terminate()
    proc.wait()
    sys.exit(1)

print(f"Connected. System={conn.target_system}")

# Drain pre-boot
time.sleep(0.5)
while conn.recv_match(blocking=False) is not None:
    pass

# Test mode ACKs
results = []
for mode_name in ("AUTO", "GUIDED", "RTL", "LAND", "STABILIZE"):
    ok = set_mode_via_command(conn, mode_name)
    hb_ok = wait_mode(conn, MODE[mode_name])
    label = "PASS" if (ok and hb_ok) else "FAIL"
    results.append((mode_name, label))
    print(f"  [{label}] Mode {mode_name}: ack={ok}, hb={hb_ok}")

# Invalid mode test
conn.mav.set_mode_send(conn.target_system,
                       mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 99)
deadline = time.time() + 10
acked = False
while time.time() < deadline:
    ack = conn.recv_match(type="COMMAND_ACK", blocking=False)
    if ack is not None and ack.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
        if ack.result != mavutil.mavlink.MAV_RESULT_ACCEPTED:
            acked = True
            break
    time.sleep(0.05)
label = "PASS" if acked else "FAIL"
results.append(("Invalid mode 99 rejected", label))
print(f"  [{label}] Invalid mode rejection: {acked}")

# Summary
passed = sum(1 for _, l in results if l == "PASS")
failed = sum(1 for _, l in results if l == "FAIL")
print(f"\n{passed} passed, {failed} failed")

conn.close()
proc.terminate()
try:
    proc.wait(timeout=10)
except subprocess.TimeoutExpired:
    proc.kill()

sys.exit(0 if failed == 0 else 1)