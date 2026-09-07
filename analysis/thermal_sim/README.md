# D1.3 — Labeling & Augmentation Pipeline

## Overview

Complete pipeline for preparing thermal LWIR training data:
- **Frame extraction** from raw video (D1.1 fieldwork)
- **Annotation workspace** preparation
- **CVAT XML ↔ YOLO format** conversion
- **Dataset assembly** with train/val split and bootstrap merging
- **Augmentation** during training (altitude-band-aware transforms)

## Files

| File | Purpose |
|------|---------|
| `extract_frames.py` | Extract frames from raw thermal video clips (D1.1 field capture) |
| `labeling_pipeline.py` | Annotation workspace prep + CVAT XML import + dataset assembly |
| `augmentation_pipeline.py` | Training/validation augmentations, mosaic, helpers |
| `test_labeling_pipeline.py` | 30 unit tests (prepare, CVAT import, assemble, validate) |
| `test_augmentation_pipeline.py` | 20 unit tests (transforms, mosaic, CLI) |

## Workflow

```
D1.1 Field Capture (raw .mp4)
         │
         ▼ extract_frames.py --input raw_clips/ --output extracted_frames/
         │
         ▼ labeling_pipeline.py prepare --input extracted_frames/ --output annotation_workspace/
         │
    ┌────▼────┐
    │  CVAT   │  ← manual annotation at http://localhost:8080
    └────┬────┘
         │ Export as CVAT XML 1.1
         ▼
 labeling_pipeline.py import-cvat \
     --cvat-xml annotations.xml \
     --image-dir annotation_workspace/images/ \
     --label-dir annotation_workspace/labels/
         │
         ▼
 labeling_pipeline.py assemble \
     --annotated annotation_workspace/ \
     --output datasets/final_thermal_v1/ \
     --bootstrap /path/to/bootstrap_birdsai/
         │
         ▼
 labeling_pipeline.py validate --dataset datasets/final_thermal_v1/
         │
    ┌────▼────┐
    │ TRAIN   │  ← src/train.py (+ augmentation_pipeline.py for transforms)
    └─────────┘
```

## Quick Start — Labeling Pipeline

```bash
# Step 1: Set up annotation workspace from extracted frames
python3 labeling_pipeline.py prepare \
    --input extracted_frames/ \
    --output annotation_workspace/ \
    --max-images 500

# Step 2: (manual) Annotate in CVAT
#   Import images from annotation_workspace/images/
#   Export CVAT XML 1.1 when done

# Step 3: Import CVAT XML → YOLO labels
python3 labeling_pipeline.py import-cvat \
    --cvat-xml annotations.xml \
    --image-dir annotation_workspace/images/ \
    --label-dir annotation_workspace/labels/

# Step 4: Assemble final dataset (with bootstrap merge)
python3 labeling_pipeline.py assemble \
    --annotated annotation_workspace/ \
    --output datasets/final_thermal_v1/ \
    --bootstrap /path/to/bootstrap_birdsai/

# Validate
python3 labeling_pipeline.py validate --dataset datasets/final_thermal_v1/
```

## Quick Start — Augmentation Pipeline

```python
from augmentation_pipeline import get_train_augmentations, get_val_augmentations

# Training pipeline (stochastic transforms)
aug = get_train_augmentations(target_size=(640, 640), altitude_band="nominal")
result = aug(image=img, bboxes=bboxes, class_labels=class_labels)

# Validation pipeline (deterministic, resize + normalise only)
val_aug = get_val_augmentations(target_size=(640, 640))
```

## Augmentation Transforms

### Training (albumentations — when available)

| Transform | Strength | Probability |
|-----------|----------|-------------|
| RandomScale | 0.7–1.2× (nominal); tuned per altitude band | 0.8 |
| Rotate ±15° | constant border | 0.6 |
| HorizontalFlip | — | 0.5 |
| RandomBrightnessContrast | ±20% | 0.8 |
| RandomGamma | 80–160 | 0.5 |
| CLAHE | 8×8 tiles | 0.3 |
| MotionBlur / GaussianBlur / MedianBlur | 3–5 px | 0.3 |
| GaussNoise / ISONoise | light | 0.2 |
| CoarseDropout | 8 holes, 32 px max | 0.3 |
| Mosaic | 4-image stitch | caller-chosen p |

### Training (OpenCV fallback — no albumentations)

- Random horizontal flip (0.5)
- Random brightness shift (0.5)
- Random gamma (0.3)
- Gaussian blur (0.3)
- Resize + normalise to [0, 1]

### Validation

Resize + normalise to [0, 1]. No stochastic transforms.

## Altitude-Band Awareness

Three bands tune scale/blur transforms to match expected apparent object size:

| Band | Altitude | Scale | Blur |
|------|----------|-------|------|
| low | 80–100 m | 0.5–1.0× | 5 px max |
| nominal | 100–120 m | 0.7–1.2× | 5 px max |
| high | 120–140 m | 0.85–1.25× | 3 px max |

## Dependencies

- **Required:** Python 3.8+, NumPy, OpenCV
- **Optional:** `albumentations` (recommended for richer transforms): `pip install albumentations`

## Run Tests

```bash
python3 -m pytest analysis/thermal_sim/ -v
# 50 tests total (20 augmentation + 30 labeling)
```

## Class Mapping

```
0: deer         (needs D1.1 self-collected footage — 0 boxes in bootstraps)
1: turkey       (needs D1.1 self-collected footage — 0 boxes in bootstraps)
2: other_animal (bootstrapped from BIRDSAI: 74,668 boxes)
3: human        (bootstrapped from BIRDSAI: 12,531 boxes)
```

## Current Dataset Status (2026-09-03)

- **BIRDSAI bootstrap**: ✅ 21,209 labeled frames assembled (train: 18,028 / val: 3,181)
- **FLIR ADAS v2**: ⛔ Gated behind Teledyne click-through / Kaggle account
- **D1.1 self-collected (deer/turkey)**: ⛔ Needs field capture session
- **Augmentation pipeline**: ✅ Built, tested (50/50)
- **Labeling pipeline**: ✅ Built, tested (30 tests)
- **D1.4 training**: Can start for human/other_animal only; deer/turkey still pending D1.1