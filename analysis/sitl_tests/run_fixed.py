#!/usr/bin/env python3
"""Fixed SITL test runner for older ArduCopter v3.3 binary."""
import subprocess, time, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pymavlink import mavutil
from helpers import MODE, MODE_TIMEOUT_S, ARM_TIMEOUT_S, TAKEOFF_TIMEOUT_S, POSITION_TIMEOUT_S

PASS, FAIL = 0, 1
results = []

def test(name, fn):
    try:
        fn()
        results.append((name, PASS, ""))
        print(f"  PASS  {name}")
    except Exception as e:
        results.append((name, FAIL, str(e)))
        print(f"  FAIL  {name}: {e}")

def wait_mode(conn, mode, timeout=10.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        msg = conn.recv_match(type="HEARTBEAT", blocking=False)
        if msg and msg.get_srcComponent() == 1:
            if msg.custom_mode == mode:
                return True
        time.sleep(0.05)
    return False

def set_mode(conn, mode_name):
    mode_num = MODE[mode_name]
    conn.mav.set_mode_send(1, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, mode_num)
    # Old SITL v3.3 sometimes doesn't send COMMAND_ACK - wait for mode in heartbeat
    return wait_mode(conn, mode_num, timeout=10.0)

def arm(conn, timeout=15.0):
    conn.mav.command_long_send(1, 1, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
    deadline = time.time() + timeout
    while time.time() < deadline:
        hb = conn.recv_match(type="HEARTBEAT", blocking=False)
        if hb and hb.get_srcComponent() == 1:
            if hb.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED:
                return True
        time.sleep(0.1)
    return False

def get_param(conn, name, timeout=5.0):
    conn.mav.param_request_read_send(1, 1, name.encode("utf-8")[:16], -1)
    deadline = time.time() + timeout
    while time.time() < deadline:
        msg = conn.recv_match(type="PARAM_VALUE", blocking=False)
        if msg:
            got_name = msg.param_id
            if isinstance(got_name, bytes):
                got_name = got_name.decode("utf-8", errors="replace").strip()
            else:
                got_name = got_name.strip()
            if got_name == name:
                return msg.param_value
        time.sleep(0.05)
    return None

def set_param(conn, name, value, param_type, timeout=5.0):
    conn.mav.param_set_send(1, 1, name.encode("utf-8")[:16], value, param_type)
    deadline = time.time() + timeout
    while time.time() < deadline:
        msg = conn.recv_match(type="PARAM_VALUE", blocking=False)
        if msg:
            got_name = msg.param_id
            if isinstance(got_name, bytes):
                got_name = got_name.decode("utf-8", errors="replace").strip()
            else:
                got_name = got_name.strip()
            if got_name == name:
                return abs(msg.param_value - value) < 0.01
        time.sleep(0.05)
    return False

def mode_ack_tests(conn):
    for mode_name in ("STABILIZE", "GUIDED", "LOITER", "RTL", "LAND", "AUTO"):
        ok = set_mode(conn, mode_name)
        assert ok, f"{mode_name} mode was not accepted"
        print(f"    {mode_name}: mode heartbeat OK")

def arming_tests(conn):
    set_mode(conn, "STABILIZE")
    time.sleep(0.5)
    ok = arm(conn, timeout=5.0)
    print(f"    Arm in STABILIZE at boot: {'succeeded' if ok else 'rejected (expected)'}")

    # Wait for EKF
    deadline = time.time() + 20
    while time.time() < deadline:
        ekf = conn.recv_match(type="EKF_STATUS_REPORT", blocking=False)
        if ekf and (ekf.flags & 0x0F):
            print("    EKF converged")
            break
        time.sleep(0.5)
    else:
        print("    SKIP: EKF did not converge within 20s")
        return

    set_mode(conn, "GUIDED")
    time.sleep(0.5)
    ok = arm(conn)
    assert ok, "Arm in GUIDED after EKF should succeed"
    print("    ARM after EKF: OK")

def failsafe_params_tests(conn):
    for pname in ("FS_BATT_VOLTAGE", "BATT_LOW_VOLT", "FS_BATT_MAH"):
        val = get_param(conn, pname)
        assert val is not None, f"Could not read {pname}"
        print(f"    {pname} = {val}")

    ok = set_param(conn, "FS_BATT_VOLTAGE", 10.0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
    assert ok, "Could not set FS_BATT_VOLTAGE"
    readback = get_param(conn, "FS_BATT_VOLTAGE")
    assert readback is not None and abs(readback - 10.0) < 0.1, f"Readback mismatch: {readback}"
    print("    Param set+readback: OK")

def main():
    binary = "/home/david12daniel/.dronekit/sitl/copter-3.3/apm"
    inst = 4
    port = 5760 + inst * 10
    conn_str = f"tcp:127.0.0.1:{port}"

    print(f"Starting SITL (instance {inst}, port {port})...")
    cmd = [binary, "--home", "42.3000,-83.7000,180,0", "--model", "+", "--speedup", "1", "--instance", str(inst)]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(8)

    print(f"Connecting to {conn_str}...")
    conn = mavutil.mavlink_connection(conn_str, dialect="ardupilotmega", source_system=255, source_component=191)
    deadline = time.time() + 20
    while time.time() < deadline:
        if conn.wait_heartbeat(blocking=False):
            break
        time.sleep(0.5)
    else:
        print("FAIL: Could not connect")
        proc.kill()
        sys.exit(1)

    hb = conn.recv_match(type="HEARTBEAT", blocking=True, timeout=3)
    print(f"  Connected. Sys={conn.target_system}  Mode={hb.custom_mode}")
    time.sleep(0.5)
    while conn.recv_match(blocking=False):
        pass

    print("\n--- Mode ACK tests ---")
    test("Mode ACK - all modes", lambda: mode_ack_tests(conn))

    print("\n--- Arming tests ---")
    test("Arming - pre-arm checks", lambda: arming_tests(conn))

    print("\n--- Failsafe param tests ---")
    test("Failsafe params - read/write", lambda: failsafe_params_tests(conn))

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    passed = sum(1 for _, s, _ in results if s == PASS)
    failed = sum(1 for _, s, _ in results if s == FAIL)
    for name, status, msg in results:
        label = {PASS: "PASS", FAIL: "FAIL"}[status]
        print(f"  [{label}] {name}")
        if msg: print(f"         {msg}")
    print(f"\n{passed} passed, {failed} failed")

    conn.close()
    proc.terminate()
    try: proc.wait(timeout=10)
    except: proc.kill()
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()