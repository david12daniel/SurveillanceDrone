"""Shared utilities for SITL integration tests.

Functions that arm, take off, wait for mode, set params, and poll position
convergence. All use pymavlink and assume an active SITL connection.
"""
from __future__ import annotations
import time
from pymavlink import mavutil
from pymavlink.dialects.v20 import ardupilotmega as AP

# ArduCopter mode numbers (must match the firmware build).
# Verified against ArduCopter 4.5 — see task D2.14.
MODE = {"STABILIZE": 0, "AUTO": 3, "GUIDED": 4, "LOITER": 5, "RTL": 6, "LAND": 9}

# Timeouts (conservative for SITL on modest hardware)
MODE_TIMEOUT_S = 10.0
ARM_TIMEOUT_S = 20.0
TAKEOFF_TIMEOUT_S = 30.0
POSITION_TIMEOUT_S = 60.0


def wait_mode(conn: mavutil.mavfile, mode: int, timeout: float = MODE_TIMEOUT_S) -> bool:
    """Block until the FC's HEARTBEAT reports the given flight mode.

    Returns True if the mode was achieved within timeout, False otherwise.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        msg = conn.recv_match(type="HEARTBEAT", blocking=False)
        if msg is not None and msg.get_srcComponent() == mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1:
            if msg.custom_mode == mode:
                return True
        time.sleep(0.05)
    return False


def set_mode_via_command(conn: mavutil.mavfile, mode_name: str, timeout: float = MODE_TIMEOUT_S) -> bool:
    """Set flight mode, trying both MAV_CMD_DO_SET_MODE and raw SET_MODE.

    Modern ArduPilot (4.5+) requires MAV_CMD_DO_SET_MODE via command_long_send.
    Older firmware (Copter 3.3) only accepts raw SET_MODE via set_mode_send.
    This function tries MAV_CMD_DO_SET_MODE first, falls back to raw SET_MODE
    if the ACK indicates failure, then verifies via HEARTBEAT.
    Returns True if the mode was confirmed in HEARTBEAT within timeout.
    """
    mode_num = MODE[mode_name]

    # Try MAV_CMD_DO_SET_MODE first (modern ArduPilot)
    conn.mav.command_long_send(
        conn.target_system, conn.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,  # confirmation
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,  # base_mode
        mode_num,  # custom_mode
        0, 0, 0, 0, 0  # unused params
    )
    deadline = time.time() + timeout
    do_set_mode_acked = False
    while time.time() < deadline:
        ack = conn.recv_match(type="COMMAND_ACK", blocking=False)
        if ack is not None and ack.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
            do_set_mode_acked = True
            if ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                # Confirmed via ACK; still verify via HEARTBEAT
                return wait_mode(conn, mode_num, timeout=3.0)
            # ACK received but rejected/unsupported — fall through to raw SET_MODE
            break
        time.sleep(0.02)

    # Fallback: raw SET_MODE (works on older firmware like Copter 3.3)
    conn.mav.set_mode_send(
        conn.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_num,
    )
    return wait_mode(conn, mode_num, timeout=timeout)


def _decode_param_name(raw):
    """Decode a param_id to a string, handling both bytes and str inputs."""
    if isinstance(raw, bytes):
        return raw.decode("utf-8", errors="replace").strip()
    return raw.strip()


def set_param(conn: mavutil.mavfile, name: str, value: float,
              param_type: int, timeout: float = 5.0) -> bool:
    """Set a parameter and verify it sticks (PARAM_VALUE readback).

    param_type: one of MAV_PARAM_TYPE_* constants.
    Returns True on success.
    """
    conn.mav.param_set_send(conn.target_system, conn.target_component,
                            name.encode("utf-8")[:16], value, param_type)
    deadline = time.time() + timeout
    while time.time() < deadline:
        msg = conn.recv_match(type="PARAM_VALUE", blocking=False)
        if msg is not None:
            got_name = _decode_param_name(msg.param_id)
            if got_name == name:
                return abs(msg.param_value - value) < 0.01  # close enough
        time.sleep(0.05)
    return False


def get_param(conn: mavutil.mavfile, name: str, timeout: float = 5.0) -> float | None:
    """Request a PARAM_READ and return the value.

    Returns None if the param was not received within timeout.
    """
    conn.mav.param_request_read_send(conn.target_system, conn.target_component,
                                     name.encode("utf-8")[:16], -1)
    deadline = time.time() + timeout
    while time.time() < deadline:
        msg = conn.recv_match(type="PARAM_VALUE", blocking=False)
        if msg is not None:
            got_name = _decode_param_name(msg.param_id)
            if got_name == name:
                return msg.param_value
        time.sleep(0.05)
    return None


def arm_and_check(conn: mavutil.mavfile, timeout: float = ARM_TIMEOUT_S) -> bool:
    """Arm the vehicle and wait for the armed bit in HEARTBEAT."""
    conn.mav.command_long_send(
        conn.target_system, conn.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, 1, 0, 0, 0, 0, 0, 0)
    deadline = time.time() + timeout
    while time.time() < deadline:
        hb = conn.recv_match(type="HEARTBEAT", blocking=False)
        if hb is not None and hb.get_srcComponent() == mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1:
            armed = hb.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
            if armed:
                return True
        time.sleep(0.1)
    return False


def guided_takeoff(conn: mavutil.mavfile, alt_m: float = 15.0,
                   timeout: float = TAKEOFF_TIMEOUT_S) -> bool:
    """Switch to GUIDED, arm, and take off to alt_m using MAV_CMD_NAV_TAKEOFF.

    Returns True if the vehicle reaches within 1 m of the target altitude.
    """
    # Switch to GUIDED
    if not set_mode_via_command(conn, "GUIDED"):
        return False
    time.sleep(0.5)
    # Arm
    if not arm_and_check(conn):
        return False
    time.sleep(0.3)
    # Takeoff command
    conn.mav.command_long_send(
        conn.target_system, conn.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0, 0, 0, 0, 0, 0, 0, alt_m)
    deadline = time.time() + timeout
    while time.time() < deadline:
        msg = conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg is not None:
            rel_alt = msg.relative_alt / 1000.0
            if rel_alt >= alt_m - 1.0:
                return True
        time.sleep(0.1)
    return False


def auto_takeoff(conn: mavutil.mavfile, timeout: float = TAKEOFF_TIMEOUT_S) -> bool:
    """Send AUTO mode and wait for the vehicle to leave the ground (>1.5 m).

    Use after uploading a mission with a TAKEOFF command as the first waypoint.
    """
    if not set_mode_via_command(conn, "AUTO"):
        return False
    deadline = time.time() + timeout
    while time.time() < deadline:
        msg = conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg is not None:
            rel_alt = msg.relative_alt / 1000.0
            if rel_alt >= 1.5:
                return True
        time.sleep(0.1)
    return False


def wait_position(conn: mavutil.mavfile, target_lat: int, target_lon: int,
                  pos_tolerance_m: float = 5.0,
                  timeout: float = POSITION_TIMEOUT_S) -> bool:
    """Wait for the vehicle's GLOBAL_POSITION_INT to be within pos_tolerance_m
    of (target_lat, target_lon), given as ints in 1e7 degrees.

    Returns True if the vehicle converges within tolerance before timeout.
    """
    # Convert target lat/lon ints to approximate meters (at mid-latitudes, 1e7 deg ~ 1.1 m)
    tol_e7 = int(pos_tolerance_m * 1.0e7 / 111_320.0)  # crude deg->m for lat
    deadline = time.time() + timeout
    while time.time() < deadline:
        msg = conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg is not None:
            dlat = abs(msg.lat - target_lat)
            dlon = abs(msg.lon - target_lon)
            if dlat <= tol_e7 and dlon <= tol_e7:
                return True
        time.sleep(0.1)
    return False


def send_position_target(conn: mavutil.mavfile, lat_e7: int, lon_e7: int,
                         alt_m: float, coord_frame: int = 6) -> None:
    """Send SET_POSITION_TARGET_GLOBAL_INT for a GUIDED loiter/descent target.

    coord_frame: 6 = MAV_FRAME_GLOBAL_RELATIVE_ALT_INT (position only).
    """
    type_mask = 0b0000111111111000  # position only (ignore vel/accel/yaw)
    ms = int(time.time() * 1000)
    conn.mav.set_position_target_global_int_send(
        ms, conn.target_system, conn.target_component, coord_frame,
        type_mask, lat_e7, lon_e7, alt_m,
        0, 0, 0, 0, 0, 0, 0, 0)


def force_failsafe(conn: mavutil.mavfile, mode_name: str) -> None:
    """Trigger a failsafe mode on the FC (simulate link-loss or low-batt).

    For SITL this sets the mode directly; in real flight the FC decides on
    its own via its internal monitors.
    """
    set_mode_via_command(conn, mode_name)


def read_mission_item(conn: mavutil.mavfile, seq: int,
                      timeout: float = 5.0) -> dict | None:
    """Request a MISSION_REQUEST_INT for the given sequence number.

    Returns the mission item dict, or None on timeout.
    """
    conn.mav.mission_request_int_send(conn.target_system, conn.target_component, seq)
    deadline = time.time() + timeout
    while time.time() < deadline:
        msg = conn.recv_match(type="MISSION_ITEM_INT", blocking=False)
        if msg is not None and msg.seq == seq:
            return msg.to_dict()
        time.sleep(0.05)
    return None


def upload_mission(conn: mavutil.mavfile, items: list[dict],
                   timeout: float = 10.0) -> bool:
    """Upload a list of mission items to SITL using the MISSION protocol.

    Each item dict should have keys: frame, command, current, autocontinue,
    param1-param4, x, y, z.

    Returns True if the mission was accepted.
    """
    n = len(items)
    conn.mav.mission_count_send(conn.target_system, conn.target_component, n)
    deadline = time.time() + timeout
    received_seq = -1
    while received_seq < n:
        msg = conn.recv_match(type="MISSION_REQUEST_INT", blocking=False)
        if msg is not None:
            if msg.seq == received_seq + 1:
                received_seq = msg.seq
                it = items[received_seq]
                conn.mav.mission_item_int_send(
                    conn.target_system, conn.target_component,
                    received_seq, it.get("frame", 3),  # MAV_FRAME_GLOBAL_RELATIVE_ALT
                    it.get("command", 16),              # MAV_CMD_NAV_WAYPOINT
                    it.get("current", 0),
                    it.get("autocontinue", 1),
                    it.get("param1", 0.0),
                    it.get("param2", 0.0),
                    it.get("param3", 0.0),
                    it.get("param4", 0.0),
                    int(it.get("x", 0)),
                    int(it.get("y", 0)),
                    float(it.get("z", 0.0)),
                )
                if received_seq >= n - 1:
                    break
        time.sleep(0.05)
    # Wait for MISSION_ACK
    deadline2 = time.time() + timeout
    while time.time() < deadline2:
        ack = conn.recv_match(type="MISSION_ACK", blocking=False)
        if ack is not None:
            return ack.type == 0  # MISSION_RESULT_ACCEPTED
        time.sleep(0.05)
    return False