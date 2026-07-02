# System Engineering Plan

The build proceeds in **three incremental phases** (merged from the original four —
the old Phase 1 "basic flight" and Phase 2 "FPV + waypoints" are now a single Phase 1).
Selected parts: [`SELECTED_COMPONENTS.md`](SELECTED_COMPONENTS.md); full phased bill of
materials: [`BOM.md`](BOM.md).

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
- RadioControlTransmitter — **RadioMaster Boxer ELRS** (`TX1`, handheld)
- ELRS USB dongle — primary laptop control + telemetry link (TBD)
- GPS — **TBS M10** (`G6`) for waypoint navigation
- VideoReceiver — **Skydroid 150CH 5.8 GHz UVC** (`VRX6`); laptop-direct video
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

## Phase 2 — EO/IR Thermal Camera + Onboard Recording
**Goal** — Mount the thermal camera, record onboard to microSD, and downlink live thermal video.

**New Components (vs Phase 1)**
- Thermal Camera Subsystem — **PurpleRiver Mini 640** (`T13`, 640×512, 12 µm, 13 mm lens, USB)
- ThermalVideoRecorder — **Monster UVC Recorder** (`DVR9`, standalone USB-UVC DVR to microSD)

**Components Required (full list)** — all of Phase 1, plus the thermal camera and DVR.

**Phase Steps**
1. Mount the thermal camera on the airframe (clear FOV, nose/chin) and power from the airframe rail.
2. Route the thermal video → DVR (records to microSD) and to the laptop (live view).
3. Configure the DVR to auto-start recording on power-up (per-flight files).
4. Fly and recover thermal footage from microSD post-flight (footage survives RF loss).
5. Confirm live thermal downlink on the laptop and Johnson detect/recognize performance at 90–120 m.

**Result** — Thermal video recorded onboard (survives signal loss) with live downlink; meets the R3 detection/recognition requirements.

---

## Phase 3 — On-Board Detection + Autonomous Route Modification
**Goal** — Add on-board AI thermal detection/classification and dynamic mission adaptation.

**New Components (vs Phase 2)**
- Single-Board Computer — **NanoPi M5, 4 GB** (`SBC3`, Rockchip RK3576, RKNN NPU)
- SBC mount + cooling (3D-printed deck + fan — see [`reference/cad-resources.md`](reference/cad-resources.md))

**Components Required (full list)** — all of Phase 2, plus the SBC (the SBC records at this stage, so the DVR is no longer required).

**Phase Steps**
1. Mount the SBC on a 3D-printed deck; connect to the airframe rail and the flight controller (UART/MAVLink).
2. Route the thermal camera video → SBC (USB-UVC).
3. Deploy the INT8-quantized detection/classification model via the RKNN toolchain (RKNPU2); verify ≥ ~25 fps.
4. Map detections to MAVLink commands (loiter/adjust on a target); modify the mission in-flight.
5. Validate fallback: if the SBC fails, the drone completes the current waypoint and RTLs.

**Result** — Autonomous drone that detects and reacts to thermal targets, meeting all SBC and camera requirements.
