# D1.3 — Augmentation Pipeline

## Files

| File | Purpose |
|------|---------|
| `augmentation_pipeline.py` | Main module: training/validation augmentations, mosaic, helpers |
| `test_augmentation_pipeline.py` | 20 unit tests (passes with OpenCV-only, no albumentations required) |

## Quick Start

```python
from augmentation_pipeline import get_train_augmentations, get_val_augmentations

# Training pipeline (stochastic transforms)
aug = get_train_augmentations(target_size=(640, 640), altitude_band="nominal")
result = aug(image=img, bboxes=bboxes, class_labels=class_labels)

# Validation pipeline (deterministic, resize + normalise only)
val_aug = get_val_augmentations(target_size=(640, 640))
result = val_aug(image=img, bboxes=bboxes, class_labels=class_labels)
```

## Transforms

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
python3 -m pytest analysis/thermal_sim/test_augmentation_pipeline.py -v
```

## CLI Quick Test

```bash
python3 augmentation_pipeline.py --image /path/to/frame.png --label /path/to/label.txt --samples 4
```