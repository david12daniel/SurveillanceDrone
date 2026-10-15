# D1.1 — Thermal Data Collection Plan & Capture Rig

**Status:** v2 — refreshed 2026-10-15 (external sources re-verified, tooling smoke-tested, season-aware schedule)
**Est. collection effort:** ~40 h field capture · ~8 h labeling & QA
**Blocking:** None for planning/download — no hardware dependency for the bootstrap stream. Field capture with the actual T13 awaits Phase 2 hardware (order #40); a surrogate UVC camera can start capture earlier (see §11, David's decision).
**Related tasks:** D1.2 (bootstrap assembly), D1.3 (labeling/aug pipeline), D1.4 (training)

---

## 0. Changelog

| Date | Change |
|------|--------|
| 2026-08 (v1) | Original plan (author: prior session). |
| 2026-10-15 (v2) | **Verified every external dataset claim.** BAMBI confirmed REAL (Zenodo DOI correct, CC-BY-4.0, current) — it is the deer-class backbone and was never downloaded. BIRDSAI confirmed assembled 08-20 (21,209 frames; see D1_2_BIRDSAI_ASSEMBLY.md). FLIR ADAS still gated on Teledyne registration. **§3.4 "ROAD" dataset could not be located — replaced with verified HIT-UAV.** Fixed §2.3 geometry to the authoritative model.sysml OffNadirGsd numbers (was a sloppy `1/cos²(45°?)` approximation). Smoke-tested the capture tooling (extract_frames.py PASS, thermal_capture.py CLI OK — see §5). Added season-aware schedule (§7), Session-0 dry-run checklist (§9), and the decisions David must make (§11). |

---

## 1. Overview

D1.1 covers everything needed to go from zero labeled thermal data to a training-ready set of
LWIR deer, turkey, human, and other-animal images at 90–120 m AGL, in the look-down / 45°
forward-tilt geometry of the build. **This is the project's long pole and single biggest risk**
— deer and turkey have **zero** labeled frames in any public source currently in the pipeline,
and only self-capture produces the exact sensor (12 µm, 18 mm, 640×512), geometry (45° tilt,
90–120 m standoff), and local ecosystem (NY white-tailed deer, wild turkey) the model needs.

**Three parallel streams (updated from v1's two):**

| Stream | Source | Contribution | Effort |
|--------|--------|-------------|--------|
| **Bootstrap — BAMBI** | Austria UAV thermal: red deer, roe deer, wild boar | ~92k key frames, MOT annotations on thermal, CC-BY-4.0 — **deer-class backbone** | 2–4 h to download filtered subset (D1.2) |
| **Bootstrap — BIRDSAI + FLIR ADAS** | Human + African megafauna; urban persons/vehicles | BIRDSAI already assembled (21,209 frames: 12,531 human / 74,668 other_animal). FLIR ADAS gated on registration | BIRDSAI done; FLIR ~2 h when un-gated |
| **Self-capture** | Field recording with the actual T13 (or surrogate) at 45°/90–120 m | 45°-geometry fidelity for ALL classes; the **only** source of turkey and white-tailed deer; NY habitat backgrounds | ~40 h total |

---

## 2. Capture Rig Specification

### 2.1 Tripod-based (no drone needed — start immediately)

Since the T13 hasn't been ordered (Phase 2), use a surrogate thermal camera for early capture.
Recommended: **any USB-UVC thermal camera with as high a resolution as available** — e.g. an
InfiRay P2 Pro (256×192, ~$200, immediate availability) or a borrowed FLIR One Pro
(iOS/Android). Lower resolution means images are good for species ID practice, pipeline
testing, and procedure dry-runs — but NOT for final training. **The v2 note (2026-10-14,
task #39) confirms the T13's radiometric variant only ships 9/13/18 mm lenses and our 18 mm
pick is valid and is its longest radiometric option** — lock the rig spec to the T13
18 mm USB variant as the primary sensor.

**Minimum viable rig:**
- T13 18 mm USB (primary, when ordered) or surrogate UVC thermal camera (immediate)
- Laptop running `thermal_capture.py` (see §5)
- Tripod with adjustable tilt (0–60°) and a pan head
- Battery pack for laptop (or AC if range extends to an outlet)
- Measuring tape + laser rangefinder for distance calibration
- IR thermometer (temp probe) to log ambient vs target ΔT

### 2.2 Drone-based (Phase 2+ hardware)

Once the Phase 2 build is complete, capture from the actual drone platform:
- T13 USB → NanoPi M5 → frame capture script
- Fly at 90–120 m AGL, 45° forward tilt
- Log: altitude (GPS), heading, GPS coordinates of each frame
- This produces the **operationally perfect** training set (task 2.17 validates Johnson
  detect/recognize at these exact ranges)

### 2.3 Geometry benchmark (corrected to model.sysml OffNadirGsd, 2026-10-15)

The T13's 12 µm pitch × 18 mm lens — authoritative numbers from `model.sysml`
(`OffNadirGsd` = nadir GSD / cos²(tilt), as-built mount tilt 45°):

| Altitude | Nadir GSD | Along-range GSD @45° (×2.0) | 0.5 m target, along-range |
|----------|-----------|-----------------------------|---------------------------|
| 90 m     | 6.0 cm/px   | 12.0 cm/px                   | **4.2 px → Recognize ✓** (recognition threshold ~4 px, thin margin) |
| 120 m    | 8.0 cm/px   | 16.0 cm/px                   | **3.1 px → Detect ✓** (detection threshold ~1.5–2 px) |

Matches `ThermalRecognitionCheck` (4.17 px) / `ThermalDetectionCheck` (3.13 px) in
model.sysml (reconciled into the CDR deck 2026-10-12). Recognition at 120 m does NOT pass —
**collecting real imagery from this exact along-range geometry is load-bearing** for the
R3.2 claim; do not rely on nadir-camera assumptions (the old 6.25/8.33 px numbers were
optimistic — see MODEL_ISSUES §11).

**Capture implication:** at 45° and 90–120 m standoff, a deer fills only ~3–5 px along its
body axis. The camera must be sharp (no motion blur), the target well-resolved (≥5 °C ΔT),
and the extractor's blur filter correctly tuned (see §5 calibration note).

---

## 3. Bootstrap Public Datasets (all claims re-verified 2026-10-15)

### 3.1 BAMBI Detection Dataset — VERIFIED, deer-class backbone (Top Priority)

| Property | Value |
|----------|-------|
| URL | https://zenodo.org/records/15773102 (DOI 10.5281/zenodo.15773102) |
| GitHub | https://github.com/bambi-eco/Dataset (official tooling + docs) |
| Content | Thermal drone imagery: red deer, roe deer, wild boar (+ 12 species total) |
| Coverage | **389 paired RGB+thermal UAV sequences**, ~45 h flight time, 92,701 key frames, 5,100 annotated tracks, 1,218,903 interpolated boxes |
| Recording period | Jan 2023 – Nov 2024, Austria (Tyrol, Upper/Lower Austria, Salzburg, Styria, Carinthia) |
| Format | 2048×1024 video (thermal 1024×1024 left half, RGB right half), MOT-format annotations on the **thermal** view, per-frame geo-reference (lat/lon/alt) + drone poses |
| **License** | **CC-BY-4.0** for base/raw/matched/orthographic/owl-transferred versions. ⚠️ `environment-nc` version is CC-BY-NC — avoid it. (Verified in docs/dataset-versions.md) |
| Geometry | Aerial look-down (nadir) — NOT our 45° along-range condition |
| Effort | `git clone https://github.com/bambi-eco/Dataset.git` → `filter_flights.py --species "Red deer"` → `download_from_zenodo.py -f <flight>` (⚠️ the v1 plan named the tool `download_flights.py` — **correct name is `download_from_zenodo.py`**) |

**Species mapping for our 4 classes:** red deer + roe deer → `deer` (cervid thermal analog of
white-tailed deer); wild boar → `other_animal`. ⚠️ BAMBI contains **no white-tailed deer and
no turkey** — it de-risks the deer class (thermal signature + forest habitat diversity,
1024×1024 ground truth quality) but does not replace native white-tail 45° captures.

**Bonus resource (found 2026-10-15):** Hugging Face `cpraschl/bambi-thermal-detection` — a
YOLO11 wildlife detector trained on BAMBI thermal data. Candidate pre-trained init for D1.4's
fine-tune (evaluate then; not a D1.1 deliverable).

**Download strategy:** don't bulk-pull all 389 flights (~45 h of video). Use
`filter_flights.py --species "Red deer"` (and Roe deer, Wild boar) and the per-frame altitude
metadata to select flights in the 60–140 m AGL band; start with 3–5 flights (~2–4 GB each,
check sizes in the Zenodo record) and assess label quality before scaling.

### 3.2 BIRDSAI Dataset — ASSEMBLED (D1.2, done 2026-08-20)

| Property | Value |
|----------|-------|
| URL | https://sites.google.com/view/elizabethbondi/dataset |
| Content | LWIR aerial surveillance: humans + African animals (elephant, giraffe, rhino, dog, zebra, etc.) |
| Coverage | 21,209 labeled frames (18,028 train / 3,181 val); 87,199 boxes: **12,531 human, 74,668 other_animal, 0 deer, 0 turkey** |
| License | CDLA-Permissive-1.0 |
| Local | `.openclaw/tmp/datasets/bootstrap_birdsai/` (YOLO format, dataset.yaml, `assemble_birdsai.py` regenerator) |
| Remap | human → `human`; all African species → `other_animal` (decision of 08-20: diversity beats species purity for thermal generalization) |

### 3.3 FLIR ADAS v2 — STILL GATED (needs David)

| Property | Value |
|----------|-------|
| URL | https://adas-dataset-v2.flirconservator.com/ |
| Content | 26,442 annotated thermal frames (v2), urban automotive scenes, 640×512, 16-bit pre-AGC |
| Remap | person → `human`; dog → `other_animal`; vehicles → background/hard negatives |
| Status | Registration form (Teledyne) still required — **no change since Aug 2026**. Would add ~12–26k mostly-human frames, fixing the current 86% other_animal / 14% human imbalance. |

### 3.4 Hard-negative / vehicle supplement — REPLACED (v2)

v1 cited a "ROAD — RObust Aerial vehicle Detection in thermal" dataset. **Two independent
searches (2026-10-15) could not locate any thermal dataset by that name** — treat the v1
claim as unverified/possibly fabricated and do not spend time hunting it. Verified
replacement with geometry directly in our operating band:

| Property | Value |
|----------|-------|
| Dataset | **HIT-UAV** (github.com/suojiashun/HIT-UAV-Infrared-Thermal-Dataset; IEEE DataPort) |
| Content | **2,898 infrared thermal images** extracted from 43,470 UAV frames |
| Geometry | Flight altitude **60–130 m**, camera perspective **30–90°** — matches our 90–120 m @45° band closely |
| Classes | Person, Bicycle, Car, OtherVehicle |
| Use | person → `human` (bonus), vehicles → background/hard negatives to suppress false positives on roads/vehicles |

---

## 4. Self-Capture Procedure

### 4.1 Site Selection

| Criteria | Requirement |
|----------|-------------|
| Location | Known deer/turkey habitat with clear lines of sight |
| Distance | 90–120 m from expected animal positions |
| Terrain | Slope/clearing where animals can be seen from above (consistent with survey angles) |
| Time | Dawn/dusk (peak activity, ≥5 °C ΔT from ground) |
| Weather | Clear, no rain/fog, wind < 15 mph |
| Thermal contrast | ≥5 °C between target and background (verified with IR thermometer) |

v2 addition — **season timing (NY, America/New_York):** it is mid-October 2026 now: white-tailed
deer activity is ramping into the pre-rut/rut (late Oct–Nov) — **prime capture window**;
dawn/dusk activity peaks. Fall wild turkey season is also open in NY through ~mid-November.
Capture sessions scheduled in the next 4–6 weeks have the highest sighting probability of the
whole year. Don't let the T13 wait push capture past this window — a surrogate camera (or even
RGB-sightings-only scouting on the same sites) kept the rig warm is better than nothing.

### 4.2 Capture Protocol

1. Set up tripod + camera at known height
2. Aim at 90–120 m standoff range (measured with rangefinder)
3. Tilt to 45° down-look (matches build)
4. Record 30–60 second clips per animal encounter
5. Log: species, distance, altitude, ambient temp, ground temp, sky condition, time
6. Vary backgrounds (field, treeline, clearing, dirt road)
7. Vary angles (±10° from 45° forward, ±30° azimuth)
8. Vary distances (80–140 m sweep through the operating band)
9. After capture, split into individual frames at ~1 fps (100–200 frames per clip)
10. **BAMBI leverage (v2):** because BAMBI already supplies substantial nadir cervid thermal
    data, bias session time toward the 45° along-range condition and white-tailed/turkey
    sightings — those are the two things no public dataset provides.

### 4.3 Target Per-Species Count

| Class | Minimum | Target | Stretch |
|-------|---------|--------|---------|
| Deer (white-tailed) — native 45° only | 200 | 500 | 1000 |
| Turkey | 50 | 150 | 300 |
| Human | 100 | 200 | 400 |
| Other animal (coyote, fox, raccoon, etc.) | 50 | 100 | 200 |
| Background (no target) | 200 | 500 | 1000 |
| **Total** | **600** | **1450** | **2900** |

v2 footnote: these are *native-capture* targets (45°, 640×512, NY habitat). BAMBI adds
deer-class diversity on top (nadir, 1024×1024, Austrian forest) and can cover ~60–80% of the
*deer thermal diversity* need — the native column is what guarantees geometry fidelity. Turkey
remains **entirely** self-captured (no public source — verified again 2026-10-15).

Background images are equally important — a classifier trained on dense positives without
negatives will fire on trees and rocks. Collect backgrounds from the same locations and
angles as the positive captures (and consider HIT-UAV/FLIR vehicle frames as hard negatives).

### 4.4 Data Management

```
analysis/thermal_sim/captured/
  raw/                      # Raw .mp4 or .mkv clips from the camera
    YYYY-MM-DD_species_location/
      clip_001.mp4
      clip_002.mp4
      metadata.csv          # Per-clip: species, dist, alt, temp, angle, weather
  frames/                   # Extracted frames (output of extract_frames.py)
    YYYY-MM-DD_species_location/
      clip_001/
        frame_0001.png
        frame_0002.png
      clip_002/
  labeled/                  # Labeled subset (after annotation)
    images/
    labels/                 # YOLO-format .txt labels
    classes.txt             # deer, turkey, human, other_animal
```

---

## 5. Capture Software — TOOLING VERIFIED 2026-10-15

### `analysis/thermal_sim/thermal_capture.py`

Live UVC capture script (opens first UVC device, live preview, 'r' record / 's' snapshot /
'q' quit, saves 16-bit TIFF + 8-bit AGC PNG, logs metadata CSV). Works with any UVC thermal
device (T13, InfiRay, FLIR Lepton, etc.). **Smoke test 2026-10-15: CLI parses cleanly;
runtime needs a real UVC device** (none attached to this host — expected).

### `analysis/thermal_sim/extract_frames.py`

Post-capture frame extraction (configurable rate, Laplacian-variance blur rejection, AGC
normalization, structured output + `extraction_log.csv`). **Smoke test 2026-10-15: PASS** —
6 s synthetic 640×512 16-bit clip (60 frames, hot moving blobs, injected blur burst):
extracted 6 frames @1 fps, blur scores computed and logged per frame, no crash.

**Calibration note (real finding from the smoke test):** on synthetic 16-bit imagery the
Laplacian-variance blur score is dominated by per-pixel sensor noise (all scores ~66–71k,
blurred and sharp alike), so a fixed `--blur-threshold` tuned on one camera may not transfer.
**Before first field use:** record ~30 s with the lens cap on (pure noise floor) + ~30 s of a
sharp high-contrast scene through the actual T13, then set `--blur-threshold` between the two
score distributions (aim for ~2× the noise-floor score). The mechanism is correct; only the
threshold needs per-camera calibration.

### Other pipeline tools (D1.3 scope, noted for coordination)

`labeling_pipeline.py` (annotation workspace + CVAT XML ↔ YOLO + dataset assembly), 30 tests;
`augmentation_pipeline.py` (Albumentations), 20 tests. ⚠️ **`albumentations` is NOT installed
in the current Python env** (import fails) — D1.3 needs `pip install albumentations` before
its pipeline runs. Not fixed here (different task's scope); flagged 2026-10-15.

---

## 6. Annotation Strategy

### Tooling

Primary: **CVAT** (self-hosted via Docker, free, supports XAI interpolation).
Fallback: LabelImg (lightweight, local, YOLO-format native).

We use the **detection** task type (bounding boxes):
- `deer` — any deer species
- `turkey` — wild turkey
- `human` — any human
- `other_animal` — fox, coyote, raccoon, etc.

### Process

1. Bootstrap datasets already have labels — remap class IDs via a conversion script (D1.2)
   - BAMBI: MOT → YOLO via the repo's own annotation-tools docs
2. Self-captured frames are imported to CVAT
3. Use automatic tracking/interpolation for single-species clips (label first + last frame,
   interpolate, then QA the mid frames)
4. QA pass: random 20% sample reviewed by a second person (David or a friend)
5. Export as YOLO-format `.txt` files (class_id cx cy w h, normalized [0, 1])

### Augmentation Plan (D1.3)

Albumentations pipeline on the training set:
- RandomScale (±20%), RandomRotate (±15°)
- RandomBrightnessContrast (thermal contrast varies with sun angle)
- RandomGamma (AGC behaves differently across scenes)
- GaussianBlur (motion blur)
- HorizontalFlip (mirror)
- Cutout (occlusion robustness)
- MixUp (domain generalization)

Test set: **no augmentation** — only raw frames.

---

## 7. Schedule & Milestones (updated 2026-10-15 — season-aware)

| Step | Duration | Dependencies | Can start |
|------|----------|--------------|-----------|
| 1. **Download BAMBI** (filtered Red/Roe deer + Wild boar flights, 60–140 m band) | 2–4 h | None | **Now** (go-ahead: see §11) |
| 2. Build/refresh bootstrap dataset (D1.2 — add BAMBI to assembled BIRDSAI) | 6 h | Step 1 | After step 1 |
| 3. Build capture rig (tripod + surrogate cam, or wait for T13) | 2 h | Surrogate purchase decision (§11) | Now (surrogate) / Phase 2 (T13) |
| 4. **Session 0 dry-run** (checklist §9, no animals needed) | 2 h | Step 3 | Next clear dawn/dusk |
| 5. Field capture Sessions 1–10 (**prime: mid-Oct through Nov**) | 32 h | Step 3/4 | Immediately |
| 6. Label self-captured frames | 6 h | Step 5 | After first session |
| 7. Augmentation pipeline (D1.3 — needs `pip install albumentations`) | 8 h | Step 2 | In parallel with 4–6 |
| 8. Training (D1.4) | 6 h | Steps 2, 6, 7 | After labeling |

**Critical path:** field capture → labeling. No single session needs to collect everything —
incremental labeling keeps the pipeline moving. With BAMBI in the mix, even 100–200 native
deer frames + BAMBI samples are enough for the first YOLO-nano fine-tune to validate the
approach.

**Season warning:** capture sessions must be concentrated in the next 4–6 weeks (pre-rut/rut
activity peak + open fall turkey season). Do not let the T13-order lead time push the first
session past mid-November; use a surrogate camera or scout sites with RGB in the meantime.

---

## 8. Risk Mitigation (updated 2026-10-15)

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| No deer/turkey sightings in session | Medium | High (lost time) | Scout locations first; use trail cameras for intelligence; deploy bait/mineral blocks at least 2 weeks before; **schedule in the Oct–Nov activity peak** |
| Thermal contrast <5 °C on cloudy day | Medium | Medium | Check forecast: capture only when ΔT ≥5 °C is verified; wet/damp conditions worsen contrast |
| T13 still not ordered (Phase 2 not funded) | High | High (no 640×512 native data) | Use lower-res surrogate for pipeline validation; **BAMBI now provides 1024×1024 thermal deer data for algorithm development** (this risk is materially reduced vs v1) |
| Deer class under-represented | Low (v2) | Medium | **BAMBI covers red/roe deer at nadir**; native white-tail 45° captures still needed for geometry fidelity |
| Turkey class rare / absent | Medium | High | Accept lower turkey count — augmentation multiplies samples; if <50 turkey frames, consider merging turkey→other_animal and deferring turkey-specific detection to Phase 3 field trials |
| Motion blur from tripod vibration | Low | Medium | Use remote shutter/cable release; weigh down tripod; per-camera blur-threshold calibration (§5) |
| Blur filter threshold mismatched to T13 | Medium | Low | Lens-cap noise-floor calibration before first session (§5) |
| Unverified v1 dataset claims ("ROAD") | Resolved | — | Replaced with verified HIT-UAV (§3.4); all §3 claims re-checked 2026-10-15 |
| Labeling is slow | Medium | Medium | Use CVAT interpolation aggressively; batch-label similar clips; first ~200 frames are enough to start training |

---

## 9. Session-0 Dry-Run Checklist (new in v2)

Run this once, on any clear day, **before any animal-dependent session** — it validates the
whole capture chain with zero wildlife:

1. [ ] Gear: camera (T13 or surrogate), laptop, tripod, rangefinder, IR thermometer, battery pack, SD/cable spares
2. [ ] Power: laptop at ≥80%; camera enumerates as `/dev/video0`; `thermal_capture.py` preview runs
3. [ ] Focus: point at a distant known object (tree line at ~100 m by rangefinder); verify crisp edge
4. [ ] Tilt: set 45° (protractor or phone inclinometer on the camera body)
5. [ ] ΔT procedure: record ground temp + ambient temp with IR thermometer; note the ΔT (need ≥5 °C)
6. [ ] Blur calibration: 30 s lens-cap (noise floor) + 30 s sharp scene; set `--blur-threshold` ≈ 2× noise-floor score
7. [ ] Record a 30 s clip; run `extract_frames.py --rate 1.0`; verify PNGs + `extraction_log.csv`
8. [ ] Metadata form: fill one row for the test clip (species=test, dist, alt, ΔT, weather, time) — validates the CSV schema
9. [ ] Check output against §4.4 folder layout
10. [ ] Confirm site access/permission for the planned capture locations

---

## 10. Files Created

| File | Purpose |
|------|---------|
| `analysis/data_collection_plan.md` | This document (v2, 2026-10-15) |
| `analysis/thermal_sim/thermal_capture.py` | Live UVC capture script (verified 2026-10-15) |
| `analysis/thermal_sim/extract_frames.py` | Frame extraction from video clips (smoke-tested 2026-10-15, PASS) |
| `analysis/thermal_sim/labeling_pipeline.py` | Annotation workspace + CVAT ↔ YOLO (D1.3) |
| `analysis/thermal_sim/augmentation_pipeline.py` | Augmentation suite (D1.3; needs `albumentations` install) |
| `analysis/thermal_sim/datasets/` | Dataset storage directory |

---

## 11. Decisions Needed from David (new in v2 — the only D1.1 blockers)

1. **BAMBI download go-ahead** — 2–4 h of download/processing, completely agent-doable the
   night you say "go" (filters to Red/Roe deer + Wild boar in the 60–140 m band to control
   size). No money involved. This is the single highest-value D1.x action available right now
   (adds the deer class that has 0 frames today).
2. **Surrogate thermal camera purchase (~$200 InfiRay P2 Pro) or wait for the T13** — a
   purchase, so it's yours to make. Relevant because **the Oct–Nov activity window is the best
   capture season of the year** and the T13 order is itself still blocked on the CDR sign-off
   (#85 → order #40).
3. **FLIR ADAS registration** (Teledyne click-through, ~2 min) — unlocks ~26k mostly-human
   frames that fix the current 86% other_animal / 14% human bootstrap imbalance.