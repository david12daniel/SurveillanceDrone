# PurpleRiver Mini 640 / T13 (thermal camera) — CAD spec sheet

**Purpose:** dimensional spec for a parametric CAD model of the thermal camera (T13 =
**18 mm-lens** variant, SELECTED 2026-07-29; was 13 mm) for the Chimera9 nose bracket.
Companion to [`nanopi_m5_cad_spec.md`](nanopi_m5_cad_spec.md).

**OEM identity:** the PurpleRiver Mini 640 is a rebrand of the **Raytron/iRay "WN640"**
uncooled core (title block on the drawing: `WN640_384_9.1mm Assembly`). The authoritative
dimensions come from the iRay OEM manual, **not** the lite PurpleRiver sheet.

**Sources (2026-07-29):**
- ⭐ `iRay_MINI_384-640_Module_Manual_V1.10.pdf` §6 "Structure and Dimensions" — mechanical
  drawing embedded at **1183×810 px (legible)**. Primary source for all geometry below.
- `PurpleRiver_Mini640_Mini2_specifications.pdf` — same drawing but 508×351 px (blurry); text confirms connector.
- `PurpleRiver_Mini640_specs.pdf` — lite one-pager (lens/FOV table per focal length).

**Confidence:** ✅ read clearly off the legible drawing · ⚠️ minor source conflict · ❌ not shown (caliper)

---

## Core module (lens-independent — the mounting interface)

| Attribute | Value | Conf. |
|---|---|---|
| Body (square) | **21.00 × 21.00 mm** (±0.10) | ✅ |
| Mounting holes | **8 × M2 threaded, 1.5 mm deep** ("8-M2▽1.5") — **4 on front face + 4 on rear face** | ✅ |
| Hole pattern | **18.40 × 18.40 mm** (±0.10), centered | ✅ |
| Front lens-mount boss | **Ø21.00 mm** (±0.10) circular boss on the front face | ✅ |
| Focal-plane ref ("focus panel") | **4.57 mm** (iRay) — rebrand lists 4.775 | ⚠️ |
| Rear connector | **50-pin Hirose DF40C-50DP-0.4V(51)** (mating: DF40HC(2.5)-50DS-0.4V(51)) | ✅ (text) |
| Core depth (no lens) | **~8 mm** (iRay text "21×21×8") vs **10.3 mm** (rebrand text) — variant/measurement conflict | ❌ caliper |
| Weight (core, no lens) | **< 20 g** | ✅ |
| Detector | 640×512, 12 µm, VOx, 8–14 µm | ✅ |

**General tolerance table (unmarked dims):** ≤10 → ±0.08 · 10–30 → ±0.12 · 30–80 → ±0.15 · >80 → ±0.2 mm; angles ≤30° ±0.15°, 31–90° ±0.2°.

## Lens (T13 = 18 mm) — barrel adds to the core depth

The drawing details only the **9.1 mm** lens example (overall depth **22.4 ±0.25 mm**,
FOV drawn 63.5°). The **18 mm barrel is longer/heavier and not dimensioned** in any
resource we have — model it as an estimate and caliper the real lens.

| T13 lens attribute | Value | Conf. |
|---|---|---|
| Focal length | **18 mm**, F1.0 (SELECTED; was 13 mm) | ✅ (lite sheet lens table) |
| FOV (18 mm) | **24.1° × 19.4°** (below R3_CAM_FOV 30° — accepted, surveillance-only) | ✅ computed |
| Barrel outer Ø / length | ~Ø20 / ~24 mm protrusion (est.; longer than 13 mm) | ❌ caliper |

## For the nose-bracket model

**Fully known now (build to spec):** the 21×21 body + the **8-M2 / 18.40 mm mounting
pattern** on both faces + the Ø21 front boss. That is the entire bracket interface —
you bolt the bracket to the **rear** face's 4× M2 holes (front face holds the lens),
and the camera looks out the front. This is lens-independent, so it's valid for T13.

**Confirm with calipers (small):** core depth (8 vs 10.3), the **18 mm** barrel Ø + length,
and which face's holes you use for the bracket.

## Corrections this supersedes

- My earlier low-res read of "4 × Ø1.6/2.0 holes" was **wrong** — it's **8 × M2 tapped, 1.5 deep**.
- `candidates.sysml` T13 `dimensions` updated `~17×17×35` → **`21x21x~34`** (21×21 core + 18 mm lens).
- **Lens updated 13 mm → 18 mm** (2026-07-29); the mounting interface (21×21, 8-M2/18.40, Ø21 boss)
  is **lens-independent**, so the bracket geometry is unaffected — only the barrel length/mass change.
