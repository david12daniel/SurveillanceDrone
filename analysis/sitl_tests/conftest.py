"""pytest configuration for SITL integration tests.

Provides the `sitl_conn` fixture that manages an ArduPilot SITL process
lifecycle and returns a connected pymavlink mavfile.

Usage:
    pytest --sitl-binary=/path/to/arducopter   # specify SITL binary
    pytest                                      # auto-discover in PATH

Skip tests if no SITL binary is found.
"""
from __future__ import annotations
import os
import subprocess
import time
import shutil

import pytest
from pymavlink import mavutil


def pytest_addoption(parser):
    parser.addoption("--sitl-binary", default=None,
                     help="Path to the ArduPilot SITL binary (arducopter)")
    parser.addoption("--sitl-connection", default="tcp:127.0.0.1:5780",
                     help="Connection string for the SITL instance (SERIAL0 TCP port)")
    parser.addoption("--sitl-home", default="42.3000,-83.7000,180,0",
                     help="Home location (lat,lon,alt,hdg)")


@pytest.fixture(scope="session")
def sitl_binary(request):
    """Return the path to the ArduPilot SITL binary, or skip."""
    given = request.config.getoption("--sitl-binary")
    if given:
        if not os.path.isfile(given):
            pytest.skip(f"SITL binary not found: {given}")
        return given
    # Search local bin first, then PATH for common names
    local_bin = os.path.join(os.path.dirname(__file__), "bin", "arducopter")
    if os.path.isfile(local_bin):
        return local_bin
    for name in ("arducopter", "sim_vehicle.py"):
        found = shutil.which(name)
        if found:
            return found
    pytest.skip("No SITL binary found (install ardupilot-sitl or set --sitl-binary)")


@pytest.fixture(scope="session")
def sitl_connection_string(request):
    return request.config.getoption("--sitl-connection")


@pytest.fixture(scope="session")
def sitl_home(request):
    return request.config.getoption("--sitl-home")


@pytest.fixture(scope="session")
def sitl_process(sitl_binary, sitl_connection_string, sitl_home):
    """Start a SITL process for the test session and yield its listen address.

    The process is terminated after all tests complete.
    Connect via SERIAL0 TCP (default port 5760 + instance*10).
    """
    cmd = [
        sitl_binary,
        "--home", sitl_home,
        "--model", "+",  # default quadcopter model
        "--speedup", "3",  # 3× real-time to make tests faster
        "--instance", "2",  # unique instance to avoid port conflicts with other users
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Give SITL a moment to boot
    time.sleep(5)

    yield proc, sitl_connection_string

    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


@pytest.fixture(scope="function")
def sitl_conn(sitl_process):
    """Create a fresh MAVLink connection to SITL for each test function.

    Connects to the running SITL instance, waits for the first HEARTBEAT,
    then yields the connection. Automatically closes the link after the test.
    """
    _, conn_str = sitl_process
    conn = mavutil.mavlink_connection(conn_str, dialect="ardupilotmega",
                                      source_system=255, source_component=191)
    # Wait up to 15 s for first heartbeat
    deadline = time.time() + 15
    connected = False
    while time.time() < deadline:
        if conn.wait_heartbeat(blocking=False) is not None:
            connected = True
            break
        time.sleep(0.5)

    if not connected:
        conn.close()
        pytest.fail("SITL did not send a HEARTBEAT within 15 s")

    # Flush pre-boot messages
    time.sleep(0.5)
    _drain(conn)

    yield conn

    conn.close()


def _drain(conn):
    """Drain all pending messages (non-blocking)."""
    while conn.recv_match(blocking=False) is not None:
        pass