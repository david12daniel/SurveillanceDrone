# Software Gap Analysis — Adopt vs. Build

## Purpose
Determine, for the committed Phase 1–3 system, **which software already exists** (adopt/configure COTS or open-source) and **which software must be created** to realize the behavior model in [`behavior.sysml`](../behavior.sysml). The unit of analysis is the **function** (`action def`) and its **allocation** to a component (from `missionContext`), not a purchasable part — this is the software analogue of the component trade studies in [`analysis/`](.).

Scope: the committed build (Phases 1–3). Phase 4 (OpenHD digital downlink) is noted where relevant but is deferred (MODEL_ISSUES.md §C20/§C19). Derived from the four-layer behavior model; the mission-defining autonomy is the UC-5 loop closed in **MODEL_ISSUES.md §C25**.

> **Companions:** [`software_by_component.md`](software_by_component.md) — the same analysis cut **per component** (laptop / FC / SBC): full function lists, existing software per function, and the **D-register** of capabilities to be developed (D-1 thermal model, D-2 mission app, D-3 optional GCS POI display). · [`software_trade_studies.md`](software_trade_studies.md) — **alternatives (free + paid) traded** for each adopt/EXISTS item (GCS, FC firmware, NPU runtime, MAVLink library, router, capture).

## Behavioral basis (from `behavior.sysml`)
The software scope is exactly the set of functions the model allocates to programmable components — the flight controller (`drone.platform`), the SBC (`drone.sbc`), and the laptop GCS (`gcs.viewingComputer`). Operator-allocated functions (`prepareSystem`, `monitorMission`) are human tasks and out of software scope except for the tools they operate.

| Function (`action def`) | Allocated to | Phase | Software owner |
|---|---|---|---|
| `ConductSortie.planRoute` | `gcs.viewingComputer` | 1 | **Adopt** — QGroundControl |
| `ConductSortie.launch` | `drone.platform` | 1 | **Adopt** — ArduPilot |
| `ExecuteSurveillance.flyRoute` | `drone.platform` | 1 | **Adopt** — ArduPilot (AUTO) |
| `ConductSortie.returnAndRecover` | `drone.platform` | 1 | **Adopt** — ArduPilot (RTL/LAND) |
| `FlightMode` failsafe transitions | `drone.platform` | 1 | **Adopt** — ArduPilot failsafes (config) |
| `ExecuteSurveillance.streamThermal` | `drone.camera` → `drone.sbc` | 2 | **Adopt** — V4L2/UVC capture |
| `InferFrame` / `ClassifyTarget` | `drone.sbc` | 3 | **Build** — thermal CV model (+ RKNN runtime = adopt) |
| `SweepAndDetect` | `drone.sbc` | 3 | **Build** — mission app (cruise mode) |
| `InvestigateAndClassify` | `drone.sbc` | 3 | **Build** — mission app (loiter mode) |

**Bottom line: two things must be built** — a thermal detection/classification model, and the onboard mission application that wraps it. Everything else is adopt-and-configure.

## Software requirement summary (from `model.sysml`)

| ID | Constraint | Software implication |
|---|---|---|
| R3_1 | Detect deer/turkey/human @ 120 m, ≥ 90% confidence | Model recall/precision burden (cruise) |
| R3_2 | Classify species @ 90 m, ≥ 80% confidence | Model class-accuracy burden (loiter) |
| R4_SBC_VIDEO_IN | Accept camera video format | UVC/V4L2 capture of T13 USB stream |
| R4_SBC_VIDEO_PROC | Process w/o degrading detect/classify | Real-time inference budget (see below) |
| R4_SBC_DATA_AF | Exchange telemetry/status with FC | MAVLink over UART |
| R4_SBC_PWR | ≤ 10 W avg at cruise | NPU-accelerated, not CPU inference |
| R4_SBC_TEMP | Passive cooling across temp range | Sustained-load thermal limit on inference |
| R4_GCS_TELEM | Present telemetry to operator | QGC (adopt) |
| R4_GCS_CTRL | Flight control inputs | ELRS radio + QGC (adopt) |

## Adopt — existing software (configure, don't write)

| Model function(s) | Software | Version | License | Notes / config burden |
|---|---|---|---|---|
| `launch`, `flyRoute`, `returnAndRecover`, `FlightMode` core + failsafe transitions | **ArduPilot / ArduCopter** | 4.5+ | GPLv3 | AUTO/GUIDED/RTL/LAND modes, arming, GUIDED position targets. Configuring `FS_*` / `BATT_*` params **is** the realization of the two open §3.7 failsafe requirements (see §"Failsafes"). |
| `planRoute`, `monitorMission` display, detection alerts | **QGroundControl** | 4.4+ | Apache-2.0 / GPLv3 | Mission upload, live telemetry map, `STATUSTEXT` display. No code — operator tool. |
| `streamThermal` capture | **Linux V4L2 + libuvc**, GStreamer or OpenCV `VideoCapture` | kernel 5.x/6.x | LGPL / Apache-2.0 | T13 is USB-UVC; capture is solved. Frame grab → NPU input tensor. |
| NPU inference runtime | **RKNN-Toolkit2 + rknn-runtime (librknnrt)** | 2.x | Rockchip proprietary (free redistribution) | The reason SBC3/RK3576 was locked (memory: RKNN-confirmed). Converts the trained model `.onnx`→`.rknn`; runs on the 6-TOPS NPU. |
| FC ↔ SBC MAVLink plumbing | **pymavlink** or **MAVSDK-Python** | pymavlink 2.4.x / MAVSDK 2.x | LGPLv3 / BSD-3 | Message encode/decode + helpers (`set_mode`, position targets). MAVSDK if you prefer async/typed API. |
| Multiplexing MAVLink (FC↔SBC↔GCS telemetry) | **mavlink-router** or **mavproxy** | current | Apache-2.0 / GPLv3 | Lets the SBC app and the ground telemetry link share the one FC serial port. |
| Route/waypoint math, geodesy | **pymap3d** / **geographiclib** | current | BSD / MIT | Lat/lon offset + slant-range math for POI geotag and descent target. |

**Adopt-side cost: $0** (all free/OSS). No new procurement — consistent with R4 and with the Phase-3 "software-only, no hardware" plan.

## Build — software that does not exist

### Build item 1 — Thermal detection/classification model (`InferFrame`, `ClassifyTarget`)
No off-the-shelf deer/turkey/human classifier exists for 640×512 LWIR. This carries the **R3_1 (90% detect) / R3_2 (80% classify)** burden.

- **Approach:** fine-tune a small object detector (YOLO-family) on thermal wildlife imagery, export ONNX → convert to `.rknn` for the NPU.
- **Model:** Ultralytics YOLOv8n/YOLO11n (nano) is the pragmatic default for a 6-TOPS NPU at video rate. **License caveat: Ultralytics is AGPL-3.0** — fine for personal/hobbyist use, but it "infects" redistribution; YOLOv5 (also AGPL) or a permissively-licensed reimplementation are alternatives if that ever matters.
- **Data sources (bootstrapping):** Teledyne **FLIR ADAS** thermal dataset (person/animal, research license), **BIRDSAI** (thermal wildlife, aerial, CC), plus **self-collected** deer/turkey thermal clips — expect this to be the real effort. Augment with rotation/scale to cover the 90–120 m altitude range and the ≥ 5 °C differential (R3) daytime condition.
- **Two operating points, one model:** R3_1 is *presence* at 120 m (favor recall); R3_2 is *species* at 90 m (favor per-class precision). The model runs at both altitudes; the mission app applies the two confidence thresholds (`detectThreshold = 0.90`, `classifyThreshold = 0.80`) already in the model.
- **Verification:** this is where the R3_1/R3_2 percentages get earned — a held-out thermal test set + field demonstration per the requirements export §4 (Demonstration).

### Build item 2 — Onboard mission application (`SweepAndDetect`, `InvestigateAndClassify`)
**This is the loop that doesn't exist yet, and its design is literally the two new `action def`s.** A Python (or C++) app on the NanoPi that runs the detect-investigate cycle and drives the FC over MAVLink. Its structure maps 1:1 to the model:

| Model element | App responsibility |
|---|---|
| `DetectInvestigateClassify` (umbrella, cycles the halves) | Main loop / state controller |
| `SweepAndDetect` (cruise half) | Grab frame → `InferFrame` (NPU) → if conf ≥ 0.90: geotag POI, alert operator, **emit `TargetDetected`** |
| `InvestigateAndClassify` (loiter half) | Command GUIDED descent → `ClassifyTarget` (NPU) w/ retry → report → rejoin route → **emit `InvestigationComplete`** |
| `send targetDetectedEvt to missionContext` | MAVLink **AUTO → GUIDED** mode switch |
| `send investigationCompleteEvt to missionContext` | MAVLink **GUIDED → AUTO** mode switch |

The two `send`s formalized in §C25 are the app's mode-switch events. `TargetDetected`/`InvestigationComplete` are **internal** (SBC-originated); `LinkLossDetected`/`LowBatteryReached` are **external** (FC-originated) — the app does not generate them, matching the model.

## Interface contract for the mission app (derived from the sequence scenarios)

**Consumes (from FC via MAVLink):**
- `GLOBAL_POSITION_INT` (#33) — lat/lon/alt for POI geotag + descent target math
- `HEARTBEAT` (#0) — current flight mode (confirm AUTO before a detection excursion; detect FC-commanded RTL)
- `SYS_STATUS` (#1) / `BATTERY_STATUS` (#147) — awareness only; the *failsafe decision* is the FC's, not the app's
- Video: T13 USB-UVC stream via V4L2 (not MAVLink)

**Produces (to FC / GCS via MAVLink):**
- `MAV_CMD_DO_SET_MODE` (#176) or `SET_MODE` — the two mode switches (AUTO=3 / GUIDED=4 in ArduCopter — *verify against your firmware version*)
- `SET_POSITION_TARGET_GLOBAL_INT` (#86) — GUIDED descent/loiter target over the animal (120 m → 90 m)
- `STATUSTEXT` (#253) — operator alerts (detection "DEER 90m N42.3.. W…", classification result) shown on the QGC map/message panel (the committed no-downlink alert path, §C20)

**Nominal detection encounter (the main sequence):**
1. FC in **AUTO**, flying the route at 120 m; app in `SweepAndDetect`, inferring each frame.
2. Detection ≥ 0.90 → app reads `GLOBAL_POSITION_INT`, computes POI, sends `STATUSTEXT` alert, **emits `TargetDetected`** → `MAV_CMD_DO_SET_MODE` **GUIDED**. (FlightMode: `cruise → loiter`.)
3. App sends `SET_POSITION_TARGET_GLOBAL_INT` to descend to 90 m over the POI; runs `ClassifyTarget` with bounded retries (`adjustOrbit` on < 0.80, timeout policy TBD).
4. On success (or timeout) → `STATUSTEXT` species report → command climb + **emit `InvestigationComplete`** → `MAV_CMD_DO_SET_MODE` **AUTO** (resume route). (FlightMode: `loiter → cruise`.)

**Link-loss / low-battery (failsafe sequences):** the **FC** detects the condition and autonomously switches to RTL — no app action required. The app simply observes the mode change via `HEARTBEAT` and stops issuing GUIDED commands. This is why the model shows these triggers as external (`FlightMode.flying → returnToLaunch`), not app-emitted.

## Failsafes = ArduPilot configuration, not code (closes two open requirements)
SSS §3.7 flags link-loss and low-battery failsafe requirements as "to be specified." They are realized by **ArduPilot parameters**, so specifying those parameter values *is* writing the requirements:
- Link loss: `FS_THR_ENABLE`, `FS_OPTIONS`, `FS_THR_VALUE` → action = RTL.
- Low battery (the R6 reserve-threshold gap): `BATT_LOW_VOLT` / `BATT_CRT_VOLT`, `BATT_FS_LOW_ACT` = RTL, `BATT_LOW_MAH` reserve. Picking the reserve mAh is the open policy decision noted in the model (`HandleLowBattery` reserve TBD).
> Recommended follow-up: capture the chosen values as real requirements (R?_FS_LINK, R?_FS_BATT) — cheap, and it removes the §3.7 gap.

## Real-time budget (R4_SBC_VIDEO_PROC, R4_SBC_PWR, R4_SBC_TEMP)
The build must fit the SBC envelope: T13 streams 640×512 @ 25 Hz. YOLO-nano on a 6-TOPS RK3576 NPU runs well inside frame time at this resolution, but three model requirements must be *tested* (not assumed): end-to-end latency small enough not to degrade detect/classify (R4_SBC_VIDEO_PROC), ≤ 10 W average (R4_SBC_PWR), and sustained-inference thermals under passive cooling (R4_SBC_TEMP). These are the T (bench-test) items in the requirements export §4.

## Requirement coverage

| Requirement | Adopt | Build | Verification |
|---|---|---|---|
| R3_1 detect 90% | — | thermal model (cruise) | Demonstration + test set |
| R3_2 classify 80% | — | thermal model (loiter) | Demonstration + test set |
| R4_SBC_VIDEO_IN | V4L2/UVC | app capture glue | Inspection/Test |
| R4_SBC_VIDEO_PROC | RKNN runtime | app pipeline | Test (latency) |
| R4_SBC_DATA_AF | pymavlink | app MAVLink I/O | Test |
| R4_SBC_PWR / _TEMP | RKNN (NPU) | efficient pipeline | Test (bench) |
| launch/route/RTL/land | ArduPilot | — | Demonstration |
| planRoute/telemetry/control | QGC + ELRS | — | Demonstration |
| link-loss / low-batt failsafe | ArduPilot params | (config values) | Test |

## Open questions / risks
1. ~~**Classification retry/timeout policy** — `InvestigateAndClassify.adjustOrbit` loop is unbounded in the model; needs a loiter-time budget + a "log as unclassified, resume" exit. (Also a small R6 endurance draw.)~~
   **RESOLVED 2026-08-05:** 30 s loiter time budget per investigation, then log as unclassified and resume. See `analysis/classify_loiter_budget.md`.
2. **Low-battery reserve threshold** — still the open R6-derived gap; pick `BATT_LOW_MAH`.
3. **Thermal training data** — the single biggest build risk; self-collected deer/turkey thermal footage is likely required to hit 90/80%.
4. **Ultralytics AGPL** — fine for personal use; revisit if the app is ever shared/distributed.
5. **GUIDED-mode authority + operator override (UC-11)** — RESOLVED 2026-08-06. Operator CAN override, mechanism = QGC mode switch (no dedicated app input). See analysis/operator_override_UC11.md. Downstream: R-UC11-1 through R-UC11-4 (override detection, SWEEP re-entry, alert, model update).
6. **ArduCopter mode numbers** — verify AUTO=3/GUIDED=4 against the exact firmware build before hard-coding.

## Next steps
1. ✅ **DONE — control contract de-risked in software.** [`autonomy_sim/`](autonomy_sim/) implements the mission-app skeleton + a mock MAVLink FC + passing contract tests proving the AUTO→GUIDED→AUTO loop, GUIDED descent, operator alerts, and failsafe stand-down — no ArduPilot or CV model required (MODEL_ISSUES.md §C26). Next: run the same app against real ArduPilot SITL (README) to add mode-ACK/GUIDED-nav/arming validation.
2. Prototype **capture + RKNN** on the NanoPi M5 with a stock YOLO model to measure the real-time/power/thermal budget (R4_SBC_VIDEO_PROC/PWR/TEMP) early.
3. Begin **thermal data collection**; fine-tune YOLO-nano; iterate to the R3_1/R3_2 operating points.
4. Implement the **mission app** as the two model halves; integrate against SITL, then the real FC.
5. Capture the two **failsafe parameter sets** as requirements (removes SSS §3.7 gap).

---
*Sources: [`behavior.sysml`](../behavior.sysml) (functions, allocations, `send` events — MODEL_ISSUES.md §C25), [`model.sysml`](../model.sysml) `Requirements`, [`SELECTED_COMPONENTS.md`](../SELECTED_COMPONENTS.md) (SBC3 NanoPi M5 / RK3576, camera T13), [`systems_engineering_plan.md`](../systems_engineering_plan.md) (Phase 3 = onboard autonomy). MAVLink message/command IDs per the common.xml dialect; ArduCopter mode numbers per ArduPilot 4.5.*
