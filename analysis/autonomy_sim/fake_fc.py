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
                 lat: float = 42.30000, lon: float = -83.70000, stream_hz: float = 10.0,
                 home_lat: float | None = None, home_lon: float | None = None,
                 battery_capacity_mah: float = 12000.0, battery_voltage_v: float = 22.2,
                 battery_current_a: float = 0.0, battery_consumed_mah: float = 0.0,
                 rtl_alt_m: float = 15.0, rtl_speed_mps: float = 5.0):
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

        # D2.17: HOME_POSITION + BATTERY_STATUS, and the two RTL-relevant params
        # a real companion computer would PARAM_REQUEST_READ. home_lat/home_lon
        # default to the FC's own start position (distance-to-home == 0) --
        # a test that wants a nonzero distance passes lat/lon far from an
        # explicit home_lat/home_lon (or vice versa); this mock's own position
        # never moves (see _send_position's docstring), so that's the only way
        # to script a distance profile here.
        self.home_lat = home_lat if home_lat is not None else lat
        self.home_lon = home_lon if home_lon is not None else lon
        self.battery_capacity_mah = battery_capacity_mah
        self.battery_voltage_v = battery_voltage_v
        self.battery_current_a = battery_current_a
        self.battery_consumed_mah = battery_consumed_mah
        self.rtl_alt_m = rtl_alt_m
        self.rtl_speed_mps = rtl_speed_mps

    # ---- external control (simulate FC-side failsafe, e.g. link/batt) ----
    def force_mode(self, mode_name: str):
        self.mode = MODE[mode_name]

    def set_battery(self, *, consumed_mah: float | None = None,
                     current_a: float | None = None, voltage_v: float | None = None):
        """Let a test script a drain profile: call between run ticks to move
        the simulated pack state, same idea as force_mode() for failsafes."""
        if consumed_mah is not None:
            self.battery_consumed_mah = consumed_mah
        if current_a is not None:
            self.battery_current_a = current_a
        if voltage_v is not None:
            self.battery_voltage_v = voltage_v

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

    def _send_home_position(self):
        self.conn.mav.home_position_send(
            int(self.home_lat * 1e7), int(self.home_lon * 1e7), 0,
            0.0, 0.0, 0.0, [1.0, 0.0, 0.0, 0.0], 0.0, 0.0, 0.0)

    def _send_battery_status(self):
        # energy_model.pack_voltage_v() sums whatever entries aren't the
        # UINT16_MAX "unpopulated" sentinel, so one live cell carrying the
        # whole pack voltage plus nine unpopulated slots round-trips correctly
        # without having to fake a real per-cell breakdown.
        voltages = [int(self.battery_voltage_v * 1000)] + [65535] * 9
        self.conn.mav.battery_status_send(
            0, mavutil.mavlink.MAV_BATTERY_FUNCTION_ALL, mavutil.mavlink.MAV_BATTERY_TYPE_LIPO,
            32767, voltages, int(self.battery_current_a * 100), int(self.battery_consumed_mah),
            -1, -1)

    def _send_param(self, param_id: str, value: float):
        self.conn.mav.param_value_send(
            param_id.encode("utf-8"), value, mavutil.mavlink.MAV_PARAM_TYPE_REAL32, 1, 0)

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
        elif t == "PARAM_REQUEST_READ":
            param_id = msg.param_id if isinstance(msg.param_id, str) else msg.param_id.decode("utf-8")
            param_id = param_id.rstrip("\x00")
            # RTL_SPEED == 0 here on purpose: exercises MissionApp's documented
            # ArduPilot fallback to WPNAV_SPEED (see mission_app.py's PARAM_VALUE
            # handling) rather than only ever testing the common-case direct read.
            if param_id == "RTL_SPEED":
                self._send_param("RTL_SPEED", 0.0)
            elif param_id == "WPNAV_SPEED":
                self._send_param("WPNAV_SPEED", self.rtl_speed_mps * 100.0)
            elif param_id == "RTL_ALT":
                self._send_param("RTL_ALT", self.rtl_alt_m * 100.0)

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
                self._send_home_position()
                self._send_battery_status()
                next_stream = now + period
            time.sleep(0.002)
