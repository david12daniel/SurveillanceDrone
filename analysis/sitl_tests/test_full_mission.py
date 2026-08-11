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

    KNOWN FAILING as of task D2.13 (2026-08-10): three real bugs on the path
    to this point were found and fixed (mission upload only listened for
    MISSION_REQUEST_INT, not the legacy MISSION_REQUEST ArduPilot actually
    sends; arming was attempted directly in AUTO, which
    AUTO_OPTIONS/"Allow Arming" blocks by default; the mission was missing
    the conventional seq-0 home placeholder, so AUTO reported "Missing
    Takeoff Cmd"). What's left blocking this test is not fixable from here:
    with all of the above fixed, AUTO correctly announces "Mission: 1
    Takeoff" and arms, but the vehicle never climbs -- SERVO_OUTPUT_RAW
    shows motors ramp to arm-idle (~1100) then cut to 1000 a few seconds
    later, and direct process monitoring confirmed the arducopter SITL
    binary itself crashes at that point ("Closed connection on SERIAL0" is
    the last line in its own log, then the process is gone). This is a
    binary-level SITL instability during AUTO-mode takeoff, not a
    mission_app.py or test-harness bug -- worth flagging upstream or
    trying a different SITL build, not chasing further from the Python
    side.
    """
    # ── 1. Upload a simple mission ──────────────────────────────────────────
    # seq 0 is a conventional home/reference placeholder, not a real command
    # -- ArduPilot's mission protocol expects it and treats a mission that
    # skips straight to real commands at seq 0 as having no takeoff command
    # at all ("Auto: Missing Takeoff Cmd" / "Mode change to Auto failed:
    # init failed"), confirmed by direct probing (task D2.13, 2026-08-10).
    # Real commands start at seq 1, matching how QGroundControl/Mission
    # Planner structure an upload.
    items = [
        # 0: home placeholder (conventional, not executed)
        {"frame": 0, "command": 16, "current": 1, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": HOME_LAT, "y": HOME_LON, "z": 180.0},
        # 1: TAKEOFF to 20 m (lower for test speed)
        {"frame": 3, "command": 22, "current": 0, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": HOME_LAT, "y": HOME_LON, "z": 20.0},
        # 2: WAYPOINT 50 m north
        {"frame": 3, "command": 16, "current": 0, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": HOME_LAT + 50, "y": HOME_LON, "z": 20.0},
        # 3: WAYPOINT 50 m east
        {"frame": 3, "command": 16, "current": 0, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": HOME_LAT + 50, "y": HOME_LON + 50, "z": 20.0},
        # 4: RTL (return to launch)
        {"frame": 3, "command": 20, "current": 0, "autocontinue": 1,
         "param1": 0, "param2": 0, "param3": 0, "param4": 0,
         "x": 0, "y": 0, "z": 0},
    ]

    ok = upload_mission(sitl_conn, items)
    assert ok, "Mission upload failed"

    # ── 2. Arm, then engage AUTO to start the mission ───────────────────────
    # Arming happens BEFORE the AUTO mode switch, per this module's own
    # docstring ("arm -> takeoff -> AUTO -> ..."). An earlier version armed
    # AFTER switching to AUTO and hit ArduCopter's "Auto mode not armable"
    # gate: AUTO_OPTIONS bit 0 (Allow Arming) is off by default, a
    # deliberate safety feature blocking arm-directly-in-AUTO so a vehicle
    # can't be armed and immediately launch into its mission with no
    # attitude/RC sanity check first (confirmed via direct probing, task
    # D2.13, 2026-08-10). Arming from GUIDED first and switching to AUTO
    # once armed and flying is the standard, unblocked ArduCopter workflow
    # -- fixing the test's own sequencing rather than loosening that
    # firmware safety gate.
    ok = set_mode_via_command(sitl_conn, "GUIDED")
    assert ok, "GUIDED mode command failed"

    ok = arm_and_check(sitl_conn)
    assert ok, "Arm in GUIDED failed"

    ok = set_mode_via_command(sitl_conn, "AUTO")
    assert ok, "AUTO mode command failed"

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
    # An earlier version of this test asserted that SITL "echoes" a
    # STATUSTEXT the app sends -- confirmed false by direct probing (task
    # D2.13, 2026-08-10): only messages ArduPilot itself originates
    # (srcSystem=1) ever come back; a GCS-originated STATUSTEXT is simply
    # not something the FC relays. There's also no way to verify "a real
    # GCS would see it" from inside this suite -- SITL's SERIAL0 TCP port
    # only accepts one client, so a second connection to independently
    # observe app-to-GCS traffic isn't available here. What IS verifiable
    # from this side of the link: the app can send an operator alert
    # without a protocol error, and the send doesn't perturb SITL's own
    # message flow (still get real HEARTBEATs back afterward).
    from pymavlink import mavutil

    sent_text = "TEST_ALERT mission_app_detection 0.95"

    sitl_conn.mav.statustext_send(
        mavutil.mavlink.MAV_SEVERITY_NOTICE,
        sent_text.encode("utf-8")[:50],
    )

    hb = None
    deadline = time.time() + 5.0
    while time.time() < deadline:
        hb = sitl_conn.recv_match(type="HEARTBEAT", blocking=False)
        if hb is not None:
            break
        time.sleep(0.1)

    assert hb is not None, "SITL stopped responding after the app sent a STATUSTEXT"