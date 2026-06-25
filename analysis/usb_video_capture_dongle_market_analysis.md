# USB Video Capture Dongle Market Analysis

**File:** `analysis/usb_video_capture_dongle_market_analysis.md`
**Date:** 2026-06-13
**Purpose:** Convert analog CVBS/composite video from the ground-side 5.8 GHz VRX to USB for display on the MacBook.

## Architecture Context

Path: `Analog VRX (RCA AV) → USB Capture Dongle → MacBook Air`

The dongle presents itself as a UVC (USB Video Class) device — the MacBook sees it as a standard webcam, no drivers needed. Works with QGC / Mission Planner / OBS.

## Compatibility Notes

- **Input:** Analog CVBS/composite (NTSC or PAL) — standard analog FPV format
- **Output:** UVC 1.0 — driverless on macOS, recognized as a webcam
- **Resolution:** 1080p MJPEG or 720p YUV422 typical; analog FPV source is effectively ~600TVL so any capture card handles it
- **Connectivity:** USB-A or USB-C on the computer side
- **Range note:** The capture dongle itself does NOT affect range. Range is determined by the analog VRX feeding into it. The dongle is purely a format converter.

## Candidates

### Option 1: FPV-Specific — Flying Tech USB-C Analog FPV Capture Adapter
| Field | Value |
|-------|-------|
| Price | ~$15-20 |
| Store | flyingtech.co.uk |
| Input | RCA composite (via included cable) |
| Output | USB-C (UVC) |
| macOS | ✅ Driverless |
| Notes | Purpose-built for FPV ground stations. Compact. Includes RCA-to-adapter cable. Best compatibility. |

### Option 2: Generic — CVBS/AV to USB Module Board (AliExpress)
| Field | Value |
|-------|-------|
| Price | $7-15 |
| Store | AliExpress, Amazon |
| Input | CVBS (pin headers) |
| Output | USB-A (UVC) |
| macOS | ✅ Driverless |
| Notes | Bare PCB module (25×12mm). 1080p MJPEG. Pin headers need wiring to RCA — requires minor soldering. Can be integrated into a custom GCS enclosure. |

### Option 3: Generic — ATCCPYDM / Kqcibz AV-to-USB Capture Card
| Field | Value |
|-------|-------|
| Price | $10-16 |
| Store | Amazon |
| Input | RCA composite (female jack) |
| Output | USB-A (UVC) |
| macOS | ✅ Driverless |
| Notes | Plug-and-play in an enclosure. Available on Amazon Prime. 1080p. Enclosed with RCA jacks — no soldering. |

### Option 4: EasyCAP USB 2.0
| Field | Value |
|-------|-------|
| Price | $11-15 |
| Store | Amazon, eBay |
| Input | RCA/S-Video |
| Output | USB-A |
| macOS | ⚠️ May need driver on newer macOS versions (not pure UVC). Older chipset. |
| Notes | Skip this — driver issues on recent macOS. Prefer UVC-native options above. |

### Option 5: Magewell USB Capture (HDMI/SDI)
| Field | Value |
|-------|-------|
| Price | $150-300 |
| Input | HDMI or SDI |
| Output | USB-C (UVC) |
| macOS | ✅ Driverless |
| Notes | Pro-grade. Overkill and over budget for analog FPV. Only relevant if thermal camera outputs HDMI directly. |

## Recommendation

**For a laptop-based GCS with analog VTX: FPV-Specific USB-C adapter (Option 1) at ~$15-20** or a **generic AV-to-USB dongle from Amazon (Option 3) at ~$10-16**.

Both are UVC-compliant, driverless on macOS, and below the noise floor of the $2,500 budget. Avoid EasyCAP — the driver situation on modern macOS is unreliable.

### Cost Allocation (GCS)

| Component | Cost |
|-----------|------|
| Analog VRX (5.8 GHz) | $20-40 |
| USB Video Capture Dongle | **$10-20** |
| Total video downlink | $30-60 |

## Data Source
- Flying Tech (UK): https://www.flyingtech.co.uk/product/usb-c-analog-fpv-video-capture-adapter/
- Amazon: ATCCPYDM / Kqcibz AV-to-USB cards
- AliExpress: CVBS-to-USB modules
- Web search, Jun 2026