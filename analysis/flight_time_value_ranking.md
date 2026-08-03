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

### 1. 34.19 min/$1k — 55.9 min hover · drone $1460 / system $1635 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 2. 34.14 min/$1k — 57.4 min hover · drone $1506 / system $1682 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 3. 33.91 min/$1k — 56.9 min hover · drone $1502 / system $1677 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 4. 33.89 min/$1k — 58.4 min hover · drone $1548 / system $1724 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 5. 31.03 min/$1k — 48.2 min hover · drone $1379 / system $1554 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 6. 30.83 min/$1k — 49.2 min hover · drone $1421 / system $1596 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 7. 30.72 min/$1k — 45.2 min hover · drone $1295 / system $1470 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **GNB (Gaoneng) 6S3P 12Ah 21700 Li-ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 8. 30.36 min/$1k — 45.9 min hover · drone $1335 / system $1510 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 9. 30.31 min/$1k — 45.8 min hover · drone $1337 / system $1512 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **GNB (Gaoneng) 6S3P 12Ah 21700 Li-ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 10. 30.1 min/$1k — 48.5 min hover · drone $1437 / system $1612 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 11. 30.04 min/$1k — 46.6 min hover · drone $1377 / system $1552 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 12. 29.86 min/$1k — 49.4 min hover · drone $1479 / system $1654 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 13. 29.01 min/$1k — 47.3 min hover · drone $1455 / system $1630 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 14. 28.78 min/$1k — 48.1 min hover · drone $1497 / system $1672 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 15. 27.52 min/$1k — 40.8 min hover · drone $1308 / system $1483 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **iFlight Fullsend 6S 8000mAh EVE INR21700-40PL**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 16. 27.24 min/$1k — 41.6 min hover · drone $1350 / system $1525 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **iFlight Fullsend 6S 8000mAh EVE INR21700-40PL**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 17. 26.39 min/$1k — 40.9 min hover · drone $1375 / system $1550 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 12000mAh 6S 21700 XT90**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 18. 26.05 min/$1k — 41.5 min hover · drone $1417 / system $1592 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 12000mAh 6S 21700 XT90**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 19. 25.99 min/$1k — 36.7 min hover · drone $1235 / system $1410 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **DOGCOM 6S1P 5000mAh Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 20. 25.95 min/$1k — 37.5 min hover · drone $1269 / system $1445 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **iFlight Fullsend 6S2P 6000mAh Samsung 30Q**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 21. 25.91 min/$1k — 38.8 min hover · drone $1321 / system $1496 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **GNB 8000mAh 6S2P Samsung 21700 40T**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 22. 25.81 min/$1k — 37.5 min hover · drone $1277 / system $1452 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **DOGCOM 6S1P 5000mAh Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 23. 25.73 min/$1k — 38.3 min hover · drone $1311 / system $1487 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **iFlight Fullsend 6S2P 6000mAh Samsung 30Q**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 24. 25.64 min/$1k — 39.4 min hover · drone $1363 / system $1538 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **GNB 8000mAh 6S2P Samsung 21700 40T**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 25. 25.01 min/$1k — 37.8 min hover · drone $1335 / system $1510 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Tattu G-Tech 6S 12Ah LiPo 30C**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 26. 24.87 min/$1k — 38.1 min hover · drone $1358 / system $1533 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Pyrodrone Hyperjuice 6S2P 6000mAh Sony VTC6**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 27. 24.71 min/$1k — 38.9 min hover · drone $1400 / system $1575 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Pyrodrone Hyperjuice 6S2P 6000mAh Sony VTC6**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 28. 24.65 min/$1k — 38.3 min hover · drone $1377 / system $1552 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Tattu G-Tech 6S 12Ah LiPo 30C**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 29. 24.43 min/$1k — 36.1 min hover · drone $1304 / system $1479 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy RED V3 6S1P 5Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 30. 24.3 min/$1k — 37.0 min hover · drone $1346 / system $1521 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy RED V3 6S1P 5Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 31. 23.83 min/$1k — 34.7 min hover · drone $1281 / system $1456 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 5000mAh 6S 21700**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 32. 23.67 min/$1k — 35.5 min hover · drone $1323 / system $1498 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 5000mAh 6S 21700**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 33. 23.6 min/$1k — 36.6 min hover · drone $1374 / system $1549 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 6000mAh 6S 18650**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 34. 23.44 min/$1k — 37.3 min hover · drone $1416 / system $1591 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 6000mAh 6S 18650**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: (none — SBC records) (`—`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($44) · GCS subtotal $175
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

