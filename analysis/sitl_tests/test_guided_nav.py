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

    This exact capability (GUIDED descend-to-classify-altitude) is what
    UC-5/InvestigateAndClassify relies on in the real mission app, so it's
    worth recording how this was fixed, not just that it now passes.

    Was KNOWN FAILING as of task D2.13 (2026-08-10): the vehicle held its
    takeoff altitude and never moved toward a same-lat/lon lower-altitude
    target, even with settle delays, periodic resend, and continuous 4Hz
    streaming -- not a one-shot-message-dropped race. Root cause (confirmed
    by hands-on verification against this firmware, task D2.15,
    2026-08-11): helpers.send_position_target's type_mask had bit 9
    (POSITION_TARGET_TYPEMASK_FORCE_SET) unintentionally set -- a common
    copy-paste artifact from example offboard-control code, where that bit
    isn't actually one of the "ignore" bits. Clearing it (mask 3576 /
    0b0000110111111000, ArduPilot's own documented "position only" value,
    down from 4088 / 0b0000111111111000) produced a clean, monotonic
    descent from 20m to 10m. Same fix applied to the real mission app's
    _command_descent() in analysis/autonomy_sim/mission_app.py, which had
    the identical bug -- and should be checked against the live
    DroneMissionApp repo (analysis/autonomy_sim/ is a frozen prototype;
    see its README), since this would have silently broken the real
    descend-to-classify behavior on actual hardware too.

    Once fixed, this surfaced a separate timing wrinkle worth documenting:
    how long ArduPilot takes to actually start responding to the new
    target after a takeoff varies a lot run-to-run -- observed anywhere
    from ~9s to ~25s before altitude even starts moving, then another
    ~20-25s of steady descent once it does. A 20s total budget (the
    original value) was too tight and failed intermittently even with a
    correct fix; 60s gives comfortable margin for the slow end of that
    range without masking a real non-convergence (a genuinely broken
    target would never move at all, regardless of how long you wait).
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
    # message rides out that race -- kept even though it wasn't the root
    # cause of the original failure, since it's cheap and still good
    # practice against a live FC.
    deadline = time.time() + 60.0
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

    assert reached, f"Vehicle did not descend to {target_alt}m within 60s"


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