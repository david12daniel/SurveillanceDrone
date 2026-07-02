# RF Link-Budget Analysis

**Auto-generated** by [`rf_link_budget.py`](rf_link_budget.py). Regenerate: `python analysis/rf_link_budget.py`.

Verifies every RF link meets the **2.8 km** hard range requirement (**R7 / R4_GCS_RANGE**) with a **≥ 10 dB** fade margin, using the selected components ([`SELECTED_COMPONENTS.md`](../SELECTED_COMPONENTS.md)). Free-space path-loss (FSPL) model; the fade margin absorbs real-world excess loss (ground reflection, foliage, multipath, polarisation mismatch).

**FSPL @ 2.8 km:** 5.825 GHz (OpenHD ch 165) = 116.7 dB · 5.8 GHz (analog VTX) = 116.7 dB · 2.4 GHz (ELRS) = 109.0 dB.

## All RF links — summary table

| Link | TX pwr | TX ant | RX ant (eff.) | FSPL | RX power | **Margin @2.8 km** | Reliable range† | Verdict |
|---|--:|--:|--:|--:|--:|--:|--:|:--:|
| Analog FPV video — 5.8 GHz (PATCH1 ground antenna) | 32 dBm | 2 dBi | 10 dBi | 116.7 dB | -74.7 dBm | **+15.3 dB** | 5.2 km | ✅ PASS |
| Analog FPV video — 5.8 GHz (stock omni RX antenna, contrast only) | 32 dBm | 2 dBi | 2 dBi | 116.7 dB | -82.7 dBm | **+7.3 dB** | 2.1 km | ⚠️ THIN |
| Control uplink — 2.4 GHz ELRS (TX12 MkII → iFlight TD RX) | 24 dBm | 2 dBi | 2 dBi | 109.0 dB | -83.0 dBm | **+23.0 dB** | 12.5 km | ✅ PASS |
| Telemetry downlink — 2.4 GHz ELRS (TD RX → Hermes dongle) | 20 dBm | 2 dBi | 2 dBi | 109.0 dB | -87.0 dBm | **+19.0 dB** | 7.9 km | ✅ PASS |
| OpenHD thermal video — 5.825 GHz WFB-ng (dual Foxeer Echo 2 Max diversity) | 29 dBm | 3 dBi | 16.0 dBi (13.0+3 div) | 116.7 dB | -73.7 dBm | **+11.3 dB** | 3.3 km | ✅ PASS |

† *Reliable range = distance at which the full 10 dB fade margin remains (free-space FSPL only). Beyond it the link still works with reduced fade tolerance.*

### Per-link notes

- **VIDEO-patch:** AF3a BLITZ Whoop 5.8 GHz **1.6 W** (32 dBm) → Skydroid VRX6 + TrueRC X-AIR PATCH1 (10 dBic, 120° beam, RHCP). Analog 'usable' threshold ≈ −90 dBm.
- **VIDEO-omni:** Same link with the VRX's stock omni (~2 dBi) instead of PATCH1 — shows why the dedicated patch antenna is required.
- **CONTROL:** RadioMaster TX12 MkII @**250 mW** (24 dBm) → iFlight True Diversity RX. ELRS 150 Hz sensitivity ≈ −106 dBm (−108 at 50 Hz long-range mode). True diversity adds ~2 dB above nominal (not included — margin is already enormous).
- **TELEMETRY:** iFlight TD RX reverse-link @100 mW (20 dBm) → HGLRC Hermes USB dongle (2.4 GHz ELRS). Same sensitivity threshold as control.
- **OPENHD:** BL-M8812EU2 (WLAN_AIR1) @>800 mW (29 dBm) → AWUS036ACH (WLAN_GND1) + dual Foxeer Echo 2 Max (13 dBi, 60° beam, Linear). WFB-ng MCS1 sensitivity ≈ −85 dBm. +5 dB loss for driver/connector variability. +3 dB spatial-diversity gain (two-antenna receive on AWUS036ACH dual RP-SMA ports; Echo 2 Max is RP-SMA male, no pigtail needed).

## OpenHD ground antenna options (cost / beamwidth trade-off)

All rows assume the same TX (BL-M8812EU2, EIRP = 32 dBm) and +3 dB receive diversity. The 10 dB margin target is the design threshold; links above 6 dB are usable but with reduced tolerance to fading.

| Antenna (×2 for diversity) | Gain | Beam H×V | Pol. | Price (pair) | Margin @2.8 km | Reliable range† | Verdict |
|---|--:|--:|--:|--:|--:|--:|:--:|
| **Foxeer Echo 2 Max × 2** | 13.0 dBi | 60°×60° | Linear | $60.00 | **+11.3 dB** | 3.3 km | ✅ PASS |
| Lumenier AXII Quadro × 2 | 14.7 dBi | 40°×40° | RHCP | $64.98 | **+13.0 dB** | 4.0 km | ✅ PASS |
| Foxeer Echo 2 × 2 | 9.0 dBi | 84°×84° | RHCP | $40.00 | **+7.3 dB** | 2.1 km | ⚠️ THIN |

**Reading the table:**

- **AXII Quadro (selected):** +13 dB margin at 2.8 km; reliable out to ~4 km. 40° beam requires a rough initial aim at the survey area — once pointed, no tracking needed for a drone within ±20° of centre.
- **Foxeer Echo 2 Max:** saves ~$5/antenna ($60 vs $65 pair); 60° beam is more forgiving — ±30° from centre before losing half-power. Margin is 11.3 dB, well above the 10 dB target. **Best 'wide-beam' option if range > 2.8 km matters.** Linear vs RHCP costs ~1–3 dB in multipath; negligible at 90–120 m AGL in open fields.
- **Foxeer Echo 2:** 84° beam is essentially point-and-forget, but 7.3 dB margin at 2.8 km falls below the 10 dB design target (reliable range is only 2.1 km). Works with reduced confidence; not recommended for the full 2.8 km requirement.

**Selected: Foxeer Echo 2 Max** ($60 pair). +11.3 dB margin at 2.8 km comfortably passes the R7 requirement, with a 60° beam that covers the survey area without re-aiming. RP-SMA male connector mates directly to the AWUS036ACH (no pigtails).

## Findings

- **ELRS (control + telemetry):** enormous margin (22–19 dB) — the control link closes 2.8 km many times over and is never the limiting link. TX12 MkII at 250 mW (6 dB below the old Boxer 1 W assumption) still delivers 22 dB.
- **Analog FPV video:** binding constraint without a patch antenna. With PATCH1 (10 dBic, 120° beam) the margin is +15.3 dB — reliable to 6 km. Without PATCH1, the stock-omni link has only +7.3 dB and fails the 10 dB target.
- **OpenHD thermal video (WFB-ng):** the tightest link, but still comfortable. With dual Foxeer Echo 2 Max diversity (+11.3 dB @2.8 km) the thermal downlink closes the full R7 range with margin and is reliable to ~3.3 km. The 60° beam means no re-aiming needed during a survey (±30° slack).
- **All selected-component RF links pass** the 2.8 km / 10 dB requirement. The analog patch antenna and OpenHD diversity antennas are the enabling components.

## Assumptions & notes

- **TX powers (selected components):** analog VTX = BLITZ Whoop 1.6 W (32 dBm, AF3a actual; the 2.5 W variant would add +2 dB); ELRS TX12 MkII = 250 mW (24 dBm); ELRS RX telemetry = 100 mW (20 dBm); OpenHD BL-M8812EU2 = >800 mW (29 dBm — driver_txpower_override 40–50 recommended to avoid PA clipping).
- **Air-side antennas:** VTX/RX omni ≈ 2 dBi (cloverleaf/patch); OpenHD air ≈ 3 dBi (RHCP cloverleaf on u.fl pigtail).
- **Ground antennas:** PATCH1 = TrueRC X-AIR 5.8 MK II, ~10 dBic, 120° beam, RHCP, RP-SMA; OpenHD = dual Foxeer Echo 2 Max, 13 dBi, 60° beam, Linear, RP-SMA male (mates directly to AWUS036ACH RP-SMA female — no pigtail required).
- **Sensitivity thresholds:** analog 'usable' video ≈ −90 dBm; ELRS 2.4 GHz ≈ −106 dBm @ 150 Hz (−108 @ 50 Hz long-range mode); WFB-ng / OpenHD MCS1 ≈ −85 dBm (clean video; FEC begins recovering packets below this).
- **Losses:** 2 dB lumped (connectors, cable, mismatch) for analog/ELRS links; 5 dB for OpenHD (higher, to cover 802.11ac driver variability + pigtail + adapter tolerance).
- **Diversity:** OpenHD uses two AXII Quadro panels on the AWUS036ACH dual RP-SMA ports; WFB-ng selects the best-SNR packet per frame (+3 dB in fading). The iFlight TD RX (ELRS control) also has true diversity (~2 dB, not modelled separately — ELRS margin is already 22 dB).
- **Polarisation:** all RHCP pairs are matched (+0 dB). Linear vs RHCP costs ~1–3 dB in reflected-ground environments; negligible at 90–120 m AGL in open / semi-open terrain.
- **GNSS** is satellite-receive only (~−130 dBm, L1 1575 MHz) — not a controlled link in this budget; covered by the GPS module's own sensitivity specification.
- **Free-space model only.** For dense foliage or non-LOS, raise TX power, switch to higher-gain antennas, or lower the ELRS packet rate. The 10 dB margin is the practical cushion for realistic survey conditions at 90–120 m AGL.

