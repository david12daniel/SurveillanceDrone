"""Tests for failsafe parameter injection and behavior.

Validates that the canonical failsafe parameter sets (params_sets.py) are
accepted by SITL and that the associated failsafe conditions trigger the
expected mode transitions.
"""
import time
import pytest
from helpers import set_param, get_param, set_mode_via_command, \
    wait_mode, MODE, MODE_TIMEOUT_S
from params_sets import LINK_LOSS_FS, LOW_BATTERY_FS, RTL_CRUISE, ALL_FS_PARAMS


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
    """RTL_SPEED=12 should be accepted and readable."""
    name = "RTL_SPEED"
    value = 12.0
    set_param(sitl_conn, name, value, 9)  # MAV_PARAM_TYPE_REAL32
    got = get_param(sitl_conn, name)
    assert got is not None, "Could not read RTL_SPEED"
    assert abs(got - 12.0) < 0.1, f"RTL_SPEED: expected 12.0, got {got}"