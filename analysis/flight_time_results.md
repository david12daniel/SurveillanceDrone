# Flight-Time Analysis — Holistic Configuration Sweep

**Auto-generated** by [`flight_time_model.py`](flight_time_model.py). Regenerate with `python analysis/flight_time_model.py`.

Momentum-theory (actuator-disk) propulsion model + forward-flight parasitic drag. "Max flight time" = still-air hover endurance (R6 ≥ 30 min / R8 ≥ 60 min metric).

## Sweep scope

- **34 real configurations** = airframe × battery × VTX, fully crossed (respecting airframe component inclusion) and **filtered for interface compatibility**; thermal fixed to **T13** and SBC fixed to **SBC3** (design choices, not swept). The DVR is compatibility-gated, not crossed, and excluded from flight time (it is an earlier-stage part; the SBC records at the SBC stage).
- Flight-time drivers swept in full; sub-1 W peripherals held at lightest representatives: FPV `FpvCamBundled`, GPS `GpsBundled`, RX `RxBundled`.
- **Inclusion logic:** airframe-bundled VTX/FPV/GPS/RX contribute power only (their mass is already in the airframe's as-built weight); non-bundled peripherals contribute mass + power.
- Candidates: 22 airframes (with mass data), 23 real battery candidates, 65 swept payload components.
- **Cost (R4 ≤ $2,500):** each config's drone cost + a laptop-based GCS = control base **$131** (Phase-1/backup handheld radio + ELRS USB control dongle) **plus a ground video receiver matched to the airframe's VTX format** (CVBS Skydroid 150CH 5.8GHz True-Diversity UVC Receiver $44; DJI DJI Goggles N3 $230; WALKSNAIL Walksnail Avatar HD Goggles L $199). Analog frames use the cheap analog VRX; frames with a digital air unit (DJI/Walksnail) carry the matching goggles. Bundled VTX/FPV/GPS/RX add $0 (already in the airframe price); no DVR (the SBC records onboard).
- **Compatibility filtering** (declared in `DroneSystemModel::Architecture::Compatibility`): 46 raw pairings reduced to 34 real configs — pruned 12 on battery↔airframe cell-count (P1, e.g. a 4S pack on a 6S-only frame). The former V2 thermal↔DVR video-format filter is retired: the standalone DVR was removed from the architecture (the SBC records onboard).

## Model assumptions

- Rotors **4** · ρ **1.225 kg/m³** · FoM **0.65** · η **0.8** · C_d **1.0** · cruise **2.23 m/s** (R2) · wind **4.5 m/s** (R7)

> **Why cruise/wind endurance can exceed hover** — the multirotor *power bucket*: in slow forward flight the rotors gain translational lift, so induced power drops faster than parasitic drag rises. **Max FT** uses hover (conservative); *Cruise* (2.23 m/s) is the realistic still-air surveillance endurance; *Wind* is airspeed = cruise + 4.5 m/s (R7).

> **Caveats** — first-order comparative estimates (FoM, η, C_d, frontal area, thrust lookup are assumptions; battery mass derived from chemistry specific energy). Airframes missing mass/wheelbase are skipped (MODEL_ISSUES.md §D). Full per-instance data: [`flight_time_results.csv`](flight_time_results.csv).

## Recommended baseline

**iFlight Chimera9 ECO** (AF3a) + **Lumenier NAV 12000mAh 6S 21700 Amprius**, SBC SBC3, VTX included, thermal T13 → **58.7 min** hover (1744.0 g AUW, 14.9% throttle; drone $1533 / system $1709 ≤ $2,500 R4).

## Top 34 configurations (ranked by max flight time)

| Cfg | Airframe | Battery | SBC | VTX | Therm | AUW g | Pld W | Max FT | Cruise | Wind | Thr% | Drone $ | Sys $ | R4 | R6 | R8 | Fly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C000008 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1744.0 | 16.93 | 58.7 | 60.3 | 72.3 | 14.9 | 1533.48 | 1708.93 | ✅ | ✅ | — | ✅ |
| C000025 | DarwinFPV X9 (AF4a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | included | T13 | 1762.0 | 16.93 | 57.9 | 59.4 | 71.3 | 13.6 | 1459.48 | 1634.93 | ✅ | ✅ | — | ✅ |
| C000009 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1743.0 | 16.93 | 57.2 | 58.7 | 70.4 | 14.9 | 1486.99 | 1662.44 | ✅ | ✅ | — | ✅ |
| C000026 | DarwinFPV X9 (AF4a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC3 | included | T13 | 1761.0 | 16.93 | 56.4 | 57.9 | 69.5 | 13.6 | 1412.99 | 1588.44 | ✅ | ✅ | — | ✅ |
| C000003 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1692.0 | 16.93 | 49.6 | 51.0 | 61.4 | 14.4 | 1463.99 | 1639.44 | ✅ | ✅ | — | ✅ |
| C000006 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1441.0 | 16.93 | 49.5 | 51.1 | 62.6 | 12.3 | 1405.99 | 1581.44 | ✅ | ✅ | — | ✅ |
| C000020 | DarwinFPV X9 (AF4a) | Upgrade Energy RED V3 6S2P 10Ah Molicel P50B | SBC3 | included | T13 | 1710.0 | 16.93 | 48.9 | 50.3 | 60.6 | 13.2 | 1389.99 | 1565.44 | ✅ | ✅ | — | ✅ |
| C000023 | DarwinFPV X9 (AF4a) | Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10 | SBC3 | included | T13 | 1459.0 | 16.93 | 48.7 | 50.2 | 61.7 | 11.2 | 1331.99 | 1507.44 | ✅ | ✅ | — | ✅ |
| C000002 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1724.0 | 16.93 | 48.4 | 49.7 | 59.6 | 14.7 | 1481.98 | 1657.43 | ✅ | ✅ | — | ✅ |
| C000019 | DarwinFPV X9 (AF4a) | Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S | SBC3 | included | T13 | 1742.0 | 16.93 | 47.7 | 49.0 | 58.9 | 13.4 | 1407.98 | 1583.43 | ✅ | ✅ | — | ✅ |
| C000001 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 10000mAh 6S 21700 Li-Ion | SBC3 | included | T13 | 1799.0 | 16.93 | 46.9 | 48.1 | 57.4 | 15.3 | 1361.98 | 1537.43 | ✅ | ✅ | — | ✅ |
| C000018 | DarwinFPV X9 (AF4a) | Lumenier NAV 10000mAh 6S 21700 Li-Ion | SBC3 | included | T13 | 1817.0 | 16.93 | 46.2 | 47.4 | 56.7 | 14.0 | 1287.98 | 1463.43 | ✅ | ✅ | — | ✅ |
| C000016 | iFlight Chimera9 ECO (AF3a) | GNB (Gaoneng) 6S3P 12Ah 21700 Li-ion | SBC3 | included | T13 | 2074.0 | 16.93 | 46.0 | 47.1 | 55.3 | 17.7 | 1321.99 | 1497.44 | ✅ | ✅ | — | ✅ |
| C000033 | DarwinFPV X9 (AF4a) | GNB (Gaoneng) 6S3P 12Ah 21700 Li-ion | SBC3 | included | T13 | 2092.0 | 16.93 | 45.5 | 46.5 | 54.7 | 16.1 | 1247.99 | 1423.44 | ✅ | ✅ | — | ✅ |
| C000005 | iFlight Chimera9 ECO (AF3a) | iFlight Fullsend 6S 8000mAh EVE INR21700-40PL | SBC3 | included | T13 | 1664.0 | 16.93 | 41.8 | 42.9 | 51.8 | 14.2 | 1334.98 | 1510.43 | ✅ | ✅ | — | ✅ |
| C000007 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 12000mAh 6S 21700 XT90 | SBC3 | included | T13 | 2226.0 | 16.93 | 41.7 | 42.5 | 49.5 | 19.0 | 1401.98 | 1577.43 | ✅ | ✅ | — | ✅ |
| C000022 | DarwinFPV X9 (AF4a) | iFlight Fullsend 6S 8000mAh EVE INR21700-40PL | SBC3 | included | T13 | 1682.0 | 16.93 | 41.2 | 42.3 | 51.1 | 13.0 | 1260.98 | 1436.43 | ✅ | ✅ | — | ✅ |
| C000024 | DarwinFPV X9 (AF4a) | Lumenier NAV 12000mAh 6S 21700 XT90 | SBC3 | included | T13 | 2244.0 | 16.93 | 41.2 | 42.1 | 49.0 | 17.3 | 1327.98 | 1503.43 | ✅ | ✅ | — | ✅ |
| C000004 | iFlight Chimera9 ECO (AF3a) | GNB 8000mAh 6S2P Samsung 21700 40T | SBC3 | included | T13 | 1728.0 | 16.93 | 39.6 | 40.7 | 48.9 | 14.7 | 1347.98 | 1523.43 | ✅ | ✅ | — | ✅ |
| C000010 | iFlight Chimera9 ECO (AF3a) | Pyrodrone Hyperjuice 6S2P 6000mAh Sony VTC6 | SBC3 | included | T13 | 1414.0 | 16.93 | 39.2 | 40.4 | 49.6 | 12.1 | 1384.98 | 1560.43 | ✅ | ✅ | — | ✅ |
| C000021 | DarwinFPV X9 (AF4a) | GNB 8000mAh 6S2P Samsung 21700 40T | SBC3 | included | T13 | 1746.0 | 16.93 | 39.1 | 40.1 | 48.2 | 13.5 | 1273.98 | 1449.43 | ✅ | ✅ | — | ✅ |
| C000011 | iFlight Chimera9 ECO (AF3a) | iFlight Fullsend 6S2P 6000mAh Samsung 30Q | SBC3 | included | T13 | 1432.0 | 16.93 | 38.5 | 39.7 | 48.7 | 12.2 | 1296.46 | 1471.91 | ✅ | ✅ | — | ✅ |
| C000027 | DarwinFPV X9 (AF4a) | Pyrodrone Hyperjuice 6S2P 6000mAh Sony VTC6 | SBC3 | included | T13 | 1432.0 | 16.93 | 38.5 | 39.7 | 48.9 | 11.0 | 1310.98 | 1486.43 | ✅ | ✅ | — | ✅ |
| C000017 | iFlight Chimera9 ECO (AF3a) | Tattu G-Tech 6S 12Ah LiPo 30C | SBC3 | included | T13 | 2356.0 | 16.93 | 38.4 | 39.2 | 45.3 | 20.1 | 1361.98 | 1537.43 | ✅ | ✅ | — | ✅ |
| C000034 | DarwinFPV X9 (AF4a) | Tattu G-Tech 6S 12Ah LiPo 30C | SBC3 | included | T13 | 2374.0 | 16.93 | 38.0 | 38.8 | 44.9 | 18.3 | 1287.98 | 1463.43 | ✅ | ✅ | — | ✅ |
| C000028 | DarwinFPV X9 (AF4a) | iFlight Fullsend 6S2P 6000mAh Samsung 30Q | SBC3 | included | T13 | 1450.0 | 16.93 | 37.8 | 39.0 | 48.0 | 11.2 | 1222.46 | 1397.91 | ✅ | ✅ | — | ✅ |
| C000015 | iFlight Chimera9 ECO (AF3a) | DOGCOM 6S1P 5000mAh Samsung 50S | SBC3 | included | T13 | 1269.0 | 16.93 | 37.7 | 39.0 | 48.5 | 10.8 | 1261.99 | 1437.44 | ✅ | ✅ | — | ✅ |
| C000012 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 6000mAh 6S 18650 | SBC3 | included | T13 | 1459.0 | 16.93 | 37.5 | 38.7 | 47.4 | 12.4 | 1400.98 | 1576.43 | ✅ | ✅ | — | ✅ |
| C000014 | iFlight Chimera9 ECO (AF3a) | Upgrade Energy RED V3 6S1P 5Ah Molicel P50B | SBC3 | included | T13 | 1256.0 | 16.93 | 37.2 | 38.5 | 47.9 | 10.7 | 1330.99 | 1506.44 | ✅ | ✅ | — | ✅ |
| C000032 | DarwinFPV X9 (AF4a) | DOGCOM 6S1P 5000mAh Samsung 50S | SBC3 | included | T13 | 1287.0 | 16.93 | 37.0 | 38.3 | 47.8 | 9.9 | 1187.99 | 1363.44 | ✅ | ✅ | — | ✅ |
| C000029 | DarwinFPV X9 (AF4a) | Lumenier NAV 6000mAh 6S 18650 | SBC3 | included | T13 | 1477.0 | 16.93 | 36.9 | 38.0 | 46.7 | 11.4 | 1326.98 | 1502.43 | ✅ | ✅ | — | ✅ |
| C000031 | DarwinFPV X9 (AF4a) | Upgrade Energy RED V3 6S1P 5Ah Molicel P50B | SBC3 | included | T13 | 1274.0 | 16.93 | 36.5 | 37.8 | 47.2 | 9.8 | 1256.99 | 1432.44 | ✅ | ✅ | — | ✅ |
| C000013 | iFlight Chimera9 ECO (AF3a) | Lumenier NAV 5000mAh 6S 21700 | SBC3 | included | T13 | 1323.0 | 16.93 | 35.7 | 36.9 | 45.7 | 11.3 | 1307.98 | 1483.43 | ✅ | ✅ | — | ✅ |
| C000030 | DarwinFPV X9 (AF4a) | Lumenier NAV 5000mAh 6S 21700 | SBC3 | included | T13 | 1341.0 | 16.93 | 35.0 | 36.2 | 44.9 | 10.3 | 1233.98 | 1409.43 | ✅ | ✅ | — | ✅ |
