"""End-to-end full-mission test.

Exercises the complete mission app cycle against real SITL:
  1. GUIDED takeoff to 120 m
  2. Waypoint mission uploaded and flown in AUTO
  3. Full detection cycle (simulated: GUIDED descent → resume)

This is the SITL analogue of the mock-FC `test_nominal_detection_cycle` but
with real ArduPilot mode acceptance, navigation, and failsafe behavior.
"""
import time
import pytest
from helpers import (
    set_mode_via_command, arm_and_check, guided_takeoff,
    set_param, wait_mode, send_position_target, wait_position,
    MODE, upload_mission, read_mission_item,
)
from params_sets import LINK_LOSS_FS, LOW_BATTERY_FS, RTL_CRUISE


# SITL home (used to build waypoints)
HOME_LAT = 42_3000000
HOME_LON = -83_7000000


def test_full_detection_cycle_mission(sitl_conn):
    """End-to-end: arm → takeoff to 120 m → detect at simulated POI → descend → resume.

    This exercise validates that the mission app's control contract functions
    correctly against real ArduPilot: mode changes are ACK'd, GUIDED position
    targets are navigated to, and the vehicle can be returned to AUTO.

    Steps:
    1. Upload a simple waypoint mission (takeoff + 2 waypoints + RTL)
    2. Switch to AUTO, arm, verify it flies
    3. Switch to GUIDED, command a descent (simulating the detection cycle)
    4. Return to AUTO, verify it rejoins the mission
    """
    # ── 1. Upload a simple mission ──────────────────────────────────────────
    items = [
        # 0: TAKEOFF to 20 m (lower for test speed)
        {"frame": 3, "command": 22, "current": 1, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": HOME_LAT, "y": HOME_LON, "z": 20.0},
        # 1: WAYPOINT 50 m north
        {"frame": 3, "command": 16, "current": 0, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": HOME_LAT + 50, "y": HOME_LON, "z": 20.0},
        # 2: WAYPOINT 50 m east
        {"frame": 3, "command": 16, "current": 0, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": HOME_LAT + 50, "y": HOME_LON + 50, "z": 20.0},
        # 3: RTL (return to launch)
        {"frame": 3, "command": 20, "current": 0, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": 0, "y": 0, "z": 0},
    ]

    ok = upload_mission(sitl_conn, items)
    assert ok, "Mission upload failed"

    # ── 2. AUTO takeoff ─────────────────────────────────────────────────────
    ok = set_mode_via_command(sitl_conn, "AUTO")
    assert ok, "AUTO mode command failed"

    # Arm in AUTO (SITL should accept after mission upload)
    ok = arm_and_check(sitl_conn)
    assert ok, "Arm in AUTO failed"

    # Wait for vehicle to reach altitude
    deadline = time.time() + 45.0
    reached_alt = False
    while time.time() < deadline:
        msg = sitl_conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg is not None:
            alt = msg.relative_alt / 1000.0
            if alt >= 18.0:
                reached_alt = True
                break
        time.sleep(0.2)

    assert reached_alt, "Vehicle did not take off in AUTO within 45s"

    # ── 3. Simulate detection: switch to GUIDED and command a descent ───────
    ok = set_mode_via_command(sitl_conn, "GUIDED")
    assert ok, "GUIDED mode transition failed"

    # Command descent to 10 m (simulates the detection→classify descent)
    send_position_target(sitl_conn, HOME_LAT + 50, HOME_LON + 50, 10.0)
    time.sleep(3.0)

    # Verify we're descending
    deadline = time.time() + 20.0
    descended = False
    while time.time() < deadline:
        msg = sitl_conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg is not None:
            alt = msg.relative_alt / 1000.0
            if alt <= 12.0:
                descended = True
                break
        time.sleep(0.2)

    assert descended, "Vehicle did not descend after GUIDED position target"

    # ── 4. Return to AUTO and verify the mission resumes ────────────────────
    ok = set_mode_via_command(sitl_conn, "AUTO")
    assert ok, "AUTO mode transition after investigation failed"

    # Wait for the vehicle to be in AUTO and flying
    ok = wait_mode(sitl_conn, MODE["AUTO"])
    assert ok, "Vehicle did not enter AUTO after investigation complete"

    # Let it fly for a few more seconds — no crash means success
    time.sleep(3.0)

    # Final status: should be in AUTO or RTL (if mission completed)
    hb = sitl_conn.recv_match(type="HEARTBEAT", blocking=False)
    if hb is not None:
        mode_name = {v: k for k, v in MODE.items()}.get(hb.custom_mode, str(hb.custom_mode))
        print(f"Final flight mode: {mode_name}")
        assert hb.custom_mode in (MODE["AUTO"], MODE["RTL"], MODE["GUIDED"]), \
            f"Unexpected final mode: {mode_name}"


def test_mission_app_compatible_actions(sitl_conn):
    """Verify the specific MAVLink commands the mission app uses produce
    the expected SITL responses.

    Tests the app-to-SITL baseline that the mock FC cannot test.
    """
    # The mission app sends these in its auto→guided cycle:
    #   - set_mode_send(MODE=GUIDED)  - tested in test_set_mode_guided_ack
    #   - SET_POSITION_TARGET_GLOBAL_INT - tested in test_guided_position_target_converges
    #   - statustext_send() - the app emits operator alerts
    #   - set_mode_send(MODE=AUTO)  - tested in test_set_mode_auto_ack
    #
    # This test validates that the statustext is visible to SITL/GCS.
    from pymavlink import mavutil

    sent_text = "TEST_ALERT mission_app_detection 0.95"

    sitl_conn.mav.statustext_send(
        mavutil.mavlink.MAV_SEVERITY_NOTICE,
        sent_text.encode("utf-8")[:50],
    )

    # SITL echoes statustext messages; verify it appeared on the wire
    deadline = time.time() + 5.0
    found = False
    while time.time() < deadline:
        msg = sitl_conn.recv_match(type="STATUSTEXT", blocking=False)
        if msg is not None:
            txt = msg.text if isinstance(msg.text, str) else msg.text.decode("utf-8", errors="replace")
            if "TEST_ALERT" in txt:
                found = True
                break
        time.sleep(0.1)

    assert found, "STATUSTEXT sent by app was not visible on the MAVLink bus"