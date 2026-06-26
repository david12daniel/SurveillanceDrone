# Model Issues & Corrections Log

> Tracking known data-quality issues in the SysML v2 model (`model.md` / `model.sysml`) and supporting candidate CSVs.

---

## §D — BNF As-Built Mass Understatement

**Status:** ✅ Fixed (2026-06-25)

**Issue:**  
PNP and BNF variants of the same airframe shared one bare-frame mass in `airframe-candidates.csv`. The PNP mass excluded VTX, camera, GPS, and receiver, while the BNF variant includes them. Since BNFs carried the same (lower) PNP mass, bundled-electronics weight was understated — mildly favoring BNF builds in rank scoring.

**Affected rows:**  
- Axisflying KOLAS7 BNF Analog (#2b): 257g → 302g (est.)
- Axisflying KOLAS7 BNF HD (#2c): 257g → 312g (est.)
- iFlight Chimera9 ECO BNF (#3b): 721g → 726g (est.)
- iFlight Chimera7 Pro V2 BNF (#8b): 725g → 730g (est.)

**Correction:**  
Estimated BNF masses by summing: bare-frame mass + VTX (~15g analog / ~40g DJI O3) + camera (~15g) + GPS (~10g) + receiver (~5g).

**Impact:**  
All original verified masses (455g, 257g, 721g, 725g) were PNP bare-frame masses from manufacturer specs — they were never wrong. The BNF rows simply needed their own mass column. Rank ordering may shift slightly since BNF variants no longer share their lighter PNP sibling's mass.

---

## §B4 — Missing Airframe Masses (7 Frames)

**Status:** ✅ Fixed (2026-06-25)

**Issue:**  
Seven of 15 airframe rows had `N/A` for `Airframe Wt (g)` — they were excluded from any mass-based analysis.

**Affected rows and resolved values:**

| ID | Airframe | Purchase Type | Mass | Source |
|----|----------|--------------|------|--------|
| 4a | DarwinFPV X9 | PNP | ~664g (est.) | 287.8g frame (darwinfpv.com) + 4×71.6g motors (offthegridsun.com) + stack/VTX/cam |
| 5 | EMAX Hawk 7 | BNF | ~550g | Alibaba listing: "Weight around 550g" |
| 6a | DeepSpace ROC7 O4 PRO | PNP+GPS | ~672g | unmanned.tech review: "672 grams with O4 Pro" |
| 6b | DeepSpace ROC7 O4 PRO | BNF | ~677g (est.) | 672g + RX (~5g) |
| 7 | GEPRC Crocodile75 V3 | PNP | ~593g (est.) | Frame 235g (readymaderc.com); Analog BNF 597.5g (onbuy.com) minus RX |
| 9a | DarwinFPV 129 7" | PNP | ~360g (est.) | 4×39g motors (myfpvstore.com) + frame est. + stack/VTX/GPS |
| 10 | NewBeeDrone ROC7 O4PRO | BNF only | ~672g (est.) | Same hardware as DeepSpace ROC7 |

**Methodology:**  
- **Verified masses** (ticked ✓) from manufacturer specs or independent reviews
- **Estimated masses** (marked "est.") are derived by summing known component weights (frame + motors + FC stack + VTX + camera + GPS + hardware)
- Estimates use a ±10% margin — refined masses should be substituted if published specs become available

---

## §C8 — CSV Column Expansion (DVR Port Types)

**Status:** ✅ Fixed (2026-06-24)

**Issue:**  
`thermal_dvr_candidates.csv` had `Video Input` (CVBS analog) and `Video Pass-Through` (yes/no) but no info on physical connector types or pass-through wiring method — essential for integration planning.

**Correction:**  
Added two columns:  
1. `Input Port Type` — physical connector (e.g., solder pads, JST-SH 1.0mm, 3.5mm TRRS, pigtail leads)  
2. `Pass-Through Wiring Method` — how the inline wiring is routed (direct solder, breakout cable, pre-wired pigtails)

All 7 DVR candidates updated.

---

## Open Items

| ID | Description | Priority | Status |
|----|------------|----------|--------|
| E1 | Verify DarwinFPV X9 PNP mass with scale measurement (estimated ~664g) | Low | Pending |
| E2 | Verify DarwinFPV 129 PNP mass with scale measurement (estimated ~360g) | Low | Pending |
| E3 | Verify Crocodile75 V3 PNP mass (estimated ~593g from BNF 597.5g minus RX) | Low | Pending |
| E4 | Add camera subsystem mass breakouts (thermal camera body + lens + cable) | Medium | Not started |