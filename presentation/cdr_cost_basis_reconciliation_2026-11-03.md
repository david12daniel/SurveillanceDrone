# CDR Cost-Basis & Endurance Reconciliation — 2026-11-03

**Task:** [0.1] Present CDR Briefing to Lisa (#85) — deck currency for the review.
**Trigger:** Nightly board screen found every project task blocked except #85 and #39, both at
David-only steps. Rather than a sixth no-op deck re-verification, audited the deck's numbers
against the artifacts it *claims* to derive from (`BOM.md`, `candidates.sysml`,
`analysis/flight_time_model.py`). Two real drifts found and fixed.

---

## 1. What was wrong

The deck's cost slide (Analysis 5) disagreed with the BOM it says it rolls up from, and the
project carried **four different cost figures** across artifacts:

| Artifact | Figure | Basis |
|---|---|---|
| `CDR_Thermal_Surveillance_DRONE.pptx` (pre-11-03) | ≈ $1,848 committed / 26 % margin / $2,007 all phases | deck's own Phase-2 subtotal |
| `analysis/verification_methods.csv` + RTM (pre-11-03) | ~ $1,898 committed / 24 % margin | older rollup |
| `model.sysml` `R3_CAM_COST` doc | ~ $1,724 total | `flight_time_model.py` sweep basis (cost-representative radio/RX) |
| **`BOM.md` (source of truth, line-item rollup)** | **$2,242.23 committed all-in → $1,910.23 on the R4 basis** | phased BOM |

### Root cause (arithmetic)

BOM Phase 2 = $871.48. Deck Phase 2 = $809. **Δ = $62.48**, explained exactly by two deck errors:

- camera priced at **$650** in the deck vs **$700** in `candidates.sysml`
  (`T13 :>> cost_USD = 700.00` — $640 base incl. the +$50 18 mm lens, **+$60 shipping**): **+$50**
- the **SBC heatsink** line (~$12.50 est., spec'd in `BOM.md` as "TBD — not yet sourced") was
  **omitted entirely** from the deck subtotal: **+$12.48**

Deck committed total was then $2,180 and, after excluding the $332 of reusable support gear
(2× `BAT22` dev packs $220 + `CHG1` charger $112), the deck's $1,848 was *internally consistent*
but built on the two wrong Phase-2 inputs.

### Second drift: endurance

Deck claimed **58.4 min hover at 1,751 g AUW**. Re-ran `analysis/flight_time_model.py`
(reproducible; output byte-stable) — the selected config **C000009** (Chimera9 ECO + GREEN V2
6S3P 12 Ah Amprius + T13 + M5) is **57.2 min hover, 58.7 cruise, 14.9 % throttle, 1,743 g AUW**.
The deck pair was self-inconsistent too (+8 g mass should not fly 1.2 min *longer*), i.e. it was
built from an older model export. Corrected to the live model rather than hand-tuned.

---

## 2. Reconciled numbers (authoritative from BOM.md line items)

| Line | Value |
|---|---|
| Phase 1 — flight + FPV + waypoints | $1,370.75 |
| Phase 2 — thermal + SBC | ~$871.48 |
| Phase 3 — software only | $0.00 |
| **Committed, all-in (Phases 1–3)** | **~$2,242.23** |
| less reusable support gear (2× BAT22 $220 + CHG1 $112) | −$332.00 |
| **Committed, R4 basis** | **≈ $1,910** |
| Margin under R4 cap ($2,500) | **$590 ≈ 24 %** |
| All four phases, R4 basis | ≈ $2,069 (17 % margin) |
| Largest single line | T13 thermal camera, $700 |

Verification arithmetic: 2,242.23 − 332.00 = 1,910.23 · 2,500 − 1,910.23 = 589.77 (23.6 %) ·
2,401.22 − 332.00 = 2,069.22 · (2,500 − 2,069.22)/2,500 = 17.2 %.

**Verdict unchanged: R4 PASS.** Headroom drops from a stated 26 % to a true 24 %, still $590 under
the cap. Nothing about the procurement decision changes — only the honesty of the number.

---

## 3. Changes made

`presentation/build_cdr.py` (deck regenerated, 41 slides):
- slide 25: $1,850 → $1,910 committed · 58 min → 57 min hover
- slide 28 (Analysis 1): "58.4 min … 1,751 g" → "57.2 min … 16.9 W payload, 1,743 g"; stat tile 58.4 → 57.2
- slide 29 (trade space): "≈ $1,910 / 57 min"
- slide 33 (Analysis 5 cost): Phase 2 $809 → $871 · committed $2,180 → $2,242 · R4 $1,848 → $1,910 ·
  margin 26 % → 24 % · all-phases $2,007 → $2,069 · camera $650 → $700 · sweep-basis footnote
  $1,674 → $1,662 (C000009) with the heatsink explanation
- slide 35 (SV-7): R4 row $1,848/+$652(26 %) → $1,910/+$590(24 %); R6 margin +95 % → +91 %;
  R8 −3 % → −5 %
- slide 41 (exit criteria): "R4 cost ✓ (26 % margin)" → 24 %
- speaker notes (slides 25/28): "58 minutes / eighteen-hundred-fifty dollars" → "fifty-seven
  minutes / nineteen-hundred-ten dollars"
- PV-2 timeline: Phase 2 ≈ $809 → ≈ $871

Docs aligned: `presentation/cdr_executive_summary.md` (budget table + decision 2),
`presentation/cdr_briefing_prep.md` (§0 checklist, key callouts, slide 25/28/29/33/41 talking
points, decision 2, risk #5), `presentation/cdr_deck_verification.md` (briefing-time re-confirm note).

`analysis/verification_methods.csv` (hand-authored VCRM side-car — the documented "one file to
hand-edit") then regenerated into the RTM:
- `R4` evidence: "~1898 USD — 24 percent margin" → "~1910 USD on the R4 basis (~2242 USD all-in,
  less 332 USD of reusable dev packs + charger) — 24 percent margin"
- `R3_CAM_COST` evidence: "~1724 USD total system" → R4-basis $1,910 plus a note that ~$1,662 is the
  flight-time-sweep basis (cost-representative radio/RX)
- Regeneration also picked up **two stale doc rows** that had never been refreshed from the model:
  `R3_BHV_SBC_FAILSAFE` (now carries the confirmed FS_GCS_ENABLE / FS_GCS_TIMEOUT=5 /
  MAV_GCS_SYSID parameter set) and `R7` (the parenthetical naming the range's downstream
  dependencies). Both are model-current text; no model edit was made.

**Verification:** `python3 presentation/verify_cdr_deck.py` → **ALL CHECKS PASS** (41 slides,
slide-14 diagram md5 `4067545fb80e` unchanged, 36/36 date stamps consistent, RTM 57 rows / 0 blank
verification cells, 0 dangling rels). Only known WARNING: deck stamped 2026-07-26 (100 days) —
David sets `CDR_DATE`, deliberately not changed here. Automated stale-figure sweep over the rebuilt
pptx for `1,848 / 1,850 / 2,007 / 2,180 / $650 / 26 %` → **0 hits**.

---

## 4. If Lisa asks why the cost moved

> "Checking the deck against the bill of materials, I found the deck's Phase-2 line used the camera
> price before shipping and had dropped the SBC heatsink. Corrected: committed system is $1,910 on
> the R4 basis, not $1,848 — margin is 24 %, $590 under the $2,500 cap instead of 26 %. Verdict is
> unchanged: we're under budget with room for price drift, and the thermal camera at $700 is still
> the single largest line."

Same answer for endurance: *"57.2 min hover, not 58.4 — I rebuilt it against the current model; the
old figure came from an earlier export. Still ~91 % over the 30-minute requirement; the 60-minute
stretch is 5 % short and stays documented as not met."*

---

## 5. Left open (deliberately)

1. **`CDR_DATE` is still 2026-07-26** (100 days stale). Only David knows the real review date:
   `CDR_DATE=YYYY-MM-DD python3 presentation/build_cdr.py && python3 presentation/verify_cdr_deck.py`.
2. **`model.sysml` `R3_CAM_COST` doc still cites "~$1,724 total system"** for the sweep basis, and
   the `R10` doc's "58.4 min cruise" reference is now 58.7 min in the live sweep. Left
   untouched — model-doc edits belong with the sweep refresh in task 2.10 (which re-runs the
   endurance/cost sweep after measured dims land), not with a briefing-prep pass.
3. **`analysis/requirements_traceability.py` writes CRLF** while the tracked CSV is LF. Regenerating
   churns all 58 lines; tonight's file was normalized back to LF (2 substantive + 2 stale-row diffs,
   committed intentionally). One-line fix (`lineterminator="\n"` at the two writers) for a future
   tooling pass.
4. **Sweep-basis vs BOM-basis cost** remain two legitimate, differently-defined numbers ($1,662 vs
   $1,910). The deck footnote now states the difference; do not let them get averaged or quoted
   interchangeably at the review.
