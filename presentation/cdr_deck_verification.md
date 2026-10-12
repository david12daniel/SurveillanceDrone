# CDR Deck Verification — Task [0.1] / #85

**Date:** 2026-10-11 (nightly run) · **Follow-up:** 2026-10-12 (nightly run)
**Deck:** `CDR_Thermal_Surveillance_Drone.pptx` (41 slides, 13.333×7.5 in)
**Verifier:** `presentation/verify_cdr_deck.py` (new, 2026-10-11 run)

Closes the open pre-briefing checklist item from `presentation/cdr_briefing_prep.md`:
> Slide 14 (System Composition) — Confirm the replacement looks correct in the
> real deck. Verify the graphviz-rendered diagram is present, the 33 old
> hand-drawn shapes are gone, and the caption text is preserved.

## What was verified (all PASS)

1. **Deck opens cleanly** — 41 slides, no package corruption.
2. **Slide 14 has exactly one picture** — the model-derived
   `presentation/assets/diagrams/system_composition.png` (graphviz render of
   `AerialObservationSystem` from `model.sysml`). Embedded image md5
   `4067545fb80e…` matches the source file byte-for-byte.
3. **No legacy hand-drawn shapes remain** — no shape text carries the old
   `sysml_box`/`def_panel` labels (`AerialObservationSystem`, `Drone`, `GCS`,
   part names). Raw-ID checking was dropped: fresh builds renumber shapes, and
   the `framed_image` card rectangle legitimately lands in the old ID range.
4. **Caption + title preserved** — "System Composition — Block-Definition View"
   title and the "Block-definition (composition) view…" caption are intact.
5. **Picture does not overlap the caption** — placed at 4.28″/1.46″, 3.68×5.13″,
   well above the caption at y≈6.82″.
6. **All package relationships resolve** — no dangling image/part targets.
7. **RTM table has no blank verification cells** — `requirements_traceability.csv`
   (57 rows): `method` 0 blank, `status_at_cdr` 0 blank (prep checklist item).
8. **Backup present** — `CDR_Thermal_Surveillance_Drone.pptx.bak.pptx` (pre-diagram
   swap, 4,389,246 B) preserved for reversibility.

## Hazard found and fixed

`presentation/build_cdr.py` **regenerated slide 14 as hand-drawn shapes** —
re-running the deck build (which `cdr_briefing_prep.md` instructs David to do to
"pick up changes") silently clobbered the Sep 15 diagram swap and required
re-running `apply_slide14_diagram.py` as a manual second step.

**Fix (committed):** `build_cdr.py` now emits `system_composition.png` natively via
`framed_image` on slide 14, and resolves its project root from `__file__` when the
Windows path is absent (so it builds from either checkout). Rebuilds are now
idempotent — the diagram survives regeneration.

## Follow-up verification — 2026-10-12 (this run)

Full rebuild + re-run of `verify_cdr_deck.py` after a content correction to
the thermal-detection slide. ALL CHECKS PASS on the rebuilt deck (identical
check list above; slide-14 diagram md5 unchanged `4067545fb80e…`).

### Content correction applied (build_cdr.py, not the model)

Found + fixed a stale-lens inconsistency between the deck and the authoritative
model: `build_cdr.py` hard-coded the camera as **13 mm** with 13 mm-nadir GSD /
pixels-on-target, while `candidates.sysml` has used the **18 mm lens (HFOV
24.1°)** since the R3_CAM_FOV restatement and `model.sysml` models the as-built
**45° mount tilt** (OffNadirGsd, `mountTilt_deg=45`, since 2026-08-12).

- Slide 26 hardware card: `13 mm` → **18 mm** (matches the ordered T13).
- Slide 30 (Analysis 2): GSD stats corrected to 18 mm nadir values
  **6.0 cm @ 90 m / 8.0 cm @ 120 m** (was 8.3/11.1 at 13 mm); pixels-on-target
  table recomputed to the **along-range axis at the 45° mount** (×2.0 GSD):
  0.5 m @ 90 m = **4.2 px Recognize ✓** (thin), 0.5 m @ 120 m = 3.1 px Detect ✓,
  Deer @ 120 m (R3.1) = 3.1 px Detect ✓, Deer @ 90 m = 4.2 px detect/recog.,
  Human @ 90 m = 4.2 px Detect ✓, Turkey @ 120 m = 1.9 px Marginal. These match
  `model.sysml` `ThermalRecognitionCheck` (4.17 px) / `ThermalDetectionCheck`
  (3.13 px) exactly.
- Method-fidelity text now states the along-range condition; interpretation box
  now frames recognition as the tightest margin (field capture = task 2.17).

Verdicts are unchanged (R3.1 ✓ comfortable; R3.2 ✓ thin) — the old figures
overstated the margins; the corrected ones are the honest as-built numbers.
This is the deck-side counterpart of the model correction already made under
TASKS.md 0.15 (2026-08-12); the deck had not picked it up until now.

## Rebuild result

A full regeneration from current sources was run and verified. Slide 14 keeps the
diagram, and the rebuild also picked up legitimate model updates that the deck was
missing (the Sep 15 file was only the diagram patch on top of an older build):

- Slide 10/12: adds `R3_BHV_SBC_FAILSAFE` (SBC-failure fallback requirement, added
  to the model 2026-08-27).
- Slide 11: `R3_CAM_COST` restated 600 → 720 USD (post-T13-selection allocation
  restatement, David 2026-08-12).
- Slide 40 (open items): FC-firmware row now RESOLVED, AF5 row now RETIRED —
  matches `MODEL_ISSUES.md` §B7/B4.

All other 35 slides are text-identical to the pre-rebuild deck.

## Files touched

- `presentation/build_cdr.py` — slide 14 now native diagram; portable PROJ root;
  **2026-10-12: slides 26/30 corrected to 18 mm lens + along-range (45°) px**.
- `presentation/verify_cdr_deck.py` — new automated verifier (re-runnable).
- `presentation/cdr_briefing_prep.md` — **2026-10-12: reconciled to the 41-slide
  physical numbering; cost/open-items/failsafe content updated**.
- `CDR_Thermal_Surveillance_Drone.pptx` — regenerated deck (verified; rebuilt
  again 2026-10-12 after the lens correction).
- `CDR_Thermal_Surveillance_Drone.pptx.pre-rebuild.bak` — pre-rebuild copy
  (identical slide-14 state to the Sep 15 deck; kept for diffing).

## Remaining (David)

- Present the CDR briefing to Lisa and obtain design sign-off. Deck is verified
  current and consistent; the slide-14 risk item is closed and the 2026-10-12
  lens/GSD correction is applied. See `presentation/cdr_briefing_prep.md`
  (reconciled to physical slide numbers 1–41) for the up-to-date talking points
  and the five decisions to put to Lisa.
- Per prep checklist: confirm meeting logistics (duration, audience tailoring) and
  re-confirm the $2,500 cost slide figure at briefing time if prices drift (deck
  Analysis 5 shows ≈ $1,848 committed / 26 % margin; `analysis/flight_time_model.py`
  sweep total ≈ $1,674 uses cost-representative parts — the BOM figure is the R4
  basis).