# Flight-Time Analysis — Holistic Configuration Sweep

**Auto-generated** by [`flight_time_model.py`](flight_time_model.py). Regenerate with `python analysis/flight_time_model.py`.

Momentum-theory (actuator-disk) propulsion model + forward-flight parasitic drag. "Max flight time" = still-air hover endurance (R6 ≥ 30 min / R8 ≥ 60 min metric).

## Sweep scope

- **137,088 buildable configurations** = airframe × battery × SBC × VTX × thermal camera × DVR, fully crossed (respecting airframe component inclusion).
- Flight-time drivers swept in full; sub-1 W peripherals held at lightest representatives: FPV `A7`, GPS `G6`, RX `GEPRCNanoPA100`.
- **Inclusion logic:** airframe-bundled VTX/FPV/GPS/RX contribute power only (their mass is already in the airframe's as-built weight); non-bundled peripherals contribute mass + power.
- Candidates: 8 airframes (with mass data), 28 generic battery packs, 67 swept payload components.

## Model assumptions

- Rotors **4** · ρ **1.225 kg/m³** · FoM **0.65** · η **0.8** · C_d **1.0** · cruise **2.23 m/s** (R2) · wind **4.5 m/s** (R7)

> **Why cruise/wind endurance can exceed hover** — the multirotor *power bucket*: in slow forward flight the rotors gain translational lift, so induced power drops faster than parasitic drag rises. **Max FT** uses hover (conservative); *Cruise* (2.23 m/s) is the realistic still-air surveillance endurance; *Wind* is airspeed = cruise + 4.5 m/s (R7).

> **Caveats** — first-order comparative estimates (FoM, η, C_d, frontal area, thrust lookup are assumptions; battery mass derived from chemistry specific energy). Airframes missing mass/wheelbase are skipped (MODEL_ISSUES.md §D). Full per-instance data: [`flight_time_results.csv`](flight_time_results.csv).

## Recommended baseline

**Axisflying KOLAS7** (AF2b) + **Li-ion 6S 10000mAh**, SBC SBC1, VTX included, thermal T1 → **56.4 min** hover (1304.2 g AUW, 18.6% throttle).

## Top 100 configurations (ranked by max flight time)

| Cfg | Airframe | Battery | SBC | VTX | Therm | AUW g | Pld W | Max FT | Cruise | Wind | Thr% | R6 | R8 | Fly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C096193 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T1 | 1304.2 | 17.12 | 56.4 | 57.6 | 66.6 | 18.6 | ✅ | — | ✅ |
| C096211 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T2 | 1304.2 | 17.12 | 56.4 | 57.6 | 66.6 | 18.6 | ✅ | — | ✅ |
| C096229 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T3 | 1304.2 | 17.12 | 56.4 | 57.6 | 66.6 | 18.6 | ✅ | — | ✅ |
| C104257 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T1 | 1302.2 | 17.57 | 56.4 | 57.5 | 66.6 | 18.6 | ✅ | — | ✅ |
| C104275 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T2 | 1302.2 | 17.57 | 56.4 | 57.5 | 66.6 | 18.6 | ✅ | — | ✅ |
| C104293 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T3 | 1302.2 | 17.57 | 56.4 | 57.5 | 66.6 | 18.6 | ✅ | — | ✅ |
| C096301 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T7 | 1303.9 | 17.27 | 56.3 | 57.5 | 66.6 | 18.6 | ✅ | — | ✅ |
| C104365 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T7 | 1301.9 | 17.72 | 56.3 | 57.5 | 66.5 | 18.6 | ✅ | — | ✅ |
| C094465 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T1 | 1107.9 | 17.12 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C094483 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T2 | 1107.9 | 17.12 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C094501 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T3 | 1107.9 | 17.12 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C094573 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T7 | 1107.6 | 17.27 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C095905 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T1 | 1107.9 | 17.12 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C095923 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T2 | 1107.9 | 17.12 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C095941 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T3 | 1107.9 | 17.12 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C096013 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T7 | 1107.6 | 17.27 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C096198 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T1 | 1308.7 | 16.92 | 56.2 | 57.3 | 66.4 | 18.7 | ✅ | — | ✅ |
| C096216 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T2 | 1308.7 | 16.92 | 56.2 | 57.3 | 66.4 | 18.7 | ✅ | — | ✅ |
| C096234 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T3 | 1308.7 | 16.92 | 56.2 | 57.3 | 66.4 | 18.7 | ✅ | — | ✅ |
| C096247 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T4 | 1305.6 | 17.42 | 56.2 | 57.4 | 66.4 | 18.7 | ✅ | — | ✅ |
| C102529 | Axisflying KOLAS7 (AF2c) | Li-ion 4S 12000mAh | SBC1 | included | T1 | 1105.9 | 17.57 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C102547 | Axisflying KOLAS7 (AF2c) | Li-ion 4S 12000mAh | SBC1 | included | T2 | 1105.9 | 17.57 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C102565 | Axisflying KOLAS7 (AF2c) | Li-ion 4S 12000mAh | SBC1 | included | T3 | 1105.9 | 17.57 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C102637 | Axisflying KOLAS7 (AF2c) | Li-ion 4S 12000mAh | SBC1 | included | T7 | 1105.6 | 17.72 | 56.2 | 57.5 | 67.6 | 15.8 | ✅ | — | ✅ |
| C103969 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 8000mAh | SBC1 | included | T1 | 1105.9 | 17.57 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C103987 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 8000mAh | SBC1 | included | T2 | 1105.9 | 17.57 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C104005 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 8000mAh | SBC1 | included | T3 | 1105.9 | 17.57 | 56.2 | 57.6 | 67.7 | 15.8 | ✅ | — | ✅ |
| C104077 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 8000mAh | SBC1 | included | T7 | 1105.6 | 17.72 | 56.2 | 57.5 | 67.6 | 15.8 | ✅ | — | ✅ |
| C104311 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T4 | 1303.6 | 17.87 | 56.2 | 57.4 | 66.4 | 18.6 | ✅ | — | ✅ |
| C096194 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T1 | 1309.7 | 17.02 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C096195 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T1 | 1310.6 | 16.82 | 56.1 | 57.3 | 66.2 | 18.7 | ✅ | — | ✅ |
| C096197 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T1 | 1309.7 | 17.02 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C096212 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T2 | 1309.7 | 17.02 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C096213 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T2 | 1310.6 | 16.82 | 56.1 | 57.3 | 66.2 | 18.7 | ✅ | — | ✅ |
| C096215 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T2 | 1309.7 | 17.02 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C096230 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T3 | 1309.7 | 17.02 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C096231 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T3 | 1310.6 | 16.82 | 56.1 | 57.3 | 66.2 | 18.7 | ✅ | — | ✅ |
| C096233 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T3 | 1309.7 | 17.02 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C096306 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T7 | 1308.4 | 17.07 | 56.1 | 57.3 | 66.3 | 18.7 | ✅ | — | ✅ |
| C104258 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T1 | 1307.7 | 17.47 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C104259 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T1 | 1308.6 | 17.27 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C104261 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T1 | 1307.7 | 17.47 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C104262 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T1 | 1306.7 | 17.37 | 56.1 | 57.3 | 66.3 | 18.7 | ✅ | — | ✅ |
| C104276 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T2 | 1307.7 | 17.47 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C104277 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T2 | 1308.6 | 17.27 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C104279 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T2 | 1307.7 | 17.47 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C104280 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T2 | 1306.7 | 17.37 | 56.1 | 57.3 | 66.3 | 18.7 | ✅ | — | ✅ |
| C104294 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T3 | 1307.7 | 17.47 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C104295 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T3 | 1308.6 | 17.27 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C104297 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T3 | 1307.7 | 17.47 | 56.1 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C104298 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T3 | 1306.7 | 17.37 | 56.1 | 57.3 | 66.3 | 18.7 | ✅ | — | ✅ |
| C104370 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T7 | 1306.4 | 17.52 | 56.1 | 57.3 | 66.3 | 18.7 | ✅ | — | ✅ |
| C082952 | Axisflying KOLAS7 (AF2a) | Li-ion 6S 10000mAh | SBC1 | V8 | T1 | 1315.7 | 16.0 | 56.0 | 57.2 | 66.2 | 18.8 | ✅ | — | ✅ |
| C083132 | Axisflying KOLAS7 (AF2a) | Li-ion 6S 10000mAh | SBC1 | V8 | T2 | 1315.7 | 16.0 | 56.0 | 57.2 | 66.2 | 18.8 | ✅ | — | ✅ |
| C083312 | Axisflying KOLAS7 (AF2a) | Li-ion 6S 10000mAh | SBC1 | V8 | T3 | 1315.7 | 16.0 | 56.0 | 57.2 | 66.2 | 18.8 | ✅ | — | ✅ |
| C084032 | Axisflying KOLAS7 (AF2a) | Li-ion 6S 10000mAh | SBC1 | V8 | T7 | 1315.4 | 16.15 | 56.0 | 57.2 | 66.2 | 18.8 | ✅ | — | ✅ |
| C094470 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T1 | 1112.4 | 16.92 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C094488 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T2 | 1112.4 | 16.92 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C094506 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T3 | 1112.4 | 16.92 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C094519 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T4 | 1109.3 | 17.42 | 56.0 | 57.4 | 67.4 | 15.8 | ✅ | — | ✅ |
| C094578 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T7 | 1112.1 | 17.07 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C095910 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T1 | 1112.4 | 16.92 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C095928 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T2 | 1112.4 | 16.92 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C095946 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T3 | 1112.4 | 16.92 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C095959 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T4 | 1109.3 | 17.42 | 56.0 | 57.4 | 67.4 | 15.8 | ✅ | — | ✅ |
| C096018 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T7 | 1112.1 | 17.07 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C096252 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T4 | 1310.1 | 17.22 | 56.0 | 57.2 | 66.1 | 18.7 | ✅ | — | ✅ |
| C096302 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T7 | 1309.4 | 17.17 | 56.0 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C096303 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T7 | 1310.3 | 16.97 | 56.0 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C096305 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 10000mAh | SBC1 | included | T7 | 1309.4 | 17.17 | 56.0 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C102534 | Axisflying KOLAS7 (AF2c) | Li-ion 4S 12000mAh | SBC1 | included | T1 | 1110.4 | 17.37 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C102552 | Axisflying KOLAS7 (AF2c) | Li-ion 4S 12000mAh | SBC1 | included | T2 | 1110.4 | 17.37 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C102570 | Axisflying KOLAS7 (AF2c) | Li-ion 4S 12000mAh | SBC1 | included | T3 | 1110.4 | 17.37 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C102583 | Axisflying KOLAS7 (AF2c) | Li-ion 4S 12000mAh | SBC1 | included | T4 | 1107.3 | 17.87 | 56.0 | 57.3 | 67.4 | 15.8 | ✅ | — | ✅ |
| C103974 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 8000mAh | SBC1 | included | T1 | 1110.4 | 17.37 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C103992 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 8000mAh | SBC1 | included | T2 | 1110.4 | 17.37 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C104010 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 8000mAh | SBC1 | included | T3 | 1110.4 | 17.37 | 56.0 | 57.3 | 67.4 | 15.9 | ✅ | — | ✅ |
| C104023 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 8000mAh | SBC1 | included | T4 | 1107.3 | 17.87 | 56.0 | 57.3 | 67.4 | 15.8 | ✅ | — | ✅ |
| C104316 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T4 | 1308.1 | 17.67 | 56.0 | 57.2 | 66.1 | 18.7 | ✅ | — | ✅ |
| C104366 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T7 | 1307.4 | 17.62 | 56.0 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C104367 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T7 | 1308.3 | 17.42 | 56.0 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C104369 | Axisflying KOLAS7 (AF2c) | Li-ion 6S 10000mAh | SBC1 | included | T7 | 1307.4 | 17.62 | 56.0 | 57.2 | 66.2 | 18.7 | ✅ | — | ✅ |
| C094466 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T1 | 1113.4 | 17.02 | 55.9 | 57.2 | 67.3 | 15.9 | ✅ | — | ✅ |
| C094467 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T1 | 1114.3 | 16.82 | 55.9 | 57.3 | 67.3 | 15.9 | ✅ | — | ✅ |
| C094469 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T1 | 1113.4 | 17.02 | 55.9 | 57.2 | 67.3 | 15.9 | ✅ | — | ✅ |
| C094484 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T2 | 1113.4 | 17.02 | 55.9 | 57.2 | 67.3 | 15.9 | ✅ | — | ✅ |
| C094485 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T2 | 1114.3 | 16.82 | 55.9 | 57.3 | 67.3 | 15.9 | ✅ | — | ✅ |
| C094487 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T2 | 1113.4 | 17.02 | 55.9 | 57.2 | 67.3 | 15.9 | ✅ | — | ✅ |
| C094502 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T3 | 1113.4 | 17.02 | 55.9 | 57.2 | 67.3 | 15.9 | ✅ | — | ✅ |
| C094503 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T3 | 1114.3 | 16.82 | 55.9 | 57.3 | 67.3 | 15.9 | ✅ | — | ✅ |
| C094505 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T3 | 1113.4 | 17.02 | 55.9 | 57.2 | 67.3 | 15.9 | ✅ | — | ✅ |
| C094574 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T7 | 1113.1 | 17.17 | 55.9 | 57.2 | 67.2 | 15.9 | ✅ | — | ✅ |
| C094575 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T7 | 1114.0 | 16.97 | 55.9 | 57.2 | 67.3 | 15.9 | ✅ | — | ✅ |
| C094577 | Axisflying KOLAS7 (AF2b) | Li-ion 4S 12000mAh | SBC1 | included | T7 | 1113.1 | 17.17 | 55.9 | 57.2 | 67.2 | 15.9 | ✅ | — | ✅ |
| C095906 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T1 | 1113.4 | 17.02 | 55.9 | 57.2 | 67.3 | 15.9 | ✅ | — | ✅ |
| C095907 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T1 | 1114.3 | 16.82 | 55.9 | 57.3 | 67.3 | 15.9 | ✅ | — | ✅ |
| C095909 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T1 | 1113.4 | 17.02 | 55.9 | 57.2 | 67.3 | 15.9 | ✅ | — | ✅ |
| C095924 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T2 | 1113.4 | 17.02 | 55.9 | 57.2 | 67.3 | 15.9 | ✅ | — | ✅ |
| C095925 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T2 | 1114.3 | 16.82 | 55.9 | 57.3 | 67.3 | 15.9 | ✅ | — | ✅ |
| C095927 | Axisflying KOLAS7 (AF2b) | Li-ion 6S 8000mAh | SBC1 | included | T2 | 1113.4 | 17.02 | 55.9 | 57.2 | 67.3 | 15.9 | ✅ | — | ✅ |
