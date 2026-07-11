# Flight-Time Analysis — Best Value (Endurance per Dollar)

**Auto-generated** by [`flight_time_model.py`](flight_time_model.py). Regenerate with `python analysis/flight_time_model.py`.

Ranked by **endurance-per-dollar** = max hover flight time (min) ÷ total system cost (USD) × 1000 — i.e. **minutes of hover per $1,000**. Only configs meeting R6 (≥ 30 min) and the thrust/feasibility check are ranked. Each entry lists the **complete system bill of materials** by actual product name. Peripherals shown as *included with airframe* are bundled in a BNF/PNP airframe (no separate part or cost); the DVR is an earlier-stage recorder (counted in cost, excluded from flight time).

**Ground control station** (the laptop *is* the GCS and is existing kit, not costed). The control link is fixed; the **video receiver is matched per instance to the airframe's VTX format** (shown in each entry below):
- Control + telemetry, primary: **HGLRC Hermes ELRS SIM USB Dongle** ($16)
- Manual control, Phase-1 / backup: **RadioMaster Pocket ELRS** ($85)
- Ground patch antenna (range margin): **Foxeer Echo 2 Max 5.8 GHz (Linear patch) #1** ($30)
- **Control base subtotal: $131** (+ the matched video receiver below)
- Video receiver by VTX format:
  - CVBS VTX → **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44, 5 km)
  - DJI VTX → **DJI Goggles N3 (digital receiver)** ($230, 10 km)
  - WALKSNAIL VTX → **Walksnail Avatar HD Goggles L (digital receiver)** ($199, 4 km)

**Thermal camera:** fixed to **T13** on every instance (design choice — not swept).
**SBC:** fixed to **SBC3** on every instance (design choice — not swept).

Full per-config dataset: [`flight_time_results.csv`](flight_time_results.csv); endurance-ranked view: [`flight_time_results.md`](flight_time_results.md). **This same ranking as a flat table:** [`flight_time_value_ranking.csv`](flight_time_value_ranking.csv).

## Top 34 by endurance-per-dollar

### 1. 35.27 min/$1k — 55.9 min hover · drone $1410 / system $1585 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 2. 35.19 min/$1k — 57.4 min hover · drone $1456 / system $1632 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 3. 34.96 min/$1k — 56.9 min hover · drone $1452 / system $1627 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 4. 34.9 min/$1k — 58.4 min hover · drone $1498 / system $1674 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 5. 32.06 min/$1k — 48.2 min hover · drone $1329 / system $1504 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 6. 31.83 min/$1k — 49.2 min hover · drone $1371 / system $1546 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 7. 31.81 min/$1k — 45.2 min hover · drone $1245 / system $1420 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **GNB (Gaoneng) 6S3P 12Ah 21700 Li-ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 8. 31.4 min/$1k — 45.9 min hover · drone $1285 / system $1460 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 9. 31.35 min/$1k — 45.8 min hover · drone $1287 / system $1462 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **GNB (Gaoneng) 6S3P 12Ah 21700 Li-ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 10. 31.06 min/$1k — 48.5 min hover · drone $1387 / system $1562 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 11. 31.04 min/$1k — 46.6 min hover · drone $1327 / system $1502 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 12. 30.79 min/$1k — 49.4 min hover · drone $1429 / system $1604 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 13. 29.93 min/$1k — 47.3 min hover · drone $1405 / system $1580 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 14. 29.67 min/$1k — 48.1 min hover · drone $1447 / system $1622 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 15. 28.48 min/$1k — 40.8 min hover · drone $1258 / system $1433 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **iFlight Fullsend 6S 8000mAh EVE INR21700-40PL**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 16. 28.17 min/$1k — 41.6 min hover · drone $1300 / system $1475 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **iFlight Fullsend 6S 8000mAh EVE INR21700-40PL**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 17. 27.27 min/$1k — 40.9 min hover · drone $1325 / system $1500 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 12000mAh 6S 21700 XT90**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 18. 26.94 min/$1k — 36.7 min hover · drone $1185 / system $1360 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **DOGCOM 6S1P 5000mAh Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 19. 26.9 min/$1k — 41.5 min hover · drone $1367 / system $1542 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 12000mAh 6S 21700 XT90**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 20. 26.88 min/$1k — 37.5 min hover · drone $1219 / system $1395 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **iFlight Fullsend 6S2P 6000mAh Samsung 30Q**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 21. 26.81 min/$1k — 38.8 min hover · drone $1271 / system $1446 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **GNB 8000mAh 6S2P Samsung 21700 40T**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 22. 26.73 min/$1k — 37.5 min hover · drone $1227 / system $1402 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **DOGCOM 6S1P 5000mAh Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 23. 26.63 min/$1k — 38.3 min hover · drone $1261 / system $1437 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **iFlight Fullsend 6S2P 6000mAh Samsung 30Q**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 24. 26.5 min/$1k — 39.4 min hover · drone $1313 / system $1488 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **GNB 8000mAh 6S2P Samsung 21700 40T**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 25. 25.86 min/$1k — 37.8 min hover · drone $1285 / system $1460 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Tattu G-Tech 6S 12Ah LiPo 30C**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 26. 25.7 min/$1k — 38.1 min hover · drone $1308 / system $1483 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Pyrodrone Hyperjuice 6S2P 6000mAh Sony VTC6**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 27. 25.52 min/$1k — 38.9 min hover · drone $1350 / system $1525 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Pyrodrone Hyperjuice 6S2P 6000mAh Sony VTC6**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 28. 25.47 min/$1k — 38.3 min hover · drone $1327 / system $1502 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Tattu G-Tech 6S 12Ah LiPo 30C**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 29. 25.28 min/$1k — 36.1 min hover · drone $1254 / system $1429 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy RED V3 6S1P 5Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 30. 25.13 min/$1k — 37.0 min hover · drone $1296 / system $1471 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy RED V3 6S1P 5Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 31. 24.67 min/$1k — 34.7 min hover · drone $1231 / system $1406 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 5000mAh 6S 21700**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 32. 24.48 min/$1k — 35.5 min hover · drone $1273 / system $1448 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 5000mAh 6S 21700**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 33. 24.39 min/$1k — 36.6 min hover · drone $1324 / system $1499 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 6000mAh 6S 18650**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 34. 24.2 min/$1k — 37.3 min hover · drone $1366 / system $1541 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 6000mAh 6S 18650**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

