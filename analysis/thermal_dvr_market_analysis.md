# Thermal Video Recorder (DVR) Market Analysis

**File:** `analysis/thermal_dvr_market_analysis.md`
**Date:** 2026-06-24
**Purpose:** Identify candidate inline analog DVRs for onboard recording of thermal camera CVBS video during Phase 3 (pre-SBC).

## Architecture Context

Path: `Thermal Camera CVBS → DVR (records to microSD) → VTX (pass-through live downlink)`

The DVR sits inline between the thermal camera and the video transmitter. It records to microSD while passing the video through untouched — so the live FPV feed is unaffected. This means **thermal footage survives RF dropouts** since it's recorded locally on the card.

## Phase Relevance

- **Phase 1 (Basic Flight):** Not required — no thermal camera yet
- **Phase 2 (FPV):** Not required — FPV cam → VTX is sufficient
- **Phase 3 (Thermal):** Required — records thermal footage onboard. No SBC yet, so DVR is the only recording path
- **Phase 4 (SBC):** Optional — SBC can record too, but DVR backup is cheap insurance

## Compatibility Notes

- **Input:** CVBS analog (NTSC/PAL) — matches all thermal cameras under consideration (Lepton 3.5, Boson 320/640)
- **Pass-through:** All candidates below support video passthrough — recording is transparent to the VTX
- **Resolution:** Thermal cameras output at most D1 (720×480). DVRs recording at 1280×480 HD are more than sufficient
- **Power:** All run on 5V. The RunCam can also take 3.3V. Eachine EV100/ProDVR can take 2S (7.4V) directly
- **Weight:** 3.5-12g — negligible against the thermal camera's mass budget

## Candidates

### Option 1: RunCam Mini FPV DVR (RUNCAM-DVR-S)
| Field | Value |
|-------|-------|
| Price | $17.99 (direct) / $29.99 (Amazon) |
| Weight | 3.5g |
| Dimensions | 25×25mm, ~6mm thick |
| Mounting | 20×20mm M2 holes |
| Input Voltage | 3.3-5.5V |
| Power Draw | ~250mA / 1.3W max |
| Recording | MJPEG/AVI up to 720×480 (D1) @ 30fps |
| Storage | microSD up to 32GB |
| Audio | Yes |
| Control | Flight controller GPIO (SpeedyBee App) or auto via ARM |
| Cables | USB cable sold separately |
| Notes | Lightest option. Lossless pass-through. Can auto-start recording on ARM. Regulated 5V output for camera. |
| **Verdict** | ✅ **Best for our build** — lightest, smallest, mounts to standard 20mm stack holes, GPIO-controlled |

### Option 2: Eachine EV100 Micro AV Recorder
| Field | Value |
|-------|-------|
| Price | ~$16.14 |
| Weight | 9g |
| Dimensions | 38.5×30.8×12.5mm |
| Mounting | Double-sided tape (no screw holes) |
| Input Voltage | 5V or 7.4V (2S) |
| Power Draw | ~240mA / 1.2W |
| Recording | MJPEG/AVI up to 1280×480 (HD) @ 30fps |
| Storage | TF/microSD up to 32GB |
| Audio | Yes |
| Control | Push-button on module |
| Cables | A/V cable + power cable included |
| Notes | Wider resolution (1280×480). Push-button start/stop. Includes cables. Slightly heavier. |
| **Verdict** | ✅ **Good value** — cheaper, HD resolution, includes cables |

### Option 3: Eachine ProDVR
| Field | Value |
|-------|-------|
| Price | ~$16.46 |
| Weight | 9.9g |
| Dimensions | 41×32.9×9mm |
| Mounting | Adhesive (included) |
| Input Voltage | 5V |
| Power Draw | ~200mA / 1.0W |
| Recording | MJPEG/AVI up to 1280×480 (HD) @ 30fps |
| Storage | TF/microSD up to 32GB |
| Audio | Yes |
| Control | Push-button on module |
| Cables | Power/CAM + video + key wire included |
| Notes | Full analog of HMDVR. Can be used onboard or ground-side. Firmware updatable. |
| **Verdict** | ✅ **Solid alternative** — lowest power draw, HD resolution |

### Option 4: Generic Mini FPV DVR (eBay/AliExpress variety)
| Field | Value |
|-------|-------|
| Price | $8.99 - $14.99 |
| Weight | 8-12g |
| Dimensions | ~38×30×12mm |
| Mounting | Adhesive |
| Input Voltage | 5V (some up to 8.4V) |
| Power Draw | ~220-250mA / 1.1-1.3W |
| Recording | MJPEG/AVI up to 1280×480 @ 30fps |
| Storage | TF/microSD up to 32GB |
| Audio | Yes |
| Control | Push-button or remote button |
| Cables | Varies (usually AV cable included) |
| Notes | Lowest cost option. No-name branding. Variable quality. Some include a 32GB card. |
| **Verdict** | ⚠️ **Budget option** — works but unknown reliability. Good as a spare/backup. |

## Recommendation

**Choose: RunCam Mini FPV DVR** for Phase 3.

Rationale:
1. **Lightest** at 3.5g — barely affects the mass budget
2. **Smallest** — 25×25mm with standard 20×20mm mounting, fits any stack
3. **GPIO control** — can auto-start recording on ARM (no manual button press before launch)
4. **Regulated 5V output** — can power the thermal camera too, simplifying wiring
5. **Lossless pass-through** — no video quality impact on the live downlink

The Eachine EV100 is a fine backup ($16, includes cables, HD recording) if the RunCam is unavailable.

## Cost Impact

- Recommended candidate: **$17.99** (RunCam direct) or **$16.14** (Eachine EV100)
- Add ~$5 for a 32GB microSD if not already owned
- Total cost to BOM: **~$18-22**
- Well within the $600 camera subsystem budget