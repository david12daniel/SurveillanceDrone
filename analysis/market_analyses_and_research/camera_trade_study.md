# Thermal Camera Component Trade Study

## Purpose
Identify commercially-available 640×512 LWIR thermal camera modules that satisfy the CameraSubsystem requirements (R3_CAM_WT, R3_CAM_PWR, R3_CAM_FOV, R3_CAM_NETD, R3_CAM_RES, R3_CAM_COST, R3_CAM_IF) within a $2,500 total system budget.

## Requirement Summary (from model.sysml)

| ID | Constraint | Limit |
|---|---|---|
| R3_CAM_WT | Mass | ≤ 200 g |
| R3_CAM_PWR | Avg power | ≤ 4.5 W |
| R3_CAM_FOV | HFOV | ≥ 30° |
| R3_CAM_NETD | Sensitivity | ≤ 50 mK |
| R3_CAM_RES | Pixels on target | ≥ 4 px across 0.5m at 90 m |
| R3_CAM_COST | Cost | ≤ $600 USD |
| R3_CAM_IF | Video out | Analog CVBS or digital (HDMI/CSI/USB) |

## Market Survey — 640×512 Thermal Camera Modules

### Tier 1: Established Western OEM (Out of Budget)

| Module | Price (new) | Status |
|---|---|---|
| FLIR Boson 640 (14mm, 32° HFOV) | $4,232–$6,450 | ❌ Exceeds camera budget by 7× |
| FLIR Boson+ 640 (14mm, 32° HFOV) | $4,448 | ❌ Same |

These are the gold standard for drone thermal imaging (used in DJI, Skydio), but at >$4k they consume nearly 2× the total system budget. Relevant as a performance benchmark only.

### Tier 2: Chinese OEM / FPV Marketplace Modules

| Module | Price | Mass | NETD | Video Out | HFOV (13mm) | Pass R3_CAM_COST? |
|---|---|---|---|---|---|---|
| **PurpleRiver Mini 640** | **$399 – $1,620** | **< 20 g** | **≤ 50 mK** | **CVBS, USB, MIPI** | **31.9°×25.7°** | **✅ Base config at $399** |
| Axisflying GE-3F 640 | $680 – $854 | ~20 g | ≤ 40 mK | CVBS analog | 31.9°×25.7° | ❌ Over $600 (borderline) |
| InfiRay Micro III S 640 (M3S6) | $800 – $1,520 | ~20 g | ≤ 40 mK | BT.656, USB-C | 33°×26° | ❌ Single-unit pricing too high |
| Generic AliExpress 640 module | $300 – $600 (est.) | varies | varies | CVBS/USB | varies | ⚠️ Unknown quality/support |

### PurpleRiver Mini 640 — Most Promising Candidate

**Source:** [thermal-image.com](https://www.thermal-image.com/product/mini-640-uncooled-lwir-thermal-camera-module/) and Alibaba (purpleriver.en.alibaba.com)

**Specs (base model with 13mm lens):**

| Parameter | Value | Meets Requirement? |
|---|---|---|
| Resolution | 640 × 512 | ✅ R3_CAM_RES (6.8 px on 0.5m @ 90m) |
| Pixel pitch | 12 µm | — |
| NETD | ≤ 50 mK (≤ 40 mK optional) | ✅ R3_CAM_NETD |
| HFOV (13mm lens) | 31.9° × 25.7° | ✅ R3_CAM_FOV (≥30°) |
| Mass | < 20 g (without lens) | ✅ R3_CAM_WT (≤200g) |
| Power | < 0.5 W typ | ✅ R3_CAM_PWR (≤4.5W) |
| Video out | CVBS analog + USB + MIPI | ✅ R3_CAM_IF (analog CVBS) |
| Base price (no lens) | ~$399 | ✅ R3_CAM_COST (≤$600) |
| With 13mm lens | ~$450–$550 (est.) | ✅ |
| Operating temp | −40°C to +80°C | ✅ |
| Size | 21 × 21 mm (w/o lens) | ✅ |

**Key Details:**
- Uses VOx uncooled detector (same technology as Boson)
- Available in 25 Hz radiometric or 60 Hz non-radiometric variants
- Supports BT.656, MIPI, USB, and CVBS analog output in PAL/NTSC
- Automatic non-uniformity correction, digital detail enhancement
- Optional OEM/ODM customization

### Axisflying GE-3F 640 — Runner-Up

**Specs (13.5mm lens):**

| Parameter | Value | Meets Requirement? |
|---|---|---|
| Resolution | 640 × 512 | ✅ |
| NETD | ≤ 40 mK | ✅ (exceeds) |
| HFOV (13.5mm) | 31.9° × 25.7° | ✅ (≥30°) |
| Frame rate | 60 fps | ✅ |
| Video out | CVBS analog | ✅ |
| Price | ~$680 – $854 | ❌ Over $600 |

Slightly above budget at retail; may be negotiable at volume.

### InfiRay Micro III S 640 (M3S6)

**Price discrepancy noted:** On Alibaba, single-unit pricing appears as both ~$1,500 (from some sellers) and potentially lower on AliExpress/eBay. The actual street price for this module in the FPV community is unclear but likely >$600.

## Budget Impact

If the PurpleRiver Mini 640 base module costs ~$450 with a 13mm lens:

| Camera subsystem | Cost |
|---|---|
| Thermal module + lens | $450 |
| Cabling, bracket, mount | $20 |
| **Camera subsystem total** | **$470** |
| R3_CAM_COST limit | $600 |
| **Margin remaining** | **$130** |

✅ Well within camera budget, leaving $130 for unforeseen costs or a more capable lens.

## Budget allocation check (remaining system)

| Subsystem | Allocation |
|---|---|
| Camera | ~$470 |
| Airframe (frame + motors + ESCs + props + FC) | ~$600 |
| Battery | ~$80 |
| SBC | ~$150 |
| GCS (radio + receiver + display) | ~$500 |
| **Total** | **$1,800** |
| Budget | $2,500 |
| **Margin** | **$700** — healthy |

## Next Steps

1. **Verify PurpleRiver module specs** — confirm NETD ≤ 50 mK, actual available lens options (13mm = ~32° HFOV is ideal), and ability to order single units at the ~$399 base price
2. **If PurpleRiver doesn't pan out:** The Axisflying GE-3F at $680 may be negotiable for single-unit purchase, or we could consider a 384×288 sensor as a cost-down option
3. **Integration test** — ensure CVBS analog output can be received by the selected SBC or VTX
4. **Run the analysis script** against candidate specs to verify pixels-on-target