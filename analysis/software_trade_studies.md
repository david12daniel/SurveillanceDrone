# Software Trade Studies — Alternatives for the Adopt (EXISTS) Items

## Purpose
For each software capability that **already exists as a product** (the `status = EXISTS` items in the model's `Architecture::Software` register), survey the alternative solutions — **free and paid** — that satisfy the capability, trade them against this project's real constraints, and **confirm or revise** the selection. The two `TO_DEVELOP` items (D-1 thermal model, D-2 mission app) are excluded by definition: no product satisfies them (that's why they're developed).

Companions: [`software_gap_analysis.md`](software_gap_analysis.md) (adopt-vs-build + the mission-app interface contract), [`software_by_component.md`](software_by_component.md) (per-component register + D-1/D-2 breakdown). Selections of record: [`SELECTED_COMPONENTS.md`](../SELECTED_COMPONENTS.md).

**Two constraints dominate every study below:** the GCS runs on the existing **MacBook Air (macOS/Apple Silicon)**, and the SBC is the locked **NanoPi M5 / RK3576 (6-TOPS NPU)**. Several "trades" therefore have a *forced* winner — which is itself the finding.

## Summary — all six selections CONFIRMED (no changes)
| Capability | Component | Selected | Best alternative | Verdict |
|---|---|---|---|---|
| GCS application | Laptop | **QGroundControl** | ArduDeck (native Mac) | Keep QGC; trial ArduDeck as backup |
| FC firmware | Flight controller | **ArduPilot ArduCopter** | PX4 | Keep ArduPilot (forced by tested contract + F7/FPV fit) |
| NPU inference runtime | SBC | **RKNN-Toolkit2** | (none reach the NPU) | Keep RKNN (**forced** by hardware) |
| MAVLink companion library | SBC | **pymavlink** | MAVSDK-Python | Keep pymavlink |
| MAVLink router | SBC | **mavlink-router** | mavp2p | Keep mavlink-router (mavp2p acceptable) |
| Thermal video capture | SBC | *(open)* OpenCV / V4L2 | GStreamer | Recommend OpenCV now; GStreamer if Phase-4 downlink |

Legend: ✅ meets · ⚠️ partial/caveat · ❌ fails.

---

## TS-1 — Ground Control Station application (Laptop)
**Capability (L1–L10):** plan + upload/download waypoint missions; live telemetry + map; FPV/analog video display (Skydroid UVC); FC parameter config + sensor calibration incl. `FS_*`/`BATT_*`; firmware flashing; detection-alert (`STATUSTEXT`) display; log review — all over MAVLink. **Hard filter: native macOS / Apple Silicon** (the MacBook Air is not replaced).

| Product | Cost / License | macOS (Apple Silicon) | ArduPilot MAVLink | Mission planning | Params / cal / flash | Video | Verdict |
|---|---|---|---|---|---|---|---|
| **QGroundControl 4.6.x** | Free · Apache-2.0/GPLv3 | ✅ native (ASi + Intel) | ✅ | ✅ | ✅ | ✅ UVC widget | ✅ **SELECTED** |
| **ArduDeck** | Free · source/license unverified | ✅ native Apple-Silicon builds | ✅ ArduPilot-focused | ✅ + survey grids/geofence | ✅ params + firmware + cal | ⚠️ unclear | ✅ strong Mac-native **backup** |
| Mission Planner | Free · GPLv3 | ❌ Windows/.NET (Wine/VM only) | ✅ most complete ArduPilot GCS | ✅ | ✅ | ⚠️ | ❌ macOS |
| MAVProxy | Free · GPLv3 | ✅ (Python CLI) | ✅ | ⚠️ console/CLI | ✅ CLI | ❌ | ⚠️ power-user adjunct, not a primary GCS |
| UgCS (SPH Engineering) | **Paid** (subscription) · commercial | ✅ desktop | ✅ | ✅ pro survey/mapping | ✅ | ⚠️ | ⚠️ commercial survey tool — overkill, no benefit here |

**Recommendation — keep QGroundControl.** It is the only mature, full-feature, **native-macOS** MAVLink GCS, and it already covers every laptop function. The most capable ArduPilot GCS (Mission Planner) is ruled out by the macOS constraint. **New finding: ArduDeck** is a genuinely useful native-Apple-Silicon ArduPilot GCS (waypoints, survey grids, geofence, params, firmware, calibration) — worth installing during Phase 1 as a **backup / for its survey-grid planning**, but verify its license/source before depending on it. No paid option (UgCS et al.) adds anything for a single-operator ArduPilot build.

---

## TS-2 — Flight-controller firmware (Airframe / BLITZ F7)
**Capability (F1–F14):** stabilization, EKF state estimation, AUTO waypoint flight at 2.23 m/s, **GUIDED external control from the SBC**, CRSF/ELRS RC, MAVLink telemetry, link-loss + battery failsafes, OSD, logging. **Hard filters:** runs on the **BLITZ F7 (STM32F7)**; supports **companion-driven GUIDED control + MAVLink missions**.

| Firmware | License | F7 board | AUTO waypoints | GUIDED / companion offboard | MAVLink missions | FPV-frame fit | Verdict |
|---|---|---|---|---|---|---|---|
| **ArduPilot ArduCopter 4.6.3** (4.7 beta) | Free · GPLv3 | ✅ | ✅ | ✅ **GUIDED — mature; our tested contract** | ✅ full | ✅ proven on F7 FPV | ✅ **SELECTED** |
| PX4 1.15/1.16 | Free · **BSD-3** | ⚠️ limited F7/FPV board support | ✅ | ✅ OFFBOARD (research/ROS 2 standard) | ✅ | ⚠️ Pixhawk-oriented | ⚠️ capable; weaker F7/FPV fit; would void the tested contract |
| iNav 8.x | Free · GPLv3 | ✅ | ✅ WP missions | ⚠️ no true GUIDED/companion API | ⚠️ partial | ✅ FPV-native | ⚠️ waypoints yes, **companion autonomy no** |
| Betaflight | Free · GPLv3 | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ no autonomy/missions |

**Recommendation — keep ArduPilot (strongly confirmed).** It is the only stack combining **mature GUIDED companion control** — on which the D-2 mission app and the autonomy contract are *already built and tested* ([`autonomy_sim/`](autonomy_sim/), MODEL_ISSUES.md §C26) — with full MAVLink missions, F7 support, and proven FPV-frame use. PX4's permissive BSD license and academic momentum are real advantages *in the abstract*, but its F7/FPV board support is weaker and switching would invalidate the tested AUTO↔GUIDED contract for **zero capability gain**. Betaflight and iNav cannot do companion-driven autonomy — a hard fail against R3's mission. *Currency note: current stable is Copter **4.6.3** (Nov 2025); the model's `">= 4.5"* remains valid — adopt 4.6.x.*

---

## TS-3 — SBC NPU inference runtime
**Capability (S3):** execute the quantized detection/classification model at ≥ 25 FPS within **≤ 10 W** and passive cooling (R4_SBC_PWR / _VIDEO_PROC / _TEMP), on the **RK3576 6-TOPS NPU**. **Decisive hardware fact:** the RK3576 NPU is reachable **only** through Rockchip's RKNN stack; every other runtime falls back to the ARM CPU or Mali GPU and misses the NPU.

| Runtime | License | Uses the RK3576 **NPU**? | Perf / power fit | Verdict |
|---|---|---|---|---|
| **RKNN-Toolkit2 + librknnrt 2.x** | Free · Rockchip (proprietary, free redistribution) | ✅ **only NPU path** | ✅ NPU, real-time within ≤ 10 W | ✅ **SELECTED (mandatory)** |
| ONNX Runtime | Free · MIT | ❌ CPU only on RK3576 (no NPU EP) | ❌ CPU misses real-time + power | ❌ fallback/debug only |
| LiteRT (TF-Lite) | Free · Apache-2.0 | ⚠️ CPU + Mali-GPU delegate — **not the NPU** | ❌ GPU worse on power than NPU | ❌ fallback |
| ncnn / MNN | Free · BSD-3 / Apache-2.0 | ⚠️ ARM CPU + Vulkan (Mali) — not the NPU | ❌ no NPU | ❌ fallback |

**Recommendation — RKNN is effectively mandatory.** It is the sole path to the 6-TOPS NPU, and *using that NPU is exactly why SBC3/RK3576 was locked* (memory: RKNN-confirmed; SBC2 rejected on power/cooling). Every alternative runs on CPU or Mali GPU and would bust the R4_SBC power/thermal/real-time budget. This trade has a **forced winner by design**; the alternatives matter only as a CPU-fallback path for bring-up/debug. (Toolchain: PyTorch → ONNX → RKNN; Ultralytics ships an RKNN export for YOLO, feeding D-1.)

---

## TS-4 — MAVLink companion library (mission app / D-2)
**Capability (S7, D2.1–D2.3):** MAVLink 2 encode/decode, `SET_MODE`/`DO_SET_MODE`, `SET_POSITION_TARGET_GLOBAL_INT`, telemetry parse — Python, ARM64 Linux, **control-level** access.

| Library | License | Abstraction | ArduPilot fit | Maintenance (2026) | Verdict |
|---|---|---|---|---|---|
| **pymavlink** | Free · LGPLv3 | Low (message-level) | ✅ reference/native | ✅ active (MAVLink project) | ✅ **SELECTED** (already in `autonomy_sim`) |
| MAVSDK-Python | Free · BSD-3 | High (async plugins + daemon) | ✅ (PX4-first; ArduPilot OK) | ✅ active (Dronecode) | ⚠️ cleaner API, but PX4-oriented + heavier deps |
| dronekit-python | Free · Apache-2.0 | High (vehicle API) | ✅ ArduPilot-oriented | ❌ **orphaned** — "looking for maintainers" (2025) | ❌ maintenance risk for new work |
| MAVROS (ROS 2) | Free · BSD | High (ROS) | ✅ | ✅ | ❌ ROS 2 overhead unjustified here |

**Recommendation — keep pymavlink.** It's the reference implementation, **already integrated and tested** in `autonomy_sim/`, gives the exact low-level control the mode/target logic needs, and is ArduPilot-native. MAVSDK-Python is the credible modern alternative (nicer async API) but is PX4-first and adds a background daemon + heavier dependencies — no benefit for a control-loop-level app on a constrained SBC. **dronekit is orphaned** as of 2025 (community seeking maintainers) — avoid for new development despite its historically friendly API. MAVROS only makes sense if the project were adopting ROS 2 (it isn't).

---

## TS-5 — MAVLink router / multiplexer (SBC)
**Capability (S8):** share the single FC ↔ SBC UART between the D-2 mission app and the GCS telemetry link (so both the onboard app and QGC see the FC).

| Router | License | Language | Footprint | Verdict |
|---|---|---|---|---|
| **mavlink-router** | Free · Apache-2.0 | C++ | Light on CPU; systemd-friendly; the de-facto standard | ✅ **SELECTED** |
| mavp2p | Free · MIT | Go | Very light; single static multi-arch binary; no deps | ✅ strong lightweight alternative |
| MAVProxy | Free · GPLv3 | Python | Heavy (it's a full GCS with routing) | ⚠️ overkill on a headless SBC |

**Recommendation — keep mavlink-router** (efficient, standard, clean systemd integration). **mavp2p** is an equally valid, arguably simpler pick — a single dependency-free Go binary that's easy on a constrained SBC — and is an acceptable drop-in substitute if you prefer no runtime deps. MAVProxy can route but drags in a whole Python GCS; unnecessary weight here. All three are free; there is no paid option (nor need for one).

---

## TS-6 — Thermal video capture (SBC)
**Capability (S2 / D2.5):** capture the T13 thermal stream (USB-UVC, 640×512 @ 25 Hz) into the inference pipeline with a sane frame-drop policy. **This is the one genuinely open sub-decision.**

| Method | License | Overhead | Notes | Verdict |
|---|---|---|---|---|
| **OpenCV `VideoCapture`** | Free · Apache-2.0 | Low | Trivial UVC grab; the D2.6 inference wrapper already uses OpenCV/NumPy | ✅ **recommend (prototype)** |
| V4L2 direct (libv4l) | Free · LGPL/GPL | Lowest | Most control; more code; move here if capture profiles hot | ✅ production hot-path option |
| GStreamer | Free · LGPL | Low–med | Pipelines + HW accel; easy to add RTSP/downlink later | ⚠️ best **if** Phase-4 OpenHD downlink is built |
| FFmpeg / libav | Free · LGPL/GPL | Med | Heavier; overkill for a raw UVC grab | ⚠️ |

**Recommendation — OpenCV `VideoCapture` for the prototype** (one dependency, and D2.6 already pulls in OpenCV for pre/post-processing). Drop to **V4L2-direct** only if profiling shows capture overhead eating the real-time budget, or adopt **GStreamer** if/when the Phase-4 OpenHD downlink wants a shared, hardware-accelerated pipeline. Low-risk either way; no paid option.

## Minor utilities (no full trade study warranted)
- **Geodesy** (POI offset + descent-target math, S10): **pymap3d** (BSD) is the lightest for lat/lon offset + ENU; alternatives geographiclib / pyproj are heavier and unnecessary. Any is fine.
- **Service management** (S9 / D2.12): **systemd** is the OS init, not a competitive choice — units + a watchdog, not a product selection.

## Overall findings
1. **No selection changes.** All six adopt items are confirmed against their alternatives.
2. **Two winners are *forced* by earlier hardware/platform locks** — RKNN by the RK3576 NPU, and QGroundControl by the macOS constraint (among full-feature GCSs). Good news: it means those locks don't strand you on a weak tool.
3. **Two credible alternatives are worth keeping in your pocket:** **ArduDeck** (native-Mac ArduPilot GCS — trial as a QGC backup) and **mavp2p** (dependency-free router).
4. **One open sub-decision remains** — the capture method (TS-6) — recommended **OpenCV** now, revisit for Phase 4.
5. **Avoid dronekit** for the mission app despite its friendly API — it's maintainer-orphaned as of 2025; **pymavlink** (already in use) is the safe, native choice.
6. **Cost impact: $0.** Every selected item and every viable alternative is free/open-source; the only paid option surveyed (UgCS) offers no benefit for this build. Consistent with R4.

---
*Sources (accessed 2026-07-11):*
- *ArduPilot Copter releases (4.6.3 stable / 4.7 beta): [firmware.ardupilot.org/Copter/stable](https://firmware.ardupilot.org/Copter/stable/), [github.com/ArduPilot/ardupilot/releases](https://github.com/ArduPilot/ardupilot/releases)*
- *ArduPilot GUIDED vs PX4 OFFBOARD companion control: [docs.px4.io companion_computer](https://docs.px4.io/main/en/companion_computer/), [PX4-vs-ArduPilot comparison](https://th3seus.net/guides/flight-controllers/px4-vs-ardupilot)*
- *GCS on macOS — QGC + ArduDeck (Apple Silicon), Mission Planner Windows-only: [qgroundcontrol.com/portfolio/mac-os-support](https://qgroundcontrol.com/portfolio/mac-os-support/), [ardudeck.com](https://ardudeck.com/)*
- *RKNN vs ONNX/LiteRT on Rockchip NPU (RK3576): [github.com/airockchip/rknn-toolkit2](https://github.com/airockchip/rknn-toolkit2), [Ultralytics Rockchip RKNN export](https://docs.ultralytics.com/integrations/rockchip-rknn), [Edge AI using the Rockchip NPU](https://tristanpenman.com/blog/posts/2025/07/20/edge-ai-using-the-rockchip-npu/)*
- *MAVLink libraries (pymavlink / MAVSDK / dronekit status): [mavlink.io/en/mavgen_python](https://mavlink.io/en/mavgen_python/), [discuss.ardupilot.org pymavlink-vs-mavsdk-vs-dronekit](https://discuss.ardupilot.org/t/pymavlink-vs-mavsdk-python-vs-dronekit-python-for-udp-receiving-program/86422), [github.com/dronekit/dronekit-python](https://github.com/dronekit/dronekit-python)*
- *MAVLink routers (mavlink-router / mavp2p / MAVProxy): [github.com/mavlink-router/mavlink-router](https://github.com/mavlink-router/mavlink-router), [github.com/bluenviron/mavp2p](https://github.com/bluenviron/mavp2p)*
