"""Canonical parameter values for the two §3.7 failsafe requirements.

These realize the open failsafe requirements (R?_FS_LINK, R?_FS_BATT) and
the R6 BATT_LOW_MAH reserve recommendation from low_battery_reserve_analysis.md.

Each set is a dict of {PARAM_NAME: (value, type)} suitable for PARAM_SET.
"""
from pymavlink import mavutil

# Type codes for PARAM_SET (mavutil.mavlink.MAV_PARAM_TYPE_*)
INT8 = mavutil.mavlink.MAV_PARAM_TYPE_INT8
INT16 = mavutil.mavlink.MAV_PARAM_TYPE_INT16
INT32 = mavutil.mavlink.MAV_PARAM_TYPE_INT32
REAL32 = mavutil.mavlink.MAV_PARAM_TYPE_REAL32

# ── Link-loss failsafe (FS_THR_ENABLE / FS_OPTIONS / FS_THR_VALUE) ──────────
LINK_LOSS_FS = {
    "FS_THR_ENABLE": (1, INT8),       # 1 = RTL on throttle failsafe
    "FS_OPTIONS":    (0, INT16),      # 0 = no special options (re-arm on RTL, etc.)
    "FS_THR_VALUE":  (900, INT16),    # throttle below 900 (out of 1000) → loss
}
"""Link-loss failsafe: FS_THR_ENABLE=1 triggers RTL when throttle drops below
FS_THR_VALUE=900 (indicating the TX link was lost). This is the recommended
ArduPilot configuration for this class of long-range autonomous vehicle."""

# ── Low-battery failsafe (BATT_* params per low_battery_reserve_analysis.md) ─
LOW_BATTERY_FS = {
    "BATT_LOW_MAH":  (700, INT32),     # 700 mAh reserve (R6, 30% margin @ 2.8 km @ 12 m/s)
    "BATT_CRT_MAH":  (350, INT32),     # 350 mAh critical reserve
    "BATT_LOW_VOLT": (20.4, REAL32),   # 3.4 V/cell first-stage
    "BATT_CRT_VOLT": (19.2, REAL32),   # 3.2 V/cell critical
    "BATT_FS_LOW_ACT":  (2, INT8),     # 2 = RTL on low battery
    "BATT_FS_CRT_ACT":  (1, INT8),     # 1 = Land on critical battery
    # FS_BATT_ENABLE doesn't exist on modern ArduCopter (confirmed via a
    # full PARAM_REQUEST_LIST dump against 4.7.0, task D2.13, 2026-08-10)
    # -- the standalone enable flag was removed; setting a nonzero
    # BATT_FS_LOW_ACT/BATT_FS_CRT_ACT above is what enables the failsafe.
    "BATT_MONITOR":     (4, INT8),     # 4 = Fuel level + voltage
}
"""Low-battery failsafe: BATT_LOW_MAH=700 mAh triggers RTL at 700 mAh remaining
(power-bucket-optimum 12 m/s return from 2.8 km, plus 30% margin for wind/sag).
BATT_CRT_MAH=350 triggers immediate landing if the RTL drain continues to critical."""

# ── Return speed (enables the fast-RTL power-bucket advantage) ──────────────
RTL_CRUISE = {
    # Renamed from RTL_SPEED on modern ArduCopter (confirmed via a full
    # PARAM_REQUEST_LIST dump against 4.7.0, task D2.13, 2026-08-10).
    "RTL_SPEED_MS": (12.0, REAL32),    # 12 m/s return speed (power-bucket sweet spot)
}
"""RTL return speed: 12 m/s is the power-bucket minimum (~136 W on AF3a+T13+SBC3+BAT10),
returning from 2.8 km in ~5.4 min with only 555 mAh bare draw."""

# ── Combined set (everything) ───────────────────────────────────────────────
ALL_FS_PARAMS = {}
ALL_FS_PARAMS.update(LINK_LOSS_FS)
ALL_FS_PARAMS.update(LOW_BATTERY_FS)
ALL_FS_PARAMS.update(RTL_CRUISE)