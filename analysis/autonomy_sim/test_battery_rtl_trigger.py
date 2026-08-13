"""Unit tests for the D2.17 distance-adaptive RTL trigger.

Run with: python -m unittest test_battery_rtl_trigger -v
(stdlib unittest on purpose -- pytest isn't in Mission Control's venv, and
this module has no other dependency either, so `python -m unittest` is
enough to self-verify it without installing anything. pytest also discovers
and runs unittest.TestCase classes natively, so `pytest` from this directory
picks these up too, alongside the rest of the suite.)
"""
from __future__ import annotations

import unittest

from battery_rtl_trigger import BatteryRTLMonitor, RTLTriggerConfig
from energy_model import PowerDrawTracker, haversine_distance_m, remaining_energy_j

HOME_LAT, HOME_LON = 42.30000, -83.70000


class HaversineTests(unittest.TestCase):
    def test_zero_distance(self):
        self.assertAlmostEqual(haversine_distance_m(HOME_LAT, HOME_LON, HOME_LAT, HOME_LON), 0.0)

    def test_one_degree_latitude_is_about_111_km(self):
        d = haversine_distance_m(0.0, 0.0, 1.0, 0.0)
        self.assertAlmostEqual(d, 111_195, delta=200)

    def test_known_2_8km_leg(self):
        # ~0.0252 deg latitude ~= 2.8 km at this latitude band.
        d = haversine_distance_m(HOME_LAT, HOME_LON, HOME_LAT + 0.0252, HOME_LON)
        self.assertAlmostEqual(d, 2800, delta=50)


class RemainingEnergyTests(unittest.TestCase):
    def test_full_pack(self):
        # 12 Ah at 22.2 V nominal (BAT10), nothing consumed yet.
        j = remaining_energy_j(capacity_mah=12000, consumed_mah=0, pack_voltage_v=22.2)
        self.assertAlmostEqual(j, 12.0 * 22.2 * 3600, delta=1)

    def test_partially_consumed(self):
        j = remaining_energy_j(capacity_mah=12000, consumed_mah=6000, pack_voltage_v=22.2)
        self.assertAlmostEqual(j, 6.0 * 22.2 * 3600, delta=1)

    def test_never_goes_negative(self):
        j = remaining_energy_j(capacity_mah=12000, consumed_mah=99000, pack_voltage_v=22.2)
        self.assertEqual(j, 0.0)


class PowerDrawTrackerTests(unittest.TestCase):
    def test_first_sample_seeds_average(self):
        t = PowerDrawTracker(alpha=0.1)
        avg = t.sample(current_a=10.0, voltage_v=22.2)
        self.assertAlmostEqual(avg, 222.0)

    def test_converges_toward_steady_draw(self):
        t = PowerDrawTracker(alpha=0.2)
        for _ in range(50):
            avg = t.sample(current_a=12.0, voltage_v=22.2)
        self.assertAlmostEqual(avg, 12.0 * 22.2, delta=0.5)

    def test_rejects_bad_alpha(self):
        with self.assertRaises(ValueError):
            PowerDrawTracker(alpha=0.0)
        with self.assertRaises(ValueError):
            PowerDrawTracker(alpha=1.5)


class BatteryRTLMonitorTests(unittest.TestCase):
    def _monitor(self, **overrides) -> BatteryRTLMonitor:
        config = RTLTriggerConfig(
            capacity_mah=12000,
            return_speed_mps=12.0,   # ~conservative cruise/RTL ground speed
            margin_fraction=0.10,
            climb_energy_j=0.0,
        )
        for k, v in overrides.items():
            setattr(config, k, v)
        return BatteryRTLMonitor(HOME_LAT, HOME_LON, config)

    def test_far_from_home_low_battery_triggers(self):
        mon = self._monitor()
        # 2.8 km out (the static worst-case leg), 250 W steady draw, only
        # ~5% of the pack left -- clearly not enough to make it home.
        far_lat = HOME_LAT + 0.0252
        fired = mon.update(
            lat=far_lat, lon=HOME_LON, below_rtl_alt=False,
            current_a=250.0 / 22.2, voltage_v=22.2, consumed_mah=11400,
        )
        self.assertTrue(fired)
        self.assertGreater(mon.last_diagnostics["distance_to_home_m"], 2700)

    def test_close_to_home_same_battery_does_not_trigger(self):
        """The whole point of D2.17: the static threshold would fire here
        too (it's calibrated for the 2.8 km worst case regardless of actual
        position), but the adaptive trigger should not, since the energy
        needed to cover the *actual* short remaining distance is small."""
        mon = self._monitor()
        near_lat = HOME_LAT + 0.0005  # ~55 m out
        fired = mon.update(
            lat=near_lat, lon=HOME_LON, below_rtl_alt=False,
            current_a=250.0 / 22.2, voltage_v=22.2, consumed_mah=11400,
        )
        self.assertFalse(fired)

    def test_margin_boundary_is_crossed_by_extra_consumption(self):
        """Two ticks at the same distance/draw, differing only in how much
        has been consumed so far: the one with less energy left should
        trigger, the one with more should not. This pins down the direction
        of the inequality without relying on hitting an exact float
        boundary (the haversine distance for a given lat offset isn't an
        exact inverse of the offset used to construct it, so an exact-zero
        margin case is inherently a few mJ off either way)."""
        distance_m = 1000.0
        speed = 12.0
        power_w = 100.0
        needed_j = (distance_m / speed) * power_w
        needed_mah = needed_j / 3600 / 22.2 * 1000
        lat = HOME_LAT + (distance_m / 111_195)

        just_enough = self._monitor(margin_fraction=0.0)
        fired_enough = just_enough.update(
            lat=lat, lon=HOME_LON, below_rtl_alt=False,
            current_a=power_w / 22.2, voltage_v=22.2,
            consumed_mah=12000 - needed_mah - 5,  # 5 mAh of extra slack
        )
        self.assertFalse(fired_enough)

        just_short = self._monitor(margin_fraction=0.0)
        fired_short = just_short.update(
            lat=lat, lon=HOME_LON, below_rtl_alt=False,
            current_a=power_w / 22.2, voltage_v=22.2,
            consumed_mah=12000 - needed_mah + 5,  # 5 mAh short
        )
        self.assertTrue(fired_short)

    def test_latches_only_fires_once(self):
        mon = self._monitor()
        far_lat = HOME_LAT + 0.0252
        first = mon.update(lat=far_lat, lon=HOME_LON, below_rtl_alt=False,
                            current_a=250.0 / 22.2, voltage_v=22.2, consumed_mah=11400)
        second = mon.update(lat=far_lat, lon=HOME_LON, below_rtl_alt=False,
                             current_a=250.0 / 22.2, voltage_v=22.2, consumed_mah=11500)
        self.assertTrue(first)
        self.assertFalse(second)
        self.assertTrue(mon.triggered)

    def test_climb_energy_adds_to_requirement(self):
        base = self._monitor(climb_energy_j=0.0)
        with_climb = self._monitor(climb_energy_j=50_000.0)
        lat = HOME_LAT + 0.005
        kwargs = dict(lat=lat, lon=HOME_LON, current_a=200.0 / 22.2,
                      voltage_v=22.2, consumed_mah=10000)
        base.update(below_rtl_alt=True, **kwargs)
        with_climb.update(below_rtl_alt=True, **kwargs)
        self.assertGreater(
            with_climb.last_diagnostics["energy_needed_j"],
            base.last_diagnostics["energy_needed_j"],
        )

    def test_climb_energy_ignored_when_already_above_rtl_alt(self):
        mon = self._monitor(climb_energy_j=50_000.0)
        mon.update(lat=HOME_LAT + 0.005, lon=HOME_LON, below_rtl_alt=False,
                    current_a=200.0 / 22.2, voltage_v=22.2, consumed_mah=10000)
        self.assertEqual(mon.last_diagnostics["climb_energy_j"], 0.0)


if __name__ == "__main__":
    unittest.main()
