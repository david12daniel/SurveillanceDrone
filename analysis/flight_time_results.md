# Flight-Time Analysis — Holistic Configuration Sweep

**Auto-generated** by [`flight_time_model.py`](flight_time_model.py). Regenerate with `python analysis/flight_time_model.py`.

Momentum-theory (actuator-disk) propulsion model + forward-flight parasitic drag. "Max flight time" = still-air hover endurance (R6 ≥ 30 min / R8 ≥ 60 min metric).

## Sweep scope

- **351 real configurations** = airframe × battery × VTX, fully crossed (respecting airframe component inclusion) and **filtered for interface compatibility**; thermal fixed to **T13** and SBC fixed to **SBC3** (design choices, not swept). The DVR is compatibility-gated, not crossed, and excluded from flight time (it is an earlier-stage part; the SBC records at the SBC stage).
- Flight-time drivers swept in full; sub-1 W peripherals held at lightest representatives: FPV `A7`, GPS `G6`, RX `GEPRCNanoPA100`.
- **Inclusion logic:** airframe-bundled VTX/FPV/GPS/RX contribute power only (their mass is already in the airframe's as-built weight); non-bundled peripherals contribute mass + power.
- Candidates: 15 airframes (with mass data), 21 real battery candidates, 70 swept payload components.
- **Cost (R4 ≤ $2,500):** each config's drone cost + a fixed laptop-based GCS (ELRS USB dongle + analog VRX/capture + a Phase-1/backup handheld radio = $126; the laptop is the ground station); bundled VTX/FPV/GPS/RX add $0 (already in the airframe price); the DVR is included (earlier-stage part).
- **Compatibility filtering** (declared in `DroneSystemModel::Architecture::Compatibility`): 504 raw pairings reduced to 351 real configs — pruned 153 on battery↔airframe cell-count (P1, e.g. a 4S pack on a 6S-only frame) and 0 on thermal↔DVR video format (V2, a thermal whose output no DVR can record — CVBS via DVR1-6 or digital HDMI/USB via DVR7-9).

## Model assumptions

- Rotors **4** · ρ **1.225 kg/m³** · FoM **0.65** · η **0.8** · C_d **1.0** · cruise **2.23 m/s** (R2) · wind **4.5 m/s** (R7)

> **Why cruise/wind endurance can exceed hover** — the multirotor *power bucket*: in slow forward flight the rotors gain translational lift, so induced power drops faster than parasitic drag rises. **Max FT** uses hover (conservative); *Cruise* (2.23 m/s) is the realistic still-air surveillance endurance; *Wind* is airspeed = cruise + 4.5 m/s (R7).

> **Caveats** — first-order comparative estimates (FoM, η, C_d, frontal area, thrust lookup are assumptions; battery mass derived from chemistry specific energy). Airframes missing mass/wheelbase are skipped (MODEL_ISSUES.md §D). Full per-instance data: [`flight_time_results.csv`](flight_time_results.csv).

## Recommended baseline

**DarwinFPV 129 7in** (AF9a) + **Lumenier NAV 12000mAh 4S 21700 Amprius**, SBC SBC3, VTX included, thermal T13 → **69.1 min** hover (968.7 g AUW, 16.3% throttle; drone $1379 / system $1505 ≤ $2,500 R4).

## Top 100 configurations (ranked by max flight time)

| Cfg | Airframe | Battery | SBC | VTX | Therm | AUW g | Pld W | Max FT | Cruise | Wind | Thr% | Drone $ | Sys $ | R4 | R6 | R8 | Fly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C000331 | DarwinFPV 129 7in (AF9a) | Lumenier NAV 12000mAh 4S 21700 Amprius | SBC3 | included | T13 | 968.7 | 16.85 | 69.1 | 71.0 | 84.7 | 16.3 | 1378.97 | 1504.97 | ✅ | ✅ | ✅ | ✅ |
| C000218 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1746.7 | 16.8 | 58.6 | 60.2 | 72.1 | 14.9 | 1518.83 | 1644.83 | ✅ | ✅ | — | ✅ |
| C000233 | iFlight Chimera9 ECO (AF3b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1752.0 | 16.87 | 58.4 | 59.9 | 71.8 | 14.9 | 1545.48 | 1671.48 | ✅ | ✅ | — | ✅ |
| C000248 | DarwinFPV X9 (AF4a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1772.7 | 16.8 | 57.4 | 58.9 | 70.7 | 13.7 | 1654.47 | 1780.47 | ✅ | ✅ | — | ✅ |
| C000219 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1745.7 | 16.8 | 57.1 | 58.6 | 70.3 | 14.9 | 1472.34 | 1598.34 | ✅ | ✅ | — | ✅ |
| C000234 | iFlight Chimera9 ECO (AF3b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1751.0 | 16.87 | 56.8 | 58.3 | 69.9 | 14.9 | 1498.99 | 1624.99 | ✅ | ✅ | — | ✅ |
| C000249 | DarwinFPV X9 (AF4a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1771.7 | 16.8 | 55.9 | 57.4 | 68.9 | 13.6 | 1607.98 | 1733.98 | ✅ | ✅ | — | ✅ |
| C000293 | GEPRC Crocodile75 V3 (AF7) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1623.2 | 16.8 | 54.8 | 55.9 | 64.3 | 15.0 | 1940.47 | 2066.47 | ✅ | ✅ | — | ✅ |
| C000188 | Axisflying KOLAS7 (AF2b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1563.0 | 16.47 | 54.3 | 55.2 | 62.8 | 14.0 | 1603.39 | 1729.39 | ✅ | ✅ | — | ✅ |
| C000294 | GEPRC Crocodile75 V3 (AF7) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1622.2 | 16.8 | 53.4 | 54.4 | 62.6 | 15.0 | 1893.98 | 2019.98 | ✅ | ✅ | — | ✅ |
| C000203 | Axisflying KOLAS7 (AF2c) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1586.0 | 16.92 | 53.1 | 54.0 | 61.3 | 14.2 | 1710.49 | 1836.49 | ✅ | ✅ | — | ✅ |
| C000189 | Axisflying KOLAS7 (AF2b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1562.0 | 16.47 | 52.8 | 53.8 | 61.2 | 13.9 | 1556.9 | 1682.9 | ✅ | ✅ | — | ✅ |
| C000204 | Axisflying KOLAS7 (AF2c) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1585.0 | 16.92 | 51.7 | 52.6 | 59.7 | 14.2 | 1664.0 | 1790.0 | ✅ | ✅ | — | ✅ |
| C000308 | iFlight Chimera7 Pro V2 (AF8a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1726.7 | 16.85 | 50.2 | 51.2 | 58.6 | 21.6 | 1621.47 | 1747.47 | ✅ | ✅ | — | ✅ |
| C000323 | iFlight Chimera7 Pro V2 (AF8b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1732.0 | 16.92 | 50.0 | 51.0 | 58.3 | 21.6 | 1632.0 | 1758.0 | ✅ | ✅ | — | ✅ |
| C000213 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1694.7 | 16.8 | 49.6 | 50.9 | 61.3 | 14.4 | 1449.34 | 1575.34 | ✅ | ✅ | — | ✅ |
| C000216 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1443.7 | 16.8 | 49.4 | 51.0 | 62.5 | 12.3 | 1391.34 | 1517.34 | ✅ | ✅ | — | ✅ |
| C000336 | DarwinFPV 129 7in (AF9a) | Lumenier NAV 8000mAh 4S 18650 Amprius | SBC3 | included | T13 | 918.7 | 16.85 | 49.4 | 50.8 | 60.9 | 15.4 | 1294.97 | 1420.97 | ✅ | ✅ | — | ✅ |
| C000228 | iFlight Chimera9 ECO (AF3b) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1700.0 | 16.87 | 49.3 | 50.7 | 61.0 | 14.5 | 1475.99 | 1601.99 | ✅ | ✅ | — | ✅ |
| C000231 | iFlight Chimera9 ECO (AF3b) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1449.0 | 16.87 | 49.2 | 50.7 | 62.1 | 12.4 | 1417.99 | 1543.99 | ✅ | ✅ | — | ✅ |
| C000309 | iFlight Chimera7 Pro V2 (AF8a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1725.7 | 16.85 | 48.9 | 49.9 | 57.0 | 21.6 | 1574.98 | 1700.98 | ✅ | ✅ | — | ✅ |
| C000324 | iFlight Chimera7 Pro V2 (AF8b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1731.0 | 16.92 | 48.7 | 49.6 | 56.7 | 21.6 | 1585.51 | 1711.51 | ✅ | ✅ | — | ✅ |
| C000263 | DeepSpace ROC7 O4 PRO (AF6a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1688.7 | 16.85 | 48.6 | 49.4 | 55.9 | 21.1 | 2007.47 | 2133.47 | ✅ | ✅ | — | ✅ |
| C000173 | GEPRC MOZ7 V2 O4 Pro (AF1c) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1771.7 | 16.85 | 48.5 | 49.4 | 56.3 | 14.8 | 1856.47 | 1982.47 | ✅ | ✅ | — | ✅ |
| C000243 | DarwinFPV X9 (AF4a) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1720.7 | 16.8 | 48.5 | 49.8 | 60.0 | 13.3 | 1584.98 | 1710.98 | ✅ | ✅ | — | ✅ |
| C000333 | DarwinFPV 129 7in (AF9a) | Upgrade Energy RED V3 4S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1081.7 | 16.85 | 48.5 | 49.7 | 58.7 | 18.2 | 1299.97 | 1425.97 | ✅ | ✅ | — | ✅ |
| C000334 | DarwinFPV 129 7in (AF9a) | Upgrade Energy GREEN V2 4S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 912.7 | 16.85 | 48.5 | 49.8 | 59.8 | 15.3 | 1314.98 | 1440.98 | ✅ | ✅ | — | ✅ |
| C000278 | DeepSpace ROC7 O4 PRO (AF6b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1693.0 | 16.92 | 48.4 | 49.2 | 55.7 | 21.2 | 2018.48 | 2144.48 | ✅ | ✅ | — | ✅ |
| C000344 | NewBeeDrone ROC7 O4PRO (AF10) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1693.0 | 16.92 | 48.4 | 49.2 | 55.7 | 21.2 | 1966.48 | 2092.48 | ✅ | ✅ | — | ✅ |
| C000212 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1726.7 | 16.8 | 48.3 | 49.6 | 59.5 | 14.7 | 1467.33 | 1593.33 | ✅ | ✅ | — | ✅ |
| C000246 | DarwinFPV X9 (AF4a) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1469.7 | 16.8 | 48.2 | 49.7 | 61.1 | 11.3 | 1526.98 | 1652.98 | ✅ | ✅ | — | ✅ |
| C000227 | iFlight Chimera9 ECO (AF3b) | Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1732.0 | 16.87 | 48.1 | 49.4 | 59.2 | 14.8 | 1493.98 | 1619.98 | ✅ | ✅ | — | ✅ |
| C000093 | GEPRC MOZ7 V2 WTFPV (AF1b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V8 | T13 | 1794.5 | 15.4 | 47.8 | 48.7 | 55.5 | 15.0 | 1628.47 | 1754.47 | ✅ | ✅ | — | ✅ |
| C000090 | GEPRC MOZ7 V2 WTFPV (AF1b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V5 | T13 | 1799.7 | 15.4 | 47.6 | 48.5 | 55.3 | 15.0 | 1623.47 | 1749.47 | ✅ | ✅ | — | ✅ |
| C000094 | GEPRC MOZ7 V2 WTFPV (AF1b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V10 | T13 | 1797.3 | 15.9 | 47.6 | 48.5 | 55.3 | 15.0 | 1620.47 | 1746.47 | ✅ | ✅ | — | ✅ |
| C000332 | DarwinFPV 129 7in (AF9a) | Upgrade Energy GREEN V1 4S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1095.7 | 16.85 | 47.6 | 48.8 | 57.6 | 18.4 | 1289.97 | 1415.97 | ✅ | ✅ | — | ✅ |
| C000092 | GEPRC MOZ7 V2 WTFPV (AF1b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V7 | T13 | 1800.7 | 15.9 | 47.5 | 48.4 | 55.1 | 15.0 | 1641.47 | 1767.47 | ✅ | ✅ | — | ✅ |
| C000186 | Axisflying KOLAS7 (AF2b) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1260.0 | 16.47 | 47.4 | 48.5 | 56.3 | 11.2 | 1475.9 | 1601.9 | ✅ | ✅ | — | ✅ |
| C000008 | GEPRC MOZ7 V2 Analog (AF1a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1803.7 | 16.85 | 47.3 | 48.1 | 54.8 | 15.0 | 1641.47 | 1767.47 | ✅ | ✅ | — | ✅ |
| C000088 | GEPRC MOZ7 V2 WTFPV (AF1b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V3 | T13 | 1803.7 | 16.4 | 47.3 | 48.2 | 54.9 | 15.0 | 1618.47 | 1744.47 | ✅ | ✅ | — | ✅ |
| C000242 | DarwinFPV X9 (AF4a) | Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1752.7 | 16.8 | 47.3 | 48.6 | 58.4 | 13.5 | 1602.97 | 1728.97 | ✅ | ✅ | — | ✅ |
| C000264 | DeepSpace ROC7 O4 PRO (AF6a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1687.7 | 16.85 | 47.3 | 48.1 | 54.5 | 21.1 | 1960.98 | 2086.98 | ✅ | ✅ | — | ✅ |
| C000291 | GEPRC Crocodile75 V3 (AF7) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1320.2 | 16.8 | 47.3 | 48.4 | 56.9 | 12.2 | 1812.98 | 1938.98 | ✅ | ✅ | — | ✅ |
| C000086 | GEPRC MOZ7 V2 WTFPV (AF1b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V1 | T13 | 1806.6 | 16.4 | 47.2 | 48.1 | 54.7 | 15.1 | 1623.47 | 1749.47 | ✅ | ✅ | — | ✅ |
| C000174 | GEPRC MOZ7 V2 O4 Pro (AF1c) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1770.7 | 16.85 | 47.2 | 48.1 | 54.8 | 14.8 | 1809.98 | 1935.98 | ✅ | ✅ | — | ✅ |
| C000279 | DeepSpace ROC7 O4 PRO (AF6b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1692.0 | 16.92 | 47.1 | 47.9 | 54.2 | 21.1 | 1971.99 | 2097.99 | ✅ | ✅ | — | ✅ |
| C000345 | NewBeeDrone ROC7 O4PRO (AF10) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1692.0 | 16.92 | 47.1 | 47.9 | 54.2 | 21.1 | 1919.99 | 2045.99 | ✅ | ✅ | — | ✅ |
| C000091 | GEPRC MOZ7 V2 WTFPV (AF1b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V6 | T13 | 1802.7 | 18.9 | 47.0 | 47.8 | 54.4 | 15.0 | 1660.47 | 1786.47 | ✅ | ✅ | — | ✅ |
| C000087 | GEPRC MOZ7 V2 WTFPV (AF1b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V2 | T13 | 1807.7 | 18.9 | 46.8 | 47.6 | 54.1 | 15.1 | 1633.47 | 1759.47 | ✅ | ✅ | — | ✅ |
| C000089 | GEPRC MOZ7 V2 WTFPV (AF1b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V4 | T13 | 1807.7 | 18.9 | 46.8 | 47.6 | 54.1 | 15.1 | 1618.47 | 1744.47 | ✅ | ✅ | — | ✅ |
| C000211 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 10000mAh 6S 21700 Li-Ion | SBC3 | included | T13 | 1801.7 | 16.8 | 46.8 | 48.0 | 57.3 | 15.4 | 1347.33 | 1473.33 | ✅ | ✅ | — | ✅ |
| C000103 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | V8 | T13 | 1793.5 | 15.4 | 46.6 | 47.4 | 54.1 | 14.9 | 1581.98 | 1707.98 | ✅ | ✅ | — | ✅ |
| C000226 | iFlight Chimera9 ECO (AF3b) | Lumenier NAV 10000mAh 6S 21700 Li-Ion | SBC3 | included | T13 | 1807.0 | 16.87 | 46.6 | 47.8 | 57.0 | 15.4 | 1373.98 | 1499.98 | ✅ | ✅ | — | ✅ |
| C000288 | GEPRC Crocodile75 V3 (AF7) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1571.2 | 16.8 | 46.5 | 47.5 | 54.8 | 14.5 | 1870.98 | 1996.98 | ✅ | ✅ | — | ✅ |
| C000100 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | V5 | T13 | 1798.7 | 15.4 | 46.4 | 47.2 | 53.8 | 15.0 | 1576.98 | 1702.98 | ✅ | ✅ | — | ✅ |
| C000104 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | V10 | T13 | 1796.3 | 15.9 | 46.4 | 47.2 | 53.8 | 15.0 | 1573.98 | 1699.98 | ✅ | ✅ | — | ✅ |
| C000102 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | V7 | T13 | 1799.7 | 15.9 | 46.3 | 47.1 | 53.7 | 15.0 | 1594.98 | 1720.98 | ✅ | ✅ | — | ✅ |
| C000201 | Axisflying KOLAS7 (AF2c) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1283.0 | 16.92 | 46.2 | 47.2 | 54.7 | 11.5 | 1583.0 | 1709.0 | ✅ | ✅ | — | ✅ |
| C000098 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | V3 | T13 | 1802.7 | 16.4 | 46.1 | 46.9 | 53.4 | 15.0 | 1571.98 | 1697.98 | ✅ | ✅ | — | ✅ |
| C000183 | Axisflying KOLAS7 (AF2b) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1511.0 | 16.47 | 46.1 | 47.0 | 53.6 | 13.5 | 1533.9 | 1659.9 | ✅ | ✅ | — | ✅ |
| C000009 | GEPRC MOZ7 V2 Analog (AF1a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1802.7 | 16.85 | 46.0 | 46.8 | 53.3 | 15.0 | 1594.98 | 1720.98 | ✅ | ✅ | — | ✅ |
| C000095 | GEPRC MOZ7 V2 WTFPV (AF1b) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V11 | T13 | 1817.7 | 21.5 | 46.0 | 46.8 | 53.1 | 15.1 | 1623.47 | 1749.47 | ✅ | ✅ | — | ✅ |
| C000096 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | V1 | T13 | 1805.6 | 16.4 | 46.0 | 46.8 | 53.3 | 15.0 | 1576.98 | 1702.98 | ✅ | ✅ | — | ✅ |
| C000241 | DarwinFPV X9 (AF4a) | Lumenier NAV 10000mAh 6S 21700 Li-Ion | SBC3 | included | T13 | 1827.7 | 16.8 | 45.9 | 47.0 | 56.2 | 14.1 | 1482.97 | 1608.97 | ✅ | ✅ | — | ✅ |
| C000101 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | V6 | T13 | 1801.7 | 18.9 | 45.7 | 46.5 | 52.9 | 15.0 | 1613.98 | 1739.98 | ✅ | ✅ | — | ✅ |
| C000097 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | V2 | T13 | 1806.7 | 18.9 | 45.5 | 46.4 | 52.7 | 15.1 | 1586.98 | 1712.98 | ✅ | ✅ | — | ✅ |
| C000099 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | V4 | T13 | 1806.7 | 18.9 | 45.5 | 46.4 | 52.7 | 15.1 | 1571.98 | 1697.98 | ✅ | ✅ | — | ✅ |
| C000287 | GEPRC Crocodile75 V3 (AF7) | Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1603.2 | 16.8 | 45.2 | 46.1 | 53.1 | 14.8 | 1888.97 | 2014.97 | ✅ | ✅ | — | ✅ |
| C000198 | Axisflying KOLAS7 (AF2c) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1534.0 | 16.92 | 45.1 | 45.9 | 52.3 | 13.7 | 1641.0 | 1767.0 | ✅ | ✅ | — | ✅ |
| C000105 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | V11 | T13 | 1816.7 | 21.5 | 44.8 | 45.6 | 51.7 | 15.1 | 1576.98 | 1702.98 | ✅ | ✅ | — | ✅ |
| C000182 | Axisflying KOLAS7 (AF2b) | Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1543.0 | 16.47 | 44.8 | 45.6 | 51.9 | 13.8 | 1551.89 | 1677.89 | ✅ | ✅ | — | ✅ |
| C000197 | Axisflying KOLAS7 (AF2c) | Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1566.0 | 16.92 | 43.8 | 44.6 | 50.7 | 14.0 | 1658.99 | 1784.99 | ✅ | ✅ | — | ✅ |
| C000286 | GEPRC Crocodile75 V3 (AF7) | Lumenier NAV 10000mAh 6S 21700 Li-Ion | SBC3 | included | T13 | 1678.2 | 16.8 | 43.6 | 44.4 | 50.9 | 15.5 | 1768.97 | 1894.97 | ✅ | ✅ | — | ✅ |
| C000181 | Axisflying KOLAS7 (AF2b) | Lumenier NAV 10000mAh 6S 21700 Li-Ion | SBC3 | included | T13 | 1618.0 | 16.47 | 43.1 | 43.8 | 49.7 | 14.4 | 1431.89 | 1557.89 | ✅ | ✅ | — | ✅ |
| C000306 | iFlight Chimera7 Pro V2 (AF8a) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1423.7 | 16.85 | 42.6 | 43.6 | 50.9 | 17.8 | 1493.98 | 1619.98 | ✅ | ✅ | — | ✅ |
| C000303 | iFlight Chimera7 Pro V2 (AF8a) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1674.7 | 16.85 | 42.5 | 43.4 | 49.7 | 20.9 | 1551.98 | 1677.98 | ✅ | ✅ | — | ✅ |
| C000321 | iFlight Chimera7 Pro V2 (AF8b) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1429.0 | 16.92 | 42.4 | 43.4 | 50.6 | 17.9 | 1504.51 | 1630.51 | ✅ | ✅ | — | ✅ |
| C000318 | iFlight Chimera7 Pro V2 (AF8b) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1680.0 | 16.92 | 42.3 | 43.1 | 49.5 | 21.0 | 1562.51 | 1688.51 | ✅ | ✅ | — | ✅ |
| C000196 | Axisflying KOLAS7 (AF2c) | Lumenier NAV 10000mAh 6S 21700 Li-Ion | SBC3 | included | T13 | 1641.0 | 16.92 | 42.2 | 42.9 | 48.5 | 14.7 | 1538.99 | 1664.99 | ✅ | ✅ | — | ✅ |
| C000335 | DarwinFPV 129 7in (AF9a) | Upgrade Energy Dark Lithium V2 4S 8400mAh Molicel P42A | SBC3 | included | T13 | 1059.7 | 16.85 | 41.8 | 42.9 | 50.8 | 17.8 | 1308.97 | 1434.97 | ✅ | ✅ | — | ✅ |
| C000215 | iFlight Chimera9 ECO (AF3a) | iFlight Fullsend 6S 8000mAh EVE INR21700-40PL | SBC3 | included | T13 | 1666.7 | 16.8 | 41.7 | 42.9 | 51.7 | 14.2 | 1320.33 | 1446.33 | ✅ | ✅ | — | ✅ |
| C000217 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 12000mAh 6S 21700 XT90 | SBC3 | included | T13 | 2228.7 | 16.8 | 41.6 | 42.5 | 49.5 | 19.0 | 1387.33 | 1513.33 | ✅ | ✅ | — | ✅ |
| C000230 | iFlight Chimera9 ECO (AF3b) | iFlight Fullsend 6S 8000mAh EVE INR21700-40PL | SBC3 | included | T13 | 1672.0 | 16.87 | 41.5 | 42.7 | 51.4 | 14.3 | 1346.98 | 1472.98 | ✅ | ✅ | — | ✅ |
| C000261 | DeepSpace ROC7 O4 PRO (AF6a) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1385.7 | 16.85 | 41.5 | 42.4 | 48.9 | 17.3 | 1879.98 | 2005.98 | ✅ | ✅ | — | ✅ |
| C000232 | iFlight Chimera9 ECO (AF3b) | Lumenier NAV 12000mAh 6S 21700 XT90 | SBC3 | included | T13 | 2234.0 | 16.87 | 41.4 | 42.3 | 49.3 | 19.0 | 1413.98 | 1539.98 | ✅ | ✅ | — | ✅ |
| C000276 | DeepSpace ROC7 O4 PRO (AF6b) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1390.0 | 16.92 | 41.4 | 42.2 | 48.7 | 17.4 | 1890.99 | 2016.99 | ✅ | ✅ | — | ✅ |
| C000302 | iFlight Chimera7 Pro V2 (AF8a) | Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1706.7 | 16.85 | 41.4 | 42.2 | 48.3 | 21.3 | 1569.97 | 1695.97 | ✅ | ✅ | — | ✅ |
| C000342 | NewBeeDrone ROC7 O4PRO (AF10) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1390.0 | 16.92 | 41.4 | 42.2 | 48.7 | 17.4 | 1838.99 | 1964.99 | ✅ | ✅ | — | ✅ |
| C000258 | DeepSpace ROC7 O4 PRO (AF6a) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1636.7 | 16.85 | 41.2 | 41.9 | 47.5 | 20.5 | 1937.98 | 2063.98 | ✅ | ✅ | — | ✅ |
| C000317 | iFlight Chimera7 Pro V2 (AF8b) | Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1712.0 | 16.92 | 41.2 | 42.0 | 48.1 | 21.4 | 1580.5 | 1706.5 | ✅ | ✅ | — | ✅ |
| C000168 | GEPRC MOZ7 V2 O4 Pro (AF1c) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1719.7 | 16.85 | 41.0 | 41.7 | 47.8 | 14.3 | 1786.98 | 1912.98 | ✅ | ✅ | — | ✅ |
| C000273 | DeepSpace ROC7 O4 PRO (AF6b) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1641.0 | 16.92 | 41.0 | 41.7 | 47.3 | 20.5 | 1948.99 | 2074.99 | ✅ | ✅ | — | ✅ |
| C000339 | NewBeeDrone ROC7 O4PRO (AF10) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1641.0 | 16.92 | 41.0 | 41.7 | 47.3 | 20.5 | 1896.99 | 2022.99 | ✅ | ✅ | — | ✅ |
| C000247 | DarwinFPV X9 (AF4a) | Lumenier NAV 12000mAh 6S 21700 XT90 | SBC3 | included | T13 | 2254.7 | 16.8 | 40.9 | 41.8 | 48.7 | 17.4 | 1522.97 | 1648.97 | ✅ | ✅ | — | ✅ |
| C000171 | GEPRC MOZ7 V2 O4 Pro (AF1c) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1468.7 | 16.85 | 40.8 | 41.7 | 48.5 | 12.2 | 1728.98 | 1854.98 | ✅ | ✅ | — | ✅ |
| C000245 | DarwinFPV X9 (AF4a) | iFlight Fullsend 6S 8000mAh EVE INR21700-40PL | SBC3 | included | T13 | 1692.7 | 16.8 | 40.8 | 41.9 | 50.6 | 13.0 | 1455.97 | 1581.97 | ✅ | ✅ | — | ✅ |
| C000043 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | V8 | T13 | 1742.5 | 15.4 | 40.4 | 41.2 | 47.1 | 14.5 | 1558.98 | 1684.98 | ✅ | ✅ | — | ✅ |
| C000040 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | V5 | T13 | 1747.7 | 15.4 | 40.3 | 41.0 | 46.9 | 14.6 | 1553.98 | 1679.98 | ✅ | ✅ | — | ✅ |
| C000044 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | V10 | T13 | 1745.3 | 15.9 | 40.3 | 41.0 | 46.9 | 14.5 | 1550.98 | 1676.98 | ✅ | ✅ | — | ✅ |
| C000073 | GEPRC MOZ7 V2 WTFPV (AF1b) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | V8 | T13 | 1491.5 | 15.4 | 40.3 | 41.1 | 47.8 | 12.4 | 1500.98 | 1626.98 | ✅ | ✅ | — | ✅ |
