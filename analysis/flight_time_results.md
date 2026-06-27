# Flight-Time Analysis — Holistic Configuration Sweep

**Auto-generated** by [`flight_time_model.py`](flight_time_model.py). Regenerate with `python analysis/flight_time_model.py`.

Momentum-theory (actuator-disk) propulsion model + forward-flight parasitic drag. "Max flight time" = still-air hover endurance (R6 ≥ 30 min / R8 ≥ 60 min metric).

## Sweep scope

- **14,112 real configurations** = airframe × battery × SBC × VTX × thermal camera, fully crossed (respecting airframe component inclusion) and **filtered for interface compatibility**. The DVR is compatibility-gated, not crossed, and excluded from flight time (it is an earlier-stage part; the SBC records at the SBC stage).
- Flight-time drivers swept in full; sub-1 W peripherals held at lightest representatives: FPV `A7`, GPS `G6`, RX `GEPRCNanoPA100`.
- **Inclusion logic:** airframe-bundled VTX/FPV/GPS/RX contribute power only (their mass is already in the airframe's as-built weight); non-bundled peripherals contribute mass + power.
- Candidates: 14 airframes (with mass data), 21 real battery candidates, 70 swept payload components.
- **Cost (R4 ≤ $2,500):** each config's drone cost + a fixed laptop-based GCS (ELRS USB dongle + analog VRX/capture + a Phase-1/backup handheld radio = $126; the laptop is the ground station); bundled VTX/FPV/GPS/RX add $0 (already in the airframe price); the DVR is included (earlier-stage part).
- **Compatibility filtering** (declared in `DroneSystemModel::Architecture::Compatibility`): 23,184 raw pairings reduced to 14,112 real configs — pruned 7,056 on battery↔airframe cell-count (P1, e.g. a 4S pack on a 6S-only frame) and 2,016 on thermal↔DVR video format (V2, a thermal whose output no DVR can record — CVBS via DVR1-6 or digital HDMI/USB via DVR7-9).

## Model assumptions

- Rotors **4** · ρ **1.225 kg/m³** · FoM **0.65** · η **0.8** · C_d **1.0** · cruise **2.23 m/s** (R2) · wind **4.5 m/s** (R7)

> **Why cruise/wind endurance can exceed hover** — the multirotor *power bucket*: in slow forward flight the rotors gain translational lift, so induced power drops faster than parasitic drag rises. **Max FT** uses hover (conservative); *Cruise* (2.23 m/s) is the realistic still-air surveillance endurance; *Wind* is airspeed = cruise + 4.5 m/s (R7).

> **Caveats** — first-order comparative estimates (FoM, η, C_d, frontal area, thrust lookup are assumptions; battery mass derived from chemistry specific energy). Airframes missing mass/wheelbase are skipped (MODEL_ISSUES.md §D). Full per-instance data: [`flight_time_results.csv`](flight_time_results.csv).

## Recommended baseline

**Axisflying KOLAS7** (AF2a) + **Lumenier NAV 12000mAh 6S 21700 Amprius**, SBC SBC1, VTX V8, thermal T1 → **74.6 min** hover (1250.4 g AUW, 11.2% throttle; drone $946 / system $1072 ≤ $2,500 R4).

## Top 100 configurations (ranked by max flight time)

| Cfg | Airframe | Battery | SBC | VTX | Therm | AUW g | Pld W | Max FT | Cruise | Wind | Thr% | Drone $ | Sys $ | R4 | R6 | R8 | Fly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C003578 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T1 | 1250.4 | 14.7 | 74.6 | 76.3 | 88.8 | 11.2 | 946.48 | 1072.48 | ✅ | ✅ | ✅ | ✅ |
| C003608 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T2 | 1250.4 | 14.7 | 74.6 | 76.3 | 88.8 | 11.2 | 987.48 | 1113.48 | ✅ | ✅ | ✅ | ✅ |
| C003638 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T3 | 1250.4 | 14.7 | 74.6 | 76.3 | 88.8 | 11.2 | 1001.48 | 1127.48 | ✅ | ✅ | ✅ | ✅ |
| C003668 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T4 | 1251.8 | 15.0 | 74.4 | 76.0 | 88.5 | 11.2 | 899.47 | 1025.47 | ✅ | ✅ | ✅ | ✅ |
| C003575 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V5 | T1 | 1255.6 | 14.7 | 74.2 | 75.8 | 88.3 | 11.2 | 941.48 | 1067.48 | ✅ | ✅ | ✅ | ✅ |
| C003579 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V10 | T1 | 1253.2 | 15.2 | 74.2 | 75.8 | 88.2 | 11.2 | 938.48 | 1064.48 | ✅ | ✅ | ✅ | ✅ |
| C003605 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V5 | T2 | 1255.6 | 14.7 | 74.2 | 75.8 | 88.3 | 11.2 | 982.48 | 1108.48 | ✅ | ✅ | ✅ | ✅ |
| C003609 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V10 | T2 | 1253.2 | 15.2 | 74.2 | 75.8 | 88.2 | 11.2 | 979.48 | 1105.48 | ✅ | ✅ | ✅ | ✅ |
| C003635 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V5 | T3 | 1255.6 | 14.7 | 74.2 | 75.8 | 88.3 | 11.2 | 996.48 | 1122.48 | ✅ | ✅ | ✅ | ✅ |
| C003639 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V10 | T3 | 1253.2 | 15.2 | 74.2 | 75.8 | 88.2 | 11.2 | 993.48 | 1119.48 | ✅ | ✅ | ✅ | ✅ |
| C003577 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V7 | T1 | 1256.6 | 15.2 | 73.9 | 75.5 | 87.9 | 11.2 | 959.48 | 1085.48 | ✅ | ✅ | ✅ | ✅ |
| C003607 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V7 | T2 | 1256.6 | 15.2 | 73.9 | 75.5 | 87.9 | 11.2 | 1000.48 | 1126.48 | ✅ | ✅ | ✅ | ✅ |
| C003637 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V7 | T3 | 1256.6 | 15.2 | 73.9 | 75.5 | 87.9 | 11.2 | 1014.48 | 1140.48 | ✅ | ✅ | ✅ | ✅ |
| C003665 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V5 | T4 | 1257.0 | 15.0 | 73.9 | 75.6 | 88.0 | 11.2 | 894.47 | 1020.47 | ✅ | ✅ | ✅ | ✅ |
| C003669 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V10 | T4 | 1254.6 | 15.5 | 73.9 | 75.6 | 87.9 | 11.2 | 891.47 | 1017.47 | ✅ | ✅ | ✅ | ✅ |
| C003667 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V7 | T4 | 1258.0 | 15.5 | 73.7 | 75.3 | 87.6 | 11.2 | 912.47 | 1038.47 | ✅ | ✅ | ✅ | ✅ |
| C003573 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V3 | T1 | 1259.6 | 15.7 | 73.5 | 75.1 | 87.3 | 11.2 | 936.48 | 1062.48 | ✅ | ✅ | ✅ | ✅ |
| C003603 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V3 | T2 | 1259.6 | 15.7 | 73.5 | 75.1 | 87.3 | 11.2 | 977.48 | 1103.48 | ✅ | ✅ | ✅ | ✅ |
| C003633 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V3 | T3 | 1259.6 | 15.7 | 73.5 | 75.1 | 87.3 | 11.2 | 991.48 | 1117.48 | ✅ | ✅ | ✅ | ✅ |
| C013231 | DarwinFPV 129 7in (AF9a) | Lumenier NAV 12000mAh 4S 21700 Amprius | SBC1 | included | T1 | 927.6 | 16.2 | 73.5 | 75.6 | 90.7 | 15.6 | 884.97 | 1010.97 | ✅ | ✅ | ✅ | ✅ |
| C013234 | DarwinFPV 129 7in (AF9a) | Lumenier NAV 12000mAh 4S 21700 Amprius | SBC1 | included | T2 | 927.6 | 16.2 | 73.5 | 75.6 | 90.7 | 15.6 | 925.97 | 1051.97 | ✅ | ✅ | ✅ | ✅ |
| C013237 | DarwinFPV 129 7in (AF9a) | Lumenier NAV 12000mAh 4S 21700 Amprius | SBC1 | included | T3 | 927.6 | 16.2 | 73.5 | 75.6 | 90.7 | 15.6 | 939.97 | 1065.97 | ✅ | ✅ | ✅ | ✅ |
| C003728 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T6 | 1264.5 | 14.85 | 73.4 | 75.0 | 87.3 | 11.3 | 922.48 | 1048.48 | ✅ | ✅ | ✅ | ✅ |
| C003571 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V1 | T1 | 1262.5 | 15.7 | 73.2 | 74.8 | 87.0 | 11.3 | 941.48 | 1067.48 | ✅ | ✅ | ✅ | ✅ |
| C003601 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V1 | T2 | 1262.5 | 15.7 | 73.2 | 74.8 | 87.0 | 11.3 | 982.48 | 1108.48 | ✅ | ✅ | ✅ | ✅ |
| C003631 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V1 | T3 | 1262.5 | 15.7 | 73.2 | 74.8 | 87.0 | 11.3 | 996.48 | 1122.48 | ✅ | ✅ | ✅ | ✅ |
| C003663 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V3 | T4 | 1261.0 | 16.0 | 73.2 | 74.8 | 87.0 | 11.3 | 889.47 | 1015.47 | ✅ | ✅ | ✅ | ✅ |
| C003698 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T5 | 1264.5 | 15.35 | 73.2 | 74.8 | 87.0 | 11.3 | 976.47 | 1102.47 | ✅ | ✅ | ✅ | ✅ |
| C013240 | DarwinFPV 129 7in (AF9a) | Lumenier NAV 12000mAh 4S 21700 Amprius | SBC1 | included | T4 | 929.0 | 16.5 | 73.2 | 75.3 | 90.2 | 15.6 | 837.96 | 963.96 | ✅ | ✅ | ✅ | ✅ |
| C003661 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V1 | T4 | 1263.9 | 16.0 | 73.0 | 74.6 | 86.7 | 11.3 | 894.47 | 1020.47 | ✅ | ✅ | ✅ | ✅ |
| C003725 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V5 | T6 | 1269.7 | 14.85 | 73.0 | 74.6 | 86.7 | 11.3 | 917.48 | 1043.48 | ✅ | ✅ | ✅ | ✅ |
| C003729 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V10 | T6 | 1267.3 | 15.35 | 73.0 | 74.6 | 86.7 | 11.3 | 914.48 | 1040.48 | ✅ | ✅ | ✅ | ✅ |
| C003598 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V8 | T1 | 1271.4 | 14.7 | 72.9 | 74.5 | 86.6 | 11.4 | 959.48 | 1085.48 | ✅ | ✅ | ✅ | ✅ |
| C003628 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V8 | T2 | 1271.4 | 14.7 | 72.9 | 74.5 | 86.6 | 11.4 | 1000.48 | 1126.48 | ✅ | ✅ | ✅ | ✅ |
| C003658 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V8 | T3 | 1271.4 | 14.7 | 72.9 | 74.5 | 86.6 | 11.4 | 1014.48 | 1140.48 | ✅ | ✅ | ✅ | ✅ |
| C003695 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V5 | T5 | 1269.7 | 15.35 | 72.8 | 74.4 | 86.4 | 11.3 | 971.47 | 1097.47 | ✅ | ✅ | ✅ | ✅ |
| C003699 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V10 | T5 | 1267.3 | 15.85 | 72.8 | 74.4 | 86.4 | 11.3 | 968.47 | 1094.47 | ✅ | ✅ | ✅ | ✅ |
| C003758 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T8 | 1270.5 | 15.25 | 72.8 | 74.4 | 86.4 | 11.3 | 876.47 | 1002.47 | ✅ | ✅ | ✅ | ✅ |
| C003788 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T9 | 1270.5 | 15.25 | 72.8 | 74.4 | 86.4 | 11.3 | 1046.47 | 1172.47 | ✅ | ✅ | ✅ | ✅ |
| C003688 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V8 | T4 | 1272.8 | 15.0 | 72.7 | 74.3 | 86.3 | 11.4 | 912.47 | 1038.47 | ✅ | ✅ | ✅ | ✅ |
| C003727 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V7 | T6 | 1270.7 | 15.35 | 72.7 | 74.3 | 86.3 | 11.3 | 935.48 | 1061.48 | ✅ | ✅ | ✅ | ✅ |
| C003818 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T10 | 1270.5 | 15.3 | 72.7 | 74.3 | 86.4 | 11.3 | 1276.47 | 1402.47 | ✅ | ✅ | ✅ | ✅ |
| C003878 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T12 | 1270.5 | 15.3 | 72.7 | 74.3 | 86.4 | 11.3 | 1246.47 | 1372.47 | ✅ | ✅ | ✅ | ✅ |
| C003908 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T13 | 1270.5 | 15.35 | 72.7 | 74.3 | 86.4 | 11.3 | 1176.47 | 1302.47 | ✅ | ✅ | ✅ | ✅ |
| C003998 | Axisflying KOLAS7 (AF2a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC1 | V8 | T1 | 1249.4 | 14.7 | 72.7 | 74.3 | 86.5 | 11.2 | 899.99 | 1025.99 | ✅ | ✅ | ✅ | ✅ |
| C004028 | Axisflying KOLAS7 (AF2a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC1 | V8 | T2 | 1249.4 | 14.7 | 72.7 | 74.3 | 86.5 | 11.2 | 940.99 | 1066.99 | ✅ | ✅ | ✅ | ✅ |
| C004058 | Axisflying KOLAS7 (AF2a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC1 | V8 | T3 | 1249.4 | 14.7 | 72.7 | 74.3 | 86.5 | 11.2 | 954.99 | 1080.99 | ✅ | ✅ | ✅ | ✅ |
| C003576 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V6 | T1 | 1258.6 | 18.2 | 72.6 | 74.1 | 86.0 | 11.2 | 978.48 | 1104.48 | ✅ | ✅ | ✅ | ✅ |
| C003606 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V6 | T2 | 1258.6 | 18.2 | 72.6 | 74.1 | 86.0 | 11.2 | 1019.48 | 1145.48 | ✅ | ✅ | ✅ | ✅ |
| C003636 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V6 | T3 | 1258.6 | 18.2 | 72.6 | 74.1 | 86.0 | 11.2 | 1033.48 | 1159.48 | ✅ | ✅ | ✅ | ✅ |
| C003595 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V5 | T1 | 1276.6 | 14.7 | 72.5 | 74.1 | 86.1 | 11.4 | 954.48 | 1080.48 | ✅ | ✅ | ✅ | ✅ |
| C003599 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V10 | T1 | 1274.2 | 15.2 | 72.5 | 74.1 | 86.1 | 11.4 | 951.48 | 1077.48 | ✅ | ✅ | ✅ | ✅ |
| C003625 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V5 | T2 | 1276.6 | 14.7 | 72.5 | 74.1 | 86.1 | 11.4 | 995.48 | 1121.48 | ✅ | ✅ | ✅ | ✅ |
| C003629 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V10 | T2 | 1274.2 | 15.2 | 72.5 | 74.1 | 86.1 | 11.4 | 992.48 | 1118.48 | ✅ | ✅ | ✅ | ✅ |
| C003655 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V5 | T3 | 1276.6 | 14.7 | 72.5 | 74.1 | 86.1 | 11.4 | 1009.48 | 1135.48 | ✅ | ✅ | ✅ | ✅ |
| C003659 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V10 | T3 | 1274.2 | 15.2 | 72.5 | 74.1 | 86.1 | 11.4 | 1006.48 | 1132.48 | ✅ | ✅ | ✅ | ✅ |
| C003697 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V7 | T5 | 1270.7 | 15.85 | 72.5 | 74.1 | 86.1 | 11.3 | 989.47 | 1115.47 | ✅ | ✅ | ✅ | ✅ |
| C003755 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V5 | T8 | 1275.7 | 15.25 | 72.4 | 73.9 | 85.9 | 11.4 | 871.47 | 997.47 | ✅ | ✅ | ✅ | ✅ |
| C003759 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V10 | T8 | 1273.3 | 15.75 | 72.4 | 73.9 | 85.9 | 11.4 | 868.47 | 994.47 | ✅ | ✅ | ✅ | ✅ |
| C003785 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V5 | T9 | 1275.7 | 15.25 | 72.4 | 73.9 | 85.9 | 11.4 | 1041.47 | 1167.47 | ✅ | ✅ | ✅ | ✅ |
| C003789 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V10 | T9 | 1273.3 | 15.75 | 72.4 | 73.9 | 85.9 | 11.4 | 1038.47 | 1164.47 | ✅ | ✅ | ✅ | ✅ |
| C004088 | Axisflying KOLAS7 (AF2a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC1 | V8 | T4 | 1250.8 | 15.0 | 72.4 | 74.0 | 86.2 | 11.2 | 852.98 | 978.98 | ✅ | ✅ | ✅ | ✅ |
| C003588 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC2 | V8 | T1 | 1269.4 | 16.7 | 72.3 | 73.9 | 85.7 | 11.3 | 983.48 | 1109.48 | ✅ | ✅ | ✅ | ✅ |
| C003618 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC2 | V8 | T2 | 1269.4 | 16.7 | 72.3 | 73.9 | 85.7 | 11.3 | 1024.48 | 1150.48 | ✅ | ✅ | ✅ | ✅ |
| C003648 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC2 | V8 | T3 | 1269.4 | 16.7 | 72.3 | 73.9 | 85.7 | 11.3 | 1038.48 | 1164.48 | ✅ | ✅ | ✅ | ✅ |
| C003666 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V6 | T4 | 1260.0 | 18.5 | 72.3 | 73.9 | 85.7 | 11.2 | 931.47 | 1057.47 | ✅ | ✅ | ✅ | ✅ |
| C003685 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V5 | T4 | 1278.0 | 15.0 | 72.3 | 73.8 | 85.8 | 11.4 | 907.47 | 1033.47 | ✅ | ✅ | ✅ | ✅ |
| C003689 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V10 | T4 | 1275.6 | 15.5 | 72.3 | 73.8 | 85.8 | 11.4 | 904.47 | 1030.47 | ✅ | ✅ | ✅ | ✅ |
| C003723 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V3 | T6 | 1273.7 | 15.85 | 72.3 | 73.9 | 85.8 | 11.4 | 912.48 | 1038.48 | ✅ | ✅ | ✅ | ✅ |
| C003815 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V5 | T10 | 1275.7 | 15.3 | 72.3 | 73.9 | 85.9 | 11.4 | 1271.47 | 1397.47 | ✅ | ✅ | ✅ | ✅ |
| C003819 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V10 | T10 | 1273.3 | 15.8 | 72.3 | 73.9 | 85.8 | 11.4 | 1268.47 | 1394.47 | ✅ | ✅ | ✅ | ✅ |
| C003848 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T11 | 1274.5 | 15.55 | 72.3 | 73.9 | 85.9 | 11.4 | 1176.47 | 1302.47 | ✅ | ✅ | ✅ | ✅ |
| C003875 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V5 | T12 | 1275.7 | 15.3 | 72.3 | 73.9 | 85.9 | 11.4 | 1241.47 | 1367.47 | ✅ | ✅ | ✅ | ✅ |
| C003879 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V10 | T12 | 1273.3 | 15.8 | 72.3 | 73.9 | 85.8 | 11.4 | 1238.47 | 1364.47 | ✅ | ✅ | ✅ | ✅ |
| C003905 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V5 | T13 | 1275.7 | 15.35 | 72.3 | 73.9 | 85.8 | 11.4 | 1171.47 | 1297.47 | ✅ | ✅ | ✅ | ✅ |
| C003909 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V10 | T13 | 1273.3 | 15.85 | 72.3 | 73.9 | 85.8 | 11.4 | 1168.47 | 1294.47 | ✅ | ✅ | ✅ | ✅ |
| C003968 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V8 | T15 | 1274.5 | 15.55 | 72.3 | 73.9 | 85.9 | 11.4 | 1237.48 | 1363.48 | ✅ | ✅ | ✅ | ✅ |
| C003995 | Axisflying KOLAS7 (AF2a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC1 | V5 | T1 | 1254.6 | 14.7 | 72.3 | 73.9 | 86.0 | 11.2 | 894.99 | 1020.99 | ✅ | ✅ | ✅ | ✅ |
| C003999 | Axisflying KOLAS7 (AF2a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC1 | V10 | T1 | 1252.2 | 15.2 | 72.3 | 73.8 | 86.0 | 11.2 | 891.99 | 1017.99 | ✅ | ✅ | ✅ | ✅ |
| C004025 | Axisflying KOLAS7 (AF2a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC1 | V5 | T2 | 1254.6 | 14.7 | 72.3 | 73.9 | 86.0 | 11.2 | 935.99 | 1061.99 | ✅ | ✅ | ✅ | ✅ |
| C004029 | Axisflying KOLAS7 (AF2a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC1 | V10 | T2 | 1252.2 | 15.2 | 72.3 | 73.8 | 86.0 | 11.2 | 932.99 | 1058.99 | ✅ | ✅ | ✅ | ✅ |
| C004055 | Axisflying KOLAS7 (AF2a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC1 | V5 | T3 | 1254.6 | 14.7 | 72.3 | 73.9 | 86.0 | 11.2 | 949.99 | 1075.99 | ✅ | ✅ | ✅ | ✅ |
| C004059 | Axisflying KOLAS7 (AF2a) | Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10 | SBC1 | V10 | T3 | 1252.2 | 15.2 | 72.3 | 73.8 | 86.0 | 11.2 | 946.99 | 1072.99 | ✅ | ✅ | ✅ | ✅ |
| C003572 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V2 | T1 | 1263.6 | 18.2 | 72.2 | 73.7 | 85.5 | 11.3 | 951.48 | 1077.48 | ✅ | ✅ | ✅ | ✅ |
| C003574 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V4 | T1 | 1263.6 | 18.2 | 72.2 | 73.7 | 85.5 | 11.3 | 936.48 | 1062.48 | ✅ | ✅ | ✅ | ✅ |
| C003597 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V7 | T1 | 1277.6 | 15.2 | 72.2 | 73.8 | 85.7 | 11.4 | 972.48 | 1098.48 | ✅ | ✅ | ✅ | ✅ |
| C003602 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V2 | T2 | 1263.6 | 18.2 | 72.2 | 73.7 | 85.5 | 11.3 | 992.48 | 1118.48 | ✅ | ✅ | ✅ | ✅ |
| C003604 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V4 | T2 | 1263.6 | 18.2 | 72.2 | 73.7 | 85.5 | 11.3 | 977.48 | 1103.48 | ✅ | ✅ | ✅ | ✅ |
| C003627 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V7 | T2 | 1277.6 | 15.2 | 72.2 | 73.8 | 85.7 | 11.4 | 1013.48 | 1139.48 | ✅ | ✅ | ✅ | ✅ |
| C003632 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V2 | T3 | 1263.6 | 18.2 | 72.2 | 73.7 | 85.5 | 11.3 | 1006.48 | 1132.48 | ✅ | ✅ | ✅ | ✅ |
| C003634 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V4 | T3 | 1263.6 | 18.2 | 72.2 | 73.7 | 85.5 | 11.3 | 991.48 | 1117.48 | ✅ | ✅ | ✅ | ✅ |
| C003657 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC3 | V7 | T3 | 1277.6 | 15.2 | 72.2 | 73.8 | 85.7 | 11.4 | 1027.48 | 1153.48 | ✅ | ✅ | ✅ | ✅ |
| C003678 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC2 | V8 | T4 | 1270.8 | 17.0 | 72.1 | 73.6 | 85.4 | 11.3 | 936.47 | 1062.47 | ✅ | ✅ | ✅ | ✅ |
| C003693 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V3 | T5 | 1273.7 | 16.35 | 72.1 | 73.7 | 85.5 | 11.4 | 966.47 | 1092.47 | ✅ | ✅ | ✅ | ✅ |
| C003721 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V1 | T6 | 1276.6 | 15.85 | 72.1 | 73.6 | 85.5 | 11.4 | 917.48 | 1043.48 | ✅ | ✅ | ✅ | ✅ |
| C003757 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V7 | T8 | 1276.7 | 15.75 | 72.1 | 73.7 | 85.5 | 11.4 | 889.47 | 1015.47 | ✅ | ✅ | ✅ | ✅ |
| C003787 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V7 | T9 | 1276.7 | 15.75 | 72.1 | 73.7 | 85.5 | 11.4 | 1059.47 | 1185.47 | ✅ | ✅ | ✅ | ✅ |
| C003817 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V7 | T10 | 1276.7 | 15.8 | 72.1 | 73.6 | 85.5 | 11.4 | 1289.47 | 1415.47 | ✅ | ✅ | ✅ | ✅ |
| C003877 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V7 | T12 | 1276.7 | 15.8 | 72.1 | 73.6 | 85.5 | 11.4 | 1259.47 | 1385.47 | ✅ | ✅ | ✅ | ✅ |
| C003907 | Axisflying KOLAS7 (AF2a) | Lumenier NAV 12000mAh 6S 21700 Amprius | SBC1 | V7 | T13 | 1276.7 | 15.85 | 72.1 | 73.6 | 85.5 | 11.4 | 1189.47 | 1315.47 | ✅ | ✅ | ✅ | ✅ |
