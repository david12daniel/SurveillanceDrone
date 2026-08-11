"""Tests for mode-ACK correctness.

Validates that SET_MODE requests elicit COMMAND_ACK responses from SITL,
and that the app can detect failures (invalid mode, non-existent mode).
"""
import time
import pytest
from pymavlink import mavutil
from helpers import set_mode_via_command, wait_mode, MODE, MODE_TIMEOUT_S


def test_set_mode_auto_ack(sitl_conn):
    """SET_MODE to AUTO should return an ACCEPTED COMMAND_ACK."""
    ok = set_mode_via_command(sitl_conn, "AUTO")
    assert ok, "AUTO mode command was not accepted"
    assert wait_mode(sitl_conn, MODE["AUTO"]), "HEARTBEAT did not report AUTO"


def test_set_mode_guided_ack(sitl_conn):
    """SET_MODE to GUIDED should return an ACCEPTED COMMAND_ACK."""
    ok = set_mode_via_command(sitl_conn, "GUIDED")
    assert ok, "GUIDED mode command was not accepted"
    assert wait_mode(sitl_conn, MODE["GUIDED"]), "HEARTBEAT did not report GUIDED"


def test_set_mode_rtl_ack(sitl_conn):
    """SET_MODE to RTL should return an ACCEPTED COMMAND_ACK."""
    ok = set_mode_via_command(sitl_conn, "RTL")
    assert ok, "RTL mode command was not accepted"
    assert wait_mode(sitl_conn, MODE["RTL"]), "HEARTBEAT did not report RTL"


def test_set_mode_land_ack(sitl_conn):
    """SET_MODE to LAND should return an ACCEPTED COMMAND_ACK."""
    ok = set_mode_via_command(sitl_conn, "LAND")
    assert ok, "LAND mode command was not accepted"
    assert wait_mode(sitl_conn, MODE["LAND"]), "HEARTBEAT did not report LAND"


def test_set_mode_stabilize_ack(sitl_conn):
    """SET_MODE to STABILIZE should return an ACCEPTED COMMAND_ACK."""
    ok = set_mode_via_command(sitl_conn, "STABILIZE")
    assert ok, "STABILIZE mode command was not accepted"
    assert wait_mode(sitl_conn, MODE["STABILIZE"]), "HEARTBEAT did not report STABILIZE"


def test_set_mode_invalid_rejected(sitl_conn):
    """An invalid/unsupported mode number should be rejected by SITL."""
    invalid_mode = 99
    sitl_conn.mav.set_mode_send(
        sitl_conn.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        invalid_mode,
    )
    # Expect a COMMAND_ACK with result != ACCEPTED
    acks = []
    deadline = time.time() + MODE_TIMEOUT_S
    while time.time() < deadline:
        ack = sitl_conn.recv_match(type="COMMAND_ACK", blocking=False)
        if ack is not None and ack.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
            acks.append(ack)
            break
        time.sleep(0.05)
    assert len(acks) > 0, "No COMMAND_ACK received for invalid mode"
    assert acks[0].result != mavutil.mavlink.MAV_RESULT_ACCEPTED, \
        f"Invalid mode {invalid_mode} should not be accepted (result={acks[0].result})"