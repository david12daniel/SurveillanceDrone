# T13 Mass — Vendor Reply Application Procedure (task 2.1 / MC #39)

**Date:** 2026-10-20
**Status:** Inquiry SENT 2026-10-19 → awaiting vendor reply (justin.lu@purpleriver.cn)
**Purpose:** Make applying the vendor's exact assembled mass a mechanical, <10-minute job.

## Context

- The vendor inquiry email was sent 2026-10-19 per David's instruction ("send the drafted
  inquiry to justin.lu@purpleriver.cn for the exact figure"). Subject: "PurpleRiver Mini 640
  18mm — assembled mass inquiry" (id 1a1551328fc097e5). Draft: `t13-vendor-inquiry-complete.md`.
- Current model value: `candidates.sysml` `T13.mass = 15.0 [g]` (12–17 g estimate, midpoint;
  set 2026-08-20, re-affirmed 2026-10-14 and 2026-10-19).
- The new CG tooling (`analysis/t13_mass_cg.py`) was added 2026-10-20 so the reply can be
  applied with a one-command verdict + paste-ready edit. It reads the LIVE T13.mass from
  candidates.sysml via the same loader `flight_time_model.py` uses, so it can never go stale.

## When the vendor reply arrives — do exactly this

1. **Run the calculator with the vendor's number:**
   ```
   python3 analysis/t13_mass_cg.py --new-mass-g <VENDOR_NUMBER>
   ```
   It prints: ΔCG over the 150–250 mm nose-arm range (and the ~1.9 kg conservative AUW),
   a verdict against the ±10 mm tolerance class, a paste-ready candidates.sysml edit, and
   the T13 additive CG contribution for task 2.11.

2. **Apply the edit to candidates.sysml** (paste the block the tool prints, ~line 1145,
   T13 part): update `mass = <vendor> [g]` and the comment with the VENDOR-CONFIRMED date +
   source. Keep the derivation history lines (they document the estimate chain).

3. **Regenerate the committed export** so the fallback loader stays fresh
   (the live parse takes priority, but keep the export honest — same command the sweep docs use):
   ```
   sysmlv2mde candidates.sysml --view structured-export > candidates.export.json
   ```
   (Also regenerates nothing else — `flight_time_model.py` parses candidates.sysml live.)

4. **Check the verdict.** Expected outcome: any plausible vendor number (10–25 g) is
   NEGLIGIBLE sub-millimetre (see sensitivity table below) — no flight-time sweep rerun
   needed, no CG re-check beyond TASKS 2.11 at build time. If the tool ever says
   SIGNIFICANT (only possible with a wildly unexpected mass), STOP and do a full mass/CG
   audit before touching the model.

5. **Update TASKS.md row 2.1** and append an `[agent YYYY-MM-DD]` note to MC #39:
   vendor confirmed mass, new model value, CG verdict, artifacts. Then the task is done —
   mark completed_by="Thermal Surveillance Drone" / Done Unverified.

6. **Feed the number forward:** task 2.2 (order T13, #40) can now use the exact mass at
   checkout, and task 2.11 (#49) has the real nose-payload term for the as-built CG re-check.

## Sensitivity table (pre-computed 2026-10-20, AUW 1743 g *or* 1900 g conservative)

| New mass [g] | Δ vs 15.0 g | ΔCG @ arm 150–250 mm | Verdict |
|---|---|---|---|
| 10.0 | −5.0 | −0.43…−0.72 mm | NEGLIGIBLE |
| 12.0 | −3.0 | −0.26…−0.43 mm | NEGLIGIBLE |
| 15.0 | 0.0 | 0.00 mm | NEGLIGIBLE |
| 17.0 | +2.0 | +0.17…+0.29 mm | NEGLIGIBLE |
| 18.5 | +3.5 | +0.30…+0.50 mm | NEGLIGIBLE |
| 20.0 | +5.0 | +0.43…+0.72 mm | NEGLIGIBLE |
| 22.0 | +7.0 | +0.60…+1.00 mm | ACCEPTABLE (flag 2.11) |
| 25.0 | +10.0 | +0.86…+1.43 mm | ACCEPTABLE (flag 2.11) |

**So:** every physically plausible vendor answer lands NEGLIGIBLE. The estimate was already
fit for purpose; the vendor number is precision on a non-load-bearing dimension.

## If the vendor does NOT reply

- The inquiry is out; reply latency is days. David's alternates (from the 10-19 closure memo)
  still stand: close #39 at 15.0 g, or chase by WhatsApp +86 130 1605 4201. Nothing is blocked
  on this value — order #40 is gated on the CDR briefing (#85), not on this mass.

## Artifacts

- `analysis/t13_mass_cg.py` — CG calculator (self-test reproduces the documented 0.5–0.8 mm anchor exactly)
- This procedure (`t13-mass-vendor-reply-procedure.md`)
- `t13-vendor-inquiry-complete.md` — the sent inquiry draft (kept for reference)
- `research-findings-oct-2026.md`, `t13-mass-closure-recommendation-2026-10-19.md` — research trail