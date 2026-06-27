# Flight-Time Analysis — Best Value (Endurance per Dollar)

**Auto-generated** by [`flight_time_model.py`](flight_time_model.py). Regenerate with `python analysis/flight_time_model.py`.

Ranked by **endurance-per-dollar** = max hover flight time (min) ÷ total system cost (USD) × 1000 — i.e. **minutes of hover per $1,000**. Only configs meeting R6 (≥ 30 min) and the thrust/feasibility check are ranked. Each entry lists the **complete system bill of materials** by actual product name. Peripherals shown as *included with airframe* are bundled in a BNF/PNP airframe (no separate part or cost); the DVR is an earlier-stage recorder (counted in cost, excluded from flight time).

**Ground control station** (fixed — same on every instance; the laptop *is* the GCS and is existing kit, not costed):
- Control + telemetry, primary: **HGLRC Hermes ELRS SIM USB Dongle** ($16)
- Live video receiver: **Skydroid 150CH 5.8GHz True-Diversity UVC Receiver** ($45)
- Manual control, Phase-1 / backup: **RadioMaster Pocket ELRS** ($65)
- **GCS subtotal: $126**

**Thermal camera:** fixed to **T13** on every instance (design choice — not swept).
**SBC:** fixed to **SBC3** on every instance (design choice — not swept).

Full per-config dataset: [`flight_time_results.csv`](flight_time_results.csv); endurance-ranked view: [`flight_time_results.md`](flight_time_results.md).

## Top 100 by endurance-per-dollar

### 1. 45.94 min/$1k — 69.1 min hover · drone $1379 / system $1505 · ✅ R4
- Airframe **DarwinFPV 129 7in** (`AF9a`) · Battery **Lumenier NAV 12000mAh 4S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 2. 35.71 min/$1k — 57.1 min hover · drone $1472 / system $1598 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 3. 35.64 min/$1k — 58.6 min hover · drone $1519 / system $1645 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 4. 34.97 min/$1k — 56.8 min hover · drone $1499 / system $1625 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 5. 34.91 min/$1k — 58.4 min hover · drone $1545 / system $1671 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 6. 34.75 min/$1k — 49.4 min hover · drone $1295 / system $1421 · ✅ R4
- Airframe **DarwinFPV 129 7in** (`AF9a`) · Battery **Lumenier NAV 8000mAh 4S 18650 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 7. 33.98 min/$1k — 48.5 min hover · drone $1300 / system $1426 · ✅ R4
- Airframe **DarwinFPV 129 7in** (`AF9a`) · Battery **Upgrade Energy RED V3 4S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 8. 33.64 min/$1k — 47.6 min hover · drone $1290 / system $1416 · ✅ R4
- Airframe **DarwinFPV 129 7in** (`AF9a`) · Battery **Upgrade Energy GREEN V1 4S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 9. 33.63 min/$1k — 48.5 min hover · drone $1315 / system $1441 · ✅ R4
- Airframe **DarwinFPV 129 7in** (`AF9a`) · Battery **Upgrade Energy GREEN V2 4S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 10. 32.57 min/$1k — 49.4 min hover · drone $1391 / system $1517 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 11. 32.25 min/$1k — 57.4 min hover · drone $1654 / system $1780 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 12. 32.25 min/$1k — 55.9 min hover · drone $1608 / system $1734 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 13. 31.84 min/$1k — 49.2 min hover · drone $1418 / system $1544 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 14. 31.75 min/$1k — 46.8 min hover · drone $1347 / system $1473 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 15. 31.47 min/$1k — 49.6 min hover · drone $1449 / system $1575 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 16. 31.4 min/$1k — 52.8 min hover · drone $1557 / system $1683 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: *included with airframe*

### 17. 31.37 min/$1k — 54.3 min hover · drone $1603 / system $1729 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: *included with airframe*

### 18. 31.05 min/$1k — 46.6 min hover · drone $1374 / system $1500 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 19. 30.8 min/$1k — 49.3 min hover · drone $1476 / system $1602 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 20. 30.31 min/$1k — 48.3 min hover · drone $1467 / system $1593 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 21. 29.68 min/$1k — 48.1 min hover · drone $1494 / system $1620 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 22. 29.61 min/$1k — 47.4 min hover · drone $1476 / system $1602 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2b`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: *included with airframe*

### 23. 29.18 min/$1k — 48.2 min hover · drone $1527 / system $1653 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 24. 29.15 min/$1k — 41.8 min hover · drone $1309 / system $1435 · ✅ R4
- Airframe **DarwinFPV 129 7in** (`AF9a`) · Battery **Upgrade Energy Dark Lithium V2 4S 8400mAh Molicel P42A**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 25. 28.89 min/$1k — 53.1 min hover · drone $1710 / system $1836 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2c`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: *included with airframe*

### 26. 28.87 min/$1k — 51.7 min hover · drone $1664 / system $1790 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2c`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: *included with airframe*

### 27. 28.84 min/$1k — 41.7 min hover · drone $1320 / system $1446 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **iFlight Fullsend 6S 8000mAh EVE INR21700-40PL**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 28. 28.77 min/$1k — 48.9 min hover · drone $1575 / system $1701 · ✅ R4
- Airframe **iFlight Chimera7 Pro V2** (`AF8a`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 29. 28.75 min/$1k — 50.2 min hover · drone $1621 / system $1747 · ✅ R4
- Airframe **iFlight Chimera7 Pro V2** (`AF8a`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 30. 28.5 min/$1k — 45.9 min hover · drone $1483 / system $1609 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 31. 28.46 min/$1k — 48.7 min hover · drone $1586 / system $1712 · ✅ R4
- Airframe **iFlight Chimera7 Pro V2** (`AF8b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: *included with airframe*

### 32. 28.45 min/$1k — 50.0 min hover · drone $1632 / system $1758 · ✅ R4
- Airframe **iFlight Chimera7 Pro V2** (`AF8b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: *included with airframe*

### 33. 28.36 min/$1k — 48.5 min hover · drone $1585 / system $1711 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 34. 28.18 min/$1k — 41.5 min hover · drone $1347 / system $1473 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **iFlight Fullsend 6S 8000mAh EVE INR21700-40PL**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 35. 27.79 min/$1k — 46.1 min hover · drone $1534 / system $1660 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2b`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: *included with airframe*

### 36. 27.65 min/$1k — 43.1 min hover · drone $1432 / system $1558 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2b`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: *included with airframe*

### 37. 27.49 min/$1k — 41.6 min hover · drone $1387 / system $1513 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 12000mAh 6S 21700 XT90**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 38. 27.42 min/$1k — 37.7 min hover · drone $1247 / system $1373 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **DOGCOM 6S1P 5000mAh Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 39. 27.36 min/$1k — 47.3 min hover · drone $1603 / system $1729 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 40. 27.29 min/$1k — 46.4 min hover · drone $1574 / system $1700 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: AKK A1918 1W (`V10`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 41. 27.29 min/$1k — 38.4 min hover · drone $1282 / system $1408 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **iFlight Fullsend 6S2P 6000mAh Samsung 30Q**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 42. 27.28 min/$1k — 47.6 min hover · drone $1620 / system $1746 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: AKK A1918 1W (`V10`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 43. 27.27 min/$1k — 47.8 min hover · drone $1628 / system $1754 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: AKK X2-Ultimate 1W (`V8`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 44. 27.27 min/$1k — 46.6 min hover · drone $1582 / system $1708 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: AKK X2-Ultimate 1W (`V8`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 45. 27.24 min/$1k — 46.4 min hover · drone $1577 / system $1703 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: RushFPV Tank SOLO 1W (`V5`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 46. 27.23 min/$1k — 47.6 min hover · drone $1623 / system $1749 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: RushFPV Tank SOLO 1W (`V5`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 47. 27.14 min/$1k — 46.1 min hover · drone $1572 / system $1698 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: GEPRC RAD 1.6W (`V3`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 48. 27.13 min/$1k — 47.3 min hover · drone $1618 / system $1744 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: GEPRC RAD 1.6W (`V3`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 49. 27.12 min/$1k — 39.6 min hover · drone $1333 / system $1459 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **GNB 8000mAh 6S2P Samsung 21700 40T**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 50. 27.01 min/$1k — 46.2 min hover · drone $1583 / system $1709 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2c`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: *included with airframe*

### 51. 27.0 min/$1k — 46.0 min hover · drone $1577 / system $1703 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: BLITZ Whoop 1.6W (`V1`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 52. 26.99 min/$1k — 47.2 min hover · drone $1623 / system $1749 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: BLITZ Whoop 1.6W (`V1`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 53. 26.91 min/$1k — 41.4 min hover · drone $1414 / system $1540 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **Lumenier NAV 12000mAh 6S 21700 XT90**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 54. 26.89 min/$1k — 47.5 min hover · drone $1641 / system $1767 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: HGLRC Zeus 1.6W VTX PRO (`V7`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 55. 26.89 min/$1k — 46.3 min hover · drone $1595 / system $1721 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: HGLRC Zeus 1.6W VTX PRO (`V7`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 56. 26.82 min/$1k — 45.5 min hover · drone $1572 / system $1698 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: EMAX 2.5W VTX (`V4`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 57. 26.81 min/$1k — 46.8 min hover · drone $1618 / system $1744 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: EMAX 2.5W VTX (`V4`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 58. 26.73 min/$1k — 47.3 min hover · drone $1641 / system $1767 · ✅ R4
- Airframe **GEPRC MOZ7 V2 Analog** (`AF1a`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 59. 26.73 min/$1k — 46.0 min hover · drone $1595 / system $1721 · ✅ R4
- Airframe **GEPRC MOZ7 V2 Analog** (`AF1a`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 60. 26.73 min/$1k — 37.4 min hover · drone $1274 / system $1400 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **DOGCOM 6S1P 5000mAh Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 61. 26.69 min/$1k — 44.8 min hover · drone $1552 / system $1678 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2b`) · Battery **Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: *included with airframe*

### 62. 26.64 min/$1k — 38.2 min hover · drone $1308 / system $1434 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **iFlight Fullsend 6S2P 6000mAh Samsung 30Q**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 63. 26.59 min/$1k — 45.5 min hover · drone $1587 / system $1713 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: BLITZ Whoop 2.5W (`V2`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 64. 26.58 min/$1k — 46.8 min hover · drone $1633 / system $1759 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: BLITZ Whoop 2.5W (`V2`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 65. 26.52 min/$1k — 39.4 min hover · drone $1360 / system $1486 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **GNB 8000mAh 6S2P Samsung 21700 40T**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 66. 26.52 min/$1k — 54.8 min hover · drone $1940 / system $2066 · ✅ R4
- Airframe **GEPRC Crocodile75 V3** (`AF7`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 67. 26.42 min/$1k — 53.4 min hover · drone $1894 / system $2020 · ✅ R4
- Airframe **GEPRC Crocodile75 V3** (`AF7`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 68. 26.32 min/$1k — 42.6 min hover · drone $1494 / system $1620 · ✅ R4
- Airframe **iFlight Chimera7 Pro V2** (`AF8a`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 69. 26.3 min/$1k — 44.8 min hover · drone $1577 / system $1703 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: SoloGood TS582000 2W (`V11`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 70. 26.29 min/$1k — 46.0 min hover · drone $1623 / system $1749 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: SoloGood TS582000 2W (`V11`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 71. 26.28 min/$1k — 47.0 min hover · drone $1660 / system $1786 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: RushFPV Tank MAX SOLO 2.5W (`V6`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 72. 26.28 min/$1k — 45.7 min hover · drone $1614 / system $1740 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S3P 12Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: RushFPV Tank MAX SOLO 2.5W (`V6`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 73. 26.12 min/$1k — 39.1 min hover · drone $1370 / system $1496 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Pyrodrone Hyperjuice 6S2P 6000mAh Sony VTC6**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 74. 26.01 min/$1k — 42.4 min hover · drone $1505 / system $1631 · ✅ R4
- Airframe **iFlight Chimera7 Pro V2** (`AF8b`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: *included with airframe*

### 75. 25.81 min/$1k — 40.8 min hover · drone $1456 / system $1582 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **iFlight Fullsend 6S 8000mAh EVE INR21700-40PL**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 76. 25.75 min/$1k — 37.1 min hover · drone $1316 / system $1442 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Upgrade Energy RED V3 6S1P 5Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 77. 25.52 min/$1k — 38.9 min hover · drone $1397 / system $1523 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **Pyrodrone Hyperjuice 6S2P 6000mAh Sony VTC6**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 78. 25.51 min/$1k — 45.1 min hover · drone $1641 / system $1767 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2c`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: *included with airframe*

### 79. 25.49 min/$1k — 37.2 min hover · drone $1332 / system $1458 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2b`) · Battery **DOGCOM 6S1P 5000mAh Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: *included with airframe*

### 80. 25.43 min/$1k — 38.9 min hover · drone $1405 / system $1531 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2b`) · Battery **iFlight Fullsend 6S 8000mAh EVE INR21700-40PL**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: *included with airframe*

### 81. 25.42 min/$1k — 40.1 min hover · drone $1450 / system $1576 · ✅ R4
- Airframe **iFlight Chimera7 Pro V2** (`AF8a`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 82. 25.35 min/$1k — 42.5 min hover · drone $1552 / system $1678 · ✅ R4
- Airframe **iFlight Chimera7 Pro V2** (`AF8a`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 83. 25.32 min/$1k — 42.2 min hover · drone $1539 / system $1665 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2c`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: *included with airframe*

### 84. 25.14 min/$1k — 39.9 min hover · drone $1460 / system $1586 · ✅ R4
- Airframe **iFlight Chimera7 Pro V2** (`AF8b`) · Battery **Lumenier NAV 10000mAh 6S 21700 Li-Ion**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: *included with airframe*

### 85. 25.13 min/$1k — 36.9 min hover · drone $1343 / system $1469 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **Upgrade Energy RED V3 6S1P 5Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 86. 25.09 min/$1k — 35.6 min hover · drone $1293 / system $1419 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 5000mAh 6S 21700**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 87. 25.07 min/$1k — 42.3 min hover · drone $1563 / system $1689 · ✅ R4
- Airframe **iFlight Chimera7 Pro V2** (`AF8b`) · Battery **Upgrade Energy RED V3 6S2P 10Ah Molicel P50B**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: *included with airframe*

### 88. 24.81 min/$1k — 40.9 min hover · drone $1523 / system $1649 · ✅ R4
- Airframe **DarwinFPV X9** (`AF4a`) · Battery **Lumenier NAV 12000mAh 6S 21700 XT90**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 89. 24.77 min/$1k — 37.5 min hover · drone $1386 / system $1512 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3a`) · Battery **Lumenier NAV 6000mAh 6S 18650**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 90. 24.74 min/$1k — 40.3 min hover · drone $1501 / system $1627 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: AKK X2-Ultimate 1W (`V8`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 91. 24.74 min/$1k — 40.1 min hover · drone $1493 / system $1619 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: AKK A1918 1W (`V10`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 92. 24.74 min/$1k — 36.9 min hover · drone $1366 / system $1492 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2b`) · Battery **iFlight Fullsend 6S2P 6000mAh Samsung 30Q**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: *included with airframe*

### 93. 24.7 min/$1k — 40.1 min hover · drone $1496 / system $1622 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: RushFPV Tank SOLO 1W (`V5`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 94. 24.57 min/$1k — 39.7 min hover · drone $1491 / system $1617 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: GEPRC RAD 1.6W (`V3`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 95. 24.53 min/$1k — 43.8 min hover · drone $1659 / system $1785 · ✅ R4
- Airframe **Axisflying KOLAS7** (`AF2c`) · Battery **Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: *included with airframe*

### 96. 24.49 min/$1k — 35.4 min hover · drone $1320 / system $1446 · ✅ R4
- Airframe **iFlight Chimera9 ECO** (`AF3b`) · Battery **Lumenier NAV 5000mAh 6S 21700**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: *included with airframe*

### 97. 24.44 min/$1k — 48.5 min hover · drone $1856 / system $1982 · ✅ R4
- Airframe **GEPRC MOZ7 V2 O4 Pro** (`AF1c`) · Battery **Lumenier NAV 12000mAh 6S 21700 Amprius**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 98. 24.43 min/$1k — 39.6 min hover · drone $1496 / system $1622 · ✅ R4
- Airframe **GEPRC MOZ7 V2 WTFPV** (`AF1b`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: BLITZ Whoop 1.6W (`V1`) · FPV cam: Caddx Ant (`A7`) · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 99. 24.42 min/$1k — 41.4 min hover · drone $1570 / system $1696 · ✅ R4
- Airframe **iFlight Chimera7 Pro V2** (`AF8a`) · Battery **Upgrade Energy GREEN V1 6S2P 10Ah Samsung 50S**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: *included with airframe* · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

### 100. 24.4 min/$1k — 47.3 min hover · drone $1813 / system $1939 · ✅ R4
- Airframe **GEPRC Crocodile75 V3** (`AF7`) · Battery **Upgrade Energy GREEN V2 6S2P 8Ah Amprius SA10**
- Thermal camera: PurpleRiver Mini 640 (`T13`) · SBC: NanoPi M5 (4 GB) (`SBC3`) · DVR: Monster UVC Recorder (standalone USB-UVC DVR) (`DVR9`)
- VTX: *included with airframe* · FPV cam: *included with airframe* · GPS: TBS M10 GPS (`G6`) · RX: GEPRC ELRS Nano 2.4G PA100 (`GEPRCNanoPA100`)

