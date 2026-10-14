# T13 (PurpleRiver Mini 640) Mass Research — October 2026 Follow-Up

**Date:** 2026-10-14
**Task:** Mission Control #39 / TASKS.md 2.1 — Confirm the 18 mm T13 variant's mass with the vendor
**Purpose:** Eight-week follow-up re-verification of the 15.0 g estimate (set 2026-08-20), re-checking
all vendor-published sources for any new per-lens or assembled-weight data before the Phase 2 order
(task 2.2 / #40).

## What changed since the August research

### 1. The official spec sheet was UPDATED on 2026-08-24 (after our 2026-08-20 download)

- Download page (`thermal-image.com/download/purpleriver-mini640-thermal-camera-specifications/`)
  shows "Last Updated 2026年8月24日" — four days after we saved the original (131,225 bytes).
- Re-downloaded the current file: **114,264 bytes, 2 pages** (saved as
  `Purpleriver-Mini640-Spec-Sheet-2026-08-24.pdf` alongside the original).
- **Mass section UNCHANGED:** `Weight <20 g (without lenses and flanges)`, size `21mm × 21mm × 28mm`.
  No per-lens weight breakdown was added. The <20 g ceiling and the 21×21×28 mm envelope stand.

### 2. NEW vendor finding — the radiometric version only comes with 9/13/18 mm lenses

The updated spec sheet now carries a note on the model table:
> **"Note: The Radiometric Version only has 9/13/18mm lenses"**

Implications for our selection (work item #40, CDR):

- The Mini640's radiometric (25 Hz, temperature-measuring) version is restricted to **three lenses:
  9 mm, 13 mm, and 18 mm**.
- Our chosen **18 mm lens is therefore valid on the radiometric variant** — and it is the
  **longest lens offered on the radiometric version** (the 18 mm is the top of the radiometric
  range; anything longer — 25/35/50/60/75 mm — is non-radiometric only).
- This closes the small open question "is the 18 mm lens available on the variant we want?" → **yes**,
  and it is the best range option on the radiometric line.
- **Variant flag for the order:** our Phase 2 acceptance criterion (task 2.15 / #53) expects
  "640×512 at ~25 Hz", which matches the **radiometric 25 Hz** version. The non-radiometric version
  runs at 60 Hz. The BOM/SELECTED_COMPONENTS do not explicitly record "radiometric" — David should
  confirm **radiometric 25 Hz + 18 mm + USB** at checkout (task 2.2). Price quote $640 base ($590 +
  $50 lens) + $60 shipping = $700 was confirmed 2026-07-29; the radiometric note does not contradict it.

### 3. Reseller listings re-checked — no assembled-weight figure anywhere

| Source | Figure | Condition | Notes |
|---|---|---|---|
| Made-in-China 18 mm CVBS listing (`XGZYESqMfoWl`) | **6 g** | Without lens | Also confirms: type = **Non-Radiometric Version**, 50 Hz (PAL CVBS), 21×21 mm |
| Alibaba MINI Mould (`1600916965973`) | — (no module weight) | — | $399–1,620 price range by config; 60 Hz non-radiometric; 21×21 mm; packaged gross 0.24 kg |
| Official spec sheet (2026-08-24) | **<20 g** | Without lenses and flanges | Mass section unchanged from the August download |
| thermal-image.com product page | **<20 g** | Without lens | Model table lists Mini640-**18**, FOV 24.2°×19.5°, F#1.0 |
| Cross-vendor sanity bound: InfiRay Mini640-class core (thermalscope made-in-china 18 mm listing) | "under 10 g" | Without lens | Same 21×21 mm core family — brackets the bare-core figure rather than asserting PurpleRiver's |

**Conclusion: eight weeks of additional vendor-published data still contain no per-lens or
assembled (module + 18 mm lens) weight.** The estimate stands:

- Bare module: **6 g** (product page, without lens)
- 18 mm Ge lens assembly: **6–9 g** (germanium density × 2-element F#1.0 construction + Al barrel)
- **Total estimate: 12–17 g, midpoint 15.0 g** — unchanged, re-affirmed.

## CG impact re-check (quantified)

The Aug 20 model change was 21.0 → 15.0 g (Δ = −6.0 g) on a nose-mounted payload, so a re-check:

- Conservative nose moment arm: 150–250 mm forward of the aircraft CG (Chimera9 ECO, 405 mm wheelbase)
- All-up mass of the reference build (AF3a 729 g + BAT10 919 g + SBC3 80 g + T13 15 g + props/VTX/FPV
  cam/RX/anti-spark/mounts ≈ 1.9 kg)
- ΔCG = (6.0 g × arm) / 1,900 g ≈ **0.5–0.8 mm** — well under the ±10–20 mm class of CG tolerance
  for a 405 mm-wheelbase quad.

**Verdict: negligible, consistent with the 2026-08-21 assessment.** No model or analysis
regeneration is warranted for this delta. (Full as-built CG re-check remains task 2.11 / #49.)

## State of the task

- `candidates.sysml` `T13.mass = 15.0 [g]` — **kept** (re-affirmed, no source contradicts the
  12–17 g range; comment extended with tonight's verification).
- The exact assembled figure still requires the vendor: inquiry package with email
  (`justin.lu@purpleriver.cn`) + ready-to-send text is in `t13-vendor-inquiry-complete.md`.
- **Remaining (David's call):** send the inquiry, or close the task at the 15.0 g estimate — it is
  sufficient for ordering and the CG impact is <1 mm either way. If the vendor replies, update
  `candidates.sysml T13.mass` with the real number.

## Artifacts

- `Purpleriver-Mini640-Spec-Sheet-2026-08-24.pdf` — re-downloaded current spec (114,264 bytes, 2 pages)
- This note (research-findings-oct-2026.md)
- `candidates.sysml` — comment-only update on `T13` (mass unchanged at 15.0 g)
- `TASKS.md` row 2.1 — reconciled to the true state (was stale: still said 21.0 g untouched)