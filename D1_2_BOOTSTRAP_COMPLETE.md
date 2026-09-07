# D1.2 Bootstrap Dataset — Complete (2026-08-30)

## What was done

Completed the D1.2 bootstrap dataset assembly with **corrected class IDs** matching `DroneThermalModel/src/dataset.py` (deer=0, turkey=1, other_animal=2, human=3).

### Sources assembled

| Source | images | human (3) boxes | other_animal (2) boxes | deer (0) / turkey (1) |
|---|---|---|---|---|
| BIRDSAI real-train (CDLA-Permissive-1.0) | 21,209 | 12,531 | 74,668 | 0 / 0 |
| FLIR ADAS v2 thermal_train (Teledyne research) | 8,205 | 50,478 | 4 | 0 / 0 |
| FLIR ADAS v2 thermal_val (Teledyne research) | 819 | 4,470 | 0 | 0 / 0 |
| FLIR ADAS v2 video_thermal_test (Teledyne research) | 2,231 | 12,323 | 25 | 0 / 0 |
| **Total** | **32,464** | **79,802** | **74,697** | **0 / 0** |

### Split
- Train: 25,413 images (63,652 other_animal + 55,993 human boxes)
- Val: 7,051 images (11,045 other_animal + 23,809 human boxes)

### Verification
- ✅ No invalid class IDs (all labels are 0-3)
- ✅ dataset.yaml class order matches canonical: `0: deer, 1: turkey, 2: other_animal, 3: human`
- ✅ Train/val label counts match image counts
- ✅ FLIR val and video_test merged fully into val split (no train leakage)

## Dataset Location (as of 2026-08-31)

✅ **Durable location**: `datasets/bootstrap/` (workspace root). Moved from `.openclaw/tmp/datasets/bootstrap_birdsai_new/` and `dataset.yaml` paths updated. This directory will not be cleaned by tmp sweeps.

### Cleaned
- `bootstrap_birdsai/` (1.3 GB) — deleted. Buggy class IDs (human=0, other_animal=3).
- `bootstrap_birdsai_backup_20260830/` (1.3 GB) — deleted. Same buggy class IDs.
- Total freed: ~2.6 GB.

### What remains in tmp/
- `birdsai_raw/` (2.2 GB) — kept. Raw BIRDSAI download in case regeneration is needed.
- Assembly scripts — kept for reference. Canonical fixed versions are on the Windows Mission-Control project.

## Remaining for D1.2 (task #58)

~~**(d) move dataset out of tmp/ — DONE 2026-08-31**~~
- (e) Decide where corrected scripts live permanently (the Windows Mission-Control project has the fixed versions). The assembly scripts in tmp/ have correct class IDs in the latest iteration but `assemble_flir_adas.py` has a minor stats-display bug.
- ~~**(d) dataset cleanup — DONE 2026-08-31**~~
- **deer + turkey**: Still 0 boxes across all sources. **D1.1 self-collected LWIR footage is the only source** for these classes. D1.3/D1.4 training can proceed for human/other_animal but will not produce a model that can detect deer or turkey.

## Next steps after this task

- **D1.3 (task #59)**: Build the augmentation pipeline. Can proceed against `bootstrap_birdsai_new` for human/other_animal classes.
- **D1.4 (task #60)**: Run training pipeline. Can start once D1.3 is done, but only for human/other_animal.
- **D1.1 (task #57)**: Self-collected deer/turkey LWIR — the long pole. No progress made here.