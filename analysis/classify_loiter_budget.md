# Classify loiter time-budget policy — DECISION (task 0.4)

**Date:** 2026-08-05
**Closes:** `InvestigateAndClassify.adjustOrbit` unbounded loop (model.sysml), software_gap_analysis.md §Open #1
**Feeds:** D2.9 (implement the budget), R6 endurance check, model.sysml `adjustOrbit` doc note

---

## 1. The problem

`InvestigateAndClassify` (model.sysml) has:

```
action adjustOrbit {   /* Adjust loiter orbit/aspect and retry classification;
                          bounded by the loiter time budget (retry/timeout policy TBD). */ }
  then classifyLoop;  // <- LOOP: no bound in the model
```

The loop is unbounded in the model. In the running software
(`analysis/autonomy_sim/mission_app.py`) there is a fast `classify_timeout_ticks = 40`
measured in 50 Hz ticks = **0.8 s**. That only bounds *sampling the classifier at a
fixed aspect* — it is NOT a loiter/orbit budget. `adjustOrbit` is a *physical*
reposition (yaw/offset the orbit to change the 18-mm lens aspect) that takes seconds,
and it is not bounded by the current code. Without a bound, a persistent false-positive
detection could loiter the drone indefinitely — an energy and mission-timeline hazard.

## 2. Decision — two-tier budget

Adopt a **two-tier** loiter/classify policy:

1. **Per-aspect classify sampling (already present):** keep `classify_timeout_ticks = 40`
   at 50 Hz ≈ **0.8 s** of classifier sampling per orbit aspect. This is the inner,
   fast bound — it just says "this aspect isn't yielding ≥ 0.80, move on."
2. **Loiter time budget (NEW — the outer bound on `adjustOrbit`):** **30 s** total in the
   INVESTIGATE/loiter state per investigation, then **log as unclassified and resume**
   the route (AUTO, rejoin cruise). This is the bound that closes the unbounded loop.

**Recommended value: 30 s per investigation.**

### Rationale
- **Retry capacity:** a reposition (orbit adjust + settle + a 0.8-s classify pass) is
  ~5 s. 30 s allows ~6 full `adjustOrbit` cycles — ample to change aspect yaw/offset and
  try the 18-mm 45° recognition (4.17 px @90 m) from a better geometry before giving up.
- **Endurance draw is negligible.** At P_loiter = P_hover = 232.4 W:
  - 30 s loiter = 1.94 Wh = 87 mAh = **0.92%** of the post-reserve mission energy.
  - Even a worst-case 3 investigations × 30 s = 90 s loiter = **2.75%** of mission.
  - R6 (30 min) and the 54-min post-reserve endurance are untouched.
- **Mission responsiveness:** a 30-s cap keeps a single detection from stalling the
  survey route for more than half a minute; false positives degrade gracefully instead
  of hanging the mission.
- **Consistency with the model intent:** the model's `doc` already promises a "loiter time
  budget" — this pins it to a concrete number and the "log as unclassified, resume" exit the
  gap analysis requested.

## 3. Exit behavior (the "log as unclassified, resume")

On budget exhaustion, the app shall:
- Emit `STATUSTEXT` alert `"UNCLASSIFIED <species?> timeout"` (operator sees the POI was
  investigated but not classified). *Already implemented in mission_app.py:136-137.*
- Command `AUTO` (emit `InvestigationComplete`) and return to `SWEEP`, rejoining the
  planned route. *Already implemented (mission_app.py:138-139).*
- Record the unclassified POI (lat/lon) to the log for post-mission review.

So the *only* code change needed is to derive the 30-s budget from the outer loop, not
the fixed 40-tick inner sampler. Concretely: bound the INVESTIGATE state by an
elapsed-time budget (30 s) rather than by classify-call count alone.

## 4. Energy table (for the record)

BAT10 (12 Ah Amprius), 22.2 V nominal, DoD 0.85 → 226.4 Wh usable; minus 700-mAh
BATT_LOW_MAH reserve → 210.9 Wh / 759 kJ. Hover/mission endurance ≈ 54.4 min.

| Loiter budget / inv. | Wh | mAh | % of mission (solo) | % ×3 investigations |
|---|---|---|---|---|
| 10 s | 0.65 | 29 | 0.31% | 0.93% |
| 20 s | 1.29 | 58 | 0.61% | 1.84% |
| **30 s (chosen)** | **1.94** | **87** | **0.92%** | **2.75%** |
| 60 s | 3.87 | 175 | 1.84% | 5.5% |
| 120 s | 7.75 | 349 | 3.67% | 11.0% |

30 s is the sweet spot: enough retry cycles to be useful, small enough endurance touch
that even 3 investigations per mission cost < 3%.

## 5. What this requires

- **D2.9** implements the 30-s budget (bind INVESTIGATE by wall-clock, not classify-count).
- **model.sysml** `adjustOrbit` doc: replace "retry/timeout policy TBD" with
  "bounded by a 30 s loiter time budget per investigation; on exhaustion, log as
  unclassified and resume route." *(model.sysml is protected — request David's approval.)*
- **software_gap_analysis.md** §Open #1: mark resolved with this value.