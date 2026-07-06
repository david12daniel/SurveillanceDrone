# Flight-Time Analysis — Best Value (Endurance per Dollar)

**Auto-generated** by [`flight_time_model.py`](flight_time_model.py). Regenerate with `python analysis/flight_time_model.py`.

Ranked by **endurance-per-dollar** = max hover flight time (min) ÷ total system cost (USD) × 1000 — i.e. **minutes of hover per $1,000**. Only configs meeting R6 (≥ 30 min) and the thrust/feasibility check are ranked. Each entry lists the **complete system bill of materials** by actual product name. Peripherals shown as *included with airframe* are bundled in a BNF/PNP airframe (no separate part or cost).

**Ground control station** (the laptop *is* the GCS and is existing kit, not costed). The control link is fixed; the **video receiver is matched per instance to the airframe's VTX format** (shown in each entry below):
- Control + telemetry, primary: **HGLRC Hermes ELRS SIM USB Dongle** ($16)
- Manual control, Phase-1 / backup: **RadioMaster Pocket ELRS** ($65)
- Ground patch antenna (range margin): **TrueRC X-AIR 5.8 MK II (RHCP patch)** ($45)
- **Control base subtotal: $126** (+ the matched video receiver below)
- Video receiver by VTX format:
  - CVBS VTX → **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45, 5 km)
  - DJI VTX → **DJI Goggles N3 (digital receiver)** ($230, 10 km)
  - WALKSNAIL VTX → **Walksnail Avatar HD Goggles L (digital receiver)** ($199, 4 km)

**Thermal camera:** fixed to **T13** on every instance (design choice — not swept).
**SBC:** fixed to **SBC3** on every instance (design choice — not swept).

Full per-config dataset: [`flight_time_results.csv`](flight_time_results.csv); endurance-ranked view: [`flight_time_results.md`](flight_time_results.md). **This same ranking as a flat table:** [`flight_time_value_ranking.csv`](flight_time_value_ranking.csv).

## Top 34 by endurance-per-dollar

### 1. 33.89 min/$1k — 55.9 min hover · drone $1479 / system $1650 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 2. 33.85 min/$1k — 57.4 min hover · drone $1525 / system $1696 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 3. 33.62 min/$1k — 56.9 min hover · drone $1521 / system $1692 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 4. 33.61 min/$1k — 58.4 min hover · drone $1567 / system $1738 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 5. 30.74 min/$1k — 48.2 min hover · drone $1398 / system $1569 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 6. 30.55 min/$1k — 49.2 min hover · drone $1440 / system $1611 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 7. 30.42 min/$1k — 45.2 min hover · drone $1314 / system $1485 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **GNB (Gaoneng) 6S3P 12Ah 21700 Li-ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 8. 30.07 min/$1k — 45.9 min hover · drone $1354 / system $1525 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 9. 30.03 min/$1k — 45.8 min hover · drone $1356 / system $1527 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **GNB (Gaoneng) 6S3P 12Ah 21700 Li-ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 10. 29.83 min/$1k — 48.5 min hover · drone $1456 / system $1627 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 11. 29.76 min/$1k — 46.6 min hover · drone $1396 / system $1567 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 12. 29.6 min/$1k — 49.4 min hover · drone $1498 / system $1669 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 13. 28.76 min/$1k — 47.3 min hover · drone $1474 / system $1645 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 14. 28.53 min/$1k — 48.1 min hover · drone $1516 / system $1687 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 15. 27.25 min/$1k — 40.8 min hover · drone $1327 / system $1498 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **iFlight Fullsend 6S 8000mAh EVE INR21700-40PL**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 16. 26.99 min/$1k — 41.6 min hover · drone $1369 / system $1540 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **iFlight Fullsend 6S 8000mAh EVE INR21700-40PL**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 17. 26.14 min/$1k — 40.9 min hover · drone $1394 / system $1565 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 12000mAh 6S 21700 XT90**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 18. 25.81 min/$1k — 41.5 min hover · drone $1436 / system $1607 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 12000mAh 6S 21700 XT90**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 19. 25.72 min/$1k — 36.7 min hover · drone $1254 / system $1425 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **DOGCOM 6S1P 5000mAh Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 20. 25.69 min/$1k — 37.5 min hover · drone $1288 / system $1459 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **iFlight Fullsend 6S2P 6000mAh Samsung 30Q**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 21. 25.66 min/$1k — 38.8 min hover · drone $1340 / system $1511 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **GNB 8000mAh 6S2P Samsung 21700 40T**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 22. 25.55 min/$1k — 37.5 min hover · drone $1296 / system $1467 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **DOGCOM 6S1P 5000mAh Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 23. 25.48 min/$1k — 38.3 min hover · drone $1330 / system $1501 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **iFlight Fullsend 6S2P 6000mAh Samsung 30Q**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 24. 25.4 min/$1k — 39.4 min hover · drone $1382 / system $1553 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **GNB 8000mAh 6S2P Samsung 21700 40T**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 25. 24.77 min/$1k — 37.8 min hover · drone $1354 / system $1525 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Tattu G-Tech 6S 12Ah LiPo 30C**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 26. 24.63 min/$1k — 38.1 min hover · drone $1377 / system $1548 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Pyrodrone Hyperjuice 6S2P 6000mAh Sony VTC6**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 27. 24.48 min/$1k — 38.9 min hover · drone $1419 / system $1590 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Pyrodrone Hyperjuice 6S2P 6000mAh Sony VTC6**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 28. 24.42 min/$1k — 38.3 min hover · drone $1396 / system $1567 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Tattu G-Tech 6S 12Ah LiPo 30C**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 29. 24.19 min/$1k — 36.1 min hover · drone $1323 / system $1494 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy RED V3 6S1P 5Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 30. 24.07 min/$1k — 37.0 min hover · drone $1365 / system $1536 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy RED V3 6S1P 5Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 31. 23.59 min/$1k — 34.7 min hover · drone $1300 / system $1471 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 5000mAh 6S 21700**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 32. 23.44 min/$1k — 35.5 min hover · drone $1342 / system $1513 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 5000mAh 6S 21700**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

### 33. 23.38 min/$1k — 36.6 min hover · drone $1393 / system $1564 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 6000mAh 6S 18650**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit 🟡: SBC 90x62 on deck 100x60 mm (battery top) — marginal: SBC 90x62 vs deck 100x60 mm (-2 mm) — snug/custom deck, slight overhang

### 34. 23.23 min/$1k — 37.3 min hover · drone $1435 / system $1606 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 6000mAh 6S 18650**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)
- Ground receiver (CVBS VTX): **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45) · GCS subtotal $171
- Physical fit ✅: SBC 90x62 on deck 110x70 mm (battery top) — fits (SBC on a raised tier; battery on deck) — 8 mm spare

