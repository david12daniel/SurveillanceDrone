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
    """Send a GUIDED altitude target and verify SITL descends to it.

    KNOWN FAILING against the modern ArduCopter (4.7.0) SITL build as of
    task D2.13 (2026-08-10) -- flagged here for follow-up, not silenced,
    because this exact capability (GUIDED descend-to-classify-altitude) is
    what UC-5/InvestigateAndClassify relies on in the real mission app.

    Confirmed by direct probing (not just this test's own timing): the
    vehicle holds its original takeoff altitude and never moves toward the
    new Z target, even with a settle delay after takeoff, periodic resend,
    and continuous 4Hz streaming of SET_POSITION_TARGET_GLOBAL_INT -- so
    it isn't a one-shot-message-got-dropped race. The X/Y component of the
    SAME message type works fine (test_guided_position_target_converges/
    test_guided_position_is_safe below both pass, including under load
    that moves the vehicle 50 m laterally). Root cause not isolated yet;
    candidates worth checking next: the type_mask's bit 9 (FORCE_SET) is
    unintentionally set by helpers.send_position_target's literal mask
    (0b0000111111111000) -- probably harmless for Copter but not verified;
    this firmware's position controller was rewritten around the PSC_D_*/
    PSC_NE_* parameter families (WPNAV_SPEED_DN and friends no longer
    exist at all, confirmed via a full PARAM_REQUEST_LIST dump), so a
    Z-axis-specific gating in that rewrite is a stronger candidate than
    anything on the test-harness side.
    """
    lat = 42_3000000  # 42.3° in 1e7 (SITL home latitude)
    lon = -83_7000000  # -83.7° in 1e7
    start_alt = 20.0
    target_alt = 10.0

    # Get airborne in GUIDED
    ok = guided_takeoff(sitl_conn, alt_m=start_alt)
    assert ok, "Guided takeoff failed"

    # guided_takeoff returns as soon as altitude is within 1 m of the takeoff
    # target, which can still be a second or two before the climb itself has
    # actually finished resolving. Resending periodically (like
    # arm_and_check's retry loop) rather than a single fire-and-forget
    # message rides out that specific race -- confirmed NOT sufficient by
    # itself to fix this test; see the docstring above.
    deadline = time.time() + 20.0
    next_send = 0.0
    reached = False
    while time.time() < deadline:
        if time.time() >= next_send:
            send_position_target(sitl_conn, lat, lon, target_alt)
            next_send = time.time() + 2.0
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