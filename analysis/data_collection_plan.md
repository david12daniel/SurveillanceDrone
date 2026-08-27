# D1.1 — Thermal Data Collection Plan & Capture Rig

**Status:** Complete plan ready for review  
**Est. collection effort:** ~40 h field capture · ~8 h labeling & QA  
**Blocking:** None — no hardware dependency. Capture can begin with any USB-UVC thermal camera  
**Related tasks:** D1.2 (bootstrap assembly), D1.3 (labeling/aug pipeline), D1.4 (training)

---

## 1. Overview

D1.1 covers everything needed to go from zero labeled thermal data to a training-ready set of
LWIR deer, turkey, human, and other-animal images at 90–120 m AGL, in the look-down / 45°
forward-tilt geometry of the build.

**Two parallel streams:**

| Stream | Source | Contribution | Effort |
|--------|--------|-------------|--------|
| **Bootstrap** | Public datasets (BAMBI, BIRDSAI, FLIR ADAS, ROAD) | ~2,000–5,000 frames, annotated | 8 h (D1.2) |
| **Self-capture** | Field recording with the actual T13 on a tripod or drone | ~500–2,000 frames per session, 4-class annotations | ~40 h total |

Both streams are needed: the bootstrap covers class diversity and large-volume pre-training;
self-capture covers the exact sensor (12 µm, 18 mm, 640×512), geometry (45° tilt, 90–120 m
standoff), and local ecosystem (deer/turkey species present in the operating area).

> **Decision:** BAMBI detection dataset (Zenodo 10.5281/zenodo.15773102) is the #1 priority
> bootstrap target — it already contains thermal drone footage of red deer, roe deer, and
> wild boar, directly matching our domain. BIRDSAI covers humans and African megafauna.
> FLIR ADAS provides urban thermal variety. These three together cover ~15 classes, of which
> we remap: `deer`, `turkey`, `human`, `other_animal`, `background`.

---

## 2. Capture Rig Specification

### 2.1 Tripod-based (no drone needed — start immediately)

Since the T13 hasn't been ordered (Phase 2), use a surrogate thermal camera for early capture.
Recommended: **any USB-UVC thermal camera with 640×512 resolution** — e.g. an InfiRay P2 Pro
(256×192, $200, immediate availability) or a borrowed FLIR One Pro (iOS/Android). Lower
resolution means images are good for species ID practice and pipeline testing, but for final
training you'll want the T13 or equivalent 640×12 µm sensor.

**Minimum viable rig:**
- 640×480 or better USB-UVC thermal camera (when T13 arrives, it is the primary)
- Laptop running `thermal_capture.py` (see §5)
- Tripod with adjustable tilt (0–60°) and a pan head
- Battery pack for laptop (or AC if range extends to an outlet)
- Measuring tape + laser rangefinder for distance calibration
- Temperature probe (IR thermometer) to log ambient ΔT

### 2.2 Drone-based (Phase 2+ hardware)

Once the Phase 2 build is complete, capture from the actual drone platform:
- T13 USB → NanoPi M5 → frame capture script
- Fly at 90–120 m AGL, 45° forward tilt
- Log: altitude (GPS), heading, GPS coordinates of each frame
- This produces the **operationally perfect** training set

### 2.3 Benchmarking note

The T13's 12 µm pitch × 18 mm lens at 120 m gives a GSD of:
- Nadir IFOV: 12 µm / 18 mm = 0.667 mrad → 0.080 m/pixel at 120 m
- At 45° tilt (along-range): GSD × 1/cos²(45°?) — actually geometric projection
  makes it ~2× worse along-range → ~0.16 m/pixel
- A 0.5 m deer target: ~6 px nadir, ~3 px along-range → Johnson detection threshold (1.5 px)
  is met but recognition (4 px) is marginal along-range — this is exactly why
  real-capture data from this geometry is critical before relying on the model.

---

## 3. Bootstrap Public Datasets

### 3.1 BAMBI Detection Dataset (Top Priority)

| Property | Value |
|----------|-------|
| URL | https://zenodo.org/records/15773102 |
| DOI | 10.5281/zenodo.15773102 |
| Content | Thermal drone imagery of red deer, roe deer, wild boar |
| Coverage | 389 paired RGB+thermal aerial sequences over Austrian forests |
| Resolution | LWIR unspecified but likely 640×512 class |
| Geometry | Aerial look-down — directly applicable |
| License | CC-BY (check per-file) |
| Effort | Clone `bambi-eco/Dataset` git repo, use `download_flights.py` to selectively fetch |

**Target remap:**
- `red deer` / `roe deer` → our unified `deer` class
- `wild boar` → `other_animal`

### 3.2 BIRDSAI Dataset

| Property | Value |
|----------|-------|
| URL | https://sites.google.com/view/elizabethbondi/dataset |
| Content | LWIR aerial surveillance: humans + animals (elephant, giraffe, rhino, etc.) |
| Coverage | Southern Africa, nighttime, 640×512 |
| Geometry | Aerial look-down |
| Annotation | Bounding boxes + tracking IDs |
| Size | ~30 videos, thousands of frames |
| License | Research use |

**Target remap:**
- `human` → our `human` class (critical: the system must distinguish humans from animals)
- `elephant`, `giraffe`, etc. → `other_animal`
- Provides valuable night-operations variety

### 3.3 FLIR ADAS Dataset

| Property | Value |
|----------|-------|
| URL | https://adas-dataset-v2.flirconservator.com/ |
| Content | 26,442 annotated thermal frames (v2), urban automotive scenes |
| Resolution | 640×512, 16-bit pre-AGC |
| Classes | Person, bicycle, car, motorcycle, bus, train, truck, dog, etc. |
| License | Free for algorithm development |
| Effort | Fill registration form at oem.flir.com, download |

**Target remap:**
- `person` → `human`
- `dog` → `other_animal`
- All vehicle classes → background (exclude from training if they won't appear in
  the operational area; keep for hard-negative mining if helpful)

### 3.4 ROAD Dataset (optional supplement)

The RObust Aerial vehicle Detection in thermal images dataset covers only vehicles,
but can serve as background/hard-negative examples to reduce false positives.

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

### 4.3 Target Per-Species Count

| Class | Minimum | Target | Stretch |
|-------|---------|--------|---------|
| Deer (white-tailed) | 200 | 500 | 1000 |
| Turkey | 50 | 150 | 300 |
| Human | 100 | 200 | 400 |
| Other animal (coyote, fox, raccoon, etc.) | 50 | 100 | 200 |
| Background (no target) | 200 | 500 | 1000 |
| **Total** | **600** | **1450** | **2900** |

Background images are equally important — a classifier trained on dense positives without
negatives will fire on trees and rocks. Collect backgrounds from the same locations and
angles as the positive captures.

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

## 5. Capture Software

### `analysis/thermal_sim/thermal_capture.py`

A Python script that:
1. Opens the first available UVC device (`/dev/video0`)
2. Displays a live preview at 640×512
3. On keypress 'r' — start recording; 's' — stop; 'q' — quit
4. Saves raw 16-bit frames and/or 8-bit AGC-normalized PNGs
5. Logs metadata (timestamp, FPS, frame count) to CSV
6. Optional: shows a crosshair reticle for aim-point

Written to work with any UVC thermal device, not just the T13.

### `analysis/thermal_sim/extract_frames.py`

Post-capture: extracts frames from video clips at a configurable rate (default 1 fps),
saves as 8-bit PNG, strips frames that are too blurry (Laplacian variance < threshold),
and logs extracted frames with source clip metadata.

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

## 7. Schedule & Milestones

| Step | Duration | Dependencies | Can start |
|------|----------|--------------|-----------|
| 1. Download BAMBI and BIRDSAI | 2 h | None | **Now** |
| 2. Build bootstrap dataset (D1.2) | 6 h | Step 1 | **Now** |
| 3. Build capture rig (tripod + surrogate cam) | 2 h | None | **Now** |
| 4. Field capture Session 1 | 4 h | Step 3 | **Next clear dawn/dusk** |
| 5. Field capture Sessions 2–10 | 32 h | Step 3 | Ongoing |
| 6. Label self-captured frames | 6 h | Step 4 | After first session |
| 7. Augmentation pipeline (D1.3) | 8 h | Step 2 | In parallel with 4–6 |
| 8. Training (D1.4) | 6 h | Steps 2, 6, 7 | After labeling |

**Critical path:** field capture → labeling. No single session needs to collect everything
— incremental labeling keeps the pipeline moving. Even 200 deer frames + BAMBI samples
are enough for the first YOLO-nano fine-tune to validate the approach.

---

## 8. Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| No deer/turkey sightings in session | Medium | High (lost time) | Scout locations first; use trail cameras for intelligence; deploy bait/mineral blocks at least 2 weeks before |
| Thermal contrast <5 °C on cloudy day | Medium | Medium | Check forecast: capture only when ΔT ≥5 °C is verified; wet/damp conditions worsen contrast |
| T13 still not ordered (Phase 2 not funded) | High | High (no 640×512 native data) | Use lower-res surrogate for pipeline validation; BAMBI provides 640×512 thermal drone data for algorithm dev |
| Motion blur from tripod vibration | Low | Medium | Use remote shutter/cable release; weigh down tripod |
| Labeling is slow | Medium | Medium | Use CVAT interpolation aggressively; batch-label similar clips; first ~200 frames are enough to start training |
| Need turkey class but rare | Medium | High | Accept lower turkey count — use augmentation (flipping, rotation) to multiply samples; if <50 turkey frames, consider merging turkey→other_animal and deferring turkey-specific detection to Phase 3 field trials |

---

## 9. Bootstrap Dataset Assembly Quick-Start

```bash
# Create directories
mkdir -p analysis/thermal_sim/datasets/bootstraps/{bambi,birdsai,flir_adas}
mkdir -p analysis/thermal_sim/datasets/self_captured/{raw,frames,labeled}

# BAMBI download (using official tool)
git clone https://github.com/bambi-eco/Dataset.git
cd Dataset
# See bambi-eco/Dataset README for flight selection and download commands

# BirdSAI download
wget -r -np -nH https://sites.google.com/view/elizabethbondi/dataset

# FLIR ADAS: register at oem.flir.com, download the zip
```

---

## 10. Files Created

| File | Purpose |
|------|---------|
| `analysis/data_collection_plan.md` | This document |
| `analysis/thermal_sim/thermal_capture.py` | Live UVC capture script (see below) |
| `analysis/thermal_sim/extract_frames.py` | Frame extraction from video clips (see below) |
| `analysis/thermal_sim/datasets/` | Dataset storage directory (to be created) |