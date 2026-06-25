# Comprehensive Thermal Camera Market Analysis

## 640×512 LWIR Modules Under $1,000

**Project:** Thermal Surveillance Drone  
**Date:** 2026-06-06  
**Purpose:** Identify every commercially available 640×512 thermal camera module under $1,000 USD that could satisfy CameraSubsystem requirements (R3_CAM_WT ≤200g, R3_CAM_PWR ≤4.5W, R3_CAM_FOV ≥30° HFOV, R3_CAM_NETD ≤50mK, R3_CAM_RES, R3_CAM_COST ≤$600, R3_CAM_IF).

---

## 1. Tier Summary

| Tier | Description | Price Range | Count |
|---|---|---|---|
| **A** | Under $600, meets all requirements | ~$350–$600 | ~5+ options |
| **B** | $600–$1,000, viable if budget stretches | ~$600–$850 | ~4 options |
| **C** | Under $1,000 but requires significant qualification | varies | ~3+ options |
| **D** | Reference only (over $1,000 new) | $4,200+ | 2 options |

---

## 2. Tier A — Under $600 (Within Camera Budget)

### A1. PurpleRiver Mini 640 — BEST OVERALL PICK

**Source:** [thermal-image.com](https://www.thermal-image.com/product/mini-640-uncooled-lwir-thermal-camera-module/) / purpleriver.en.alibaba.com

| Spec | Value | Meets Req? |
|---|---|---|
| Resolution | 640 × 512 | ✅ |
| Pixel pitch | 12 µm | ✅ |
| NETD | ≤ 50 mK (≤ 40 mK optional) | ✅ R3_CAM_NETD |
| HFOV (13mm lens) | 31.9° × 25.7° | ✅ R3_CAM_FOV (≥30°, just barely) |
| HFOV (9.1mm lens) | 48.7° × 38.6° | ✅ (exceeds) |
| Mass | < 20 g (without lens) | ✅ R3_CAM_WT |
| Power | < 0.5 W typ | ✅ R3_CAM_PWR |
| Frame rate | 25 Hz (radiometric) / 60 Hz (non-radiometric) | ✅ |
| Video out | CVBS analog + USB + MIPI | ✅ R3_CAM_IF |
| **Price (base, no lens)** | **~$399** | ✅ |
| **Price (with 13mm lens)** | **~$400–$550 (est.)** | ✅ R3_CAM_COST |
| Lens options | 4, 7, 9, 13, 15, 18, 25, 35, 50, 60, 75mm | ✅ |
| Operating temp | −40°C to +80°C | ✅ |
| Size | 21 × 21 mm (w/o lens) | ✅ |
| Supplier | Guangzhou Purple River Electronic Technology Co. | — |

**Notes:**
- Alibaba listing shows $399–$1,620 range, lower end for bare module
- 60 Hz non-radiometric version preferred for FPV (lower latency)
- 13mm lens hits 31.9° HFOV (just over the 30° requirement)
- 9.1mm lens gives 48.7° HFOV but trades off pixel resolution on target
- Established Alibaba supplier with 1-year warranty

**Verdict: ✅ Best candidate. $399 base, likely $450–$500 with lens shipped.**

---

### A2. Vcan2170 Mini-640-CVBS (ivcan.com)

**Source:** [ivcan.com](https://ivcan.com/p/uncooled-640x512-12um-lwir-thermal-camera-module/)

| Spec | Value | Meets Req? |
|---|---|---|
| Resolution | 640 × 512 | ✅ |
| Pixel pitch | 12 µm | ✅ |
| NETD | ≤ 40 mK @ F1.0 | ✅ (exceeds) |
| HFOV (9.1mm lens) | 45.9° × 36.9° | ✅ |
| HFOV (13mm lens) | 32.9° × 26.6° | ✅ (≥30°) |
| Mass | 21 g (without lens) | ✅ R3_CAM_WT |
| Power | < 0.75 W typ | ✅ R3_CAM_PWR |
| Frame rate | 50 fps | ✅ |
| Video out | CVBS + USB 2.0 | ✅ |
| Color palettes | 18 (white/black hot, fusion, etc.) | ✅ |
| Operating temp | −40°C to +70°C | ✅ |
| Size | 17.3 × 17.3 × 35.6 mm | ✅ |
| **Price** | **~$400–$500 (est., must request quote)** | Likely ✅ |
| UART control | Yes (3.3V) | ✅ |

**Notes:**
- Thinner module (17.3mm) than PurpleRiver (21mm)
- Slightly higher power (0.75W vs 0.5W) but still well under 4.5W limit
- Wide voltage input (4.5–20V DC) — simple to integrate
- Price not listed — requires inquiry, expected competitive with PurpleRiver
- Ships with CVBS expansion board (USB + analog + UART)

**Verdict: ✅ Strong competitor if pricing confirmed under $600.**

---

### A3. Arducam 640×512 USB / CVBS Module

**Source:** [arducam.com](https://www.arducam.com/arducam-640x512-12mm-60hz-analog-cvbs-thermal-imaging-module-ultra-low-latency-infrared-camera-with-9-1mm-lens-for-fpv-security-industrial-monitoring.html)

| Spec | Value | Meets Req? |
|---|---|---|
| Resolution | 640 × 512 | ✅ |
| Pixel pitch | 12 µm | ✅ |
| NETD | ≤ 40 mK (claimed) | ✅ (exceeds) |
| HFOV (9.1mm lens) | ~48° × 38° | ✅ |
| Mass | ~20 g | ✅ |
| Power | Low (not specified) | Likely ✅ |
| Frame rate | 60 Hz (CVBS version) | ✅ |
| Video out | USB 2.0 UVC **or** CVBS analog | ✅ |
| **Price** | **~$500–$650 (est.)** | Borderline |
| Operating temp | Industrial range | ✅ |

**Notes:**
- Two versions: USB (50Hz, radiometric) and CVBS (60Hz, analog, ultra-low latency)
- Arducam is a well-known brand in the camera module space — easier purchase than Alibaba
- Self-developed 12µm core (likely from the same Chinese foundries as PurpleRiver/VCAN)
- Lightweight 20g package ideal for drones
- CVBS version is purpose-built for FPV (60Hz, no USB processing delay)
- USB version has Windows/Linux SDK support

**Verdict: ✅ Good option if available at ~$500–$550. Check actual store pricing.**

---

### A4. Guide COIN612R (Wuhan Guide Infrared)

**Source:** [guideinfrared.en.made-in-china.com](https://guideinfrared.en.made-in-china.com/) / [gst-ir.net](https://www.gst-ir.net/products/uncooled-thermal-modules/coin-series-wlp+asic-uncooled-thermal-modules/coin612.html)  
Also on: Amazon ~$450–$700, eBay ~$400–$600

| Spec | Value | Meets Req? |
|---|---|---|
| Resolution | 640 × 512 | ✅ |
| Pixel pitch | 12 µm (WLP) | ✅ |
| NETD | ≤ 40 mK | ✅ (exceeds) |
| HFOV (9.1mm lens) | ~48° × 38° | ✅ |
| HFOV (13mm lens) | 31.9° × 25.7° | ✅ |
| HFOV (19mm lens) | ~22° × 17° | ❌ (too narrow) |
| Mass | 27 g (with 9.1mm lens) | ✅ (<200g) |
| Mass (13mm) | 40 g | ✅ |
| Power | 0.9 W | ✅ R3_CAM_PWR |
| Frame rate | 25/30 Hz | ✅ |
| Video out | PAL/NTSC analog + RAW/YUV/BT656 digital | ✅ |
| Digital zoom | 1–8× continuous | ✅ |
| Operating temp | −40°C to +70°C | ✅ |
| IP rating | IP67 (front surface) | ✅ |
| **Price (eBay/AliExpress)** | **~$400–$700** | ✅ (may be negotiable) |
| **Price (Amazon)** | **~$450–$700** | ✅ |

**Notes:**
- Manufactured by **Wuhan Guide Infrared Co.** — a major Chinese infrared OEM (also produces detectors for other brands)
- Uses wafer-level package (WLP) detector instead of ceramic package — smaller and cheaper
- Higher power (0.9W) than PurpleRiver (0.5W) but still well under 4.5W
- Slightly heavier (27–40g with lens) but still under 200g
- Radiometric version available (temperature measurement)
- Comes with SDK for Windows/Linux/ARM
- Available on Amazon and eBay with US shipping — easier to buy than Alibaba

**Verdict: ✅ Viable option if ~$400–$550. Higher weight and power than PurpleRiver but still within limits.**

---

### A5. Generic 640×512 FPV Modules (eBay / AliExpress)

Multiple sellers offer generic 640×512 modules using the same Chinese VOx core foundries. Examples found:

| Listing | Price | Lens | Video | Notes |
|---|---|---|---|---|
| "JS 640X512 9.1mm Lens" (eBay) | ~$550–$580 | 9.1mm | CVBS | Free shipping |
| "640X512 13mm/19mm Lens" (eBay) | ~$520 | 13mm/19mm | CVBS | Seller: e-for-uav |
| "640X512 50mm Lens" (Thanksbuyer) | ~$794 | 50mm | CVBS | Over $600, narrow FOV |
| "640x512 FPV Thermal" (Amazon) | ~$400–$700 | 9mm | CVBS | Multiple sellers |
| "640x512 USB Thermal" (Alibaba, MOQ 2) | ~$358–$398 | varies | USB/CVBS | MOQ may be issue |

**Notes:**
- These are likely the same underlying VOx core from GST/Guide/BST foundries
- Quality and support vary significantly by seller
- Some require MOQ (minimum order quantity) of 2+ pieces
- Weight, power, and NETD specifications may not be independently verified
- Often identical specifications to PurpleRiver/VCAN modules

**Verdict: ⚠️ Use with caution. Cheapest option but highest risk. Price is right if you find a reputable seller.**

---

## 3. Tier B — $600–$1,000 (Budget Stretch)

### B1. Axisflying GE-3F 640

**Source:** skyfpv.shop ($680–$690), banggood (~$854), axisflying.com

| Spec | Value | Meets Req? |
|---|---|---|
| Resolution | 640 × 512 | ✅ |
| Detector | VOx uncooled | ✅ |
| NETD | ≤ 40 mK | ✅ (exceeds R3_CAM_NETD) |
| HFOV (13.5mm lens) | 31.9° × 25.7° | ✅ R3_CAM_FOV (≥30°) |
| Frame rate | 60 fps | ✅ (excellent) |
| Video out | CVBS analog | ✅ |
| Mass | ~20 g | ✅ |
| **Price** | **$680–$854** | ❌ Over $600 |
| Lens options | 9.1mm, 13.5mm, 18mm | ✅ |

**Notes:**
- Best NETD in this class (40 mK)
- 60 fps is excellent for FPV (smooth video)
- Available through Amazon, Banggood, Axisflying direct
- ~$80–$250 over camera budget, but close enough to negotiate
- Banggood lists at $854, skyfpv at $680 — shows price variance

**Verdict: ⚠️ Slightly over budget but may be negotiable. Best specs in class.**

---

### B2. GST iTL612R Pro — Ultra-Light Drone Core

**Source:** [aliexpress](https://www.aliexpress.com/item/1005010008688639.html), [gst-ir.net](https://www.gst-ir.net/products/uncooled-thermal-modules/itl-thermal-modules/itl612g2.html)

| Spec | Value | Meets Req? |
|---|---|---|
| Resolution | 640 × 512 | ✅ |
| Pixel pitch | 12 µm | ✅ |
| NETD | ≤ 40 mK | ✅ |
| Mass | ~20 g (with 9.1mm lens) | ✅ |
| Power | 0.7 W typ | ✅ |
| Video out | CMOS8/USB 2.0, BT656 | ✅ |
| Frame rate | 30 Hz | ✅ |
| Operating temp | −40°C to +70°C | ✅ |
| **Price (AliExpress)** | **~$1,230** | ❌ Over budget by 2× |
| Lens options | 9.1mm (only) | ⚠️ Limited |

**Notes:**
- Made by Global Sensor Technology (GST) — a major detector manufacturer
- Ultra-compact: 21 × 22.3 × 27.3mm with lens
- Excellent SDK support (Windows/Linux/ARM)
- Price on AliExpress is $1,230 — well over budget
- May be available cheaper direct from GST or through Alibaba negotiation

**Verdict: ❌ Too expensive at retail. Only worth pursuing at sub-$600 via direct negotiation.**

---

### B3. UV640-9 (Various Sellers)

**Source:** Aliexpress, Auvidea, CaseeDa, Hdaniee, various Alibaba sellers

| Spec | Value | Meets Req? |
|---|---|---|
| Resolution | 640 × 512 | ✅ |
| Pixel pitch | 12 µm | ✅ |
| NETD | ≤ 40–50 mK (varies) | ✅ |
| HFOV (9.1mm lens) | ~48° × 38° | ✅ |
| Mass | ~20 g | ✅ |
| Video out | USB 2.0 UVC | ✅ (digital) |
| **Price (AliExpress)** | **~$300–$500 (est.)** | Possibly ✅ |
| **Price (Auvidea with adapter)** | **~€400–€500** | Possibly ✅ |
| MOQ (Alibaba) | 1–2 pieces | ⚠️ |

**Notes:**
- "UV640" appears to be a reference design / white-label module sold by multiple Chinese vendors
- Available with USB-only output (no analog CVBS) — may need additional adapter for FPV
- Auvidea sells an upgraded version with shielded connectors and coax adapter for NVIDIA Jetson
- CETHERMAL sells UV Series with claimed <35 mK sensitivity and <12ms latency
- Wide price range depending on seller and lens configuration

**Verdict: ⚠️ Promising but inconsistent. Price and quality depend heavily on specific seller.**

---

## 4. Tier C — Under $1,000 but Requires Significant Qualification

### C1. Used / Surplus FLIR Tau 2 640

**Source:** eBay, EEVblog forums, drone surplus

| Spec | Value | Meets Req? |
|---|---|---|
| Resolution | 640 × 512 | ✅ |
| Detector | VOx (FLIR proven) | ✅ |
| NETD | ≤ 50 mK | ✅ |
| Mass | ~35 g (module), ~80 g (with lens) | ✅ (but heavier) |
| Power | ~1.5 W | ✅ |
| Video out | CameraLink / analog | ⚠️ (may need interface board) |
| **Price (used)** | **~$300–$700** | ✅ (used) |
| Status | **EOL (End of Life, June 2025)** | ⚠️ No manufacturer support |

**Notes:**
- FLIR announced Tau 2 EOL as of June 2025 — no longer sold new
- Used/surplus market is the only source
- Requires 50-pin Hirose connector and interface board (adds cost and complexity)
- CameraLink output is not plug-and-play with typical FPV VTX
- Proven in countless drone projects, excellent image quality
- Priced at $599 on eBay for a 640 30Hz unit with 25mm lens — very competitive
- Heavier and higher power than modern Chinese modules

**Verdict: ⚠️ High risk due to EOL, interface complexity, and variable condition. Could be viable if you find a clean unit with interface board.**

### C2. InfiRay Micro III S 640 (M3S6)

**Source:** AliExpress, eBay, Alibaba

| Spec | Value | Meets Req? |
|---|---|---|
| Resolution | 640 × 512 | ✅ |
| Detector | XCore VOx (InfiRay) | ✅ |
| NETD | ≤ 40 mK | ✅ (exceeds) |
| HFOV (13mm lens) | 33° × 26° | ✅ (≥30°) |
| Mass | ~20 g | ✅ |
| Power | ~0.8 W | ✅ |
| Video out | BT.656, USB-C | ✅ |
| Frame rate | 50 Hz | ✅ |
| **Price (Alibaba, B2B)** | **~$800–$1,520** | ❌ Over $600 |
| **Price (AliExpress retail)** | **~$600–$1,500** | ❌ / ⚠️ |
| **Price (eBay)** | **~$700+** | ❌ |

**Notes:**
- InfiRay is a top-tier Chinese thermal sensor manufacturer (competitor to FLIR)
- The Micro III S has a dedicated FPV variant (M3S601201312X00NPX) with BT.656 analog output
- Widely used in the FPV drone community
- Single-unit pricing appears to be $800+ — significantly over the $600 camera budget
- Some AliExpress listings may be lower but require investigation
- Strong SDK and Linux support

**Verdict: ❌ Exceeds $600 budget at single-unit retail. Only viable if found used/sub-$600.**

---

## 5. Tier D — Reference Only (Well Over $1,000)

These are the industry gold standards — included for performance comparison only.

| Module | Price | Mass | NETD | Power | Why out of budget |
|---|---|---|---|---|---|
| **FLIR Boson 640** (14mm, 32°) | $4,232–$6,450 | 7.5 g (no lens) | ≤ 50 mK | 0.5–1.0 W | 7–10× budget |
| **FLIR Boson+ 640** (14mm, 32°) | $4,448 | 7.5 g | ≤ 20 mK | 0.9 W | 7× budget |

The Boson is the benchmark every other module is compared against. The Chinese modules copy the Boson's 21×21mm form factor and interface philosophy but at 10–15% of the cost.

---

## 6. Lens Selection Analysis

For the 30° HFOV requirement, the key question is which lens focal length to choose.

| Focal Length | HFOV | IFOV (640 wide) | GSD @ 90 m | Px on 0.5 m @ 90 m | Best for |
|---|---|---|---|---|---|
| 9.1 mm | ~48° × 38° | 1.31 mrad | 11.8 cm | 4.2 px | Wide area scans (detection) |
| **13 mm** | **~32° × 26°** | **0.87 mrad** | **7.8 cm** | **6.4 px** | **Best balance (meets 30°)** |
| 15 mm | ~29° × 23° | 0.79 mrad | 7.1 cm | 7.0 px | Better resolution, fails FOV req |
| 18 mm | ~24° × 19° | 0.66 mrad | 5.9 cm | 8.4 px | Best classification, FOV too narrow |
| 25 mm | ~18° × 14° | 0.48 mrad | 4.3 cm | 11.5 px | Long range, way too narrow |
| 35 mm | ~13° × 10° | 0.34 mrad | 3.1 cm | 16.2 px | Spotlighting only |

**The 13mm lens is the sweet spot.** It hits 32° HFOV (barely meeting ≥30°), gives 6.4 px on a 0.5 m target at 90 m, and keeps ground swath at ~52 m. 

The 9.1mm option gives wider area coverage (48° HFOV) but drops to 4.2 px on target — barely meeting R3_CAM_RES (4 px). The 15mm gives better resolution but fails the FOV requirement.

---

## 7. Camera Subsystem Budget Impact (Best Candidates)

Assuming 13mm lens on the best candidates:

| Candidate | Module | Lens | Shipping/Adapter | Total | Within $600? |
|---|---|---|---|---|---|
| **PurpleRiver Mini 640** | $399 | ~$60 | ~$20 | **~$479** | ✅ (21% margin) |
| **Vcan2170 Mini-640-CVBS** | ~$400 | ~$60 | ~$20 | **~$480** | ✅ (20% margin) |
| **Arducam 640×512 CVBS** | ~$500 | Included | ~$15 | **~$515** | ✅ (14% margin) |
| **Guide COIN612R** | ~$450 | ~$50 | ~$15 | **~$515** | ✅ (14% margin) |
| **Generic eBay 640×512** | ~$520 | Included | Free | **~$520** | ✅ (13% margin) |
| **Axisflying GE-3F 640** | $680 | Included | ~$15 | **~$695** | ❌ (16% over) |
| **InfiRay Micro III S** | ~$800 | Included | ~$15 | **~$815** | ❌ (36% over) |

---

## 8. Requirement Compliance Matrix

| Candidate | Cost ≤$600 | Mass ≤200g | Power ≤4.5W | FOV ≥30° | NETD ≤50mK | Video IF | Source Risk |
|---|---|---|---|---|---|---|---|
| PurpleRiver Mini 640 | ✅ | ✅ | ✅ | ✅ (13mm) | ✅ | CVBS+USB | Medium (Alibaba) |
| Vcan2170 | ✅ | ✅ | ✅ | ✅ (13mm) | ✅ (40mK) | CVBS+USB | Medium (ivcan.com) |
| Arducam 640×512 | ✅ | ✅ | ✅ | ✅ (9mm) | ✅ (40mK) | CVBS or USB | Low (Amazon/Arducam) |
| Guide COIN612R | ✅ | ✅ | ✅ | ✅ (13mm) | ✅ (40mK) | PAL+USB | Low (Amazon/eBay) |
| Generic FPV 640 | ✅ | ✅ | ✅ | varies | varies | CVBS | High (unknown) |
| Axisflying GE-3F | ❌ | ✅ | ✅ | ✅ (13mm) | ✅ (40mK) | CVBS | Low (Amazon/retail) |
| InfiRay Micro III S | ❌ | ✅ | ✅ | ✅ (13mm) | ✅ (40mK) | BT.656 | Low (AliExpress) |
| FLIR Tau 2 (used) | ✅ | ✅ (heavy) | ✅ | ✅ (19mm) | ✅ | CameraLink | High (EOL, adapter) |
| FLIR Boson 640 | ❌ | ✅ | ✅ | ✅ | ✅ | CMOS/USB | Low (distributor) |

---

## 9. Final Ranking

### Top Recommendation

**1. PurpleRiver Mini 640 with 13mm lens** (~$479 total)
- Lowest price, meets all requirements, known supplier
- < 20g, < 0.5W, CVBS analog output
- 31.9° HFOV just clears the 30° threshold
- Good margin ($121 under $600 cap)

### Strong Alternatives

**2. Guide COIN612R with 13mm lens** (~$515 total)
- Available on Amazon with US shipping
- Slightly heavier (40g with lens), higher power (0.9W)
- IP67 front, radiometric option, excellent SDK
- More established brand (Wuhan Guide Infrared)

**3. Arducam 640×512 CVBS** (~$515 total)
- Easy purchase through established retailer
- 60Hz frame rate (best for FPV)
- 9.1mm lens gives wide 48° HFOV
- Lower pixels-on-target with 9.1mm lens (4.2 px)

### If Budget Allows ($680–$700)

**4. Axisflying GE-3F 640** (~$695 total)
- Best NETD (40 mK), best frame rate (60 Hz)
- Slightly over $600 cap but may be negotiable
- Available through Amazon with easy returns

### Not Recommended

- **InfiRay Micro III S** — too expensive for single unit
- **FLIR Boson** — $4k+ is non-starter
- **FLIR Tau 2** — EOL, interface complexity, uncertain condition
- **Generic no-name modules** — quality and support unknown

---

## 10. Next Steps

1. **Contact PurpleRiver** for live single-unit pricing with 13mm lens + CVBS adapter + shipping
2. **Check Arducam store** directly for 640×512 CVBS module pricing
3. **Order a Guide COIN612R** from Amazon if immediate testing is desired (easiest purchase path)
4. **Run thermal_camera_analysis.py** against candidate specs to verify pixels-on-target
5. **Proceed to SBC trade study** — the camera interface (CVBS vs USB) drives SBC selection