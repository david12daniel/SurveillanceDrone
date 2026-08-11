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
import threading
import time
import shutil

import pytest
from pymavlink import mavutil

# Mid-stick roll/pitch/yaw, throttle held at idle (matches RC3_MIN so the
# arm-time "throttle too high" check passes). GUIDED/AUTO ignore RC stick
# input for navigation once armed and flying -- this feed's only job is to
# stand in for a live ELRS receiver so ArduPilot doesn't see an RC failsafe.
_RC_OVERRIDE_IDLE = (1500, 1500, 1100, 1500, 0, 0, 0, 0)


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
        "--wipe",  # force a fresh EEPROM every run -- SITL persists params
                   # (including the fixups below) to eeprom.bin in the cwd
                   # and reuses it across runs by default. Without this,
                   # state accumulated by earlier/other SITL sessions on the
                   # same --instance can silently make arming flaky in ways
                   # that have nothing to do with this suite's own code
                   # (confirmed the hard way, task D2.13, 2026-08-10).
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Give SITL a moment to boot
    time.sleep(5)

    _apply_fresh_eeprom_fixups(sitl_connection_string)

    yield proc, sitl_connection_string

    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


def _apply_fresh_eeprom_fixups(conn_str):
    """Work around two fresh-EEPROM SITL quirks that only appear when the
    raw arducopter/apm binary is launched directly (sim_vehicle.py normally
    papers over both via a bundled default-params file we don't have here):

    1. The frame class defaults to undefined -> permanent "PreArm: Motors:
       Check frame class and type", regardless of --model.
    2. A never-calibrated virtual IMU permanently reports "PreArm: 3D Accel
       calibration needed" (offsets/scale already sit at the identity
       values a real cal would produce, so there's nothing to calibrate;
       running the interactive MAVLink accelcal handshake against SITL is
       unreliable). Skipping just the INS check leaves EKF/GPS/battery/etc
       checks -- the ones these tests actually care about -- active.

    This suite runs against two very different firmware builds (see the
    README/CLAUDE.md): modern ArduCopter (4.7.0) uses FRAME_CLASS/
    FRAME_TYPE and a bitmask ARMING_SKIPCHK; the legacy Copter 3.3 binary
    predates both and instead has a single FRAME param and the older
    ARMING_CHECK bitmask (where a bare "1" means "ALL", not just bit 0 --
    to skip one specific check you replace it with the OR of every other
    bit instead). Setting all four here is harmless: PARAM_SET on a name a
    given firmware doesn't have is silently ignored by ArduPilot, so each
    build only picks up the pair it understands.

    Uses its own short-lived connection, opened and closed here: SITL's
    SERIAL0 TCP port only accepts one client at a time, and this must not
    hold the slot the sitl_conn fixture needs afterward for each test.

    Confirmed via task D2.14/D2.13 probing (2026-08-10): none of this is
    needed for the mode-number/mode-ACK behavior itself, only for arming.
    """
    conn = mavutil.mavlink_connection(conn_str, dialect="ardupilotmega",
                                      source_system=255, source_component=191)
    conn.wait_heartbeat(timeout=15)

    def _set(name, value):
        conn.mav.param_set_send(conn.target_system, conn.target_component,
                                name.encode(), value, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
        time.sleep(0.2)

    _set("FRAME_CLASS", 1.0)                # modern: 1 = QUAD
    _set("FRAME", 1.0)                       # legacy: 1 = "+" quad
    _set("ARMING_SKIPCHK", 16.0)             # modern: bit 4 = INS only
    _set("ARMING_CHECK", 131054.0)           # legacy: ALL bits except INS (bit 4 / value 16)
    time.sleep(0.3)
    conn.close()


@pytest.fixture(scope="function")
def sitl_conn(sitl_process):
    """Create a fresh MAVLink connection to SITL for each test function.

    Connects to the running SITL instance, waits for the first HEARTBEAT,
    then yields the connection. Automatically closes the link after the test.

    Also runs a background RC_CHANNELS_OVERRIDE feed for the life of the
    connection: with no RC hardware or joystick attached, ArduPilot never
    sees any RC_CHANNELS input at all, which reads as a permanent throttle
    failsafe ("PreArm: Check FS_THR_VALUE" / "Arm: Throttle too high") --
    not a real gate on the actual vehicle, which always has a live ELRS
    receiver per the project's RC architecture (see CLAUDE.md). This feed
    stands in for that receiver, the same mechanism a companion computer
    without a physical RC would use. It shares this connection rather than
    opening a second one because SITL's SERIAL0 TCP port only accepts one
    client at a time.

    Skips outright if the SITL process has already died: it's session-
    scoped and shared across every test file, and at least one known
    scenario (AUTO-mode takeoff, see test_full_mission.py) has been
    observed to crash the arducopter binary outright (task D2.13,
    2026-08-10). Without this check, every remaining test in the session
    independently burns its own 15 s connection timeout only to fail with
    a generic "no HEARTBEAT" -- confusing on its own and easy to mistake
    for N unrelated new bugs instead of one already-diagnosed crash.
    """
    proc, conn_str = sitl_process
    if proc.poll() is not None:
        pytest.skip(f"SITL process has already exited (code {proc.poll()}); "
                    "see test_full_mission.py for a known AUTO-takeoff crash")
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

    # pymavlink's target_system auto-populates from the first HEARTBEAT
    # (via self.sysid), but target_component does NOT -- it stays 0
    # (broadcast) unless set explicitly. COMMAND_LONG-based commands
    # (SET_MODE, ARM_DISARM, PARAM_SET) tolerate a broadcast target, but
    # ArduPilot's RC_CHANNELS_OVERRIDE handler silently drops anything not
    # addressed to its exact component ID -- which permanently strands the
    # RC feed below and makes throttle-failsafe prearm checks unclearable.
    # A real GCS always addresses the autopilot component explicitly.
    conn.target_component = mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1

    # Flush pre-boot messages
    time.sleep(0.5)
    _drain(conn)

    # Without this, SITL sends almost nothing beyond HEARTBEAT/TIMESYNC --
    # no EKF_STATUS_REPORT, no GLOBAL_POSITION_INT, no RC_CHANNELS. A real
    # GCS/companion computer always requests its telemetry streams on
    # connect; every helper that polls those message types (wait_position,
    # guided_takeoff, the EKF-convergence check) silently stalls without it.
    conn.mav.request_data_stream_send(conn.target_system, conn.target_component,
                                      mavutil.mavlink.MAV_DATA_STREAM_ALL, 10, 1)

    stop_event = threading.Event()

    def _feed():
        while not stop_event.is_set():
            try:
                conn.mav.rc_channels_override_send(
                    conn.target_system, conn.target_component, *_RC_OVERRIDE_IDLE)
            except OSError:
                break
            stop_event.wait(0.2)

    feed_thread = threading.Thread(target=_feed, daemon=True, name="sitl-rc-feed")
    feed_thread.start()

    yield conn

    # The vehicle itself (armed state, mode, altitude) is server-side and
    # outlives this connection -- sitl_process is session-scoped, so the
    # SAME running vehicle carries into the next test. A test that leaves
    # it armed and mid-air (e.g. a flight test that doesn't land/disarm on
    # its own) would otherwise hand the next test a corrupted starting
    # state. Force-disarm unconditionally: param2=21196 is ArduPilot's
    # documented magic value for disarming even while flying (the same
    # mechanism a GCS "kill switch" uses), so this is safe to send
    # regardless of whether the vehicle is actually armed or airborne.
    conn.mav.command_long_send(
        conn.target_system, conn.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, 0, 21196, 0, 0, 0, 0, 0)
    time.sleep(0.3)

    stop_event.set()
    feed_thread.join(timeout=2)
    conn.close()


def _drain(conn):
    """Drain all pending messages (non-blocking)."""
    while conn.recv_match(blocking=False) is not None:
        pass