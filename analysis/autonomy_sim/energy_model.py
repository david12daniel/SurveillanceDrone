"""Pure math helpers for the distance-adaptive low-battery RTL trigger (D2.17).

No MAVLink/pymavlink dependency on purpose -- this module is the testable
core; battery_rtl_trigger.py wraps it with the MAVLink-facing glue described
in README.md. Keeping the two separate means the arithmetic can be unit
tested without pymavlink installed (it isn't in Mission Control's own venv,
and shouldn't need to be).
"""
from __future__ import annotations

import math

EARTH_RADIUS_M = 6_371_000.0


def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two lat/lon points, in meters."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(min(1.0, a)))


def pack_voltage_v(cell_millivolts: list[int]) -> float:
    """Sum a MAVLink BATTERY_STATUS.voltages[] reading (mV per cell, UINT16_MAX
    for unpopulated cells) into a pack voltage in volts."""
    live = [v for v in cell_millivolts if 0 < v < 65535]
    return sum(live) / 1000.0


def remaining_energy_j(capacity_mah: float, consumed_mah: float, pack_voltage_v: float) -> float:
    """Energy left in the pack, in joules, from configured capacity minus
    MAVLink BATTERY_STATUS.current_consumed (mAh) -- an independent estimate
    from the FC's own battery_remaining %, since that field is only as good
    as ArduPilot's battery monitor calibration (often unset/wrong on a new
    build)."""
    remaining_mah = max(0.0, capacity_mah - consumed_mah)
    return (remaining_mah / 1000.0) * pack_voltage_v * 3600.0


class PowerDrawTracker:
    """Exponential moving average of measured electrical power draw (W),
    fed from BATTERY_STATUS each tick during cruise flight. Using a live
    measurement instead of a fixed assumed wattage is the key difference
    from the static-threshold approach: the return-energy estimate reflects
    this airframe/payload/wind on this flight, not a worst-case design-time
    number that's `TBD` in the model regardless (MODEL_ISSUES.md UC-10)."""

    def __init__(self, alpha: float = 0.1, initial_w: float | None = None):
        if not 0.0 < alpha <= 1.0:
            raise ValueError("alpha must be in (0, 1]")
        self.alpha = alpha
        self._avg_w = initial_w

    @property
    def average_w(self) -> float | None:
        return self._avg_w

    def sample(self, current_a: float, voltage_v: float) -> float:
        instantaneous_w = current_a * voltage_v
        if self._avg_w is None:
            self._avg_w = instantaneous_w
        else:
            self._avg_w = self.alpha * instantaneous_w + (1 - self.alpha) * self._avg_w
        return self._avg_w
