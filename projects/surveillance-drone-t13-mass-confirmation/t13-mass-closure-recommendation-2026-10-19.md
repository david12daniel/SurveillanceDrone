# T13 Mass — Closure Recommendation (Task 2.1 / Mission Control #39)

**Date:** 2026-10-19
**Prepared by:** Thermal Surveillance Drone agent (nightly sweep)
**Decision requested from David:** Close task 2.1 at the 15.0 g estimate — or send the vendor inquiry first.

## Recommendation

**CLOSE the task at the 15.0 g estimate. Do not send the vendor inquiry.** The ±3 g
uncertainty has no build, CG, or ordering impact; the inquiry is 13 weeks stale and the
estimate is already fit for purpose. Details below.

## Tonight's re-verification (2026-10-19) — nothing changed in 5 days

| Check | Result |
|---|---|
| Vendor download page (thermal-image.com) | Page touched 2026-10-07, but the actual PDF is **byte-identical** to the 2026-08-24 revision we hold (md5 `9b78295dc07959dd503b0113bae472b4`, 114,264 bytes, 2 pages) |
| On-site spec PDF (re-downloaded via wpdmdl=1293) | Mass section still **<20 g (without lenses and flanges)**; no per-lens or assembled weight added |
| Product page (Mini 640 module) | Weight still **<20 g (without lens)**, 21×21 mm; 18 mm lens confirmed in the model table (Mini640-18, FOV 24.2°×19.5°) |
| Made-in-China 18 mm listing | Still **6 g (without lens)**, non-radiometric 50 Hz — no assembled figure |
| Web sweep (2 queries, fresh) | No new reseller/listing publishes an assembled 18 mm weight |

**Verdict: the 12–17 g estimate (midpoint 15.0 g) stands, re-affirmed for the third time
(Aug 20 → Oct 14 → Oct 19).**

## Why closing is the right call

1. **Every public source has been checked — repeatedly.** Over 8 weeks: official spec sheet
   (2 revisions), product page, made-in-china, Alibaba, cross-vendor (InfiRay-class core
   "<10 g" bracket). No source publishes a per-lens or assembled figure. Waiting longer will
   not surface new data; only the vendor can produce the exact number.
2. **The estimate is a bounded range with a documented derivation**, not a guess:
   bare module 6 g (published) + 18 mm Ge F#1.0 2-element lens assembly 6–9 g (density-based
   estimate) = 12–17 g.
3. **CG impact is negligible — quantified, not hand-waved.** Δ6 g at a 150–250 mm nose arm
   over ~1.9 kg AUW ≈ **0.5–0.8 mm** CG shift. The 405 mm-wheelbase quad's CG tolerance is
   an order of magnitude larger (±10–20 mm class). Even the ±3 g residual uncertainty moves
   CG <0.4 mm.
4. **The inquiry has no downstream urgency.** Task 2.2 (order T13) is gated on the CDR
   briefing (#85 → Lisa sign-off) anyway, which is the actual critical path. When the order
   happens, the checkout flags matter more than ±3 g: **radiometric 25 Hz + 18 mm + USB**
   (per the 2026-08-24 spec note that radiometric only ships with 9/13/18 mm lenses).
5. **Friction cost:** the inquiry (justin.lu@purpleriver.cn) is still ready to send and takes
   2 minutes if David ever wants the exact number — but it is nice-to-have, not build-blocking,
   and vendor reply latency is days.

## Decision table

| Option | Effort | Value | Verdict |
|---|---|---|---|
| Close at 15.0 g | 0 (this memo) | Unblocks task 2.1; order can proceed at 15.0 g | **Recommended** |
| Send inquiry, wait for reply | 2 min + days | Exact number, ±0 g | Optional; adds no build value |
| Hold the task open | 0 | Keeps a stale open item on the board | Not useful |

## What happens next (if David approves the close)

1. Task 2.1 (#39) → Done (David/Claude verification).
2. `candidates.sysml` keeps `T13.mass = 15.0 [g]` — **no change needed**; comment already
   documents the estimate's source chain.
3. Order task 2.2 (#40) proceeds at 15.0 g with the three checkout flags
   (**radiometric 25 Hz + 18 mm + USB**).
4. When the unit arrives: weigh it, update `candidates.sysml` with the real number, and
   re-check CG as part of task 2.11 (#49) — that is the natural place to close the loop.

## Artifacts

- This memo (`t13-mass-closure-recommendation-2026-10-19.md`)
- `research-findings-oct-2026.md` (prior sweep, confirmatory)
- `t13-vendor-inquiry-complete.md` (inquiry package, kept for the optional path)
- `Purpleriver-Mini640-Spec-Sheet-2026-08-24.pdf` (current spec, re-verified byte-identical)