"""Distance-adaptive low-battery RTL trigger (D2.17).

Reference implementation for thermal-surveillance-drone's D2.17 task:
"SBC (or FC Lua script) computes energy-needed-to-return from the current
GPS distance-to-home each cycle and commands RTL via MAVLink at ~10% margin,
instead of waiting for the static R6_FS_BATT worst-case (2.8 km) threshold."

Design summary (full rationale in README.md in this directory):
  - Recompute distance-to-home every tick (haversine on GLOBAL_POSITION_INT
    vs. HOME_POSITION), not just once at takeoff.
  - Estimate return power draw from a live EMA of measured cruise power
    (BATTERY_STATUS.current_battery * pack voltage) rather than a fixed
    assumed wattage -- see energy_model.PowerDrawTracker's docstring for why.
  - Estimate remaining energy from configured pack capacity minus
    BATTERY_STATUS.current_consumed, independent of the FC's own
    battery_remaining % (which depends on ArduPilot battery-monitor
    calibration that may not be trustworthy on a new build).
  - Trigger RTL the first time remaining energy <= (1 + margin) * energy
    needed to fly the current distance home at the tracked return speed,
    plus a fixed climb-to-RTL_ALT energy allowance if currently below it.
  - BATT_CRT_MAH stays configured in ArduPilot as-is: this is a *tighter,
    earlier* trigger that fires before that hard floor in the normal case,
    never a replacement for it. If this monitor never fires (e.g. bad
    telemetry), the existing firmware-level backstop is still there.

This module intentionally does not import pymavlink -- it exposes plain
methods taking primitive values, so the actual MAVLink message unpacking
stays in mission_app.py-style glue (see README.md's "Integration point"
section for the exact fields to pull from GLOBAL_POSITION_INT,
HOME_POSITION, and BATTERY_STATUS), and this file's logic is unit-testable
without a MAVLink stack installed.
"""
from __future__ import annotations

from dataclasses import dataclass

from energy_model import PowerDrawTracker, haversine_distance_m, remaining_energy_j


@dataclass
class RTLTriggerConfig:
    capacity_mah: float            # configured pack capacity, e.g. BAT10 = 12000
    return_speed_mps: float        # ArduPilot RTL_SPEED (cm/s / 100), or WPNAV_SPEED if RTL_SPEED=0
    margin_fraction: float = 0.10  # ~10% margin over the computed return energy
    climb_energy_j: float = 0.0    # fixed allowance for climb-to-RTL_ALT if below it; 0 disables
    power_ema_alpha: float = 0.1   # PowerDrawTracker smoothing factor


class BatteryRTLMonitor:
    """One instance per flight. Call `update()` once per SBC tick (same
    cadence as MissionApp.step()); it returns True exactly once, the first
    tick the reserve margin is breached -- mirrors the edge-triggered
    `failsafe_observed` pattern mission_app.py already uses for FC-commanded
    RTL/LAND, so the call site can plug straight into that branch."""

    def __init__(self, home_lat: float, home_lon: float, config: RTLTriggerConfig):
        self.home_lat = home_lat
        self.home_lon = home_lon
        self.config = config
        self._power_tracker = PowerDrawTracker(alpha=config.power_ema_alpha)
        self._triggered = False
        self.last_diagnostics: dict | None = None

    @property
    def triggered(self) -> bool:
        return self._triggered

    def _evaluate(
        self,
        lat: float,
        lon: float,
        below_rtl_alt: bool,
        current_a: float,
        voltage_v: float,
        consumed_mah: float,
    ) -> tuple[bool, dict]:
        return_power_w = self._power_tracker.sample(current_a, voltage_v)
        distance_m = haversine_distance_m(lat, lon, self.home_lat, self.home_lon)
        time_to_return_s = distance_m / self.config.return_speed_mps
        flight_energy_j = time_to_return_s * return_power_w
        climb_j = self.config.climb_energy_j if below_rtl_alt else 0.0
        energy_needed_j = (flight_energy_j + climb_j) * (1.0 + self.config.margin_fraction)

        remaining_j = remaining_energy_j(
            self.config.capacity_mah, consumed_mah, voltage_v
        )

        diagnostics = {
            "distance_to_home_m": distance_m,
            "return_power_w": return_power_w,
            "time_to_return_s": time_to_return_s,
            "climb_energy_j": climb_j,
            "energy_needed_j": energy_needed_j,
            "remaining_energy_j": remaining_j,
            "margin_j": remaining_j - energy_needed_j,
        }
        return remaining_j <= energy_needed_j, diagnostics

    def update(
        self,
        *,
        lat: float,
        lon: float,
        below_rtl_alt: bool,
        current_a: float,
        voltage_v: float,
        consumed_mah: float,
    ) -> bool:
        """Returns True on the tick the trigger first fires, False every
        other tick (including all ticks after the first firing -- it
        latches, same as mission_app.py's PASSIVE state, so the call site
        commands RTL exactly once)."""
        should_trigger, diagnostics = self._evaluate(
            lat, lon, below_rtl_alt, current_a, voltage_v, consumed_mah
        )
        self.last_diagnostics = diagnostics
        if should_trigger and not self._triggered:
            self._triggered = True
            return True
        return False
