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
import signal
import subprocess
import sys
import threading
import time
import shutil

import pytest
from pymavlink import mavutil

from helpers import get_param


def pytest_addoption(parser):
    parser.addoption("--sitl-binary", default=None,
                     help="Path to the ArduPilot SITL binary (arducopter)")
    parser.addoption("--sitl-connection", default="tcp:127.0.0.1:5780",
                     help="Connection string for the SITL instance (SERIAL0 TCP port)")
    parser.addoption("--sitl-home", default="42.3000,-83.7000,180,0",
                     help="Home location (lat,lon,alt,hdg)")
    parser.addoption("--ardupilot-root", default=os.path.expanduser("~/ardupilot-sitl-src"),
                     help="Path to an ArduPilot checkout providing Tools/autotest/"
                          "sim_vehicle.py, used to launch SITL instead of the raw "
                          "binary (see sim_vehicle_script's docstring for why)")


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
def sim_vehicle_script(request):
    """Return the path to ArduPilot's sim_vehicle.py orchestrator, or skip.

    Launching the prebuilt arducopter binary directly (the previous approach
    here) crashes the SITL process non-deterministically during AUTO-mode
    takeoff (task D2.13/#70, task D2.16/#141) -- direct process monitoring
    confirmed the binary itself dies, not a test-harness or mission_app.py
    bug. Launching the SAME binary through sim_vehicle.py instead (via
    --vehicle-binary + --no-rebuild, which skips waf/compilation entirely)
    eliminated the crash in repeated attempts during investigation. The
    likely mechanism: sim_vehicle.py auto-loads
    Tools/autotest/default_params/copter.parm, which a raw-binary launch
    never had. See #141's notes for the full writeup.

    This fixture expects an ArduPilot checkout (not a full build -- we only
    need sim_vehicle.py and its waf/mavlink submodules to launch the
    existing prebuilt binary):
      git clone https://github.com/ArduPilot/ardupilot.git ~/ardupilot-sitl-src
      cd ~/ardupilot-sitl-src && git checkout 1511f271   # tag Copter-4.7.0,
                                                          # matches the binary
                                                          # ("strings arducopter
                                                          # | grep 'ArduCopter V'")
      git submodule update --init modules/waf modules/mavlink
    """
    root = os.path.expanduser(request.config.getoption("--ardupilot-root"))
    script = os.path.join(root, "Tools", "autotest", "sim_vehicle.py")
    if not os.path.isfile(script):
        pytest.skip(f"sim_vehicle.py not found at {script} -- see this "
                    "fixture's docstring, or pass --ardupilot-root")
    return script


@pytest.fixture(scope="session")
def sitl_process(sitl_binary, sim_vehicle_script, sitl_connection_string, sitl_home):
    """Start a SITL process for the test session and yield its listen address.

    Launched through sim_vehicle.py rather than the raw binary -- see
    sim_vehicle_script's docstring for why. sim_vehicle.py in turn launches
    the actual vehicle binary via a detached background subshell (its
    headless fallback when no terminal/tmux/screen is attached, see
    run_in_terminal_window.sh), not as a direct child process -- confirmed
    by process-tree inspection (task #141, 2026-08-13). Terminating just
    this Popen's own PID would therefore leave the vehicle binary running as
    an orphan holding the TCP port; start_new_session=True puts the whole
    tree in one new process group at launch so the os.killpg below actually
    reaches it.

    The process is terminated after all tests complete.
    Connect via SERIAL0 TCP (default port 5760 + instance*10).
    """
    cmd = [
        sys.executable, sim_vehicle_script,
        "-v", "ArduCopter",
        "-f", "+",  # default quadcopter model
        "--vehicle-binary", sitl_binary,
        "-N",  # --no-rebuild: launch --vehicle-binary as-is, skip waf/compilation
        "-l", sitl_home,
        "-S", "3",  # 3x real-time to make tests faster
        "-I", "2",  # unique instance to avoid port conflicts with other users
        "-w",  # force a fresh EEPROM every run -- SITL persists params to
               # eeprom.bin in the cwd and reuses it across runs by default.
               # Without this, state accumulated by earlier/other SITL
               # sessions on the same --instance can silently make arming
               # flaky in ways that have nothing to do with this suite's own
               # code (confirmed the hard way, task D2.13, 2026-08-10).
        "--no-mavproxy",
        "--no-extra-ports",
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    # Give SITL a moment to boot
    time.sleep(5)

    yield proc, sitl_connection_string

    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass


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

    # Mid-stick roll/pitch/yaw, throttle held at idle. GUIDED/AUTO ignore RC
    # stick input for navigation once armed and flying -- this feed's only
    # job is to stand in for a live ELRS receiver so ArduPilot doesn't see an
    # RC failsafe. The idle throttle value MUST match RC3_MIN or the
    # "throttle not neutral" arm gate trips in GUIDED/AUTO -- read it live
    # rather than hardcoding: RC3_MIN is 1000 under sim_vehicle.py's bundled
    # copter.parm defaults but was 1100 under the old raw-binary launch path
    # (board-compiled default), and silently differs again on any future
    # launch-path change. Confirmed via task #141, 2026-08-13.
    rc3_min = get_param(conn, "RC3_MIN", timeout=5.0)
    if rc3_min is None:
        rc3_min = 1100  # match the old hardcoded assumption if the read itself fails
    idle_override = (1500, 1500, int(rc3_min), 1500, 0, 0, 0, 0)

    stop_event = threading.Event()

    def _feed():
        while not stop_event.is_set():
            try:
                conn.mav.rc_channels_override_send(
                    conn.target_system, conn.target_component, *idle_override)
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