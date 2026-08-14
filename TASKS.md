# TASKS — remaining work by phase

_Generated 2026-08-02 from [`systems_engineering_plan.md`](systems_engineering_plan.md),
[`SELECTED_COMPONENTS.md`](SELECTED_COMPONENTS.md), [`BOM.md`](BOM.md),
[`MODEL_ISSUES.md`](MODEL_ISSUES.md) §B/§G, [`analysis/software_by_component.md`](analysis/software_by_component.md)
(D-register), [`analysis/syson_view_plan.md`](analysis/syson_view_plan.md),
[`cad-resources/README.md`](cad-resources/README.md), and the sibling repos
`DroneMissionApp` (D-2) / `DroneThermalModel` (D-1)._

**Where the project stands:** design is essentially complete — requirements, architecture,
compatibility rules, parametric analysis, trade studies, and component locks are all done.
**Nothing has been procured yet.** The critical path from here is: close the last model
approvals → order Phase 1 → build/fly → Phase 2 hardware + CAD mounts → Phase 3 software
(D-1 is the long pole and can start today, no hardware needed).

Status keys: **☐** not started · **◐** partially done · **✅** done · **⛔** blocked

**Estimates** are hands-on effort for one person already familiar with this project — not
calendar time. Where elapsed time dominates (shipping leads, vendor replies, and especially
D1.1 thermal data collection, which is season- and opportunity-dependent) that is called out
in the task's note rather than inflating the hours.

### Effort rollup

| Phase | Tasks | Est. effort |
|---|--:|--:|
| Phase 0 — cross-cutting model/docs | 12 | 33 h |
| Phase 1 — flight + FPV + waypoints | 23 | 38.5 h |
| Phase 2 — thermal + SBC | 18 | 53 h |
| Phase 3 — AI detection + autonomy | 20 | 168 h |
| **Committed build (Phases 0–3)** | **73** | **~292 h** |
| Phase 4 — deferred OpenHD downlink | 8 | 31 h |
| **Total** | **81** | **~323 h** |

Phase 3 is over half the remaining effort, and **D1.1 alone (thermal data collection, ~48 h)
is 15% of the whole project** — it is both the long pole and the only task with no hardware
dependency, which is why it should start now.

---

## Phase 0 — Cross-cutting: model, docs, and repo hygiene

These are not gated on hardware and should clear before/alongside Phase 1.

| # | Task | Est. | Notes | Status |
|---|---|--:|---|:--:|
| 0.1 | ~~**Approve + apply the R3_CAM_FOV re-tag**~~ **DONE 2026-08-11** | **2 h** | Restated as a **≥42 m ground-swath floor** at 120 m AGL (not a bare lens angle), plus **new `R9`** (hard: ≥30 acres/sortie), **new `R10`** (stretch: 60 acres), and **new `R4_GCS_SWEEP_SPACING`** (line spacing ≤90% of swath) against the flight-planning software. T13 @18 mm gives 51.2 m → 22% margin, so `satisfy R3_CAM_FOV` on `IRCamera` is true again. Hard/stretch pairs coherently: **R6↔R9**, **R8↔R10**. See MODEL_ISSUES §B7. | ☑ |
| 0.2 | ~~**Capture the two failsafe parameter sets as real requirements**~~ **DONE 2026-08-11** | **3 h** | SSS §3.7 link-loss + low-battery failsafes are "to be specified". Wrote the chosen `FS_THR_ENABLE`/`FS_OPTIONS`/`FS_THR_VALUE` and `BATT_LOW_VOLT`/`BATT_CRT_VOLT`/`BATT_FS_LOW_ACT`/`BATT_LOW_MAH` values into `model.sysml` as **`R7_FS_LINK`** / **`R6_FS_BATT`**. Closes the §3.7 gap. David reviewed two design forks during approval (static-vs-dynamic battery reserve, abort-vs-finish on link loss) and picked the simpler option for both — see MODEL_ISSUES.md §B8. Dynamic reserve tracked separately as D2.17. | ☑ |
| 0.3 | ~~**Pick the low-battery reserve (`BATT_LOW_MAH`)**~~ **DONE 2026-08-11** | **1 h** | The open R6-derived policy decision (`HandleLowBattery` reserve = TBD). Feeds 0.2 and 1.12. Resolved via `analysis/low_battery_reserve_analysis.md` (700 mAh @ 12 m/s RTL_SPEED, 30% margin on the worst-case 2.8 km return) — ported into this repo and folded into `R6_FS_BATT` as part of closing 0.2. | ☑ |
| 0.4 | ~~**Decide the classify loiter time-budget policy**~~ **DONE 2026-08-05** | **2 h** | `InvestigateAndClassify.adjustOrbit` is an unbounded loop in the model; needs a loiter-time budget + a "log as unclassified, resume" exit. Feeds D2.9. Small R6 endurance draw. Resolved via `analysis/classify_loiter_budget.md`: 30 s per investigation, then log as unclassified and resume (0.92% endurance draw). David approved 2026-08-05; folded into the `model.sysml` `adjustOrbit` doc. **Local checkbox was stale** — the decision + D2.9's code landed via a separate session and only reached this checkout on the 2026-08-12 merge (and only patched the frozen `analysis/autonomy_sim/mission_app.py`, not the live `DroneMissionApp` repo — see D2.9/D2.8 below). | ☑ |
| 0.5 | ~~**Decide operator override authority (UC-11)**~~ **DONE 2026-08-12** | **2 h** | Can the operator veto/abort an autonomous investigation, and is that a QGC mode switch or an app input? Decided 2026-08-06 (`analysis/operator_override_UC11.md`): yes, via QGC mode switch, no dedicated app input. Modeled 2026-08-12 as `OperatorOverride` + `FlightMode.loiterToCruiseOnOverride` + `UseCases::OperatorOverrideUC` (MODEL_ISSUES.md §B9) and implemented in `DroneMissionApp/mission_app.py` (INVESTIGATE override check + `alerts.override`), with a new passing contract test. | ☑ |
| 0.6 | **Reconcile the stale MODEL_ISSUES §B7 (FC firmware) entry** | **30 min** | **PARTIALLY DONE (found during the 2026-08-12 WSL/Windows repo merge)** — the WSL clone had independently deleted the stray misnumbered duplicate "7." (FC firmware) that used to sit out of order between items 5 and 6; that fix carried over cleanly in the merge. The rest of the original complaint stands: the FC-firmware RESOLVED writeup now lives as item **15** at the end of §B rather than in chronological order among items 7-14. See MODEL_ISSUES.md item 15's note. | ◐ |
| 0.7 | **Resolve or retire AF5 (EMAX Hawk 7)** | **30 min** | Only airframe still lacking a confirmed as-built mass; skipped by the sweep. Airframe is locked to AF3a, so retiring AF5 from `candidates.sysml` is the cheap close. (MODEL_ISSUES §B4) **Correction (2026-08-12 merge):** the WSL clone's TASKS.md/MODEL_ISSUES.md claimed this was done 2026-08-08, but `candidates.sysml`'s `AF5` block is byte-identical on both branches — the retirement was never actually applied on either side. Still open. | ☐ |
| 0.8 | **Add a `totalMass` rollup to the model** | **3 h** | §G follow-up: `mass` drives the *external* endurance model but is analytically inert in-model. A rollup makes `maxTakeoffMass`/payload requirements load-bearing SysML. Requires model approval. | ☐ |
| 0.9 | ~~**Commit the working tree**~~ **DONE 2026-08-13** | **1 h** | The 18 modified + 2 untracked files were already folded in by the 2026-08-12 WSL/Windows merge (tree was clean by the time this was picked up). The remaining half — `reference/cad-resources.md` had moved to `cad-resources/cad-resources.md` and 4 docs (`README.md`, `BOM.md`, `SELECTED_COMPONENTS.md`, `systems_engineering_plan.md`) still linked the old path — fixed 2026-08-13; also corrected the `README.md` repo-layout table row that still described `reference/` as holding CAD resources. | ☑ |
| 0.10 | **Build the remaining SysON diagrams** | **14 h** | 12 of 14 rows open: 0b (system composition/BDD), 1 (system context), 2 (GCS internals), 3 (flight modes), 5 (sortie thread), 6a/6b/6c (action flows), 7 (SBC software internals — the D-1/D-2 scope on one page, key Phase 3 diagram), 8 (compatibility), 9 (analysis), 10 (allocation). Rows 0 and 4 are done. | ◐ |
| 0.11 | **Export SysON views into the CDR deck** | **2 h** | Replace the hand-drawn "System Composition" slide with the row-0b export → `presentation/assets/diagrams/`. | ☐ |
| 0.12 | **Keep `model_community_balanced.sysml` in sync** | **2 h** | The lean CATIA/MSOSA export must track any model change from 0.2/0.8 (watch the ~500-element cap). **0.1 needed no mirroring** — that export deliberately omits the Requirements pillar and all `satisfy` statements (verified 2026-08-11: 0 requirement refs, 0 satisfy). Still open: re-export the SSS `REQUIREMENTS_EXPORT_26_06_30.md` to pick up R9/R10/R3_CAM_FOV/R4_GCS_SWEEP_SPACING. | ☐ |
| 0.13 | ~~**Reconcile R9 against the R6 30-min endurance floor**~~ **RESOLVED 2026-08-11** | — | Closed by splitting the requirement: **R9 hard = 30 acres** (R6's 30 min delivers ~36.6 ac, so R6 still governs) and **R10 stretch = 60 acres** (~49 min, inside R8's 60-min stretch, which delivers ~73.2 ac). No conflict remains. | ☑ |
| 0.15 | ~~**Make the thermal analysis layer evaluate the as-built 45° tilt**~~ **DONE 2026-08-12** | **2 h** | `Analysis::GroundSampleDistance` was nadir-only, so `ThermalRecognitionCheck`/`ThermalDetectionCheck` asserted Johnson pass/fail against a geometry the system doesn't have — **optimistically**, showing ~8.3 px recognition margin where the true along-range figure is ~4.2. Added `calc def OffNadirGsd` (×2.0 along-range at 45°) + new `IRCamera.mountTilt_deg` (bound 45.0 on T13). Both verdicts still pass; the *margin* is now honest. Approved by David 2026-08-12. See MODEL_ISSUES.md §11. **Still worth confirming Syside diagnostics in-editor** (no CLI validator available). | ☑ |
| 0.14 | **Clarify R7's "2800 m linear distance"** | **1 h** | Ambiguous: reads as swept *track length*, but [R4_GCS_RANGE](model.sysml) uses the same 2800 m as RF *slant range*. If it means transit range, out-and-back at 2.23 m/s costs ~42 min and collapses the R9/R10 area budget. Surfaced during 0.1. | ☑ |

---

## Phase 1 — Basic flight + FPV downlink + waypoints  ·  ~$1,371

**Goal:** stable manual LOS flight, live analog video on the MacBook, and pre-programmed
waypoint missions. All components are LOCKED; nothing is ordered.

### 1A. Procurement (BOM Phase 1)

| # | Task | Est. | Notes | Status |
|---|---|--:|---|:--:|
| 1.1 | Order **iFlight Chimera9 ECO 6S 9" PNP (`AF3a`)** — with the **GPS pre-install option (+$39)** | **30 min** | $490.99 incl. GPS + analog VTX + FPV cam + 4 extra props + shipping. The GPS option is easy to miss at checkout. | ☐ |
| 1.2 | Order **iFlight True Diversity ELRS RX (`iFlightTD`)** | **10 min** | $31.99 | ☐ |
| 1.3 | Order **RadioMaster TX12 Mark II ELRS (`TX5`)** | **10 min** | $117.93 | ☐ |
| 1.4 | Order **HGLRC Hermes ELRS USB dongle (`TLM2`)** | **10 min** | $16 — primary laptop control + telemetry link | ☐ |
| 1.5 | Order **Upgrade Energy GREEN V2 6S3P 12 Ah Amprius (`BAT10`)** | **20 min** | $275 flight pack. Confirm in stock (BAT09 already went out of stock). | ☐ |
| 1.6 | Order **2× GNB 6S3P 12 Ah (`BAT22`)** | **15 min** | $220 — development/shakedown packs; fly these first | ☐ |
| 1.7 | Order **Skydroid 150CH 5.8 GHz UVC VRX (`VRX6`)** | **45 min** | ~$44.45 — **select the dual-antenna variant and confirm price at checkout** (Alibaba listing) | ☐ |
| 1.8 | Order **TrueRC X-AIR 5.8 MK II patch (`PATCH1`)** | **10 min** | $36.85 | ☐ |
| 1.9 | Order **iFlight Anti Spark Filter XT60 (`ASF1`)** | **10 min** | $14.99 | ☐ |
| 1.10 | Order **HOTA D6 Pro charger (`CHG1`)** + **USB-A→USB-C adapter** | **15 min** | $111.55 + ~$11 | ☐ |
| 1.11 | Verify the whole power chain is **XT60** on arrival | **30 min** | Battery → anti-spark → airframe lead. Already verified on paper for BAT10/BAT22. | ☐ |

### 1B. Build, configure, fly (SE plan Phase 1 steps)

| # | Task | Est. | Notes | Status |
|---|---|--:|---|:--:|
| 1.12 | Flash **ArduPilot ArduCopter ≥ 4.5** to the BLITZ F7; configure the GPS | **3 h** | Firmware decision is RESOLVED — this is the execution | ☐ |
| 1.13 | Bind the ELRS RX to the TX12 **and** to the Hermes laptop dongle | **2 h** | Two bindings; the dongle is the primary 2.8 km link, TX12 is manual/backup | ☐ |
| 1.14 | Calibrate sensors — compass, accelerometer, gyro | **1 h** | | ☐ |
| 1.15 | Configure arming, **failsafe (`FS_*`), battery failsafe (`BATT_*`), and RTL** | **3 h** | This *is* the realization of the two §3.7 requirements — record the values (→ 0.2) | ☐ |
| 1.16 | Basic flight-envelope tests in LOS — hover, pitch, roll, yaw | **4 h** | Fly the cheap `BAT22` packs first | ☐ |
| 1.17 | Connect **VRX6 + PATCH1** to the MacBook (USB/UVC); view/record in QuickTime or OBS | **2 h** | | ☐ |
| 1.18 | Confirm live analog FPV + MAVLink telemetry into **QGroundControl 4.4+** | **2 h** | | ☐ |
| 1.19 | Plan, upload, and execute a **waypoint mission** in QGC with FPV monitoring + manual ELRS override | **4 h** | | ☐ |
| 1.20 | Validate **position-hold and RTL** | **2 h** | | ☐ |
| 1.21 | **Field-verify the 2.8 km range** on both links (R7 / R4_GCS_RANGE) | **6 h** | Control link and video link. Compare against [`analysis/rf_link_budget.md`](analysis/rf_link_budget.md). | ☐ |
| 1.22 | **Measure real hover endurance** and compare to the model's ~58.6 min | **4 h** | Feed the as-built numbers back into `candidates.sysml` / rerun `flight_time_model.py` | ☐ |
| 1.23 | **Caliper the real top-plate bolt pattern + deck dimensions** | **2 h** | Unblocks the Phase 2 CAD (the mount currently *assumes* a 30.5 mm pitch) and converts the §C16 EST deck dims to measured | ☐ |

---

## Phase 2 — Thermal camera + SBC (onboard live-inference feed)  ·  ~$859

**Goal:** mount the T13 and NanoPi M5, establish the live thermal → SBC USB-UVC feed.
No recording, no downlink.

### 2A. Open questions + procurement

| # | Task | Est. | Notes | Status |
|---|---|--:|---|:--:|
| 2.1 | **Confirm the 18 mm T13 variant's mass** with the vendor | **30 min** | Expect ~5–10 g over the 13 mm; update `candidates.sysml` `T13.mass` if so (it is nose payload → CG impact) | ☐ |
| 2.2 | Order **PurpleRiver Mini 640 `T13`** — 640×512, 12 µm, **18 mm lens**, **USB** variant | **30 min** | $700 ($590 base + $50 lens + $60 shipping — confirmed 2026-07-29). Specify USB, not MIPI/CVBS. | ☐ |
| 2.3 | Order **NanoPi M5 4 GB (`SBC3`)** | **15 min** | $126 | ☐ |
| 2.4 | Order **2-6S→12 V 3 A UBEC (2-pack)** + **USB-C power-only cable** | **10 min** | $9.99 + $7.99. The 2nd UBEC unit is held (at 5 V) for Phase 4. | ☐ |
| 2.5 | Buy mount hardware — 30 mm fan, M2/M2.5 heat-set inserts, screws, standoffs | **30 min** | ~$15 with filament | ☐ |

### 2B. CAD + physical integration

| # | Task | Est. | Notes | Status |
|---|---|--:|---|:--:|
| 2.6 | **Design the SBC deck** (`SBC_deck`) — the main missing CAD deliverable | **10 h** | Parametric build123d/FreeCAD body: bolts to the 30.5×30.5 stack/standoffs, raised tier above the top-mount battery, standoff bosses with heat-set inserts, **fan duct + vents** (the M5 dumps ~10 W). Only the M5 *component* model and keep-out exist today; the deck itself is not started. | ☐ |
| 2.7 | **Thermal mount v2** — resolve the v1 open items | **6 h** | Caliper-correct the assumed `FRAME_BOLT_PITCH`; add a stiffening rib/gusset to the flat cantilever; consider soft-mount grommets for vibration; verify the lens tip (~31 mm below the plate) clears the bottom plate and landing gear. | ◐ |
| 2.8 | ~~**Decide nadir vs 45° down-look mount**~~ **DONE 2026-08-07 — 45° SELECTED** | **1 h** | Both v1 brackets exist (`thermal_mount.py` / `thermal_mount_45.py`). 18 mm recognizes at 45° (4.17 px along-range @90 m; 3.13 px detect @120 m), so the tilt is valid — **45° down-look chosen** on CONOPS fit (forward look suits both sweep and investigate), ~4 g mass penalty, no meaningful coverage loss. **Local checkbox was stale** (Mission Control #46 already Done). Rationale doc [`analysis/thermal_mount_angle_decision.md`](analysis/thermal_mount_angle_decision.md) **ported from the WSL clone 2026-08-12** (it had only ever existed there — same gap as `low_battery_reserve_analysis.md`). Downstream still open: face-plate trim + gusset cleanup + landing clearance (→ 2.7). | ☑ |
| 2.9 | **Print, test-fit, iterate** | **8 h** | PETG/ABS/ASA/nylon — **not PLA** (softens near a 10 W SBC + motors). 3–4 walls, 30–40% infill. | ☐ |
| 2.10 | **Update `candidates.sysml` deck/battery dims EST → measured** and rerun the sweep | **2 h** | Sharpens the §C16 `sbc_fit_status` from estimate to measured (AF3a currently shows 8 mm spare) | ☐ |
| 2.11 | **Re-check all-up mass, CG, and payload margin** with the nose thermal + deck SBC | **2 h** | Rerun `flight_time_model.py` with as-built masses | ☐ |

### 2C. Integration + verification

| # | Task | Est. | Notes | Status |
|---|---|--:|---|:--:|
| 2.12 | Set the **UBEC jumper to 12 V** (not 5 V), solder its 12 V+/GND leads to the USB-C pigtail, power the M5 | **2 h** | Build-time check called out in SELECTED_COMPONENTS — verify *before* connecting the SBC | ☐ |
| 2.13 | Mount the thermal (clear FOV, nose/chin) and the SBC on the printed deck | **3 h** | | ☐ |
| 2.14 | Wire **SBC ↔ FC MAVLink over UART** (GPIO header, 1 of 4) | **2 h** | | ☐ |
| 2.15 | Confirm the T13 enumerates as **`/dev/video0` UVC** and streams stable 640×512 @ ~25 Hz | **2 h** | USB-A #1; no driver work expected | ☐ |
| 2.16 | Stand up **mavlink-router / mavproxy** on the SBC | **3 h** | So the mission app and the ground telemetry link can share the one FC serial port | ☐ |
| 2.17 | **Field-verify Johnson detect/recognize at 90–120 m** | **6 h** | R3_1 @120 m, R3_2 @90 m — the geometric claim at the as-built 45° mount tilt (3.13 px detect / 4.17 px recognize, along-range axis; nadir would read 6.25 / 8.33 px — see model.sysml OffNadirGsd, 2026-08-12) needs real imagery. The 4.17 px recognition figure is thin — this field test is the load-bearing check. | ☐ |
| 2.18 | **Bench-test the SBC envelope** — ≤10 W avg (R4_SBC_PWR), sustained passive-cooling thermals (R4_SBC_TEMP) | **4 h** | Do this early with a stock YOLO model; it gates the Phase 3 pipeline design | ☐ |

---

## Phase 3 — AI detection + autonomous route modification  ·  $0 hardware

Software only, on hardware already on board. **The entire development scope of the project
is D-1 + D-2**; everything else is adopt-and-configure. Both live in sibling repos.

### 3A. D-1 — Thermal detection/classification model (`DroneThermalModel`) — **the long pole**

| # | Task | Est. | Notes | Status |
|---|---|--:|---|:--:|
| D1.1 | **Data-collection plan + capture rig; collect deer/turkey/human LWIR @ 90–120 m** | **8 h plan + ~40 h collection** | Daytime/clear with ≥5 °C differential. **Start now** — season/opportunity-dependent, longest lead, and the single biggest project risk. No hardware dependency. | ☐ |
| D1.2 | Assemble the bootstrap dataset — FLIR ADAS + BIRDSAI subsets | **8 h** | Tooling ✅ (`src/dataset.py`); source data not yet gathered | ◐ |
| D1.3 | Labeling + **augmentation** pipeline | **8 h** | Label→class mapping ✅; scale/rotation/contrast augmentation across the altitude band TBD | ◐ |
| D1.4 | Run the training pipeline — YOLO-nano fine-tune → ONNX | **6 h** | `src/train.py` ✅ ready; blocked on the dataset | ☐ ⛔ D1.1/D1.2 |
| D1.5 | Eval harness vs the R3_1/R3_2 operating points | **done** | `eval/metrics.py` built + tested | ✅ |
| D1.6 | RKNN conversion + INT8 quantization accuracy-delta check | **4 h** | `conversion/to_rknn.py` ✅ ready (x86 host); blocked on the ONNX model | ☐ ⛔ D1.4 |
| D1.7 | On-target benchmark — latency/FPS, power, passive-cooling thermals | **6 h** | Needs the SBC (→ 2.18) | ☐ ⛔ Phase 2 |
| D1.8 | Field-validation protocol — the SSS §4 Demonstration of R3_1 (90%) / R3_2 (80%) | **12 h** | Where the percentages are actually earned | ☐ |
| D1.9 | Revisit the **Ultralytics AGPL-3.0** caveat if the app is ever shared | **1 h** | Fine for personal use; YOLOv5 or a permissive reimplementation otherwise | ☐ |

### 3B. D-2 — Onboard mission application (`DroneMissionApp`)

Done and tested: D2.1 heartbeat, D2.2 telemetry tracker, D2.3 `COMMAND_ACK` verify + retry,
D2.4 sweep controller, D2.7 pixel→ground POI geolocation, D2.10 structured `STATUSTEXT`
schema, D2.11 failsafe stand-down.

| # | Task | Est. | Notes | Status |
|---|---|--:|---|:--:|
| D2.5 | **UVC thermal capture pipeline** (V4L2, 640×512 @ 25 Hz, frame queue/drop policy) | **8 h** | First real-SBC task | ☐ ⛔ Phase 2 |
| D2.6 | **RKNN inference wrapper** implementing the `Detector` interface | **12 h** | Letterbox/NMS pre-post; consumes the D-1 `.rknn` | ☐ ⛔ D1.6 + Phase 2 |
| D2.8 | ~~`adjustOrbit` loiter maneuver — active re-aim while classifying~~ **DONE 2026-08-12** | **6 h** | Implemented in `DroneMissionApp/mission_app.py`: a stalled aspect (classify_timeout_ticks reached without success) moves the vehicle to view the target from a different **side**, holding the standoff geometry the rigid **45°** mount dictates (`geolocation.standoff_from_poi`: stand off `alt·cot θ` = 90 m at the classify altitude, and **yaw to face the POI**), settles, then resamples. First cut wrongly assumed a nadir camera — corrected during review; the same nadir assumption was also latent in the pre-existing investigate descent, now fixed, along with stale `CameraModel` defaults (13 mm/nadir → 18 mm/45°) and a `type_mask` `FORCE_SET` bug. 29 tests pass. See MODEL_ISSUES.md §10. | ☑ |
| D2.9 | ~~Classification controller **loiter time-budget policy**~~ **DONE 2026-08-12** | **3 h** | 30 s wall-clock budget (decided 0.4, `analysis/classify_loiter_budget.md`) now bounds the whole INVESTIGATE state regardless of adjustOrbit cycles. **Ported to the live `DroneMissionApp` repo** — the 2026-08-05 implementation had only ever landed in the frozen `analysis/autonomy_sim/mission_app.py` prototype here, never the live repo; this closes that gap alongside D2.8. | ☑ |
| D2.12 | ~~Service hardening — systemd unit, watchdog, logging, config, safe stand-down~~ **DONE 2026-08-14** | **6 h** | Field-ops requirement (single operator). [agent 2026-08-14] Built the deliverable in `analysis/service_hardening/`: `mission_app.service` (WatchdogSec=30, Restart=always, security hardening), `mission_app_config.yaml`, `mission_app_logging.py` (JSON/text structured logging), `run_service.py` (config loader, sd_notify watchdog, SafeStandDown crash-recovery thread, SIGTERM/SIGINT graceful LAND). [claude 2026-08-14] Reviewed and fixed several bugs: the crash handler exited after a fixed 3 s sleep, well under SafeStandDown's default 15 s heartbeat timeout, so the daemon thread got killed before it could send LAND — replaced with a real wait for the thread to finish; `disarm()` set a `_clear_event` attribute nobody read, so it didn't actually stop the thread — added a real `_stopped` Event; `if app.fc_mode and ...` treated STABILIZE (mode 0) as falsy, silently skipping the shutdown LAND command; `merge_config` shallow-`update()`'d config sections, so a SITL override touching one `mavlink` key (the exact pattern shown in the config's own example) dropped its untouched siblings — now a recursive deep merge; `JSONFormatter` hardcoded a fixed field whitelist that silently dropped most of what `run_service.py` actually logs — now surfaces every `extra={}` field automatically; `_safe_land()`'s `MAV_CMD_NAV_LAND` COMMAND_LONG path was unvalidated — switched to the same `set_mode_send` GUIDED→LAND sequence already proven elsewhere, confirmed via a new real-SITL test (`analysis/sitl_tests/test_service_hardening_sitl.py`) that drives `SafeStandDown._safe_land()` against ArduCopter 4.7.0 and checks the FC actually reaches LAND. Added `test_service_hardening.py` (15 unit tests: SafeStandDown lifecycle against a fake connection, config deep-merge, logging extras, config→app construction). **Ported to the live `DroneMissionApp` repo** (`run_service.py`/`mission_app_logging.py`/config/unit file/tests there): adapted to that repo's actual `MissionApp` API (ACK+retry `_request_mode`/`_service_mode` instead of `_set_mode`, `detector.py`'s `ScriptedDetector`, no free-text `_alert` — a plain `SVC\|` STATUSTEXT instead); `battery_rtl` config there is inert and logs a warning if enabled, since D2.17 was never ported to that repo (separate gap, not closed here). 43/43 existing DroneMissionApp tests still pass; added 13 unit tests + a subprocess end-to-end smoke test (config→connect→loop→SIGTERM→graceful-LAND, skipped on Windows where `SIGTERM` doesn't map to a real signal) there too. Remaining: wire the real RKNN detector (D2.6) when available; deploy config to `/etc/mission_app/` on the NanoPi M5 when it arrives; port D2.17's battery-RTL trigger to DroneMissionApp separately. | ✅ |
| D2.13 | **Real ArduPilot SITL integration suite** | **12 h** | Adds mode-ACK, EKF/arming gates, GUIDED nav tracking, and real `FS_*`/`BATT_*` failsafe behavior. No hardware needed — **can start today.** [agent 2026-08-10] Created the full suite: `sitl_tests/` with `test_mode_ack.py` (5 tests), `test_arming_gates.py` (3 tests), `test_guided_nav.py` (3 tests), `test_failsafe_params.py` (4 parametrized + 3 structural), `test_full_mission.py` (2 tests), plus `helpers.py`, `conftest.py`, `params_sets.py`, `README.md`. Suite is structured, documented, and ready to run against any SITL binary. [agent 2026-08-10] Executed against both SITL binaries. **Old copter-3.3:** connected, mode-set and param readback work, but LOITER mode not reached, BATT_LOW_VOLT not found, EKF didn't converge within 30s, and arm failed. **Modern arducopter (4.5):** connected but mode switching via MAV_CMD_DO_SET_MODE failed, no params readable, no EKF convergence. Both versions need debug of the test scripts' mode-switching approach (raw SET_MODE vs COMMAND_LONG, timing, and firmware version-specific behavior). Remaining: debug failures against both SITL binaries, integrate with CI. [claude 2026-08-11] Fixed ~13 real bugs found via direct SITL probing (see commit f2a3559 for the full list — target_component defaulting to broadcast, recv_match's cross-cannibalization trap, a real infinite loop in upload_mission, mission seq-0 home-placeholder convention, AUTO_OPTIONS arming gate, etc). Now 27/28 tests pass in isolated per-file runs against the real target firmware (4.7.0): `test_mode_ack` 6/6, `test_failsafe_params` 14/14, `test_arming_gates` 3/3, `test_guided_nav` 3/3 (see D2.15), `test_full_mission` 1/2 (see D2.16 for the remaining SITL-binary-crash blocker). Mission Control task #70 has the full writeup. | ◐ |
| D2.14 | **Verify ArduCopter mode numbers** (AUTO=3, GUIDED=4, RTL=6, LAND=9) against the exact firmware build | **1 h** | Hard-coded in `mission_app.py`; verify before flight. [claude 2026-08-11] Verified against both real SITL binaries — the hard-coded numbers were already correct. Mission Control task #71. | ✅ |
| D2.15 | Fix GUIDED altitude-target `type_mask` (FORCE_SET bit accidentally set) | **done** | Found while debugging D2.13: `type_mask` in both `sitl_tests/helpers.py` and the real mission app's `_command_descent()` (`analysis/autonomy_sim/mission_app.py`) had bit 9 (`POSITION_TARGET_TYPEMASK_FORCE_SET`) set, silently discarding the whole position — including altitude — on a same-lat/lon Z-only GUIDED target. This is the exact call UC-5/InvestigateAndClassify's descend-to-classify uses. Fixed in both places (commit 44ddec4); `analysis/autonomy_sim/` is a frozen prototype (see dd1596a) — **the same fix needs porting to the live DroneMissionApp repo**, not done here. **Independently re-discovered and fixed a second time on the Windows clone (commit 94b72d6, 2026-08-12)** — identical resulting `type_mask`, plus a `fake_fc.py`/`test_autonomy_loop.py` regression test this branch's fix didn't have; both test additions are now merged in. | ✅ |
| D2.16 | Fix ArduCopter SITL crash on AUTO-mode takeoff | **5 h** | Found while debugging D2.13: the raw arducopter binary crashes (confirmed via process monitoring, not just symptom) during an AUTO-mode mission takeoff. Launching the same binary via ArduPilot's official `sim_vehicle.py` (not a full rebuild — `--vehicle-binary` points at the existing prebuilt binary) eliminated the crash 4/4 times, but surfaces a new "disarms instead of climbing" issue that needs its own debugging pass. Full reproduction steps, launch commands, and upstream ArduPilot issue references in Mission Control task #141. | ☐ |
| D2.17 | ~~**Distance-adaptive low-battery RTL trigger**~~ **DONE 2026-08-13** | **6 h** | Deferred from 0.2 (David 2026-08-11): SBC (or FC Lua script) computes energy-needed-to-return from the current GPS distance-to-home each cycle and commands RTL via MAVLink at ~10% margin, instead of waiting for the static `R6_FS_BATT` worst-case (2.8 km) threshold — avoids cutting a mission short when the drone is already near home with reserve to spare. `BATT_CRT_MAH` stays a firmware-level hard-floor backstop regardless. See MODEL_ISSUES.md §B8/§12 and Mission Control task #142. [claude-nightly 2026-08-12] Reference implementation (haversine distance, pack-energy accounting, live cruise-power EMA) built + 15 unit tests, standalone in the Mission-Control repo. [claude 2026-08-13] Ported into `analysis/autonomy_sim/`; wired `BatteryRTLMonitor` into `MissionApp` (`_pump()` handles `HOME_POSITION`/`BATTERY_STATUS`/`PARAM_VALUE` for `RTL_SPEED`/`RTL_SPEED_MS`→`WPNAV_SPEED` fallback→`RTL_ALT`, read live); extended `FakeFC` to emit both and answer `PARAM_REQUEST_READ`; 2 mock-FC integration tests (`analysis/autonomy_sim/test_autonomy_loop.py`). **Then the real SITL validation pass** (`analysis/sitl_tests/test_battery_rtl_sitl.py`, 2 tests): runs the actual `MissionApp`/`BatteryRTLMonitor` — not a reimplementation — against real ArduCopter 4.7.0, `DO_SET_HOME` relocating home ~2.8 km away (only succeeds armed+GUIDED, confirmed by direct probing) plus a shrunk `BATT_CAPACITY` to deplete a pack in a practical test window; confirms both the trigger decision AND that ArduPilot accepts the resulting RTL command. Along the way found and fixed a real pre-existing cross-test isolation bug: `test_failsafe_params.py`'s cleanup fixture only restored 3 of ~10 params it touches, **and** a second bug in the fix itself — holding one MAVLink connection open across a whole module's `yield` collides with SITL's single-client TCP port and hangs every later test in that module. Full 30-test suite (all `sitl_tests` files together) green across 2 consecutive runs. **Still open:** `climb_energy_j` stays the placeholder `0.0` (conservative-safe direction — fires slightly later than ideal when RTL needs to climb first — not unsafe, since `BATT_CRT_MAH` remains the hard backstop); needs a real climb-rate measurement from an actual flight to set properly. Everything else in the reference doc's recommended path is done. | ✅ |

### 3C. Phase 3 integration + acceptance

| # | Task | Est. | Notes | Status |
|---|---|--:|---|:--:|
| 3.1 | Deploy the INT8 `.rknn` via RKNPU2 and run live inference on the USB thermal stream at ≥~25 fps | **8 h** | R4_SBC_VIDEO_PROC | ☐ |
| 3.2 | Map detections → MAVLink and modify the mission in flight (AUTO→GUIDED→AUTO, descent to 90 m, resume) | **8 h** | Contract already proven against the mock FC | ☐ |
| 3.3 | **Validate the SBC-failure fallback** — drone completes the current waypoint and RTLs | **4 h** | | ☐ |
| 3.4 | Decide **D-3** (optional GCS map-POI display) after Phase 3 field trials | **1 h** | Text `STATUSTEXT` alerts may be fully sufficient | ☐ |

---

## Phase 4 — (Deferred) OpenHD digital video downlink  ·  ~$159

Not part of the committed Phase 1–3 build. Components are selected but unordered; prices are
estimates.

| # | Task | Est. | Notes | Status |
|---|---|--:|---|:--:|
| 4.1 | **Re-confirm Phase 4 prices** before building | **1 h** | `WLAN_AIR1` ~$20, `WLAN_GND1` $65, Foxeer pair $60, cloverleaf pair $13.99 — all estimates | ☐ |
| 4.2 | Order `WLAN_AIR1` (LB-LINK BL-M8812EU2) + USB-A stub + 2× u.fl→RP-SMA pigtails | **45 min** | Bare module — a ~5-minute assembly, not a solder job (per the trade study) | ☐ |
| 4.3 | Order the 5.8 GHz RHCP cloverleaf pair (air) and `WLAN_GND1` + 2× Foxeer Echo 2 Max (ground) | **30 min** | | ☐ |
| 4.4 | Set the **spare Phase 2 UBEC unit to 5 V** and power the air module (~10 W) | **1 h** | No new part | ☐ |
| 4.5 | Mount the air module on **USB-A #2** (reserved) + air antennas | **2 h** | | ☐ |
| 4.6 | Build the RTL8812EU **ARM64 DKMS driver** on the M5 and configure H.264 encode + **WFB-ng TX** at 5.8 GHz | **12 h** | | ☐ |
| 4.7 | Ground side: **ARM64 Ubuntu VM (VMware Fusion)** on the MacBook + AWUS036ACH + Foxeer diversity → decode the WFB-ng stream | **8 h** | | ☐ |
| 4.8 | **Field-confirm link margin at 2.8 km** (predicted +11.3 dB, reliable to ~3.3 km) | **6 h** | | ☐ |

---

## Suggested near-term ordering

1. **D1.1** — start thermal data collection immediately. It is the longest lead and needs no hardware.
2. **D2.13** — the SITL suite, also hardware-free, and it validates the failsafe params before they matter.
3. **Phase 1 procurement (1.1–1.10)** — long shipping tails (iFlight, Alibaba, Upgrade Energy).
4. **1.23** — caliper the frame as soon as it lands; that single measurement unblocks all the Phase 2 CAD.
