# GPS Module Market Analysis

## Context

The `GpsModule` in the model provides position, velocity, and time data to the flight controller. It's critical for return-to-home (RTH), GPS rescue, position hold, and autonomous waypoint navigation (Phase 2+). Several airframes include GPS as standard — see airframe-research.md for per-frame GPS inclusion.

## Candidates

| ID | Model | Chipset | Constraints | Weight | Price | Key Tradeoff |
|----|-------|---------|-------------|--------|-------|-------------|
| G1 | Beitian BN-220 | M10050 (M8N-class) | GPS+BDS+GAL+SBAS+QZSS | 5g | $15-20 | Budget bare GPS. No compass. Slow cold start (30-45s) |
| G2 | Beitian BN-880 | M8N clone | GPS+GLO+GAL+BDS+SBAS | 8g | $10-14 | Classic budget. Has compass (EMI-vulnerable on quads). Slow cold start |
| G3 | Matek M10Q-5883 | u-blox SAM-M10Q | GPS+GLO+GAL+BDS | 5g | $22-28 | Best value. Real M10. Fast lock (15-20s). 10-18Hz. 4 constellations |
| G4 | iFlight BLITZ M10 GPS V2 Mini | u-blox M10 | GPS+GAL+QZSS+Glonass | 8g | $41.99 | iFlight native. Built-in farad cap. LNA+TCXO. TPU mounts included |
| G5 | iFlight BLITZ M10 GPS V2 Std | u-blox M10 | GPS+GAL+QZSS+Glonass | 16g | $41.99 | Bigger antenna (25mm). Same electronics as Mini. For larger frames |
| G6 | TBS M10 GPS | u-blox M10 | GPS+GLO+GAL+BDS | 4g | $30-35 | Premium. Fastest lock (12-18s). 18Hz. No compass. Active antenna via u.FL |

## Key Findings

### Chipset Generations

- **M8N-class** (BN-220, BN-880): Older, slower cold starts (30-45s), 2.5m accuracy, GPS+GLONASS only. Price advantage: $10-20.
- **M10-class** (all others): Modern, fast cold starts (12-27s), 1.5m accuracy, 4 constellations. Worth the $8-12 premium for any drone with GPS rescue.

### Airframe GPS Inclusion Mapping

| Airframe | GPS Included? | Recommended Module if Adding |
|----------|--------------|------------------------------|
| Axisflying KOLAS7 — BNF (Analog or HD) | ✅ Yes | Already included |
| DeepSpace ROC7 O4 PRO — PNP | ✅ Yes | Already included |
| DarwinFPV 129 7" | ✅ Yes | Already included |
| NewBeeDrone ROC7 O4PRO | ✅ Likely Yes | Already included (same hardware as DeepSpace) |
| GEPRC MARK4 LR7 — PNP | ❌ No | G3 (Matek M10Q) — $22-28 |
| Axisflying KOLAS7 — PNP | ❌ No | G3 (Matek M10Q) — $22-28; frame has built-in mount ✅ |
| iFlight Chimera9 ECO — PNP | ❌ No (optional +$39) | G4 (BLITZ M10 Mini) — $41.99 (native iFlight, compatible TPU mount) |
| iFlight Chimera7 Pro V2 — PNP | ❌ Not confirmed | G4 (BLITZ M10 Mini) — $41.99 (known iFlight Chimera compatibility) |
| GEPRC Crocodile75 V3 — PNP | ❌ Not confirmed | G3 (Matek M10Q) — $22-28 |
| EMAX Hawk 7 — BNF ELRS | ❌ Likely No | G3 (Matek M10Q) — $22-28 |

### Recommendation for Standalone Purchase

For any airframe that needs a GPS added, the **Matek M10Q-5883 ($22-28)** is the sweet spot:
- Real u-blox M10 (4 constellations, fast lock)
- Lightweight (5g)
- Low power (~0.23W)
- Supercap for hot start retention
- ~0.43Wh/day worst-case energy impact — negligible vs flight battery

The **BLITZ M10 GPS V2 ($41.99)** is the next step up for iFlight Chimera airframes where native TPU mount compatibility simplifies installation.

### Cost Impact

- Adding GPS to an airframe that lacks it: **$22-42**
- Well within budget — crossed against R4 and airframe-specific cost caps
- 6 of 11 candidate airframes already include GPS, so many build paths need $0 for this component

## Notes

- GPS module power draw (~50mA @5V = 0.25W) is negligible — <0.5% of total system power on a typical 7" build (~50-80W cruise). No requirement written in model for GPS power because it's de minimis.
- Compass (magnetometer) included on BN-880, Matek M10Q, and BLITZ M10 is largely irrelevant — Betaflight uses GPS course-over-ground, not magnetometer heading for GPS rescue. The I2C wiring for compass adds complexity without benefit on Betaflight quads.
- GPS mounting matters significantly: must have clear sky view, not under battery or carbon fiber. Airframes with built-in GPS mounts (KOLAS7, ROC7, Chimera9 ECO option) have an advantage.