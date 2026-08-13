"""Tests for failsafe parameter injection and behavior.

Validates that the canonical failsafe parameter sets (params_sets.py) are
accepted by SITL and that the associated failsafe conditions trigger the
expected mode transitions.
"""
import time
import pytest
from pymavlink import mavutil
from helpers import set_param, get_param, set_mode_via_command, \
    wait_mode, MODE, MODE_TIMEOUT_S
from params_sets import LINK_LOSS_FS, LOW_BATTERY_FS, RTL_CRUISE, ALL_FS_PARAMS


@pytest.fixture(scope="module", autouse=True)
def _restore_arming_safe_defaults(sitl_process):
    """This module's tests set several params to values that are only valid
    for "can it be set and read back" testing, not for actually arming --
    and never reset them. sitl_process is session-scoped and shared across
    every test file, so those values leak into every LATER test file's arm
    attempts when the full suite runs together (confirmed:
    test_full_mission.py failing to arm, task #141, 2026-08-13). Two
    distinct issues found, both fixed here:

    1. LOW_BATTERY_FS's 6S-pack voltage thresholds (BATT_LOW_VOLT=20.4,
       BATT_CRT_VOLT=19.2) are both ABOVE the fixed 12.6V SIM_BATT_VOLTAGE
       this SITL binary simulates (libraries/SITL/SITL.cpp's
       SIM.batt_voltage default), so every later PreArm battery check sees
       the battery as critically low.
    2. LINK_LOSS_FS's FS_THR_VALUE=900 is actually an INVALID value per
       ArduCopter's own arming-parameter sanity check
       (AP_Arming_Copter.cpp's parameter_checks(): FS_THR_VALUE must be
       >= 910, "above ppm encoder's loss-of-signal value of 900" per its own
       comment) -- once set, PreArm reports "Check FS_THR_VALUE" and blocks
       arming outright, regardless of RC input. This is not a leaked-state
       side effect like the battery case; 900 is simply never a legal value
       to arm with.

    Restore ArduCopter's own firmware defaults (LOW_VOLT=10.5,
    CRT_VOLT=0/disabled, FS_THR_VALUE=975 -- see ArduCopter/config.h's
    FS_THR_VALUE_DEFAULT) once this module's tests are done with them,
    regardless of which test in this file ran last.

    Uses its own short-lived connection rather than depending on the
    function-scoped sitl_conn fixture: a module-scoped fixture can't depend
    on a narrower-scoped one, and this only needs to fire once, after every
    test in this module has finished.
    """
    yield
    _, conn_str = sitl_process
    conn = mavutil.mavlink_connection(conn_str, dialect="ardupilotmega",
                                      source_system=255, source_component=191)
    conn.wait_heartbeat(timeout=15)
    set_param(conn, "BATT_LOW_VOLT", 10.5, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
    set_param(conn, "BATT_CRT_VOLT", 0.0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
    set_param(conn, "FS_THR_VALUE", 975, mavutil.mavlink.MAV_PARAM_TYPE_INT16)
    conn.close()


@pytest.mark.parametrize("name,val_typ", list(ALL_FS_PARAMS.items()))
def test_all_fs_params_accept(sitl_conn, name, val_typ):
    """Every failsafe parameter in the canonical sets should be writable."""
    value, ptype = val_typ
    ok = set_param(sitl_conn, name, value, ptype)
    assert ok, f"Failed to set {name} = {value}"


def test_link_loss_fs_rtl(sitl_conn):
    """Set link-loss failsafe params and verify they persist."""
    for name, (value, ptype) in LINK_LOSS_FS.items():
        set_param(sitl_conn, name, value, ptype)
    time.sleep(0.5)

    for name, (value, _) in LINK_LOSS_FS.items():
        got = get_param(sitl_conn, name)
        assert got is not None, f"Could not read back {name}"
        assert abs(got - value) < 0.1, f"{name}: expected {value}, got {got}"


def test_low_battery_fs_rtl(sitl_conn):
    """Set low-battery failsafe params and verify they persist."""
    for name, (value, ptype) in LOW_BATTERY_FS.items():
        set_param(sitl_conn, name, value, ptype)
    time.sleep(0.5)

    for name, (value, _) in LOW_BATTERY_FS.items():
        got = get_param(sitl_conn, name)
        assert got is not None, f"Could not read back {name}"
        # For battery params, allow small floating point differences
        # INT32 values (MAH) should match exactly
        assert abs(got - value) < 0.1 or int(got) == int(value), \
            f"{name}: expected {value}, got {got}"


def test_rtl_speed_param(sitl_conn):
    """RTL_SPEED_MS=12 should be accepted and readable.

    Renamed from RTL_SPEED on modern ArduCopter (task D2.13, 2026-08-10).
    """
    name = "RTL_SPEED_MS"
    value = 12.0
    set_param(sitl_conn, name, value, 9)  # MAV_PARAM_TYPE_REAL32
    got = get_param(sitl_conn, name)
    assert got is not None, "Could not read RTL_SPEED_MS"
    assert abs(got - 12.0) < 0.1, f"RTL_SPEED_MS: expected 12.0, got {got}"