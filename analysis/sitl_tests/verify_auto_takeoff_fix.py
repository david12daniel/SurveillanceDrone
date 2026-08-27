#!/usr/bin/env python3
"""D2.16 Minimal SITL smoke test — just verify SITL boots, connects, arms in GUIDED."""
import os, sys, signal, subprocess, time, threading
from pymavlink import mavutil

SITL_BIN = os.path.expanduser("~/.openclaw/bin/arducopter")
SIM_VPY = os.path.expanduser("~/ardupilot-sitl-src/Tools/autotest/sim_vehicle.py")
I = 42  # unique instance
PORT = 5760 + I * 10

def cleanup(proc):
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except: pass
    try: proc.wait(timeout=5)
    except:
        try: os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except: pass

print("1. Launching SITL...", flush=True)
proc = subprocess.Popen(
    [sys.executable, SIM_VPY, "-v", "ArduCopter", "-f", "+",
     "--vehicle-binary", SITL_BIN, "-N", "-l", "42.3000,-83.7000,180,0",
     "-S", "3", "-I", str(I), "-w", "--no-mavproxy", "--no-extra-ports"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    start_new_session=True)

time.sleep(5)

print("2. Connecting...", flush=True)
conn = mavutil.mavlink_connection(f"tcp:127.0.0.1:{PORT}",
    dialect="ardupilotmega", source_system=255, source_component=191)

deadline = time.time() + 15
while time.time() < deadline:
    if conn.wait_heartbeat(blocking=False): break
    time.sleep(0.5)
else:
    print("FAIL: No HEARTBEAT", flush=True); cleanup(proc); sys.exit(1)

print(f"   HEARTBEAT OK, sys={conn.target_system}", flush=True)
conn.target_component = mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1
time.sleep(0.5)
while conn.recv_match(blocking=False): pass

conn.mav.request_data_stream_send(conn.target_system, conn.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_ALL, 10, 1)

# RC override feed
stop = threading.Event()
def feed():
    while not stop.is_set():
        try: conn.mav.rc_channels_override_send(conn.target_system, conn.target_component, 1500,1500,1100,1500,0,0,0,0)
        except: break
        stop.wait(0.2)
t = threading.Thread(target=feed, daemon=True); t.start()

print("3. Checking params...", flush=True)
conn.mav.param_request_read_send(conn.target_system, conn.target_component, b"AUTO_OPTIONS", -1)
time.sleep(2)
for _ in range(50):
    m = conn.recv_match(type="PARAM_VALUE", blocking=False)
    if m and m.param_id.upper() == b"AUTO_OPTIONS":
        print(f"   AUTO_OPTIONS = {m.param_value}", flush=True)
        break
    time.sleep(0.1)
else:
    print("   AUTO_OPTIONS: read timeout", flush=True)
    
# Try RC3_MIN
conn.mav.param_request_read_send(conn.target_system, conn.target_component, b"RC3_MIN", -1)
time.sleep(2)
for _ in range(50):
    m = conn.recv_match(type="PARAM_VALUE", blocking=False)
    if m and m.param_id.upper() == b"RC3_MIN":
        print(f"   RC3_MIN = {m.param_value}", flush=True)
        break
    time.sleep(0.1)
else:
    print("   RC3_MIN: read timeout", flush=True)

print("4. Setting GUIDED mode...", flush=True)
conn.mav.command_long_send(conn.target_system, conn.target_component,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 4, 0, 0,0,0,0)
time.sleep(2)

print("5. Arming...", flush=True)
conn.mav.command_long_send(conn.target_system, conn.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1,0,0,0,0,0,0)
time.sleep(3)

hb = conn.recv_match(type="HEARTBEAT", blocking=False)
armed = hb and (hb.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
print(f"   Armed: {armed}", flush=True)

if not armed:
    print("5b. Waiting for EKF and retrying...", flush=True)
    time.sleep(10)
    conn.mav.command_long_send(conn.target_system, conn.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1,0,0,0,0,0,0)
    time.sleep(3)
    hb = conn.recv_match(type="HEARTBEAT", blocking=False)
    armed = hb and (hb.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
    print(f"   Armed (retry): {armed}", flush=True)

if not armed:
    print("FAIL: Could not arm", flush=True)
    stop.set(); cleanup(proc)
    # Also check STATUSTEXT for prearm reasons
    for _ in range(20):
        m = conn.recv_match(type="STATUSTEXT", blocking=False)
        if m:
            print(f"   SITL says: {m.text}", flush=True)
        time.sleep(0.1)
    sys.exit(1)

print("6. Setting AUTO_OPTIONS=2...", flush=True)
conn.mav.param_set_send(conn.target_system, conn.target_component,
    b"AUTO_OPTIONS", 2.0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
time.sleep(1)

print("7. Switching to AUTO...", flush=True)
conn.mav.command_long_send(conn.target_system, conn.target_component,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 3, 0,0,0,0,0)
time.sleep(2)

hb = conn.recv_match(type="HEARTBEAT", blocking=False)
mode = hb.custom_mode if hb else -1
print(f"   Mode: {mode} (AUTO=3)", flush=True)

print("8. Monitoring climb (30s)...", flush=True)
deadline = time.time() + 30
max_alt = 0.0
while time.time() < deadline:
    m = conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
    if m:
        alt = m.relative_alt / 1000.0
        if alt > max_alt:
            max_alt = alt
        if alt > 1.0:
            print(f"   Climbing: {alt:.1f}m", flush=True)
    time.sleep(0.3)

print(f"   Max alt: {max_alt:.1f}m", flush=True)

stop.set()
cleanup(proc)

if max_alt >= 13.0:
    print("\nPASS: AUTO-mode takeoff confirmed with AUTO_OPTIONS=2 fix", flush=True)
    sys.exit(0)
elif max_alt > 1.0:
    print(f"\nPARTIAL: Climbed to {max_alt:.1f}m but below 13m target", flush=True)
    sys.exit(2)
else:
    print("\nFAIL: No climb detected", flush=True)
    sys.exit(1)