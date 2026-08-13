# System Engineering Plan

The build proceeds in **three committed phases plus a deferred Phase 4 (future capability)**.
The committed system (Phases 1–3) is analog FPV for piloting + a thermal camera feeding the
onboard SBC for **real-time inference** (no recording, no downlink); **Phase 4** adds an OpenHD
digital video downlink to the ground station. Selected parts:
[`SELECTED_COMPONENTS.md`](SELECTED_COMPONENTS.md); full phased bill of materials: [`BOM.md`](BOM.md).

## Phase 1 — Basic Flight + FPV Downlink + Waypoints
**Goal** — Stable manual line-of-sight flight, live analog video on the laptop, and
pre-programmed waypoint missions.

**Requirements**
- R4_AF_PAYLOAD, R4_AF_WT, R4_AF_ASSY, R4_AF_STIFF, R4_AF_LANDING, R4_AF_COST, R4_AF_PROP_CFG, R4_AF_PWR_DIST
- R4_BAT_VOLT, R4_BAT_WT, R4_BAT_IF
- R4_GCS_VIDEO_DISP, R4_GCS_RANGE, R4_GCS_IF, R4_GCS_CTRL, R4_GCS_TELEM

**Components Required**
- Airframe — **iFlight Chimera9 ECO 9" PNP** (`AF3a`); bundles a 5.8 GHz analog VTX + FPV camera (air-side video, $0)
- RadioReceiver — **iFlight True Diversity ELRS** (`iFlightTD`); RC control + telemetry on one link
- Battery — **Upgrade Energy GREEN V2 6S3P 12 Ah Amprius** (`BAT10`, flight default) + **2× GNB 6S3P 12 Ah** (`BAT22`, development packs)
- RcTx — **RadioMaster Boxer ELRS** (`TX1`, handheld)
- ELRS USB dongle — primary laptop control + telemetry link (TBD)
- GPS — **TBS M10** (`G6`) for waypoint navigation
- Vrx — **Skydroid 150CH 5.8 GHz UVC** (`VRX6`); laptop-direct video
- Antenna — **TrueRC X-AIR 5.8 patch** (`PATCH1`); video-link range margin (see `analysis/rf_link_budget.md`)
- Anti-spark filter — **iFlight Anti Spark** (`ASF1`, XT60 inline)
- Battery charger — **HOTA D6 Pro** (`CHG1`, 6S Li-ion/LiPo, bench/reusable)
- GCS laptop (MacBook — existing equipment, $0)

**Phase Steps**
1. Power-on and bind the ELRS receiver to the handheld + the laptop ELRS dongle.
2. Flash ArduPilot/PX4 onto the flight controller; configure the GPS.
3. Calibrate sensors (compass, accelerometer, gyro).
4. Configure arming, failsafe, and return-to-launch (RTL) behavior.
5. Basic flight-envelope tests (hover, pitch, roll, yaw) in LOS.
6. Connect the Skydroid VRX (USB/UVC) + patch antenna to the laptop; view & record live video in QuickTime/OBS.
7. Confirm live analog FPV feed + telemetry to the laptop (QGroundControl).
8. Define a waypoint mission in QGroundControl; upload and execute with FPV monitoring and manual ELRS override.
9. Validate position-hold and RTL.

**Result** — Ready-to-fly airframe under manual LOS control with live laptop video and autonomous waypoint routes.

---

## Phase 2 — EO/IR Thermal Camera + SBC (Onboard Live-Inference Feed)
**Goal** — Mount the thermal camera and SBC and establish the live thermal → SBC feed. The thermal
is **not recorded and not downlinked** — it streams directly to the SBC for the real-time inference
deployed in Phase 3.

**New Components (vs Phase 1)**
- Thermal Camera Subsystem — **PurpleRiver Mini 640** (`T13`, 640×512, 12 µm, **18 mm lens**, **USB** variant)
- Single-Board Computer — **NanoPi M5, 4 GB** (`SBC3`, Rockchip RK3576, RKNN NPU) — real-time inference
- SBC mount + cooling (3D-printed deck + fan — see [`cad-resources/cad-resources.md`](cad-resources/cad-resources.md))
- SBC power — 2-6S→12 V 3 A UBEC (2-pack) + USB-C power-only cable

**Components Required (full list)** — all of Phase 1, plus the thermal camera and SBC (with mount/cooling and power).

**Phase Steps**
1. Mount the thermal camera on the airframe (clear FOV, nose/chin).
2. Mount the SBC on a 3D-printed deck; power it from the 12 V UBEC and connect to the flight controller (UART/MAVLink).
3. Route the thermal camera video → SBC over **USB-UVC** (appears as `/dev/video0`, no driver work).
4. Confirm the SBC receives a stable live thermal stream (≈25 Hz) and Johnson detect/recognize performance at 90–120 m.

**Result** — Thermal camera streaming live to the onboard SBC over USB, ready for the Phase 3 inference. Meets the R3 detection/recognition requirements. No recording device and no downlink hardware (downlink is the deferred Phase 4).

---

## Phase 3 — AI Detection + Autonomous Route Modification (Software)
**Goal** — Run **real-time** on-board thermal detection/classification on the live Phase 2 feed and adapt the mission dynamically, using the SBC already on-board.

**New Components (vs Phase 2)** — None (all hardware on-board since Phase 2).

**Components Required (full list)** — same as Phase 2 (hardware).

**Phase Steps**
1. Deploy the INT8-quantized detection/classification model via the RKNN toolchain (RKNPU2); run live inference on the USB thermal stream (≥ ~25 fps).
2. Map detections to MAVLink commands (loiter/adjust/divert on a target); modify the mission in-flight.
3. Validate fallback: if the SBC fails, the drone completes the current waypoint and RTLs.

**Result** — Autonomous drone that detects and reacts to thermal targets in real time, meeting all SBC and camera requirements.

---

## Phase 4 — (Future Capability) OpenHD Digital Video Downlink to Ground Station
**Status: deferred / future.** Not part of the committed Phase 1–3 build. Adds a live digital
downlink of the thermal (and/or AI-annotated) video to the ground station so an operator can watch
the mission live.

**Goal** — Downlink live thermal/AI video from the drone to the laptop ground station via OpenHD/WFB-ng.

**New Components (vs Phase 3)**
- WiFi adapter (air) — **LB-LINK BL-M8812EU2** (`WLAN_AIR1`) for OpenHD digital downlink
- Air-side antennas — 5.8 GHz RHCP cloverleaf × 2
- WiFi adapter (ground) — **Alfa AWUS036ACH** (`WLAN_GND1`) for OpenHD reception
- Ground diversity antennas — **Foxeer Echo 2 Max × 2** (`ANT_GND1` + `ANT_GND2`)
- Ground decode — VMware Fusion VM (ARM64 Ubuntu) on the MacBook
- Air-module 5 V power — the spare unit of the Phase 2 UBEC 2-pack (no new part)

**Phase Steps**
1. Mount `WLAN_AIR1` on the SBC (USB) + air antennas; power the module from the spare UBEC unit (5 V).
2. Configure the SBC to encode the thermal/AI feed (H.264) and transmit via WFB-ng at 5.8 GHz.
3. On the ground: `WLAN_GND1` + Foxeer diversity antennas → ARM64 Ubuntu VM (VMware Fusion) decodes the WFB-ng stream on the laptop.
4. Confirm live downlink and link margin at 2.8 km (see [`analysis/rf_link_budget.md`](analysis/rf_link_budget.md)).

**Result** — Operator sees the live thermal/AI video on the ground during the mission. See
[`analysis/openhd-air-wifi-adapter-trade-study.md`](analysis/openhd-air-wifi-adapter-trade-study.md)
for the adapter selection and open items (e.g. air-module power/soldering).
