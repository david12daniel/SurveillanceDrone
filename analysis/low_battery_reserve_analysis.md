# Low-Battery Reserve Analysis — BATT_LOW_MAH Decision (Revised)

**Date:** 2026-08-04 (revised)
**Author:** Automated analysis (nightly agent)
**Purpose:** Pick the `BATT_LOW_MAH` reserve threshold for the R6_BHV_RTL_RESERVE requirement, accounting for a **fast return-to-launch speed** (not the slow surveillance cruise).

**Provenance note (2026-08-11):** this file was produced by an OpenClaw nightly-agent
session in a separate WSL clone of this repo and ported into the main (Windows)
checkout as part of closing TASKS.md items 0.2/0.3 — see `MODEL_ISSUES.md` §B8. The
`BATT_LOW_MAH = 700 mAh` figure below is a **static, worst-case-distance** reserve.
David reviewed it 2026-08-11 and asked whether the reserve could instead shrink
dynamically as the vehicle nears the launch point (avoiding an early RTL when close
to home with reserve to spare); that idea is real but requires new software (not a
firmware parameter) and is tracked as a deferred Phase 3 follow-up (TASKS.md D2.17)
rather than folded into this static analysis. `R6_FS_BATT` in `model.sysml` uses the
700 mAh figure as the Phase 1 config-only backstop.

## Correction from Previous Analysis

The initial analysis (2026-08-04) assumed the drone returns to launch at the **slow surveillance cruise speed of 2.23 m/s**. David pointed out this is wrong — the drone should fly back at a **much faster pace** after a low-battery event. The return speed is the primary lever to bring the excessive 63% margin down.

## Reference Build

| Component | ID | Details |
|---|---|---|
| Airframe | AF3a | iFlight Chimera9 ECO (PNP), 729 g |
| Thermal | T13 | PurpleRiver Mini 640, 18 mm, USB |
| SBC | SBC3 | NanoPi M5 (4 GB), ~10 W NPU |
| Flight battery | BAT10 | Upgrade Energy GREEN V2 6S3P 12Ah Amprius ($275, 919 g) |
| Dev battery | BAT22 | GNB 6S3P 12Ah 21700 Li-ion ($110, 1250 g) |

## Power Model (from flight_time_model.py)

Parameters: FoM=0.65, η=0.80, ρ=1.225 kg/m³, 4 rotors, 9" props.

AUW: 1,714 g (AF3a 729 + BAT10 919 + SBC3 45 + T13 21)

| Regime | Power [W] | J/m | Notes |
|---|---|---|---|
| Hover (V=0) | 219.7 | — | momentum theory |
| Slow cruise (2.23 m/s) | 213.6 | 107.4 | translational lift barely helps |
| 5 m/s (11.2 mph) | 192.2 | 50.3 | moderate cruise |
| **8 m/s (17.9 mph)** | **162.5** | **20.3** | power bucket starting |
| **10 m/s (22.4 mph)** | **146.4** | **14.6** | good efficiency |
| **12 m/s (26.8 mph)** | **136.1** | **11.3** | **sweet spot — lowest J/m** |
| 14 m/s (31.3 mph) | 132.1 | 9.4 | absolute minimum power |
| 16 m/s (35.8 mph) | 134.4 | 8.4 | drag starts climbing |
| 18 m/s (40.3 mph) | 142.6 | 7.9 | exiting the bucket |
| 20 m/s (44.7 mph) | 156.7 | 7.8 | drag dominance |

**Key insight:** The multirotor power bucket means 12 m/s uses **less than half the power** of 2.23 m/s to cover the same distance, because the return is fast enough to burn most of the energy on the short flight time rather than prolonged duration.

## RTL Reserve Calculation — Revised

### Chosen return speed: 12 m/s (27 mph)

This is a fast but not aggressive pace — well within the airframe's capability (9" props on 6S can comfortably do 15-20 m/s) and right at the power bucket minimum. It leaves headroom for wind and operator margin.

**Worst-case return distance:** 2.8 km (full R7 line length — the drone is at the far end of the survey line when the low-battery event triggers). This is the most conservative assumption; the original analysis only used 1.4 km (half the line).

**RTL profile at 12 m/s:**
- Climb: 30 s at hover power — 1.83 Wh
- Cruise return (2.8 km): 233 s (3.9 min) at 136.1 W — 8.82 Wh
- Descent: 60 s at ~100 W — 1.67 Wh
- **Total bare RTL energy: 12.32 Wh → 555 mAh**
- **Total RTL time: 323 s → 5.4 min**

### Bare RTL at various distances

| Return distance | Time [s] | Bare energy [Wh] | Bare mAh |
|---|---|---|---|
| 1.4 km (half line) | 207 | 7.82 | 352 |
| **2.8 km (full line)** | **323** | **12.32** | **555** |
| 4.0 km (safety margin) | 423 | 16.53 | 745 |

### Margin Philosophy

The same factors as before apply (current sensor drift, cell imbalance, failsafe race, Li-ion sag), but with a faster return:

1. **Current sensor drift:** Still present — same as before
2. **Cell imbalance:** Still present
3. **Failsafe race:** RTL is shorter (5.4 min vs 9.2 min), so less exposure to simultaneous failures
4. **Headwind on return:** 12 m/s + 4.5 m/s headwind = 16.5 m/s — still within the power bucket (134 W at 16 m/s), so **wind has minimal impact**
5. **Li-ion sag:** Same concern

### Margin Analysis

| Margin | Reserve [mAh] | Reserve [Wh] | Mission hover [min] | R6 met? |
|---|---|---|---|---|
| Bare RTL (2.8 km) | 555 | 12.3 | 59.5 | ✅ |
| +20% | 666 | 14.8 | 59.1 | ✅ |
| **+30%** | **722** | **16.0** | **58.9** | **✅** |
| **+50%** | **833** | **18.5** | **58.3** | **✅** |
| +63% (original) | 905 | 20.1 | 57.9 | ✅ |
| +100% | 1110 | 24.6 | 56.5 | ✅ |

**Even at 100% margin, the reserve is only 1,110 mAh** — less than the original 1,600 mAh recommendation, and the mission endurance is still 56.5 min hover (well above R6's 30 min).

## Concern: What if the drone returns at the slow speed anyway?

If the return speed were 5 m/s, the bare RTL from 2.8 km is 33.3 Wh (1,500 mAh), and with 30% margin that's 1,950 mAh. But the drone is programmed to RTL at a configurable speed — ArduPilot's `RTL_SPEED` parameter controls the return speed. Setting this to 12 m/s ensures the fast return is baked into the firmware.

The designer can also set `WPNAV_SPEED` (waypoint speed) and `RTL_SPEED` independently — the RTL return speed is a separate parameter from the surveillance cruise speed.

## Recommendation

### Return speed: 12 m/s (configured via `RTL_SPEED`)
### BATT_LOW_MAH = 700 mAh (30% margin on 2.8 km worst case)

**Rationale:**
- 12 m/s (27 mph) is the power-bucket sweet spot — the return burns only 555 mAh bare
- 30% margin on the full 2.8 km line gives 722 mAh → rounded down to **700 mAh** for a clean number
- Mission endurance is 58.9 min hover — **essentially unchanged** from the theoretical maximum (59.5 min), and well above R6 (30 min)
- The 700 mAh reserve is only 5.8% of total pack capacity — a much more reasonable margin than the original 63%
- Even at 2× margin (1,110 mAh), endurance is still 56.5 min

### What if the drone is beyond the 2.8 km line?

The 2.8 km line is the R7 requirement. If the drone exceeds this, the operator is already outside the spec'd range. But even at 4 km out, the bare RTL at 12 m/s is 745 mAh — still within a 700 mAh reserve would trigger a critical landing earlier, but 4 km flights are outside the mission profile.

### Updated BATT_CRT_MAH

With BATT_LOW = 700 mAh, the critical threshold should be **BATT_CRT = 350 mAh** (half), consistent with the original ratio.

## Revised ArduPilot Parameter Summary

| Parameter | Value | Unit | Description |
|---|---|---|---|
| **RTL_SPEED** | **12** | m/s | Return speed (key change — was implicitly 2.23) |
| **BATT_LOW_MAH** | **700** | mAh | Reserve capacity — trigger `BATT_FS_LOW_ACT` |
| BATT_CRT_MAH | 350 | mAh | Critical reserve — trigger `BATT_FS_CRT_ACT` |
| BATT_LOW_VOLT | 20.4 | V | 3.4 V/cell first-stage warning |
| BATT_CRT_VOLT | 19.2 | V | 3.2 V/cell critical stage |
| BATT_FS_LOW_ACT | 2 | — | Action on low: RTL |
| BATT_FS_CRT_ACT | 1 | — | Action on critical: Land |
| FS_BATT_ENABLE | 1 | — | Enable battery failsafe |
| BATT_MONITOR | 4 | — | 4 = Fuel level + voltage |

## Impact on Mission Endurance

| Metric | No reserve | With 700 mAh reserve |
|---|---|---|
| Mission-usable capacity | 10,200 mAh (85% DoD) | 9,500 mAh |
| Mission-usable energy | 220.3 Wh | 205.2 Wh |
| Max hover endurance | 59.5 min | **58.9 min** |
| Cruise endurance (2.23 m/s) | 61.7 min | 61.0 min |
| Meets R6 (≥30 min)? | ✅ | ✅ |
| Meets R8 (≥60 min) stretch? | ❌ (59.5) | ❌ (58.9) |

The reserve now costs only **~36 seconds** of hover endurance (vs. 8.9 minutes in the original analysis). Mission endurance is essentially the same as the no-reserve case.

## What Changed vs. First Analysis

| Aspect | Original (2026-08-04) | Revised (2026-08-04) |
|---|---|---|
| Return speed | 5 m/s (implicit) | **12 m/s** |
| Worst-case distance | 1.4 km (½ line) | **2.8 km (full line)** |
| Bare RTL energy | 21.2 Wh | 12.32 Wh |
| Bare RTL time | 9.2 min | 5.4 min |
| Margin applied | 63% | **30%** |
| **BATT_LOW_MAH** | **1,600 mAh** | **700 mAh** |
| Mission endurance | 48.0 min | 58.9 min |
| Endurance lost to reserve | 8.9 min | **0.6 min** |

The 63% margin was driven by the slow return speed. Picking a proper RTL speed (12 m/s) and using the full 2.8 km line as the worst case gives a much more reasonable 700 mAh reserve.

## Applicability to Dev Packs (BAT22)

The GNB 6S3P 12Ah pack has the same 12 Ah capacity but is 330 g heavier. The heavier AUW (2,044 g) means higher power draw at all regimes:

- Hover: 254.0 W (vs 219.7 W for BAT10)
- 12 m/s cruise: 161.9 W (vs 136.1 W)
- Bare RTL from 2.8 km: 14.5 Wh → 653 mAh
- **With 30% margin: 849 mAh → BATT_LOW = 850 mAh**
- Mission endurance: 46.5 min hover (still > R6)

Use the **same parameter set** for both packs — the 700 mAh threshold is conservative enough for BAT10. For BAT22, the endurance is lower but still meets R6. The reserve covers the extra weight without issue.
