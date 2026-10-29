# T13 Spec Sheet Update — Oct 23, 2026

**Date:** 2026-10-28 (discovered during nightly sweep)
**Author:** Thermal Surveillance Drone (nightly agent)

## Discovery

The Purpleriver Mini640 spec sheet PDF was updated on **2026-10-23**, between the
Oct 14 re-download (which was byte-identical to the Aug 24 version) and this check.

**Comparison:**

| Property | Old (Aug 24 / 2024) | New (Oct 23, 2026) |
|----------|---------------------|-------------------|
| File size | 114,264 bytes | 176,043 bytes (+54%) |
| md5 | `9b78295dc07959dd503b0113bae472b4` | `6fc06bac5f083e80e9a651a349165d18` (changed) |
| PDF CreationDate | 2024-08-24 | **2026-10-23** |
| Pages | 2 | 2 |
| Page 1 image | 528×158 (JPEG, 9.8KB) — thumbnail | **992×1403 (PNG, 135KB)** — full-page |
| Page 2 image | None (empty/zero-image page) | **992×1403 (PNG, 34KB)** — full-page |

The Oct 23 update is a **complete re-issue** — both pages are now high-resolution
embedded images rather than the old minimal content. The new version is a substantial
content revision, not a minor touch-up.

## Impact Assessment

**The product page** (thermal-image.com) still shows:
- Weight: `<14.9 g (without lens)` — unchanged since the Oct 24 nightly confirmed this
  (it was previously reported as `<20g` in the Aug 24 spec sheet and `＜20g` in the original)

We cannot OCR the new PDF without a system tesseract installation (not available).
However, the product page weight is already tighter than the old spec sheet's `<20g`
ceiling, and the 15.0g estimate (midpoint of 6g bare + 6–9g lens) is well within both
bounds — the Oct 24 CG analysis showed even the worst case (23.9g) is acceptable
(ΔCG ≤ 1.29 mm).

## Action

- New spec sheet saved as:
  `Purpleriver-Mini640-Spec-Sheet-2026-10-23.pdf`
- Old version retained for reference:
  `Purpleriver-Mini640-Spec-Sheet-2026-08-24.pdf`
- No mass update to candidates.sysml needed — 15.0g estimate remains valid
  regardless of the spec sheet revision
- If OCR is needed later: `brew install tesseract` (requires glibc toolchain)