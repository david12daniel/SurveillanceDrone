# Telemetry USB Dongle Market Analysis

**File:** `analysis/telemetry_usb_dongle_market_analysis.md`
**Date:** 2026-06-13
**Purpose:** Get ELRS/CRSF telemetry from the drone into the MacBook for display in QGC / Mission Planner.

## Architecture Context

Path: `Drone FC → CRSF → ELRS RX → [RF downlink] → Ground Telemetry Receiver → USB → MacBook`

There are **two approaches** to the ground-side receiver:

---

## Approach A: Radio Controller USB Passthrough (Recommended)

**How it works:** The EdgeTX radio (Boxer, T20, TX16S, etc.) already contains the ELRS TX module. When you plug the radio into the MacBook via USB-C, EdgeTX can operate in **USB Serial (VCP) mode** — the radio appears as a virtual COM port on the laptop, forwarding all telemetry data received over the ELRS RF link.

**Why this is the preferred approach:**
- ✅ No extra hardware — the radio is already part of the system
- ✅ macOS recognizes it as a standard serial device (no special drivers)
- ✅ QGC and Mission Planner both support serial USB telemetry input
- ✅ The radio's own screen still shows telemetry simultaneously
- ✅ Full bidirectional telemetry (sensor polling works)

**Compatibility:**
| Radio | EdgeTX USB Serial | Tested with QGC/MP |
|-------|-------------------|-------------------|
| RadioMaster Boxer | ✅ | ✅ |
| RadioMaster TX16S | ✅ | ✅ |
| RadioMaster TX12 MKII | ✅ | ✅ |
| Jumper T20 V2 | ✅ | ✅ |
| Jumper T-Pro V2 | ✅ | ✅ |

**Cost:** **$0** — uses existing radio equipment.

**Range note:** Range is determined by the ELRS TX module inside the radio, not by any USB dongle. The radio's ELRS module (1W internal or external) gives 10+ km which exceeds 2.8 km requirement. See `analysis/radio_controller_tx_market_analysis.md`.

---

## Approach B: Standalone ELRS USB Receiver Dongle

**How it works:** A dedicated ESP32-based USB dongle with an ELRS receiver chip acts as a standalone telemetry ground station. It binds directly to the drone's onboard ELRS RX, receives telemetry, and pipes it over USB to the laptop.

**Use case:** Running the laptop without the radio controller powered on (e.g., for automated flight or post-flight log analysis).

**Candidates:**

### B1: HGLRC ELRS SIM USB Dongle (Hermes-based)
| Field | Value |
|-------|-------|
| Price | $14-18 |
| Store | AliExpress, Amazon |
| Chipset | ESP32 + SX1280 (ELRS 2.4 GHz) |
| Output | USB-A (serial / UVC) |
| macOS | ✅ |
| Power | Bus-powered from USB |
| Range | Same as any ELRS 2.4 GHz RX — 10+ km with 1W TX |
| Notes | Originally made for FPV sims. Can be reflashed with ELRS backpack firmware for telemetry use. Built-in antenna. |

### B2: CubeFPV USB ELRS Dongle
| Field | Value |
|-------|-------|
| Price | ~$15-20 |
| Store | cubefpv.com |
| Chipset | ESP32 + ELRS 2.4 GHz |
| Output | USB (serial) |
| macOS | ✅ |
| Power | Bus-powered from USB |
| Range | Same as B1 — 10+ km |
| Notes | Built-in ELRS receiver + solder pads for external CRSF receiver. Designed for sim use but reflashable for telemetry. |

### B3: DIY — Generic ESP32 Dev Board + ELRS RX Module
| Field | Value |
|-------|-------|
| Price | ~$10-15 (ESP32 $5 + ELRS RX $5-10) |
| Store | Amazon, AliExpress |
| Skill | ⚠️ Requires soldering and firmware flashing |
| Notes | More flexible but violates R5 (minimize DIY soldering). |

**Range note for Approach B:** The dongle acts as the ground-side ELRS receiver. The drone's 1W ELRS TX module paired with a standard ELRS receiver chip gives 10+ km. Range is not a concern. ✅

---

## Approach C: External TX Module Direct-to-Laptop (ExpressLRS AirPort)

**How it works:** An external ELRS TX module (like the RadioMaster Ranger at $70 from `radio_controller_tx_market.csv`) can be plugged directly into the laptop via USB and firmware-flashed to **AirPort** mode. AirPort creates a transparent bidirectional serial link between the module and a matching ELRS RX on the drone. The laptop sees it as a COM port — QGC/Mission Planner connects directly.

**Candidates:**

### C1: RadioMaster Ranger ELRS Module (TXM1)
| Field | Value |
|-------|-------|
| Price | $70 (module only, from TXM1 in radio TX analysis) |
| Chipset | ESP32 + SX1280, 1W output |
| Output | USB directly to laptop (flashing firmware also uses USB) |
| macOS | ✅ Serial |
| Range | 10+ km (1W module) |
| Notes | Already in our TX module market analysis. Has USB port for flashing — also usable for AirPort serial link. Comes with Moxon antenna. |

### C2: RadioMaster Ranger Micro (TXM2)
| Field | Value |
|-------|-------|
| Price | $50 |
| Chipset | SX1280, 1W output| 
| Notes | Smaller form factor, no fan, lower weight. |

### C3: Happymodel ES24TX Pro (TXM3)
| Field | Value |
|-------|-------|
| Price | $45 |
| Chipset | ESP32 + SX1281, 1W |
| Notes | Budget option. No screen. |

**Range note for Approach C:** These are 1W TX modules — the same ones analyzed in the TX market analysis. Range is 10+ km. No concern. ✅

### ⚠️ Critical Caveat (from ELRS docs):
> *"The AirPort option completely replaces the RC link, and repurposes it as a data link. If you intend to retain RC control via ELRS, you will need to run 2x TXs and 2x RXs on the ground and air, respectively. One TX+RX pair sends your normal RC link data, and the other TX+RX pair sends the serial data."*

And if running two side-by-side ELRS links: *"it is HIGHLY recommended to use different frequencies for each link (e.g., RC on 2.4 GHz, AirPort on 900 MHz)."*

This means Approach C requires:
1. A **2nd ELRS RX** on the drone (~$15-25)
2. A different frequency band (900 MHz vs 2.4 GHz)
3. The existing radio controller is still needed for RC control

**Impractical for our build — adds cost, complexity, and violates R5 (minimize DIY). Not recommended.**

---

## Approach D: ExpressLRS Backpack (Wireless ESP-NOW Telemetry Bridge)

**How it works:** Many modern ELRS TX modules (Ranger, Nomad, and several built-in modules) have an **ESP32 backpack** onboard. This creates a secondary ESP-NOW wireless link from the TX module to other backpack-compatible devices. An ESP32 on the ground (plugged into the laptop) receives telemetry wirelessly.

**Candidates:**

### D1: ESP32 Dev Board (any) + ELRS Backpack Firmware
| Field | Value |
|-------|-------|
| Price | ~$5-8 (ESP32 dev board) |
| Chipset | Any ESP32 |
| Connection | ESP-NOW (not ELRS RF), then USB to laptop |
| macOS | ✅ Serial |
| Range | ESP-NOW range ~100-400m (not suitable for 2.8 km) |
| Skill | ⚠️ Requires flashing firmware and some configuration |
| Notes | Wireless, no cable. BUT ESP-NOW range is much shorter than ELRS — only useful at close range (bench testing, staging area). |

**Range note for Approach D:** ESP-NOW range is typically ~100-400m, nowhere near our 2.8 km requirement. ❌ **Not suitable** for our surveillance mission.

---

## Summary of All Approaches

| # | Approach | Cost | Range Fit | Complexity | Best For |
|---|----------|------|-----------|------------|----------|
| **A** 🥇 | Radio USB Passthrough | **$0** | ✅ (10+ km) | Low | Primary — works with existing radio |
| **B** 🔄 | ELRS USB Dongle (HGLRC/CubeFPV) | $15-20 | ✅ (10+ km) | Low-Medium | Fallback — telemetry without radio |
| C | Ranger Module AirPort (direct USB) | $70+ ($70 module + $25 extra RX) | ✅ (10+ km) | High (dual link, freq planning) | ❌ Overkill, violates R5 |
| D | ESP32 Backpack (ESP-NOW) | $5-8 | ❌ (~100-400m only) | Medium | ❌ Range too short |

## Recommendation

**Approach A ($0)** is still the clear winner — the radio you're already buying handles telemetry passthrough via USB natively. No extra hardware.

**Approach B ($15-20)** is a nice-to-have fallback if you ever want to plug telemetry into the laptop without powering up the radio.

Approaches C and D add complexity with no meaningful benefit for this project. Skip them.

## Data Source
- ExpressLRS MAVLink documentation: https://www.expresslrs.org/software/mavlink/
- ExpressLRS AirPort documentation: https://www.expresslrs.org/software/airport/
- ExpressLRS Backpack documentation: https://www.expresslrs.org/hardware/backpack/esp-backpack/
- EdgeTX USB serial mode: https://manual.edgetx.org/
- ArduPilot Discourse: CRSF telemetry to Mission Planner
- Reddit /r/fpv: CRSF telemetry to laptop discussions
- HGLRC / CubeFPV product pages
- Oscar Liang: RadioMaster Ranger review
- Web search, Jun 2026