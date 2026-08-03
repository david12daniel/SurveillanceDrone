# Flight-Time Analysis — Holistic Configuration Sweep

**Auto-generated** by [`flight_time_model.py`](flight_time_model.py). Regenerate with `python analysis/flight_time_model.py`.

Momentum-theory (actuator-disk) propulsion model + forward-flight parasitic drag. "Max flight time" = still-air hover endurance (R6 ≥ 30 min / R8 ≥ 60 min metric).

## Sweep scope

- **34 real configurations** = airframe × battery × VTX, fully crossed (respecting airframe component inclusion) and **filtered for interface compatibility**; thermal fixed to **T13** and SBC fixed to **SBC3** (design choices, not swept). The DVR is compatibility-gated, not crossed, and excluded from flight time (it is an earlier-stage part; the SBC records at the SBC stage).
- Flight-time drivers swept in full; sub-1 W peripherals held at lightest representatives: FPV `A7`, GPS `G6`, RX `GEPRCNanoPA100`.
- **Inclusion logic:** airframe-bundled VTX/FPV/GPS/RX contribute power only (their mass is already in the airframe's as-built weight); non-bundled peripherals contribute mass + power.
- Candidates: 22 airframes (with mass data), 23 real battery candidates, 61 swept payload components.
- **Cost (R4 ≤ $2,500):** each config's drone cost + a laptop-based GCS = control base **$131** (Phase-1/backup handheld radio + ELRS USB control dongle) **plus a ground video receiver matched to the airframe's VTX format** (CVBS Skydroid 150CH 5.8GHz True-Diversity UVC Receiver $44; DJI DJI Goggles N3 $230; WALKSNAIL Walksnail Avatar HD Goggles L $199). Analog frames use the cheap analog VRX; frames with a digital air unit (DJI/Walksnail) carry the matching goggles. Bundled VTX/FPV/GPS/RX add $0 (already in the airframe price); no DVR (the SBC records onboard).
- **Compatibility filtering** (declared in `DroneSystemModel::Architecture::Compatibility`): 46 raw pairings reduced to 34 real configs — pruned 12 on battery↔airframe cell-count (P1, e.g. a 4S pack on a 6S-only frame). The former V2 thermal↔DVR video-format filter is retired: the standalone DVR was removed from the architecture (the SBC records onboard).

## Model assumptions

- Rotors **4** · ρ **1.225 kg/m³** · FoM **0.65** · η **0.8** · C_d **1.0** · cruise **2.23 m/s** (R2) · wind **4.5 m/s** (R7)

> **Why cruise/wind endurance can exceed hover** — the multirotor *power bucket*: in slow forward flight the rotors gain translational lift, so induced power drops faster than parasitic drag rises. **Max FT** uses hover (conservative); *Cruise* (2.23 m/s) is the realistic still-air surveillance endurance; *Wind* is airspeed = cruise + 4.5 m/s (R7).

> **Caveats** — first-order comparative estimates (FoM, η, C_d, frontal area, thrust lookup are assumptions; battery mass derived from chemistry specific energy). Airframes missing mass/wheelbase are skipped (MODEL_ISSUES.md §D). Full per-instance data: [`flight_time_results.csv`](flight_time_results.csv).

## Recommended baseline

**iFlight Chimera9 ECO** (AF3a) + **Lumenier NAV 12000mAh 6S 21700 Amprius**, SBC SBC3, VTX included, thermal T13 → **58.4 min** hover (1750.7 g AUW, 14.9% throttle; drone $1548 / system $1724 ≤ $2,500 R4).

## Top 34 configurations (ranked by max flight time)

| Cfg | Airframe | Battery | SBC | VTX | Therm | AUW g | Pld W | Max FT | Cruise | Wind | Thr% | Drone $ | Sys $ | R4 | R6 | R8 | Fly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C000008 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1750.7 | 16.85 | 58.4 | 60.0 | 71.9 | 14.9 | 1548.47 | 1723.92 | ✅ | ✅ | — | ✅ |
| C000025 | DarwinFPV X9 (AF4a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1772.7 | 16.8 | 57.4 | 58.9 | 70.7 | 13.7 | 1506.47 | 1681.92 | ✅ | ✅ | — | ✅ |
| C000009 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1749.7 | 16.85 | 56.9 | 58.4 | 70.0 | 14.9 | 1501.98 | 1677.43 | ✅ | ✅ | — | ✅ |
| C000026 | DarwinFPV X9 (AF4a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1771.7 | 16.8 | 55.9 | 57.4 | 68.9 | 13.6 | 1459.98 | 1635.43 | ✅ | ✅ | — | ✅ |
| C000003 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1698.7 | 16.85 | 49.4 | 50.7 | 61.0 | 14.5 | 1478.98 | 1654.43 | ✅ | ✅ | — | ✅ |
| C000006 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1447.7 | 16.85 | 49.2 | 50.8 | 62.2 | 12.3 | 1420.98 | 1596.43 | ✅ | ✅ | — | ✅ |
| C000020 | DarwinFPV X9 (AF4a) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1720.7 | 16.8 | 48.5 | 49.8 | 60.0 | 13.3 | 1436.98 | 1612.43 | ✅ | ✅ | — | ✅ |
| C000023 | DarwinFPV X9 (AF4a) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1469.7 | 16.8 | 48.2 | 49.7 | 61.1 | 11.3 | 1378.98 | 1554.43 | ✅ | ✅ | — | ✅ |
| C000002 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1730.7 | 16.85 | 48.1 | 49.4 | 59.3 | 14.8 | 1496.97 | 1672.42 | ✅ | ✅ | — | ✅ |
| C000019 | DarwinFPV X9 (AF4a) | Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1752.7 | 16.8 | 47.3 | 48.6 | 58.4 | 13.5 | 1454.97 | 1630.42 | ✅ | ✅ | — | ✅ |
| C000001 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 10000mAh 6S 21700 Li-Ion | SBC3 | included | T13 | 1805.7 | 16.85 | 46.6 | 47.8 | 57.1 | 15.4 | 1376.97 | 1552.42 | ✅ | ✅ | — | ✅ |
| C000018 | DarwinFPV X9 (AF4a) | Lumenier NAV 10000mAh 6S 21700 Li-Ion | SBC3 | included | T13 | 1827.7 | 16.8 | 45.9 | 47.0 | 56.2 | 14.1 | 1334.97 | 1510.42 | ✅ | ✅ | — | ✅ |
| C000016 | iFlight Chimera9 ECO (AF3a) | GNB (Gaoneng) 6S3P 12Ah 21700 Li-ion | SBC3 | included | T13 | 2080.7 | 16.85 | 45.8 | 46.9 | 55.0 | 17.7 | 1336.98 | 1512.43 | ✅ | ✅ | — | ✅ |
| C000033 | DarwinFPV X9 (AF4a) | GNB (Gaoneng) 6S3P 12Ah 21700 Li-ion | SBC3 | included | T13 | 2102.7 | 16.8 | 45.2 | 46.2 | 54.3 | 16.2 | 1294.98 | 1470.43 | ✅ | ✅ | — | ✅ |
| C000005 | iFlight Chimera9 ECO (AF3a) | iFlight Fullsend 6S 8000mAh EVE INR21700-40PL | SBC3 | included | T13 | 1670.7 | 16.85 | 41.6 | 42.7 | 51.5 | 14.2 | 1349.97 | 1525.42 | ✅ | ✅ | — | ✅ |
| C000007 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 12000mAh 6S 21700 XT90 | SBC3 | included | T13 | 2232.7 | 16.85 | 41.5 | 42.4 | 49.3 | 19.0 | 1416.97 | 1592.42 | ✅ | ✅ | — | ✅ |
| C000024 | DarwinFPV X9 (AF4a) | Lumenier NAV 12000mAh 6S 21700 XT90 | SBC3 | included | T13 | 2254.7 | 16.8 | 40.9 | 41.8 | 48.7 | 17.4 | 1374.97 | 1550.42 | ✅ | ✅ | — | ✅ |
| C000022 | DarwinFPV X9 (AF4a) | iFlight Fullsend 6S 8000mAh EVE INR21700-40PL | SBC3 | included | T13 | 1692.7 | 16.8 | 40.8 | 41.9 | 50.6 | 13.0 | 1307.97 | 1483.42 | ✅ | ✅ | — | ✅ |
| C000004 | iFlight Chimera9 ECO (AF3a) | GNB 8000mAh 6S2P Samsung 21700 40T | SBC3 | included | T13 | 1734.7 | 16.85 | 39.4 | 40.5 | 48.6 | 14.8 | 1362.97 | 1538.42 | ✅ | ✅ | — | ✅ |
| C000010 | iFlight Chimera9 ECO (AF3a) | Pyrodrone Hyperjuice 6S2P 6000mAh Sony VTC6 | SBC3 | included | T13 | 1420.7 | 16.85 | 38.9 | 40.2 | 49.3 | 12.1 | 1399.97 | 1575.42 | ✅ | ✅ | — | ✅ |
| C000021 | DarwinFPV X9 (AF4a) | GNB 8000mAh 6S2P Samsung 21700 40T | SBC3 | included | T13 | 1756.7 | 16.8 | 38.8 | 39.8 | 47.8 | 13.5 | 1320.97 | 1496.42 | ✅ | ✅ | — | ✅ |
| C000011 | iFlight Chimera9 ECO (AF3a) | iFlight Fullsend 6S2P 6000mAh Samsung 30Q | SBC3 | included | T13 | 1438.7 | 16.85 | 38.3 | 39.5 | 48.4 | 12.3 | 1311.45 | 1486.9 | ✅ | ✅ | — | ✅ |
| C000017 | iFlight Chimera9 ECO (AF3a) | Tattu G-Tech 6S 12Ah LiPo 30C | SBC3 | included | T13 | 2362.7 | 16.85 | 38.3 | 39.0 | 45.2 | 20.1 | 1376.97 | 1552.42 | ✅ | ✅ | — | ✅ |
| C000027 | DarwinFPV X9 (AF4a) | Pyrodrone Hyperjuice 6S2P 6000mAh Sony VTC6 | SBC3 | included | T13 | 1442.7 | 16.8 | 38.1 | 39.3 | 48.4 | 11.1 | 1357.97 | 1533.42 | ✅ | ✅ | — | ✅ |
| C000034 | DarwinFPV X9 (AF4a) | Tattu G-Tech 6S 12Ah LiPo 30C | SBC3 | included | T13 | 2384.7 | 16.8 | 37.8 | 38.5 | 44.6 | 18.4 | 1334.97 | 1510.42 | ✅ | ✅ | — | ✅ |
| C000015 | iFlight Chimera9 ECO (AF3a) | DOGCOM 6S1P 5000mAh Samsung 50S | SBC3 | included | T13 | 1275.7 | 16.85 | 37.5 | 38.8 | 48.2 | 10.9 | 1276.98 | 1452.43 | ✅ | ✅ | — | ✅ |
| C000028 | DarwinFPV X9 (AF4a) | iFlight Fullsend 6S2P 6000mAh Samsung 30Q | SBC3 | included | T13 | 1460.7 | 16.8 | 37.5 | 38.7 | 47.5 | 11.3 | 1269.45 | 1444.9 | ✅ | ✅ | — | ✅ |
| C000012 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 6000mAh 6S 18650 | SBC3 | included | T13 | 1465.7 | 16.85 | 37.3 | 38.5 | 47.1 | 12.5 | 1415.97 | 1591.42 | ✅ | ✅ | — | ✅ |
| C000014 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy RED V3 6S1P 5Ah Molicel P50B | SBC3 | included | T13 | 1262.7 | 16.85 | 37.0 | 38.3 | 47.6 | 10.8 | 1345.98 | 1521.43 | ✅ | ✅ | — | ✅ |
| C000032 | DarwinFPV X9 (AF4a) | DOGCOM 6S1P 5000mAh Samsung 50S | SBC3 | included | T13 | 1297.7 | 16.8 | 36.7 | 37.9 | 47.2 | 10.0 | 1234.98 | 1410.43 | ✅ | ✅ | — | ✅ |
| C000029 | DarwinFPV X9 (AF4a) | Lumenier NAV 6000mAh 6S 18650 | SBC3 | included | T13 | 1487.7 | 16.8 | 36.6 | 37.7 | 46.2 | 11.5 | 1373.97 | 1549.42 | ✅ | ✅ | — | ✅ |
| C000031 | DarwinFPV X9 (AF4a) | Upgrade Energy RED V3 6S1P 5Ah Molicel P50B | SBC3 | included | T13 | 1284.7 | 16.8 | 36.1 | 37.4 | 46.6 | 9.9 | 1303.98 | 1479.43 | ✅ | ✅ | — | ✅ |
| C000013 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 5000mAh 6S 21700 | SBC3 | included | T13 | 1329.7 | 16.85 | 35.5 | 36.7 | 45.3 | 11.3 | 1322.97 | 1498.42 | ✅ | ✅ | — | ✅ |
| C000030 | DarwinFPV X9 (AF4a) | Lumenier NAV 5000mAh 6S 21700 | SBC3 | included | T13 | 1351.7 | 16.8 | 34.7 | 35.9 | 44.5 | 10.4 | 1280.97 | 1456.42 | ✅ | ✅ | — | ✅ |
