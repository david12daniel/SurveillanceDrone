"""Real-SITL validation for D2.12's SafeStandDown thread (analysis/service_hardening/).

Drives the actual `SafeStandDown._safe_land()` method -- not a
reimplementation -- against real ArduCopter SITL to confirm the GUIDED-then-
LAND `set_mode_send` sequence (chosen during D2.12 review over an untested
`MAV_CMD_NAV_LAND` COMMAND_LONG path) is genuinely accepted by the firmware,
the same standard this project holds every other MAVLink control path to
(see test_battery_rtl_sitl.py, D2.13/D2.15/D2.17).

Fast unit coverage of the thread's timeout/kick/disarm lifecycle (against a
fake connection) lives in analysis/service_hardening/test_service_hardening.py;
this file only covers what a fake connection can't: whether the real firmware
actually accepts the commands.
"""
from __future__ import annotations

import logging
import os
import sys
import time

import pytest
from pymavlink import mavutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "service_hardening"))
from run_service import SafeStandDown  # noqa: E402

from helpers import wait_mode, MODE  # noqa: E402


def test_safe_stand_down_lands_on_real_sitl(sitl_process):
    """SafeStandDown opens its own separate connection (by design -- see its
    docstring: "don't touch the possibly-corrupt main loop's connection").
    Exercise that exact path here rather than the shared sitl_conn fixture."""
    proc, conn_str = sitl_process
    if proc.poll() is not None:
        pytest.skip("SITL process has already exited")

    stand = SafeStandDown(
        connection_string=conn_str,
        baudrate=9600,  # irrelevant for a tcp: connection string; matches prod default
        heartbeat_timeout_s=0.2,
    )
    log = logging.getLogger("test-safe-stand-down")

    stand._safe_land(log)  # synchronous; opens+closes its own connection, then returns

    # Verify via a second, independent connection -- _safe_land already
    # closed its own -- that the FC actually ended up in LAND.
    verify_conn = mavutil.mavlink_connection(
        conn_str, dialect="ardupilotmega", source_system=255, source_component=191)
    try:
        assert verify_conn.wait_heartbeat(timeout=10) is not None, \
            "no heartbeat from SITL on the verification connection"
        assert wait_mode(verify_conn, MODE["LAND"], timeout=5.0), \
            "FC did not confirm LAND mode after SafeStandDown's GUIDED->LAND sequence"
    finally:
        verify_conn.close()
