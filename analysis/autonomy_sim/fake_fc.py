"""Minimal MAVLink flight-controller simulator.

Just enough of an ArduPilot FC to exercise the mission app's control contract
WITHOUT installing ArduPilot SITL: streams HEARTBEAT (with current mode) and
GLOBAL_POSITION_INT, and reacts to SET_MODE / DO_SET_MODE and
SET_POSITION_TARGET_GLOBAL_INT. Records everything it receives so a test can
assert on the actual wire behavior (not the app's internal beliefs).

For real integration use ArduPilot SITL instead of this file (see README).
"""
from __future__ import annotations
import threading
import time
from pymavlink import mavutil

from mission_app import MODE, MODE_NAME


class FakeFC(threading.Thread):
    def __init__(self, conn, *, start_mode: str = "AUTO", start_alt_m: float = 120.0,
                 lat: float = 42.30000, lon: float = -83.70000, stream_hz: float = 10.0):
        super().__init__(daemon=True)
        self.conn = conn
        self.mode = MODE[start_mode]
        self.alt_m = start_alt_m
        self.lat_e7 = int(lat * 1e7)
        self.lon_e7 = int(lon * 1e7)
        self.stream_hz = stream_hz
        self._stop_evt = threading.Event()
        self._boot = time.time()
        self._peer_seen = False
        # records for assertions
        self.mode_cmds: list[int] = []           # custom_mode values commanded to us
        self.position_targets: list[tuple[int, int, float]] = []
        self.position_target_masks: list[int] = []
        self.statustexts: list[str] = []

    # ---- external control (simulate FC-side failsafe, e.g. link/batt) ----
    def force_mode(self, mode_name: str):
        self.mode = MODE[mode_name]

    def stop(self):
        self._stop_evt.set()

    # ---- outbound streams -------------------------------------------------
    def _ms(self) -> int:
        return int((time.time() - self._boot) * 1000)

    def _send_heartbeat(self):
        self.conn.mav.heartbeat_send(
            mavutil.mavlink.MAV_TYPE_QUADROTOR,
            mavutil.mavlink.MAV_AUTOPILOT_ARDUPILOTMEGA,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            self.mode,
            mavutil.mavlink.MAV_STATE_ACTIVE)

    def _send_position(self):
        # Drift altitude toward a target implied by the last GUIDED command, so
        # the app sees the descent it asked for (light touch — not real dynamics).
        self.conn.mav.global_position_int_send(
            self._ms(), self.lat_e7, self.lon_e7,
            int(self.alt_m * 1000), int(self.alt_m * 1000),
            0, 0, 0, 0)

    # ---- inbound handling -------------------------------------------------
    def _handle(self, msg):
        t = msg.get_type()
        if t == "SET_MODE":
            self.mode = msg.custom_mode
            self.mode_cmds.append(msg.custom_mode)
        elif t == "COMMAND_LONG" and msg.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
            self.mode = int(msg.param2)
            self.mode_cmds.append(int(msg.param2))
        elif t == "SET_POSITION_TARGET_GLOBAL_INT":
            self.position_targets.append((msg.lat_int, msg.lon_int, msg.alt))
            self.position_target_masks.append(int(msg.type_mask))
            self.alt_m = float(msg.alt)          # snap to commanded alt (mock descent)
        elif t == "STATUSTEXT":
            txt = msg.text
            self.statustexts.append(txt.decode() if isinstance(txt, bytes) else txt)

    def run(self):
        period = 1.0 / self.stream_hz
        next_stream = time.time()
        while not self._stop_evt.is_set():
            msg = self.conn.recv_match(blocking=False)
            if msg is not None:
                self._peer_seen = True
                self._handle(msg)
            now = time.time()
            if self._peer_seen and now >= next_stream:
                self._send_heartbeat()
                self._send_position()
                next_stream = now + period
            time.sleep(0.002)
