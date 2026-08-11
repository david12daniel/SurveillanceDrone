"""Tests for GUIDED navigation tracking.

Validates that SITL actually flies to position targets issued via
SET_POSITION_TARGET_GLOBAL_INT, and that the mission app can track
convergence via GLOBAL_POSITION_INT.
"""
import time
import pytest
from helpers import (
    set_mode_via_command, arm_and_check, guided_takeoff,
    send_position_target, wait_position, wait_mode, MODE,
)


def test_guided_altitude_change(sitl_conn):
    """Send a GUIDED altitude target and verify SITL descends to it."""
    lat = 42_3000000  # 42.3° in 1e7 (SITL home latitude)
    lon = -83_7000000  # -83.7° in 1e7
    start_alt = 20.0
    target_alt = 10.0

    # Get airborne in GUIDED
    ok = guided_takeoff(sitl_conn, alt_m=start_alt)
    assert ok, "Guided takeoff failed"

    # Command descent
    send_position_target(sitl_conn, lat, lon, target_alt)
    time.sleep(5.0)  # Let SITL respond

    # Check current altitude
    deadline = time.time() + 20.0
    reached = False
    while time.time() < deadline:
        msg = sitl_conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg is not None:
            alt = msg.relative_alt / 1000.0
            if alt <= target_alt + 1.0:
                reached = True
                break
        time.sleep(0.2)

    assert reached, f"Vehicle did not descend to {target_alt}m within 20s"


def test_guided_position_target_converges(sitl_conn):
    """SITL should navigate to a nearby position target in GUIDED mode."""
    offset_lat = 42_3000500  # ~50 m north of home
    offset_lon = -83_6999500  # ~50 m east of home
    alt = 15.0

    ok = guided_takeoff(sitl_conn, alt_m=alt)
    assert ok, "Guided takeoff failed"

    # Command a position offset
    send_position_target(sitl_conn, offset_lat, offset_lon, alt)

    ok = wait_position(sitl_conn, offset_lat, offset_lon, pos_tolerance_m=10.0)
    assert ok, "Vehicle did not converge to the GUIDED position target"


def test_guided_position_is_safe(sitl_conn):
    """Vehicle should remain at a safe altitude during GUIDED position hold.

    Mission requirement: the drone should never descend below a safe floor
    during an investigation (R3_2 classify altitude is 90 m — safe).
    """
    offset_lat = 42_3000500
    offset_lon = -83_6999500
    alt = 30.0

    ok = guided_takeoff(sitl_conn, alt_m=alt)
    assert ok, "Guided takeoff failed"

    # Hold position for a few seconds and confirm altitude is maintained
    send_position_target(sitl_conn, offset_lat, offset_lon, alt)
    time.sleep(4.0)

    min_alt = 999.0
    deadline = time.time() + 5.0
    while time.time() < deadline:
        msg = sitl_conn.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
        if msg is not None:
            alt_now = msg.relative_alt / 1000.0
            min_alt = min(min_alt, alt_now)
        time.sleep(0.2)

    # Vehicle should never descend more than 3 m below the commanded altitude
    assert min_alt >= alt - 3.0, f"Vehicle dropped to {min_alt:.1f}m (commanded {alt}m)"