# Software by Component — Functions, Existing Software, and To-Be-Developed Register

## Purpose
For each **programmable component** — the **laptop (GCS)**, the **flight controller**, and the **SBC** — identify (1) the functions the component must perform to execute the overall mission (fly a surveillance route; detect and classify deer, turkey, other animals, and humans), (2) the software that **exists today** to perform each function, and (3) where **no software exists**, record it as a new capability **to be developed** (the D-register at the end).

Companion to [`software_gap_analysis.md`](software_gap_analysis.md) (function-oriented adopt/build rationale + the mission-app MAVLink interface contract) and [`software_trade_studies.md`](software_trade_studies.md) (free/paid **alternatives traded** for each EXISTS item). This document is the **component-oriented register**. Functions trace to [`behavior.sysml`](../behavior.sysml) (Layer 1/4 elements and `missionContext` allocations); supporting functions below the model's abstraction (e.g., attitude stabilization) are marked *implied*.

**Status legend:** ✅ EXISTS (adopt; config only) · 🔧 EXISTS-CONFIG (exists, but the configuration itself is engineering work) · 🚧 DEVELOP (no existing software — see D-register) · ⏸ DEFERRED (Phase 4).

---

## 1. Laptop — GCS (`gcs.viewingComputer`)
**Platform constraint:** the laptop is the existing **MacBook Air** (external actor, not procured — CLAUDE.md). macOS rules out Mission Planner (Windows/Mono) as the primary tool; **QGroundControl is the GCS application**.

| # | Function | Phase | Trace | Existing software | Status |
|---|---|---|---|---|---|
| L1 | Plan waypoint route (90–120 m AGL, 2.23 m/s, within energy budget) | 1 | `planRoute` (UC-2); R1, R2, R6, R7 | **QGroundControl** mission editor | ✅ |
| L2 | Upload/download mission to FC over the telemetry link | 1 | `planRoute`; R4_SBC_DATA_AF path | QGC (MAVLink over ELRS dongle) | ✅ |
| L3 | Display real-time telemetry (alt, position, battery V, heading, speed) | 1 | `monitorMission` (UC-6); R4_GCS_TELEM | QGC | ✅ |
| L4 | Map situational awareness + flight-mode display | 1 | `monitorMission` | QGC | ✅ |
| L5 | Display FPV/analog video (piloting aid; Skydroid VRX → USB-UVC) | 1 | UC-6; R4_GCS_VIDEO_DISP (FPV path) | QGC video widget (UVC source) / QuickTime / VLC | ✅ |
| L6 | Configure FC parameters + sensor calibration (incl. `FS_*`, `BATT_*` failsafe values) | 1 | UC-1; §3.7 failsafe reqs | QGC parameter/calibration UI | ✅ |
| L7 | Flash/maintain FC firmware | 1 | UC-1 (R5 — no custom build) | QGC firmware flasher | ✅ |
| L8 | Display detection/classification alerts from the SBC | 3 | `alertOperator`, `reportClassification` (UC-5); R3 | QGC message panel (`STATUSTEXT` renders natively) | ✅ (text) |
| L9 | *Optional:* plot detections as map POI markers (beyond text) | 3 | UC-5 alert UX | None turnkey — QGC plugin or companion script | 🚧 **D-3 (optional)** |
| L10 | Post-flight log review (tlog/dataflash) | 1 | UC-7 post-flight | QGC, **UAV Log Viewer**, MAVExplorer | ✅ |
| L11 | *(Phase 4)* Live thermal/AI video display via OpenHD ground unit | 4 | UC-13; R4_GCS_VIDEO_DISP | **QOpenHD** (VMware VM per SE plan) | ⏸ |

**Laptop verdict: nothing required to develop.** QGC covers L1–L8/L10; D-3 is an optional UX enhancement to decide during Phase-3 field trials (text alerts may be fully sufficient).

---

## 2. Flight controller — `drone.platform` (BLITZ F7 on the Chimera9)
Everything on this component is **ArduPilot (ArduCopter ≥ 4.5)** — zero custom flight code, consistent with R5. The real engineering here is **parameter configuration**, and two of those parameter sets *are* the open §3.7 failsafe requirements.

| # | Function | Phase | Trace | Existing software | Status |
|---|---|---|---|---|---|
| F1 | Attitude stabilization / rate control | 1 | *implied* (under `launch`/`flyRoute`) | ArduCopter | ✅ |
| F2 | State estimation (EKF3: GPS + IMU + baro + compass) | 1 | *implied*; GNSS via `GpsModule` | ArduCopter | ✅ |
| F3 | Arming / takeoff / landing sequencing | 1 | `launch`, `returnAndRecover` (UC-3/7); FlightMode disarmed→armed→takeoff, land | ArduCopter | ✅ |
| F4 | Autonomous waypoint flight at set speed/altitude (AUTO) | 1 | `flyRoute` (UC-4); R1, R2 — `WPNAV_SPEED` = 2.23 m/s | ArduCopter AUTO | 🔧 |
| F5 | Accept external guidance: mode switches + position targets from SBC | 3 | FlightMode cruise⇄loiter; R4_SBC_DATA_AF | ArduCopter GUIDED (+ `SERIALx_PROTOCOL=2` for the SBC UART) | 🔧 |
| F6 | RC control link decode + manual flight modes | 1 | R4_GCS_CTRL | ArduCopter CRSF/ELRS driver | ✅ |
| F7 | Telemetry downlink to GCS (MAVLink over ELRS) | 1 | R4_GCS_TELEM | ArduCopter + ELRS airport/telemetry | ✅ |
| F8 | **Link-loss failsafe → RTL** | 1 | FlightMode `flyingToRtlOnLinkLoss` (UC-9); §3.7 *open req* | ArduCopter `FS_THR_*`, `FS_OPTIONS` | 🔧 (values = the requirement) |
| F9 | **Battery failsafe → RTL** (reserve threshold) | 1 | FlightMode `flyingToRtlOnLowBattery` (UC-10); R6 reserve *open req* | ArduCopter `BATT_LOW_VOLT/_MAH`, `BATT_FS_LOW_ACT` | 🔧 (values = the requirement) |
| F10 | ESC control (DShot) + motor mixing | 1 | *implied* | ArduCopter | ✅ |
| F11 | Battery monitoring (V/I sensing for telemetry + F9) | 1 | R4_GCS_TELEM | ArduCopter battery monitor | ✅ |
| F12 | Analog OSD overlay on FPV video | 1 | UC-6 piloting aid | ArduCopter onboard OSD | ✅ |
| F13 | Onboard dataflash logging | 1 | UC-7 post-flight analysis | ArduCopter | ✅ |
| F14 | *Optional:* geofence / altitude limits | 1 | safety (unmodeled) | ArduCopter fence | ✅ |

**FC verdict: nothing required to develop.** Verify the ArduPilot board target for the BLITZ F7 variant before committing (flagged in the gap analysis). The F8/F9 parameter choices should be captured as formal requirements (closes SSS §3.7).

---

## 3. SBC — `drone.sbc` (NanoPi M5, RK3576, 6-TOPS NPU)
**All development on the project lives here.** The SBC hosts the only two capabilities that do not exist anywhere today.

| # | Function | Phase | Trace | Existing software | Status |
|---|---|---|---|---|---|
| S1 | OS, boot, device provisioning | 2 | *implied* | FriendlyElec Ubuntu/Debian arm64 image | ✅ |
| S2 | Thermal camera capture (USB-UVC 640×512 @ 25 Hz) | 2 | `streamThermal` (UC-4); R4_SBC_VIDEO_IN | Linux V4L2/libuvc; OpenCV/GStreamer | ✅ |
| S3 | NPU inference runtime | 3 | `InferFrame`/`ClassifyTarget` execution substrate; R4_SBC_PWR | **RKNN-Toolkit2 / librknnrt** (why RK3576 was selected) | ✅ |
| S4 | **Detect deer/turkey/human-sized heat source @ 120 m, ≥ 90% conf** | 3 | `InferFrame` (R3_1) | **None exists** — no off-the-shelf LWIR wildlife detector | 🚧 **D-1** |
| S5 | **Classify species (deer/turkey/other/human) @ 90 m, ≥ 80% conf** | 3 | `ClassifyTarget` (R3_2) | **None exists** | 🚧 **D-1** |
| S6 | **Mission orchestration** — sweep/investigate state machine, POI geotag, operator alerts, AUTO⇄GUIDED mode control, descent/loiter targets, retry/timeout policy | 3 | `SweepAndDetect`, `InvestigateAndClassify`, `DetectInvestigateClassify`; the two `send`s | **None exists** as a product — control-contract skeleton already built & tested in [`autonomy_sim/`](autonomy_sim/) (§C26) | 🚧 **D-2** |
| S7 | MAVLink transport FC⇄SBC (encode/decode, helpers) | 3 | R4_SBC_DATA_AF | **pymavlink** / MAVSDK-Python | ✅ |
| S8 | MAVLink stream sharing (SBC app + GCS telemetry on one FC port) | 3 | R4_SBC_DATA_AF | **mavlink-router** / mavproxy | ✅ |
| S9 | Service hardening: auto-start on boot, crash restart, safe stand-down | 3 | *implied* (field ops, single operator) | systemd units (config) + D-2 behavior | ✅ (config; behavior in D-2) |
| S10 | Geodesy/waypoint math for POI + descent targets | 3 | `markPoi`, `rerouteToTarget` | pymap3d / geographiclib | ✅ |
| S11 | *(Phase 4)* Digital video downlink air unit | 4 | UC-13 | **OpenHD** | ⏸ |
| — | ~~Video recording / DVR~~ | — | **out of scope by design** — no recording in the committed architecture (DVR removed 2026-07-05) | — | — |

**SBC verdict: the entire development scope of the project is D-1 + D-2.**

---

## D-register — capabilities to be developed

| ID | Capability | Why it doesn't exist | Scope | Requirements carried | Status |
|---|---|---|---|---|---|
| **D-1** | **Thermal wildlife detection & classification model** (640×512 LWIR; deer/turkey/other/human; two operating points: presence @ 120 m, species @ 90 m) | No COTS/OSS model for LWIR wildlife at these classes/altitudes. Public thermal datasets (FLIR ADAS, BIRDSAI) only bootstrap — deer/turkey data must largely be **self-collected** | Dataset (collect + label) → fine-tune YOLO-nano-class detector → ONNX → `.rknn` → validate on held-out set + field demo. Training runs on a dev PC; only the `.rknn` artifact deploys | **R3, R3_1 (90%), R3_2 (80%)** — the mission-defining burden | Not started — **the long pole**; data collection can begin before Phase 2 hardware |
| **D-2** | **Onboard mission application** (the software realization of `SweepAndDetect` / `InvestigateAndClassify` / `DetectInvestigateClassify`) | Companion-computer frameworks exist for generic tasks, but the sweep→detect→investigate→classify→resume mission logic is unique to this CONOPS | Integrate S2 capture + S3/D-1 inference into the tested control skeleton; POI geotag; alert formatting; classify retry/timeout policy (open); systemd hardening; SITL then flight test | R4_SBC_VIDEO_PROC, R4_SBC_DATA_AF, R4_SBC_PWR/TEMP (budget), UC-5 | **Control contract done & tested** (`autonomy_sim/`, §C26); capture/inference integration + policy + hardening remain |
| **D-3** | *(Optional)* GCS map-POI display of detections beyond `STATUSTEXT` text | QGC has no turnkey "plot companion-computer detections as map markers" | QGC plugin or small companion viewer; **decide after Phase-3 field trials** — text alerts may suffice | UC-5 operator UX (supports R3_1/R3_2 demonstration) | Deferred decision |

## Function-level development breakdown (D-1 / D-2) — the work to start

Now **recorded in the model** (2026-07-10): `Architecture::Software` package + `SoftwareItem` part usages composed in `Laptop` (gcsApp), `Airframe` (fcSoftware), and `SBCPayload` (rknnRuntime, mavlinkRouter, **missionApp = D-2**, **thermalModel = D-1**) in `model.sysml`, `model_community_balanced.sysml`, and (lean) `test.sysml`; `thermalModel` carries `satisfy R3_1; satisfy R3_2;`. MODEL_ISSUES.md §C28.

### D-2 — Onboard mission application: software functions
Status keys: ✅ built & tested in [`autonomy_sim/`](autonomy_sim/) · ◐ partially built there · ✗ not started.

| ID | Software function | Notes | Status |
|---|---|---|---|
| D2.1 | MAVLink connection + companion heartbeat | srcComponent 191, 1 Hz | ✅ |
| D2.2 | Telemetry state tracker (FC mode, position/altitude) | `HEARTBEAT`, `GLOBAL_POSITION_INT` | ✅ |
| D2.3 | Mode supervisor (AUTO⇄GUIDED) | switching ✅; **`COMMAND_ACK` verify + retry** ✗ | ◐ |
| D2.4 | Sweep controller (`SweepAndDetect` loop, 0.90 gate) | state machine ✅ vs mock detector | ◐ |
| D2.5 | UVC capture pipeline (V4L2, 640×512 @ 25 Hz, frame queue/drop policy) | first real-SBC task | ✗ |
| D2.6 | RKNN inference wrapper implementing the `Detector` interface | pre/post-process (letterbox, NMS); interface already defined | ✗ |
| D2.7 | POI geolocator | vehicle-position POI ✅; pixel-offset ground-projection math ✗ | ◐ |
| D2.8 | Investigate maneuver generator | 90 m descent target ✅; `adjustOrbit` loiter variation ✗ | ◐ |
| D2.9 | Classification controller (0.80 gate, retries, timeout) | tick-timeout ✅; **loiter time-budget policy = OPEN decision** | ◐ |
| D2.10 | Operator alert formatter (`STATUSTEXT` conventions) | basic DETECT/CLASSIFY strings ✅; message schema ✗ | ◐ |
| D2.11 | Failsafe observer + stand-down | ✅ tested (RTL forces PASSIVE) | ✅ |
| D2.12 | Service hardening (systemd, watchdog, logging, config) | field-ops requirement | ✗ |
| D2.13 | SITL integration suite (ACKs, EKF/arming gates, GUIDED nav) | mock-FC suite ✅; real SITL ✗ | ◐ |

### D-1 — Thermal model: work items

| ID | Work item | Notes |
|---|---|---|
| D1.1 | Data collection plan + rig | deer/turkey/human LWIR clips, 90–120 m look-down, daytime with ≥5 °C thermal contrast — **start now; longest lead** |
| D1.2 | Bootstrap dataset assembly | FLIR ADAS + BIRDSAI subsets; class mapping to deer/turkey/other/human |
| D1.3 | Labeling + augmentation pipeline | boxes; scale/rot/contrast augmentation across the altitude band |
| D1.4 | Training pipeline | YOLO-nano fine-tune → ONNX (Ultralytics AGPL caveat) |
| D1.5 | Eval harness vs requirement operating points | recall@120 m ≥ 0.90 (R3_1); species acc@90 m ≥ 0.80 (R3_2); held-out set |
| D1.6 | RKNN conversion + INT8 quantization validation | accuracy-delta check vs ONNX |
| D1.7 | On-target benchmark | latency/FPS, ≤10 W, passive-cooling thermals (R4_SBC_VIDEO_PROC/PWR/TEMP) |
| D1.8 | Field validation protocol | SSS §4 Demonstration of R3_1/R3_2 |

**Start-now set (no hardware dependency):** D1.1 + D1.2 (data), D2.3 (ACK handling) + D2.13 (SITL suite). **First on-SBC tasks:** D2.5 + D2.6 + D1.7.

## Other software-bearing components (config only — no development)
- **RC transmitter (RcTx):** EdgeTX firmware + ELRS TX module — model setup, bind, failsafe RC config. ✅
- **ELRS receiver (drone):** ExpressLRS firmware — bind + packet-rate/telemetry-ratio config (per the ELRS range analysis). ✅
- **Thermal camera (T13):** vendor firmware, USB-UVC out of the box. ✅
- **GPS (u-blox):** configured by ArduPilot at boot. ✅
- **Charger (CHG1):** standalone; no software interface. ✅

## Summary
| Component | Functions | Exist today | To develop |
|---|---|---|---|
| Laptop (GCS) | 11 | 10 (QGC + macOS tools) + 1 deferred | 0 required (D-3 optional) |
| Flight controller | 14 | 14 (ArduPilot; 4 are config-as-requirements) | 0 |
| SBC | 11 | 8 (+1 out of scope, 1 deferred) | **D-1 model, D-2 mission app** |

The mission is buildable with exactly **two developed capabilities**, both on the SBC — everything else is adopt-and-configure. Recommended sequencing: start **D-1 data collection now** (season/opportunity-dependent, longest lead), continue D-2 against SITL (per `autonomy_sim/README.md`), and write the F8/F9 failsafe parameter values into the model as requirements.

---
*Sources: [`behavior.sysml`](../behavior.sysml) (functions + `missionContext` allocations, §C25), [`software_gap_analysis.md`](software_gap_analysis.md) (interface contract, licenses, real-time budget), [`SELECTED_COMPONENTS.md`](../SELECTED_COMPONENTS.md), [`systems_engineering_plan.md`](../systems_engineering_plan.md), CLAUDE.md (MacBook Air GCS; DVR removal), MODEL_ISSUES.md §C20/§C25/§C26.*
