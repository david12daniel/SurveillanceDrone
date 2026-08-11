# Operator Override Authority (UC-11) — Decision Analysis

**Date:** 2026-08-06
**Author:** Agent (nightly)
**Status:** Analysis complete — recommendation ready for review

## Problem

UC-11 is flagged open in `model.sysml` (lines 1666, 1832) and `software_gap_analysis.md`
(open question #5). The operator needs a way to abort/override an autonomous
investigation while airborne, but no mechanism has been defined. Two questions:

1. **Can** the operator veto or abort an autonomous investigation mid-flight?
2. **How** — is the override a QGC mode switch, or an app-specific input?

The model doc for `DetectInvestigateClassify` already lists *operator override*
alongside route-complete and failsafe as a loop-exit condition (model.sysml:1622),
but the behavior is not modeled and the mission app has no override path.

## Current state of the mission app (mission_app.py)

| State | Expected FC mode | Override detection |
|---|---|---|
| SWEEP | AUTO (3) | Self-correct: `if fc_mode != AUTO: return` — stands down passively per tick |
| INVESTIGATE | GUIDED (4) | **None.** No fc_mode check — app will force AUTO on classify/timeout, overriding the operator |
| PASSIVE | Any | App stops sending commands and `run()` exits — no re-entry path |

The only external-actor detection today is the `_FAILSAFE_MODES = {RTL, LAND}`
check in `step()`, which deals with FC-originated failsafes, not operator
intervention. If the operator switches to LOITER (5) or STABILIZE (0) during an
INVESTIGATE, the app has no awareness and will hammer `set_mode(AUTO)` — fighting
the operator for control.

## Decision

### 1. Yes, the operator can override.

### 2. Mechanism: QGC mode switch (not a dedicated app input).

**Why QGC mode switch:**

| Criterion | QGC mode switch | Dedicated app input |
|---|---|---|
| **Infra cost** | Zero — QGC already has mode-select buttons | Must build an app command listener (MAVLink `COMMAND_LONG` or secondary serial/network channel) |
| **Latency** | Instant — FC mode change is immediate | Depends on polling rate of whatever channel carries it |
| **Robustness** | Survives SBC failure — operator still controls the FC | Dies with the SBC |
| **Operator cognitive load** | Same paradigm as arming, failsafe recovery, and manual flight | Novel interaction — another button to learn |
| **CONOPS fit** | Single operator in the field with QGC + radio — natural to use the same interface | Requires app to be reachable (SBC up, link up) |

**What the override means:** the operator switches the FC out of the expected
mode (AUTO in SWEEP, GUIDED in INVESTIGATE) via QGC. The app detects the
deviation, enters PASSIVE, and stops commanding. The operator is then free to
fly manually (STABILIZE, LOITER), RTL, or troubleshoot. When ready to resume
autonomous operation, the operator switches back to AUTO — the app detects this
and re-enters SWEEP.

## Recommended app behavior changes

These are the implementation requirements that flow from the decision:

### R-UC11-1: Expand override detection beyond failsafe modes

The current `_FAILSAFE_MODES` check catches FC-originated failsafe transitions
(RTL, LAND). Operator override also needs detection:

- **SWEEP state:** already correct — `if fc_mode != AUTO: return`
- **INVESTIGATE state:** add `if fc_mode != GUIDED: enter PASSIVE` (the
  operator has taken control; stop investigating)

### R-UC11-2: PASSIVE → SWEEP re-entry

Currently `run()` exits on PASSIVE. Change to **keep the event loop running**
in PASSIVE and re-enter SWEEP when the operator switches back to AUTO:

```
while True:
    step()
    if state == PASSIVE:
        continue  # loop still runs, listens for fc_mode changes
```

And in `step()`:
```python
if state == PASSIVE:
    if fc_mode == MODE["AUTO"]:
        state = SWEEP   # operator handed control back
        alert("AUTO re-engaged — resuming autonomous surveillance")
    return
```

### R-UC11-3: Operator override alert

When entering PASSIVE due to operator override (not failsafe), the app should
emit `STATUSTEXT` so the operator sees confirmation on QGC:

```
"Override detected — autonomous investigation aborted, PASSIVE"
```

### R-UC11-4: State-model update

The model's `FlightMode` state machine should add an `operatorOverride` trigger
that transitions from `flying.cruise` or `flying.loiter` to a new `overridden`
state (or reuses the existing `flying` with a conditional). See §Model update
below for the concrete SysML v2 patch.

## CONOPS: how it plays out

| Operator action | FC mode | App state | App reaction |
|---|---|---|---|
| Autonomous route, no detections | AUTO | SWEEP | Detecting normally |
| App detects target → switch to GUIDED | GUIDED | INVESTIGATE | Classifying at 90 m |
| Operator sees something concerning → clicks **LOITER** in QGC | LOITER | → PASSIVE | "Override detected" alert, stops commanding |
| Operator assesses, flies manual | LOITER | PASSIVE | Silent, watching |
| Operator clicks **AUTO** to resume | AUTO | → SWEEP | "AUTO re-engaged" alert, resumes detect |
| Operator clicks **RTL** | RTL | PASSIVE | Already handled (failsafe path) |

## Relationship to other open items

- **Task 5 ([0.2])** — Failsafe params: UC-11 is orthogonal, but the operator
  override logic complements FC-originated failsafe transitions.
- **Task 70 ([D2.13])** — SITL integration suite: the override behavior should
  be tested in SITL (WIP).
- **Task 54 ([2.16])** — mavlink-router: the override path uses the same
  MAVLink link — no additional routing required.
- **MODEL_ISSUES.md §C25** — the UC-5 control loop: the override exits the loop
  on operator demand, which is exactly what the existing model doc says.

## Model update (SysML v2)

In `model.sysml`, in the UseCases package, add:

```sysml
 use case def OperatorOverrideUC {   // UC-11
  subject system : AerialObservationSystem;
  actor operator : Operator;
  objective {
   doc /* The operator may override an autonomous investigation at any time
        by switching the FC flight mode via QGC (LOITER, STABILIZE, RTL, etc.).
        The mission app detects the mode change, aborts the current investigation,
        enters PASSIVE, and stops commanding. The operator resumes autonomous
        operation by switching back to AUTO. No dedicated app input is required. */
  }
 }
```

And in the `FlightMode` state machine, add an `operatorOverride` transition
from `flying.cruise` or `flying.loiter` to `overridden` (new state) or simply
document that any mode change from a non‑expected mode constitutes an override.
The simplest model choice: note in the `DetectInvestigateClassify` doc that
operator override is realized by the existing PASSIVE-state mode-detection logic,
and update the doc from "operator override" (abstract) to "QGC mode switch override."

## Key rationale summary

| Decision | Chosen | Rejected |
|---|---|---|
| **Can the operator override?** | **Yes** | No — removes the last line of defense |
| **Override mechanism** | **QGC mode switch** | Dedicated app input (extra infra, no benefit for a single-operator system) |
| **App behavior on override** | **Enter PASSIVE, await AUTO** | Force resume (dangerous — might re-enter while operator is acting) |
| **PASSIVE re-entry** | **Yes, AUTO → SWEEP** | Exit permanently (requires reboot/power cycle to re-enable autonomy) |

## Files updated by this decision

- This document: [`analysis/operator_override_UC11.md`](operator_override_UC11.md) (new)
- [`software_gap_analysis.md`](../analysis/software_gap_analysis.md) — mark open question #5 RESOLVED
- Implementation downstream (not this task): D2.13 (SITL suite) to add override tests

---
*See also: `analysis/software_gap_analysis.md` (§Open questions #5), `model.sysml` lines 1622 & 1666 & 1832, `analysis/autonomy_sim/mission_app.py`.*
