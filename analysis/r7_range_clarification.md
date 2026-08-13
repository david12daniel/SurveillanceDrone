# R7 Range Clarification — "2800 m Linear Distance"

**Task:** 0.14 — Clarify R7's "2800 m linear distance"
**Date:** 2026-08-13
**Author:** Thermal Surveillance Drone (nightly)

---

## The Ambiguity

R7 as currently written in `model.sysml` (line 95–98):

```
requirement R7 {
  doc /* Minimum linear distance during surveillance: 2800 meters when performing
        surveillance at 2.2 m/s in sustained wind conditions of 4.5 m/s. */
  @PhaseTag { phase = phase::Phase2; }
}
```

The phrase **"linear distance during surveillance"** is ambiguous — it could mean
any of three distinct things:

| # | Interpretation | Reads as | Consequence |
|---|---|---|---|
| 1 | **Swept track length** — the total length of the survey grid flown in one sortie | A *path* length: the drone flies 2800 m of route | Operating radius ~500–1000 m; return energy cost far less than budgeted; loose with R4_GCS_RANGE |
| 2 | **Operating radius / slant range** — the drone operates up to 2800 m from the GCS | A *radial* distance: the drone is 2800 m from home at its farthest point | Return energy cost ~555 mAh (bare) at 12 m/s; consistent with R4_GCS_RANGE and the low-battery reserve analysis |
| 3 | **Out-and-back transit** — the drone flies 1400 m out, surveys, and 1400 m back for 2800 m total path | A *round-trip* path length, the farthest point is 1400 m away | Operating radius only 1400 m, inconsistent with R4_GCS_RANGE's 2800 m slant range |

---

## Downstream Impact Analysis

### Clue 1: R4_GCS_RANGE subsets R7

In `model.sysml`:

```
requirement R4_GCS_RANGE {
  doc /* The GCS control link and video receiver shall maintain a reliable
        connection with the drone at a slant range of at least 2800 meters
        under clear line-of-sight conditions. */
  subsets R7;
}
```

`subsets` in SysML v2 creates a refinement/subtype relationship. **R4_GCS_RANGE is
a more specific version of R7.** This forces R7 to be the parent concept covering
operating range, not track length. If R7 meant "swept track" it would be the wrong
parent for a slant-range requirement.

### Clue 2: Low-battery reserve analysis

`analysis/low_battery_reserve_analysis.md` treats 2800 m as the **worst-case return
distance** — the drone is at the far end of the survey line when the battery alarm
fires, and must fly 2800 m back at RTL_SPEED = 12 m/s. This produces the 555 mAh
bare-RTL energy cost and the final 700 mAh BATT_LOW_MAH value (with 30% margin).

If 2800 m were a track length (interpretation 1), the worst-case return would be
much shorter (roughly 500–1000 m depending on the survey shape), and the 700 mAh
reserve would be unnecessarily large — the reserve is being sized for a scenario
that the wording of R7 doesn't make clear.

### Clue 3: R2 and R7 wind wording

R2 requires cruise speed of 2.23 m/s "correcting for sustained wind up to 4.5 m/s".
R7 restates the same wind condition. The wind matters for *endurance*, not for
reachable radius — but the RF link budget already closes at 2800 m with margin,
and wind doesn't affect FSPL. The wind clause matters for the *surveillance* reading
(interpretation 1 or 3), which is the part that's confusing.

### Clue 4: R9 area coverage

R9's doc (model.sysml line 118) computes usable swept track as ~3210 m from R6's
30-minute endurance. This is the _sortie track_, not the per-line segment. A typical
survey grid for 30 acres at 46.1 m line spacing and 2.23 m/s gives ~3210 m of
total track, which at 2.23 m/s takes ~24 min (with 20% reserve). This number (3210 m)
is in the same ballpark as 2800 m but not identical — and importantly, the survey
track itself is a path distance, not a radial distance from GCS. This is the one
clue that leans toward interpretation 1.

---

## Recommended Resolution

**Interpretation 2 (operating radius / slant range)** is the correct reading.
Here's why:

1. **R4_GCS_RANGE** explicitly `subsets R7`, which means R7 is the parent
   requirement. A slant-range parent with a "linear distance" child makes sense;
   a swept-track parent with a slant-range child does not.
2. **The low-battery reserve** is already sized for a 2800 m return. Changing R7
   to a smaller radial distance would invalidate that value and require rework.
3. **The RF link budget** analyses compute against 2800 m as a radial distance
   (the ground antenna's free-space path loss to a point 2800 m away).
4. **The verification methods** (`analysis/verification_methods.csv`) for R7 say
   "Surveillance maintained out to >= 2800 m linear distance at 2.2 m/s" — the
   same wording as the RF link budget dimension.

However, the overlap with R9's 3210 m swept track is the source of the genuine
confusion. The fix is to **reword R7** to use unambiguous language.

### Proposed rewording

Replace the current R7 doc block with:

```
requirement R7 {
  doc /* Maximum operating range: the drone shall maintain control-link and
        video-link connectivity, and shall be capable of recovering under its
        own power, from a straight-line distance of at least 2800 meters from
        the GCS launch point. At this range the drone shall be able to perform
        surveillance at 2.2 m/s ground speed in sustained wind of 4.5 m/s.
        (The range drives the GCS link budget (R4_GCS_RANGE), the return-energy
        reserve (R6_BHV_RTL_RESERVE), and the link-loss failsafe design
        (R7_BHV_LINKLOSS_RTL). The sortie track length derived from R6 endurance
        is governed by R9.) */
  @PhaseTag { phase = phase::Phase2; }
}
```

### Key changes
- Replaces "linear distance during surveillance" with "maximum operating range"
- Explicitly says "straight-line distance from the GCS launch point"
- Preserves the surveillance + wind clause (it's still part of the requirement)
- Adds a doc note explaining what the range drives and where the sortie track
  length lives (R9), so future readers don't re-encounter the same confusion

---

## What This Changes

| Artifact | Impact |
|---|---|
| `model.sysml` R7 doc | **UPDATED** — doc block reworded to the proposed text (2026-08-13, David approved by email) |
| `R4_GCS_RANGE` | No change needed (already subsets R7 + says "slant range") |
| `R6_BHV_RTL_RESERVE` | No change needed (already uses 2800 m return) |
| `R7_BHV_LINKLOSS_RTL` | No change needed (already subsets R7) |
| `R7_FS_LINK` | No change needed |
| `REQUIREMENTS_EXPORT_26_06_30.md` | Would need re-export to pick up new R7 wording |
| `analysis/rf_link_budget.md` | No change needed (already uses 2800 m as slant range) |
| `analysis/low_battery_reserve_analysis.md` | No change needed |
| `analysis/verification_methods.csv` | R7 row already aligned — no change needed |

The ambiguity is **only in the prose of R7 itself** — all downstream artifacts
already agree on interpretation 2. This means the resolution is low-risk: just
a documentation fix to make R7 say what every other artifact already assumes.

---

## Recommendation

The safest path is to:

1. **Model approval** obtained via email reply 2026-08-13.
2. **model.sysml** R7 doc block updated to the proposed wording.
3. **REQUIREMENTS_EXPORT_26_06_30.md** R7 row updated to match.
4. **analysis/requirements_traceability.csv** and **analysis/verification_methods.csv**
   R7 rows updated for consistency.
5. **TASKS.md** task 0.14 marked ☑ complete.
6. **Committed and pushed** to master.
7. **Task 0.14 closed** as resolved.

The actual engineering (link budget, battery reserve, failsafe params) is
unaffected — every downstream artifact already interpreted 2800 m as maximum
operating range / slant range, consistent with R4_GCS_RANGE.
