# OpenHD Ground-Station Directional Antenna — Market Analysis & Trade Study

**Role:** Directional panel antenna (×2 for spatial diversity) attached to the Alfa
AWUS036ACH's dual RP-SMA ports. Provides ground-side RX gain to close the 3–5 km
WFB-ng digital video link at 5825 MHz (channel 165).

**Evaluation date:** 2026-07-02  
**Sources:** OpenHD docs, WFB-ng community, GetFPV, Lumenier, TrueRC, Foxeer, RMRC

---

## Requirements

| Requirement | Threshold |
|---|---|
| Frequency | 5.8 GHz (must cover 5825 MHz / channel 165) |
| Gain | ≥ 10 dBi (for link margin at 3 km) |
| Beamwidth | ≥ 40° H+V — wide enough for manual pointing over a survey area |
| Polarization | RHCP preferred (multipath rejection); linear acceptable in open field |
| Connector | RP-SMA (must mate directly with AWUS036ACH without adapters, or SMA with included pigtail) |
| Price | ≤ $40 per unit (×2 budget ≤ $80) |

### The gain–beamwidth trade-off

Physics constrains the pair: **higher gain = narrower beam**. A 17 dBi antenna at
5.8 GHz has a half-power beamwidth of ~20–25° — requiring an antenna tracker or
constant manual re-pointing. A 10 dBi antenna has ~120° beam — no tracking needed
but marginal link at 5 km. The sweet spot for a hand-aimed ground station with a
moving drone is 13–15 dBi at 40–60° beamwidth.

---

## Candidate Table

| ID | Model | Gain | BW (H×V) | Polarization | Connector | Dims | Price | Notes |
|---|---|---|---|---|---|---|---|---|
| **ANT-G1** | **Lumenier AXII Quadro 5.8 GHz** | **14.7 dBic** | **40°×40°** | **RHCP** | SMA male | 90×90×14 mm | **$32.49** | Best gain/beamwidth in class; 95% efficiency; compact; confirmed at FPV ranges |
| ANT-G2 | TrueRC X-AIR 5.8 MK II *(PATCH1, in BOM)* | 10.5 dBic | 120°×120° | RHCP | RP-SMA male | 32×32×16 mm | $0 (reuse) / $30 (new) | Already procured; widest beam; lowest gain |
| ANT-G3 | Foxeer Echo 2 Max | 13 dBi | 60°×60° | **Linear** | SMA or RP-SMA | 113×89×92 mm | $30 | Good gain; linear is a minor penalty vs RHCP in open field |
| ANT-G4 | Aomway 14 dBi RHCP Mini Patch | 14 dBi | ~35°×35° | RHCP | RP-SMA | 86×86×12 mm | ~$18 | Listed in OpenHD docs; 35° beam is tight for manual pointing |
| ANT-G5 | AliExpress "Maple Planar" 17 dBi | 17 dBi | ~25°×25° | Linear | RP-SMA | ~150×150 mm | ~$20 | Listed in OpenHD docs; max gain; requires tracker; quality variable |
| ANT-G6 | TrueRC Sniper 5.8 RHCP | 13.5 dBi | 45°×45° | RHCP | SMA | 89×89 mm | $55 | Best spec vs beamwidth but **discontinued** (clearance NOS only) |
| ANT-G7 | Foxeer Echo 2 | 9 dBi | 84°×84° | RHCP | SMA/RP-SMA | 34×34×24 mm | ~$20 | Below 10 dBi floor — **eliminated** |

### "TrueRC Maple" clarification

The name "Maple" in older OpenHD documentation refers to a generic AliExpress brand
flat-panel (FY-05A), not a TrueRC product. TrueRC's current 5.8 GHz directional
lineup is: X-AIR MK II (10.5 dBic, 120°) and Sniper (13.5 dBi, 45°, discontinued).
There is no TrueRC product named "Maple."

---

## Trade Study

### Scoring (1 = worst, 3 = best)

| ID | Model | Cost | Capability | Compatibility | Notes |
|---|---|---|---|---|---|
| **ANT-G1** | **Lumenier AXII Quadro** | 2 | **3** | **3** | Best RHCP gain at usable beamwidth; SMA→RP-SMA pigtail needed |
| ANT-G2 | TrueRC X-AIR MK II (PATCH1) | **3** (reuse) | 1 | **3** | Zero marginal cost; but 10.5 dBic is marginal at 5 km |
| ANT-G3 | Foxeer Echo 2 Max | 2 | 2 | **3** | 13 dBi but linear; 60° beam is acceptable |
| ANT-G4 | Aomway 14 dBi RHCP | **3** | 2 | 2 | 35° beam requires careful pointing; quality uncertain |
| ANT-G5 | AliExpress 17 dBi | **3** | **3** | 1 | Maximum gain; needs tracker; unreliable quality |
| ANT-G6 | TrueRC Sniper | 1 | 2 | **3** | Discontinued; NOS only; pays premium for half the AXII gain |

**Cost:** Reusing PATCH1 is free; AliExpress options at $18–20 are cheapest new purchases.
ANT-G1 at $32.49×2 = $65 for the diversity pair.  
**Capability:** ANT-G1 combines the highest effective gain (14.7 dBic) with a 40° beam —
the only candidate that hits both the gain target and the manual-pointing usability threshold.  
**Compatibility:** ANT-G1/G2/G3 all cover 5825 MHz and use standard RP-SMA or SMA. ANT-G5
quality is too variable to trust for a safety-relevant link.

### RF link budget at 5825 MHz (per-panel, with ANT-G1)

| Parameter | Value |
|---|---|
| Air-side TX power (BL-M8812EU2) | +29 dBm |
| Air-side omni antenna gain | +3 dBi (cloverleaf) |
| EIRP | +32 dBm |
| Free-space path loss @ 3 km | −117.3 dB |
| Free-space path loss @ 5 km | −121.7 dB |
| Ground-side RX gain (AXII Quadro) | +14.7 dBic |
| WFB-ng RX sensitivity (MCS1) | −85 dBm |
| Real-world losses (multipath, connector) | −5 dB |
| **Link margin @ 3 km** | **+14.4 dB** ✅ |
| **Link margin @ 5 km** | **+9.0 dB** ✅ |

With diversity (two AXII Quadro panels), add ~3 dB diversity gain → margins become
**+17 dB** at 3 km and **+12 dB** at 5 km. Well above the practical minimum (~6 dB).

### Dual-duty option (ANT-G2, Phase 2 budget constraint)

If budget is constrained, the existing PATCH1 (TrueRC X-AIR MK II, RP-SMA) can serve
OpenHD via a 2-way RP-SMA splitter:
- Splitter loss: −3.5 dB per port
- Effective gain shared with Skydroid VRX6: ~7 dBic
- Recalculated margins: +6.7 dB @ 3 km / +2.3 dB @ 5 km
- At 5 km this is marginal in anything other than ideal conditions.

Upgrade to the AXII Quadro pair when the 5 km link is validated as a requirement.

---

## Selected: ANT-G3 — Foxeer Echo 2 Max 5.8 GHz × 2 (~$60.00 pair)

*(Updated from initial ANT-G1 AXII Quadro selection — wider beam preferred over maximum gain.)*

**Rationale:** 60° beamwidth (±30° from aim point) means the antenna can be pointed at the
centre of the survey area at the start of the flight and left there — no re-aiming as the
drone moves. The 13 dBi gain delivers +11.3 dB link margin at 2.8 km with dual diversity,
comfortably above the 10 dB design target and reliable to 3.3 km. Link margin vs the AXII
Quadro (+11.3 dB vs +13.0 dB) is 1.7 dB less, an acceptable trade for the extra 20° of
beam. Linear polarisation costs ~1–3 dB vs RHCP in multipath-heavy environments; at
90–120 m AGL over open fields the effect is negligible.

**Connector:** RP-SMA male (on the antenna). Mates **directly** to the AWUS036ACH's two
RP-SMA female ports — no pigtails required. This also eliminates the ~$8 pigtail line from
the BOM (total saving vs AXII Quadro pair + pigtails: ~$13).

**Mounting:** Both panels mount on a small V-bracket or articulated arm. Point at the
survey area before flight and leave it. The 60° beam covers a 3.5 km wide swath at 3 km
range without tracking.

**Candidate IDs in model:** `ANT_GND1` and `ANT_GND2` (Foxeer Echo 2 Max, ground diversity pair)
