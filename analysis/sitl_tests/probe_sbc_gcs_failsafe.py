"""Scratch investigation probe (not part of the pytest suite) for TASKS.md 3.3 /
MODEL_ISSUES.md item 34: does ArduCopter's FS_GCS_ENABLE failsafe correctly key
off one specific MAVLink source_system (SYSID_MYGCS), independent of other
live connections -- and does mission_app.py's CURRENT connection config
(source_system == target_system, i.e. it claims the FC's own sysid) actually
get recognized by that mechanism at all?

Grounded in direct ArduPilot source reading first (ArduCopter/events.cpp
failsafe_gcs_check(), libraries/GCS_MAVLink/GCS_Common.cpp handle_heartbeat(),
libraries/GCS_MAVLink/GCS.cpp sysid_is_gcs()) -- this script empirically
confirms that reading against real SITL, mirroring the D2.16 investigation's
own "standalone probe script" methodology.

Run: python3 probe_sbc_gcs_failsafe.py [--ardupilot-root PATH] [--sitl-binary PATH]
"""
from __future__ import annotations
import argparse
import os
import signal
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from pymavlink import mavutil  # noqa: E402
from helpers import set_param, get_param  # noqa: E402

HOME = "42.3000,-83.7000,180,0"
INSTANCE = 7  # distinct from the main suite's -I 2, avoid port collisions
SERIAL0 = f"tcp:127.0.0.1:{5760 + 10 * INSTANCE}"


def launch_sitl(ardupilot_root: str, sitl_binary: str) -> subprocess.Popen:
    script = os.path.join(ardupilot_root, "Tools", "autotest", "sim_vehicle.py")
    cmd = [
        sys.executable, script,
        "-v", "ArduCopter", "-f", "+",
        "--vehicle-binary", sitl_binary,
        "-N", "-l", HOME, "-S", "3", "-I", str(INSTANCE), "-w",
        "--no-mavproxy", "--no-extra-ports",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
    time.sleep(6)
    return proc


def connect(sysid: int, comp: int = 191):
    conn = mavutil.mavlink_connection(SERIAL0, dialect="ardupilotmega",
                                       source_system=sysid, source_component=comp)
    deadline = time.time() + 15
    ok = False
    while time.time() < deadline:
        if conn.wait_heartbeat(blocking=False) is not None:
            ok = True
            break
        time.sleep(0.5)
    if not ok:
        raise RuntimeError("no HEARTBEAT from SITL within 15s")
    conn.target_component = mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1
    while conn.recv_match(blocking=False) is not None:
        pass  # drain pre-connect backlog
    return conn


def drain_statustext(conn, seconds: float) -> list[str]:
    texts = []
    deadline = time.time() + seconds
    while time.time() < deadline:
        msg = conn.recv_match(type="STATUSTEXT", blocking=True, timeout=0.5)
        if msg is not None:
            texts.append(msg.text)
    return texts


def phase(title: str) -> None:
    print(f"\n=== {title} ===", flush=True)


def run_phase(title: str, sysid: int, beat_type: int, n_beats: int = 4) -> list[str]:
    phase(title)
    conn = connect(sysid=sysid)
    print(f"Connected as sysid={sysid}; sending {n_beats} heartbeats 1s apart...")
    for _ in range(n_beats):
        conn.mav.heartbeat_send(beat_type, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
        time.sleep(1)
    print("Stopped sending heartbeats from this connection; watching for 8s...")
    texts = drain_statustext(conn, 8)
    print("STATUSTEXT seen:", texts)
    fired = any("Failsafe" in t and "GCS" in t for t in texts)
    print("RESULT:", "GCS FAILSAFE FIRED" if fired else "no GCS failsafe text observed")
    conn.close()
    return texts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ardupilot-root", default=os.path.expanduser("~/ardupilot-sitl-src"))
    ap.add_argument("--sitl-binary", default=os.path.expanduser("~/.openclaw/bin/arducopter"))
    args = ap.parse_args()

    proc = launch_sitl(args.ardupilot_root, args.sitl_binary)
    try:
        # One-time setup: open a throwaway connection to arm the failsafe params,
        # using a sysid that won't collide with any phase below.
        setup = connect(sysid=250)
        assert set_param(setup, "FS_GCS_ENABLE", 1, mavutil.mavlink.MAV_PARAM_TYPE_INT8)
        assert set_param(setup, "FS_GCS_TIMEOUT", 3, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
        print("FS_GCS_ENABLE=1, FS_GCS_TIMEOUT=3 confirmed via PARAM_VALUE readback.")
        # Sanity-check SYSID_MYGCS read/write works at all, in a clean
        # pre-failsafe state, then restore it to the 255 default before
        # Phase 1/2 run (their premise depends on the default).
        mygcs0 = get_param(setup, "MAV_GCS_SYSID", timeout=8)
        print(f"SYSID_MYGCS initial value: {mygcs0}")
        probe_ok = set_param(setup, "MAV_GCS_SYSID", 42, mavutil.mavlink.MAV_PARAM_TYPE_REAL32, timeout=8)
        print(f"SYSID_MYGCS=42 set in clean state: {probe_ok} (readback {get_param(setup, 'MAV_GCS_SYSID', timeout=8)})")
        restore_ok = set_param(setup, "MAV_GCS_SYSID", 255, mavutil.mavlink.MAV_PARAM_TYPE_REAL32, timeout=8)
        print(f"SYSID_MYGCS restored to 255: {restore_ok} (readback {get_param(setup, 'MAV_GCS_SYSID', timeout=8)})")
        setup.close()

        results = {}

        # Phase 1: mission_app.py's CURRENT production config -- run_service.py
        # opens its connection with source_system=target_sys (=1), i.e. it
        # claims the FC's OWN system id. Default SYSID_MYGCS=255.
        results["phase1_sysid1_default_mygcs255"] = run_phase(
            "Phase 1: SBC heartbeats as sysid=1 (mission_app.py's CURRENT config), "
            "default SYSID_MYGCS=255 -- expect NO failsafe (1 != 255)",
            sysid=1, beat_type=mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER)

        # Phase 2: positive control -- sysid=255 matches the default SYSID_MYGCS.
        results["phase2_sysid255_default_mygcs255"] = run_phase(
            "Phase 2: heartbeats as sysid=255 (matches default SYSID_MYGCS) "
            "-- positive control, expect failsafe DOES fire",
            sysid=255, beat_type=mavutil.mavlink.MAV_TYPE_GCS)

        # Phase 3: proposed fix -- SYSID_MYGCS set to a distinct SBC id (42),
        # SBC heartbeats sent as that same id.
        setup2 = connect(sysid=250)
        before = get_param(setup2, "MAV_GCS_SYSID", timeout=8)
        print(f"SYSID_MYGCS before set: {before}")
        ok = set_param(setup2, "MAV_GCS_SYSID", 42, mavutil.mavlink.MAV_PARAM_TYPE_REAL32, timeout=8)
        after = get_param(setup2, "MAV_GCS_SYSID", timeout=8)
        print(f"set_param returned {ok}; SYSID_MYGCS readback after: {after}")
        if after != 42:
            print(f"WARNING: SYSID_MYGCS did not stick (got {after}) -- "
                  "Phase 3 will proceed anyway and its result should be read "
                  "in light of this.")
        setup2.close()
        results["phase3_sysid42_mygcs42"] = run_phase(
            "Phase 3: SYSID_MYGCS=42, SBC heartbeats as sysid=42 (proposed fix) "
            "-- expect failsafe DOES fire on this id's loss alone",
            sysid=42, beat_type=mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER)

        print("\n\n=== SUMMARY ===")
        for k, v in results.items():
            fired = any("Failsafe" in t and "GCS" in t for t in v)
            print(f"{k}: {'FIRED' if fired else 'did not fire'}")
    finally:
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


if __name__ == "__main__":
    main()
