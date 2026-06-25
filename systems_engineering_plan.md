# System Engineering Plan

## Phase 1 — Basic Flight Capability
**Goal** — Achieve stable, manual-controlled flight of the airframe (line-of-sight).

**Requirements**
- R4_AF_PAYLOAD
- R4_AF_WT
- R4_AF_ASSY
- R4_AF_STIFF
- R4_AF_LANDING
- R4_AF_COST
- R4_AF_PROP_CFG
- R4_AF_PWR_DIST
- R4_BAT_VOLT
- R4_BAT_WT

**Components Required**
- Airframe (frame, motors, ESCs, FC, propellers, power distribution)
- RadioReceiver (ELRS — handles RC control + telemetry on one link)
- Battery (6S LiPo or Li-ion pack)
- RadioControlTransmitter (handheld with ELRS TX module)
- GCS laptop (MacBook — existing equipment, no cost)

**Phase Steps**
1. Power-on and bind ELRS transmitter/receiver.
2. Flash ArduPilot/PX4 onto the flight controller.
3. Calibrate sensors (compass, accelerometer, gyro).
4. Configure basic arming, failsafe, and RTL behavior.
5. Perform basic flight envelope tests (hover, pitch, roll, yaw) in LOS.
6. Log telemetry via ELRS return link to GCS laptop.
7. Verify stable hover and control response.

**Result** — A ready-to-fly airframe under manual LOS control, satisfying all listed airframe and battery requirements.

---

## Phase 2 — FPV Downlink & Pre-Programmed Flight Routes
**Goal** — Add live FPV video feed for beyond-LOS piloting, then enable waypoint missions.

**New Components (vs Phase 1)**
- FPV Camera (analog CMOS, included with many airframes)
- VideoTransmitter (VTX — 5.8 GHz analog)
- VideoReceiver (VRX — ground side)
- ArduPilot/PX4 firmware (replaces Betaflight/INAV)

**Components Required (full list)**
- Airframe (frame, motors, ESCs, FC, propellers, power distribution)
- FPV Camera (Caddx H1 or equivalent)
- VideoTransmitter (VTX, 5.8 GHz analog)
- RadioReceiver (ELRS — RC control + telemetry)
- Battery (6S)
- RadioControlTransmitter (handheld ELRS)
- VideoReceiver (VRX — ground side, goggles or USB receiver)
- GCS laptop (MacBook — existing)

**Phase Steps**
1. Mount FPV camera and VTX; route camera → VTX.
2. Tune VTX channel and confirm live feed on ground (VRX → MacBook/QGroundControl).
3. Define a simple waypoint mission in QGroundControl.
4. Upload mission and execute — monitor via FPV feed.
5. Validate position-hold and RTL behavior.

**Result** — Live downlink enabled, drone flies pre-programmed waypoints autonomously with manual override via ELRS.

---

## Phase 3 — EOIR Thermal Camera Integration
**Goal** — Mount thermal camera, record onboard to microSD, and optionally downlink live thermal video.

**New Components (vs Phase 2)**
- Thermal Camera Subsystem (Lepton 3.5 / Boson 320 / Boson 640)
- ThermalVideoRecorder (inline analog DVR — CVBS in, microSD storage, pass-through to VTX)

**Components Required (full list)**
- Airframe
- FPV Camera → VTX (Phase 2, retained)
- Thermal Camera Subsystem (thermal sensor + lens)
- ThermalVideoRecorder (inline DVR, records to microSD)
- VideoTransmitter (VTX — shared with FPV camera; DVR pass-through feeds thermal or FPV signal)
- RadioReceiver (ELRS)
- Battery
- RadioControlTransmitter
- VideoReceiver (VRX — shared with Phase 2)
- GCS laptop

**Phase Steps**
1. Mount Thermal Camera Subsystem on airframe (top or bottom, clear FOV).
2. Connect camera power to battery rail.
3. Route CVBS from thermal camera → ThermalVideoRecorder (records) → VTX (live downlink).
4. Configure DVR to auto-start recording on power-up (loop recording, per-flight files).
5. Fly and rescue thermal footage from microSD post-flight.
6. Optionally view live thermal feed on ground via VTX → VRX → MacBook.
7. Switch VTX input between FPV camera and thermal camera (manual or switchable).

**Result** — Thermal video recorded onboard to microSD (survives signal loss) with optional live downlink.

---

## Phase 4 — On-Board Detection & Autonomous Route Modification
**Goal** — Add AI-based thermal detection and dynamic mission adaptation.

**New Components (vs Phase 3)**
- Single Board Computer (SBC — e.g. NVIDIA Jetson / Raspberry Pi 4/5)
- Co-recording path: SBC-annotated video → ThermalVideoRecorder

**Components Required (full list)**
- Airframe
- FPV Camera → VTX
- Thermal Camera Subsystem
- ThermalVideoRecorder (inline DVR)
- VideoTransmitter (VTX)
- RadioReceiver (ELRS)
- Battery
- RadioControlTransmitter
- VideoReceiver (VRX)
- SBC (Jetson / RPi — video in, inference, MAVLink commands)
- GCS laptop

**Phase Steps**
1. Mount SBC on airframe; connect to battery rail.
2. Route thermal camera video → SBC video input (USB or CSI).
3. Load TensorFlow-Lite / ONNX detection model on SBC.
4. Run inference at ≥25 Hz, mapping detections to MAVLink waypoint commands.
5. Modify mission in-flight (e.g., loiter on human/vehicle target, adjust altitude).
6. Co-record SBC-annotated video to ThermalVideoRecorder for post-flight review.
7. Validate fallback behavior: if SBC fails → drone completes current waypoint and RTL.

**Result** — Fully autonomous drone that detects and reacts to thermal targets, meeting all SBC and camera requirements.