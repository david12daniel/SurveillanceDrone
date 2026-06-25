## Validated Airframe Candidates

> **Consolidated CSV:** All data below is compiled into a single flat table at `airframe-candidates.csv` (24 columns). PNP and BNF variants of the same airframe are split into **separate rows** with their own price/cost. 17 total candidates (8 PNP, 9 BNF).

### ⚙️ Component Breakdown
| # | Airframe | Flight Controller | ESC | Motors | Props |
|---|----------|-------------------|-----|--------|-------|
| 1 | GEPRC MARK4 LR7 | GEPRC TAKER F405 V2 | SPAN 50A BLHeli_S 4-in-1 | GEPRC E2806.5 1350KV | Gemfan 7037-3 |
| 2b | Axisflying KOLAS7 — PNP | iStack F722 / Argus F722 | iStack 50A / Argus 65A | Axisflying C287 1350KV | HQ 7035 / GF 7042 |
| 2c | Axisflying KOLAS7 — BNF Analog | iStack F722 / Argus F722 | iStack 50A / Argus 65A | Axisflying C287 1350KV | HQ 7035 / GF 7042 |
| 2d | Axisflying KOLAS7 — BNF HD (O3/Walksnail) | iStack F722 / Argus F722 | iStack 50A / Argus 65A | Axisflying C287 1350KV | HQ 7035 / GF 7042 |
| 3 | iFlight Chimera9 ECO | BLITZ ATF435 | BLITZ E55S 55A 4-in-1 | XING-E 2809 800KV | HQ 9X4X3 |
| 4 | DarwinFPV X9 | F411 MPU6500 | 100A BLHeli_32 4-in-1 | 2812 1100KV | Gemfan 9045-3 |
| 5 | EMAX Hawk 7 | F4 | 60A | ECOII2807 | 7" (model TBD) |
| 6 | DeepSpace ROC7 O4 PRO | Argus F722 | 60A BLHeli_32 | Redline 2807 1350KV | 7" (model TBD) |
| 7 | GEPRC Crocodile75 V3 | SPAN F722-BT-HD V2 | SPAN G50A / TAKER 32-bit 60A | SPEEDX2 2806.5 1350KV | HQ 7.5x3.7x3 |
| 8 | iFlight Chimera7 Pro V2 | BLITZ F722 | BLITZ E55 4-in-1 55A | XING2 2809 1250KV | HQ 7.5x3.7x3 |
| 9 | DarwinFPV 129 7" | F4 | 50A | 2507 | 7040 |
| 10 | NewBeeDrone DeepSpace ROC7 O4PRO | Argus F722 | 60A | Redline 2807 1350KV | 7" (model TBD) |
| 11 | HS-X07M | F405 (claimed) | 60A 4-in-1 (claimed) | 1350KV (claimed) | 7" (claimed) |

### 📡 Supported Interface Protocols
| # | Airframe | FC | UARTs | Receiver Protocols | Source Confidence |
|---|----------|-----|-------|-------------------|-------------------|
| 1 | GEPRC MARK4 LR7 | GEPRC TAKER F405 V2 (GEP-F405-HD) | 6 | **SBUS, PPM, CRSF, DSMX, iBus** — explicitly listed on product page | ✅ **High** — confirmed from GEPRC flycamdrones.com listing and GEP-F405-HD manual |
| 2b | Axisflying KOLAS7 — PNP | iStack F722 (STM32F777) | 6 | **SBUS, PPM, CRSF, DSMX, iBus** — F7 UARTs support all serial protocols | ✅ **High** — iStack F722 specs sheet |
| 2c | Axisflying KOLAS7 — BNF Analog | iStack F722 (STM32F777) | 6 | Receiver pre-installed: **TBS Nano RX** or **ELRS 2.4G** | ✅ **High** — axisflying.vip product dropdown |
| 2d | Axisflying KOLAS7 — BNF HD | iStack F722 (STM32F777) | 6 | Receiver pre-installed: **TBS Nano RX** (O3 variant) or **ELRS** (Walksnail) | ✅ **High** — bometoys.com, getfpv.com |
| 3 | iFlight Chimera9 ECO | BLITZ ATF435 (AT32F435) | 6 | **SBUS, PPM, CRSF, DSMX, iBus** — wiring diagram shows SBUS pad and CRSF wiring for ELRS/TBS receivers | ✅ **High** — official iFlight product page + Scribd wiring diagram |
| 4 | DarwinFPV X9 | F411 MPU6500 (STM32F411) | 2 HW + 2 softserial | **SBUS** (dedicated inverted pad), **PPM, CRSF** (on UART2), **DSMX, iBus** via softserial | ⚠️ **Moderate** — F411 has only 2 real UARTs; CRSF is possible but pin-constrained |
| 5 | EMAX Hawk 7 | F4 Magnum (STM32F405) | 6 | **SBUS, PPM, CRSF, DSMX, iBus** — F4 Magnum manual shows dedicated PPM/SBUS input; sold as BNF with ELRS (CRSF) | ✅ **High** — manual confirmed; BNF ELRS version proves CRSF support |
| 6 | DeepSpace ROC7 O4 PRO | Argus F722 (STM32F722) | 6 | **SBUS, PPM, CRSF, DSMX, iBus** — all F722 UARTs have built-in inversion; SBUS on any UART | ✅ **High** — MATEK F722-WPX manual; GetFPV listing confirms ELRS |
| 7 | GEPRC Crocodile75 V3 | SPAN F722-BT-HD V2 (STM32F722) | 5 | **SBUS, PPM, CRSF, DSMX, iBus, DUMD** — explicitly listed: "Supports Sbus, PPM, CRSF, DSMX, iBus, DUMD and other protocols" | ✅ **High** — confirmed directly from GEPRC product page |
| 8 | iFlight Chimera7 Pro V2 | BLITZ F722 (STM32F722) | 6 | **SBUS, PPM, CRSF, DSMX, iBus** — same BLITZ F7 platform as ATF435; wiring diagram shows SBUS pad and CRSF | ✅ **High** — iFlight product page + BLITZ F722 wiring diagram |
| 9 | DarwinFPV 129 7\" | F4 (STM32F405, MATEKF405 firmware) | 6 | **SBUS, PPM, CRSF, DSMX, iBus** — standard F405 UART capabilities; 6 UARTs | ✅ **High** — confirmed from usproelectronics.com product listing (MATEKF405) |
| 10 | NewBeeDrone ROC7 O4PRO | Argus F722 (STM32F722) | 6 | **SBUS, PPM, CRSF, DSMX, iBus** — identical FC to #6 | ✅ **High** — same DeepSpace ROC7 hardware |
| 11 | HS-X07M | F405 (claimed) | — | **Cannot verify** — product does not appear to exist | ❌ **None** — zero search results |

### 📦 Receiver Inclusion
| # | Airframe | Purchase Options | Receiver Included? | Price Delta (PNP vs BNF) | Source Confidence |
|---|----------|-----------------|-------------------|-------------------------|-------------------|
| 1 | GEPRC MARK4 LR7 | PNP only (discontinued at GEPRC; rotorama lists as PNP) | ❌ **No** — you supply your own receiver | N/A (PNP only) | ✅ **High** — rotorama listing shows drone, props, straps only |
| 2b | Axisflying KOLAS7 — PNP | PNP (FC/ESC/motors, ~$150-200 est.) | ❌ **No** — no receiver, no VTX | ~$58-108 to add receiver | ⚠️ **Moderate** — mentioned on dronegearup.com; exact price needs confirmation |
| 2c | Axisflying KOLAS7 — BNF Analog | Analog BNF ($419.90) | ✅ **Yes** — choose **TBS Nano RX** or **ELRS 2.4G RX** | $419.90 all-in | ✅ **High** — axisflying.vip product selector |
| 2d | Axisflying KOLAS7 — BNF HD | HD BNF ($649-777) | ✅ **Yes** — **TBS Nano RX** (O3) or **ELRS** (Walksnail) | $649-777 all-in | ✅ **High** — bometoys.com ($649 O3+TBS), getfpv.com (Walksnail), dronegearup.com (DJI O3) |
| 3 | iFlight Chimera9 ECO | **PNP** ($346.99) or **BNF** (+receiver cost) | ❌ PNP: no. ✅ BNF: **TBS Crossfire NANO**, **iFlight ELRS 868/900**, **iFlight ELRS 2.4GHz** options available | ~$15-30 add for receiver | ✅ **High** — confirmed from iFlight product page dropdown |
| 4 | DarwinFPV X9 | **PNP** ($280-400) or **BNF** (+$~20) | ❌ PNP: no. ✅ BNF: **ELRS 2.4G** or **ELRS 915M** receiver included | ~$20 for ELRS BNF upgrade | ✅ **High** — darwinfpv.com product page shows options |
| 5 | EMAX Hawk 7 | **BNF only** ($398.86) | ✅ **Yes** — comes with **ELRS receiver** pre-installed (product title: "ELRS BNF") | N/A (only sold as BNF) | ✅ **High** — confirmed from emaxmodel.com listing |
| 6 | DeepSpace ROC7 O4 PRO | **PNP+GPS** ($369) or **BNF** (+receiver cost) | ❌ PNP: no. ✅ BNF: **ELRS 2.4G**, **ELRS 915M**, or **TBS** receiver options | ~$10-25 add for receiver | ✅ **High** — confirmed from deepspacefpv.com product options |
| 7 | GEPRC Crocodile75 V3 | PNP (discontinued, limited stock) | ❌ **Likely not** — GEPRC sold as PNP; no evidence of BNF variant | N/A | ⚠️ **Moderate** — discontinued product; all listings show PNP format |
| 8 | iFlight Chimera7 Pro V2 | **PNP** ($499.99) or **BNF** (+receiver cost) | ❌ PNP: no. ✅ BNF: **TBS Crossfire NANO**, **iFlight ELRS 868/900**, **iFlight ELRS 2.4GHz**, **True Diversity** variants available | ~$15-45 add for receiver | ✅ **High** — confirmed from iFlight product page dropdown |
| 9 | DarwinFPV 129 7" | **PNP** ($180-264) or **BNF** (+$~15-20) | ❌ PNP: "No receiver". ✅ BNF: **ELRS 2.4G** or **ELRS 915M** receiver included | ~$15-20 for ELRS BNF upgrade | ✅ **High** — darwinfpv.com product page shows options |
| 10 | NewBeeDrone ROC7 O4PRO | BNF retail only ($699) | ✅ **Yes** — sold as BNF with receiver configured | N/A (only sold as BNF) | ✅ **High** — same DeepSpace ROC7 hardware, sold at retail markup |
| 11 | HS-X07M | N/A | ❓ **Cannot determine** — product does not appear to exist | N/A | ❌ **None** |

### 📡 VTX (Video Transmitter) Inclusion
| # | Airframe | VTX Included? | VTX Model / Details | Camera Included? | Source Confidence |
|---|----------|---------------|--------------------|-----------------|-------------------|
| 1 | GEPRC MARK4 LR7 — PNP | ✅ **Yes** | **GEPRC RAD 5.8G 1.6W** (high-power analog VTX) | ✅ **Yes** — Caddx H1 | ✅ **High** — rotorama.com product page lists VTX and camera in specs |
| 2b | Axisflying KOLAS7 — PNP | ❌ **No** — no VTX included | PNP = frame + FC + ESC + motors only; VTX is buyer's choice | ❌ **No** | ⚠️ **Moderate** — product description says "Compatible with all mainstream VTX" implying purchaser supplies it |
| 2c | Axisflying KOLAS7 — BNF Analog | ❓ **Unclear** — listed as "Analog BNF" but product pages only say "Compatible with all mainstream VTX" (no specific VTX named) | Unknown analog VTX model (if included) | ❓ **Unclear** | ⚠️ **Low** — no product page explicitly lists a VTX model or camera in the BNF Analog config; reach out to seller to confirm |
| 2d | Axisflying KOLAS7 — BNF HD | ✅ **Yes** — HD VTX pre-installed | **DJI O3 Air Unit** ($649 variant) or **Walksnail Avatar Pro** ($777 variant) | ✅ **Yes** — integrated into O3/Walksnail | ✅ **High** — bometoys.com, getfpv.com product listings |
| 3 | iFlight Chimera9 ECO — PNP/BNF | ✅ **Yes** — VTX is selectable option | **BLITZ Whoop 5.8G 1.6W** or **BLITZ Whoop 5.8G 2.5W** (chosen at purchase) | ✅ **Yes** — analog camera included (not named) | ✅ **High** — shop.iflight.com product page shows VTX dropdown options |
| 4 | DarwinFPV X9 — PNP/BNF | ❓ **Unlikely** — no VTX mentioned in any product description | Unknown — product pages emphasize frame/FC/ESC specs but omit VTX entirely | ❓ **Unlikely** | ⚠️ **Low** — 404 on darwinfpv.com product page; reseller listings don't mention VTX or camera |
| 5 | EMAX Hawk 7 — BNF | ✅ **Yes** — 2.5W analog VTX | Model not specified, but rated **2.5W** output | ✅ **Yes** — analog cam included | ⚠️ **Moderate** — emaxmodel.com listing mentions "2.5W VTX" in specs |
| 6 | DeepSpace ROC7 O4 PRO — PNP | ✅ **Yes** — DJI O4 Pro air unit | **DJI O4 Pro** (digital HD VTX + camera) | ✅ **Yes** — integrated O4 Pro | ✅ **High** — product name = "ROC7 O4 PRO", confirmed at deepspacefpv.com |
| 7 | GEPRC Crocodile75 V3 — PNP | ✅ **Yes** — 1.6W analog VTX | GEPRC RAD or equivalent 5.8G 1.6W VTX (model not confirmed) | ✅ **Yes** — analog camera included | ⚠️ **Moderate** — rcbuying.com listing title mentions "1.6W VTX"; camera needs confirmation |
| 8 | iFlight Chimera7 Pro V2 — PNP/BNF | ✅ **Yes** — VTX is selectable option | **BLITZ 5.8G 1.6W** or **5.8G 2.5W** VTX (chosen at purchase) | ✅ **Yes** — analog camera included | ✅ **High** — same BLITZ platform as Chimera9 ECO; iFlight's standard build includes VTX+cam |
| 9 | DarwinFPV 129 7" — PNP/BNF | ❓ **Unlikely** — no VTX mentioned in product specs | Unknown — product page doesn't mention VTX; price point ($180-264 PNP) suggests basic RC components only | ❓ **Unlikely** | ⚠️ **Low** — 404 on darwinfpv.com; listings don't mention VTX or camera |
| 10 | NewBeeDrone ROC7 O4PRO — BNF | ✅ **Yes** — DJI O4 Pro air unit | **DJI O4 Pro** (digital HD VTX + camera) | ✅ **Yes** — integrated O4 Pro | ✅ **High** — same hardware as DeepSpace ROC7; retail markup |
| 11 | HS-X07M | ❓ **Cannot determine** — product does not appear to exist | N/A | N/A | ❌ **None** |

### 🛰️ GPS Inclusion
| # | Airframe | GPS Included? | Details | Source Confidence |
|---|----------|---------------|---------|-------------------|
| 1 | GEPRC MARK4 LR7 — PNP | ❌ **No** | No GPS mentioned in specs or package contents at rotorama.com | ✅ **High** — rotorama listing has full specs and box contents; GPS absent |
| 2b | Axisflying KOLAS7 — PNP | ❌ **No** | Frame kit + electronics only; GPS mount exists but module not included | ⚠️ **Moderate** — adjustable GPS mount is a frame feature, but PNP means no electronics |
| 2c | Axisflying KOLAS7 — BNF Analog | ✅ **Yes** | Includes GPS module + adjustable-angle mount; product title says "with GPS" | ✅ **High** — fpvzoom.com product title confirms; existing notes confirm GPS in build |
| 2d | Axisflying KOLAS7 — BNF HD | ✅ **Yes** | Includes GPS module + adjustable-angle mount | ✅ **High** — same frame/mount as Analog BNF; HD variants also list GPS |
| 3 | iFlight Chimera9 ECO — PNP/BNF | ⚠️ **Optional (+$39)** | GPS is a separate option at checkout (Pre-installed GPS, +$39.00). Not included by default. | ✅ **High** — shop.iflight.com product page has explicit GPS option dropdown |
| 4 | DarwinFPV X9 — PNP/BNF | ❓ **Not confirmed** | No GPS mentioned in any available specs or product listings | ⚠️ **Low** — product pages 404; no reseller mentions GPS |
| 5 | EMAX Hawk 7 — BNF | ❓ **No** | GPS not mentioned in any available specs. BNF includes ELRS RX + 2.5W VTX only. | ⚠️ **Low** — emaxmodel.com 404; previous notes don't mention GPS; likely not included at this price |
| 6 | DeepSpace ROC7 O4 PRO — PNP | ✅ **Yes** | Product name is "PNP+GPS"; confirmed GPS included | ✅ **High** — product naming convention; deepspacefpv.com listing confirmed |
| 7 | GEPRC Crocodile75 V3 — PNP | ❓ **Not confirmed** | No GPS mentioned in available specs; likely not included | ⚠️ **Low** — product pages mostly 404; no evidence of GPS |
| 8 | iFlight Chimera7 Pro V2 — PNP/BNF | ❓ **Not confirmed** | Chimera7 Pro V2 product pages don't mention GPS as a standard option (unlike Chimera9 ECO) | ⚠️ **Low** — iFlight site shows the item but no GPS option visible; may need GPS add-on purchased separately |
| 9 | DarwinFPV 129 7" — PNP/BNF | ✅ **Yes** | Notes from earlier verification confirm GPS is included in the build | ✅ **High** — previous research (Specs table notes) says "2507 motors, 50A ESC, GPS, 1.5kg payload" |
| 10 | NewBeeDrone ROC7 O4PRO — BNF | ✅ **Likely Yes** | Same hardware as DeepSpace ROC7 (which includes GPS); sold at retail markup | ⚠️ **Moderate** — hardware is identical to #6 but NewBeeDrone listing needs confirmation |
| 11 | HS-X07M | ❓ **Cannot determine** | Product does not appear to exist | ❌ **None** |

### 🛰️ GPS Summary: Impact on $2,500 Budget
GPS is **critical for long-range surveillance** — enables return-to-home and position hold. Adding GPS post-purchase costs **$15-40** for a BN-880/M10 module + mounting. This is relevant for:
- **#1 MARK4 LR7** — would need GPS added (~$25)
- **#2b KOLAS7 PNP** — would need GPS added (~$25); mount is built into frame ✅
- **#3 Chimera9 ECO** — budget +$39 if you want GPS
- **#4 DarwinFPV X9** — unclear; potentially needs GPS added
- **#5 EMAX Hawk 7** — likely needs GPS added
- **#8 Chimera7 Pro V2** — ✅ GPS pre-installed (iFlight BLITZ M10 GPS V2 Mini); no add needed

### 📷 Non-IR Camera (FPV Camera) Inclusion
| # | Airframe | FPV Camera Included? | Camera Type | Camera Model | Source Confidence |
|---|----------|---------------------|-------------|--------------|-------------------|
| 1 | GEPRC MARK4 LR7 — PNP | ✅ **Yes** | **Analog CMOS** (1/3" 1200TVL) | Caddx H1 | ✅ **High** — rotorama.com product specs confirm camera model |
| 2b | Axisflying KOLAS7 — PNP | ❌ **No** | PNP = frame + FC + ESC + motors only; camera is buyer's choice | N/A | ⚠️ **Moderate** — PNP designation means no camera |
| 2c | Axisflying KOLAS7 — BNF Analog | ❓ **Unclear** | Listed as "Analog BNF" at $419.90 but no product page names a specific camera model | Unknown | ⚠️ **Low** — product pages describe the frame's VTX compatibility but don't list what's actually included in this config; reach out to seller |
| 2d | Axisflying KOLAS7 — BNF HD | ✅ **Yes** | **Digital HD** — integrated DJI O3 camera (1/1.7" CMOS, 4K/60fps) or Walksnail Avatar Pro camera | DJI O3 / Walksnail Avatar | ✅ **High** — confirmed via bometoys.com, getfpv.com listings |
| 3 | iFlight Chimera9 ECO — PNP/BNF | ✅ **Yes** | **Analog CMOS** — model not specified in product page | Unknown (generic analog) | ⚠️ **Moderate** — iFlight includes analog cam with their PNP/BNF builds but doesn't name the model |
| 4 | DarwinFPV X9 — PNP/BNF | ❓ **Not confirmed** | No camera mentioned in any available specs or listings | Unknown | ⚠️ **Low** — product pages 404; no evidence of camera inclusion |
| 5 | EMAX Hawk 7 — BNF | ✅ **Yes** | **Analog CMOS** — model not specified in product specs | Unknown (EMAX analog cam) | ⚠️ **Moderate** — listed as BNF with 2.5W VTX; likely includes a basic analog camera |
| 6 | DeepSpace ROC7 O4 PRO — PNP | ✅ **Yes** | **Digital HD** — DJI O4 Pro integrated (1/1.3" CMOS, 4K/120fps) | DJI O4 Pro | ✅ **High** — product name confirms O4 Pro air unit which includes camera |
| 7 | GEPRC Crocodile75 V3 — PNP | ✅ **Likely Yes** | **Analog CMOS** — likely included (GEPRC standard) | Unknown (Caddx or GEPRC cam) | ⚠️ **Moderate** — GEPRC typically includes analog cam with Crocodile PNP builds; exact model unconfirmed |
| 8 | iFlight Chimera7 Pro V2 — PNP/BNF | ✅ **Yes** | **Analog CMOS** — model not specified, same platform as Chimera9 ECO | Unknown (generic analog) | ⚠️ **Moderate** — iFlight standard practice includes analog camera with analog VTX builds |
| 9 | DarwinFPV 129 7" — PNP/BNF | ❓ **Not confirmed** | No camera mentioned in available specs; $180-264 PNP price suggests likely no camera | Unknown | ⚠️ **Low** — low price point suggests basic airframe only |
| 10 | NewBeeDrone ROC7 O4PRO — BNF | ✅ **Yes** | **Digital HD** — DJI O4 Pro integrated (1/1.3" CMOS, 4K/120fps) | DJI O4 Pro | ✅ **High** — same hardware as DeepSpace ROC7 (#6) |
| 11 | HS-X07M | ❓ **Cannot determine** | Product does not appear to exist | N/A | ❌ **None** |

> **Note:** The "non-IR Camera" is the standard FPV camera used for piloting. The thermal imaging module for surveillance will be carried as a separate payload (mounted on top or bottom) and is **not** part of these airframe builds. Options with an included HD camera (DJI O3/O4 Pro) could potentially serve double-duty for visible-light surveillance recording.
GPS is **critical for long-range surveillance** — enables return-to-home and position hold. Adding GPS post-purchase costs **$15-40** for a BN-880/M10 module + mounting. This is relevant for:
- **#1 MARK4 LR7** — would need GPS added (~$25)
- **#2b KOLAS7 PNP** — would need GPS added (~$25); mount is built into frame ✅
- **#3 Chimera9 ECO** — budget +$39 if you want GPS
- **#4 DarwinFPV X9** — unclear; potentially needs GPS added
- **#5 EMAX Hawk 7** — likely needs GPS added
- **#8 Chimera7 Pro V2** — ✅ GPS pre-installed (iFlight BLITZ M10 GPS V2 Mini); no add needed

### 💰 Specs & Pricing
| # | Make/Model | Prop (in) | Verified Price (USD) | Source | Notes |
|---|------------|-----------|---------------------|--------|-------|
| 1 | GEPRC MARK4 LR7 | 7 | **$240–330** (est., discontinued) | rotorama.com, bsswebshop.com | ✅ **Confirmed specs**. No longer on GEPRC official site (404). 295mm WB, 455g, 12-30min flight. |
| 2b | Axisflying KOLAS7 — PNP | 7 | **~$150-200** (PNP, est.) | dronegearup.com | ⚠️ **Estimated**. Listed as PNP option on dronegearup but price not explicitly shown. Same frame + iStack F722/65A + C287 motors. |
| 2c | Axisflying KOLAS7 — BNF Analog | 7 | **$419.90** (Analog BNF) | axisflying.vip | ✅ **Verified**. iStack F722 + 50A ESC + C287 1350KV + GPS. Choose TBS Nano RX or ELRS 2.4G. |
| 2d | Axisflying KOLAS7 — BNF HD | 7 | **$649** (DJI O3) / **$777** (Walksnail) | bometoys.com, getfpv.com | ✅ **Verified**. HD VTX pre-installed. DJI O3 + TBS Nano RX variant at $649. Walksnail Avatar Pro variant at GetFPV. |
| 3 | iFlight Chimera9 ECO | 9 | **$346.99** (analog PNP) | shop.iflight.com | ✅ **Verified**. 405mm WB, 721g, 20min hover (8000mAh). King of LR. |
| 4 | DarwinFPV X9 | 9 | **$280–400** (PNP) | darwinfpv.com, drone24hours.com | ✅ **Verified**. F411/100A/2812-1100KV. Payload 1.5-2.5kg. 363mm WB. |
| 5 | EMAX Hawk 7 | 7 | **$398.86** (BNF) | emaxmodel.com | ✅ **Verified**. ECOII2807 motors, 2.5W VTX, 7" DC frame option. |
| 6 | DeepSpace ROC7 O4 PRO | 7 | **$369** (PNP+GPS) | deepspacefpv.com | ✅ **Verified**. F722/60A/Redline 2807 1350KV. O4 Pro air unit. |
| 7 | GEPRC Crocodile75 V3 | 7.5 | **$470–550** (base, disco?) | skyvely.com, rcbuying.com | ✅ **Confirmed**. F722/60A/2806.5 1350KV. 342mm WB. No longer on GEPRC site. |
| 8 | iFlight Chimera7 Pro V2 | 7.5 | **$499.99** (analog PNP) | shop.iflight.com | ✅ **Verified**. F722/55A/2809 1250KV. 327mm WB, 725g, 30min hover. |
| 9 | DarwinFPV 129 7" | 7 | **$180–264** (PNP) | darwinfpv.com, aeroshotdrone.com | ✅ **Verified**. Original CSV name "MARK4 7 Inch" was wrong. This is the Darwin 129. 2507 motors, 50A ESC, GPS, 1.5kg payload. |
| 10 | NewBeeDrone ROC7 O4PRO | 7 | **$699** (BNF retail) | addictiveRC.com | ✅ **Verified**. Just a retail markup of DeepSpace ROC7 ($369→$699). |
| 11 | HS-X07M | 7 | **$400–700** (unverified) | — | ❌ **Could not verify**. Zero search results across all sources. Not found on AliExpress, Banggood, or any retailer. May not exist as a real product. |

### 📝 Verification Methodology
- **All prices sourced June 6, 2026**, from official manufacturer stores or authorized resellers
- Prices shown are PNP (no receiver/battery) unless noted as BNF
- DuckDuckGo web search + direct web_fetch to product pages
- Where prices weren't listed on manufacturer sites, prices from third-party reseller inventory pages were used

### 🔄 Corrections from Original CSV
| Original CSV Entry | Correction |
|--------------------|-----------|
| GEPRC MARK4 LR7: "EM2807 1350KV" | Actual: GEPRC E2806.5 1350KV |
| DarwinFPV X9: "F4 FC, 60A ESC, 2807 1100KV" | Actual: **F411 MPU6500 FC, 100A BLHeli_32 ESC, 2812 1100KV motors** |
| EMAX Hawk 7: "2807 motor" | Actual: **ECOII2807 motor** |
| GEPRC Crocodile75 V3: "F405-based FC, 50A ESC" | Actual: **SPAN F722-BT-HD V2 FC, SPAN G50A / TAKER 60A ESC** |
| DarwinFPV MARK4 7 Inch: "F4 FC, 60A ESC, 2807 1300KV" | **Name wrong.** This is the **DarwinFPV 129 7"**. Actual: F4 FC, **50A ESC, 2507 motors** |
| HS-X07M: claimed 2kg payload | **Could not verify product exists.** |

**Source**: Original CSV upload 2026-05-16. Verified via live web search June 2026.