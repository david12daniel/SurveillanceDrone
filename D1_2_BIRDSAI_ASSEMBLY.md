# D1.2 - BIRDSAI Bootstrap Dataset Assembly - Complete

**Date:** 2026-08-20
**Status:** ✅ BIRDSAI portion complete

## Summary

Downloaded and processed the BIRDSAI (Benchmarking IR Dataset for Surveillance with Aerial Intelligence) real-world training data into YOLO-format bootstraps for the DroneThermalModel 4-class pipeline.

## Source

- **Dataset:** BIRDSAI (Conservation Drones, LILA BC)
- **License:** CDLA-Permissive-1.0
- **Download:** `conservation_drones_train_real.zip` (2.27 GB)
  - Source: Azure Blob Storage (public, no auth)
  - `https://lilawildlife.blob.core.windows.net/lila-wildlife/conservationdrones/v01/conservation_drones_train_real.zip`

## Output

| Metric | Value |
|--------|-------|
| Total labeled frames | 21,209 |
| Training frames | 18,028 |
| Validation frames | 3,181 |
| Total bounding boxes | 87,199 |
| Human boxes | 12,531 |
| Other_animal boxes | 74,668 |
| Deer boxes | 0 (needs D1.1) |
| Turkey boxes | 0 (needs D1.1) |
| Image dimension varieties | 640×512, 700×321, 840×398, 699×333, etc. |

**Decision:** Included all BIRDSAI species (elephant, lion, giraffe, dog, crocodile, hippo, zebra, rhino) as `other_animal` class. Rationale: more diverse thermal training data improves generalization, and these species' thermal signatures are more similar to deer/turkey than to humans.

## Artifacts

- **Dataset directory:** `.openclaw/tmp/datasets/bootstrap_birdsai`
  - `images/train/` - 18,028 JPEG frames
  - `images/val/` - 3,181 JPEG frames
  - `labels/train/` - 18,028 YOLO .txt files
  - `labels/val/` - 3,181 YOLO .txt files
  - `dataset.yaml` - Ultralytics-compatible config
  - `assemble_birdsai.py` - regeneration script included

## What's Left for D1.2

1. **FLIR ADAS v2** - Gated behind Teledyne click-through / Kaggle account. Needs David's action.
2. **Class balance review** - Current BIRDSAI-only data has 86% `other_animal`, 14% `human`. FLIR ADAS (26k frames, mostly human/car) would significantly improve human class representation.

## Next Steps

- D1.3 (labeling + augmentation pipeline) can proceed for human/other_animal classes
- D1.1 (self-collected deer/turkey footage) is still the critical gap