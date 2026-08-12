# UC-11: Operator Override Authority — Decision Analysis

**Date:** 2026-08-06
**Status:** RESOLVED

## Questions

1. **Can the operator veto/abort an autonomous investigation?** → Yes
2. **Is the override a QGC mode switch or a dedicated app input?** → QGC mode switch (no dedicated app input)

## Rationale

### Why QGC mode switch, not a dedicated app input?

| Criterion | QGC mode switch | Dedicated app input |
|-----------|----------------|-------------------|
| Fail-safe | QGC maintains mode even if SBC/App crashes | Lost if app crashes |
| Operator familiarity | Standard ArduPilot behavior | New UI to learn |
| Latency | Immediate (FC-level switch) | App → MAVLink → FC |
| Implementation cost | Zero new UI | New app endpoint + MAVLink message |
| Audit trail | Mode change logged by FC | App-level log only |

The QGC mode switch is strictly superior: it works even if the SBC mission app has crashed, the operator already knows how to use it, and it adds zero implementation cost.

### When can the operator override?

The override is meaningful when the mission app is in the **INVESTIGATE** state (orbiting/classifying a detection). The operator switches to a non-expected mode (e.g. GUIDED, LAND, RTL, ALT_HOLD, LOITER, STABILIZE) to abort the investigation.

### What happens after override?

| Operator action | Desired behavior |
|----------------|-----------------|
| Switch to non-AUTO mode during INVESTIGATE | Abort investigation, log "OPERATOR_OVERRIDE" alert, mode change handled by FC |
| Switch back to AUTO | If override was during INVESTIGATE, re-enter SWEEP (not INVESTIGATE — don't auto-restart classification) |
| Switch to non-AUTO during SWEEP/CRUISE | Normal ArduPilot behavior — no special handling needed |

## Implementation Requirements

### R-UC11-1: Expand override detection in INVESTIGATE state

The mission app currently detects mode changes in INVESTIGATE by checking for a transition to `mode_id == AUTO`. This is wrong — it should detect transitions to ANY mode that is not the expected INVESTIGATE mode (GUIDED).

**Change:** Replace `investigate` state's mode check from "if not AUTO" to "if mode_id not in {AUTO, GUIDED}" — but actually, since the app sets GUIDED for the loiter, the check should fire when mode_id is ANYTHING other than the expected GUIDED (or the set of expected modes for investigation).

More precisely: the app puts the FC in GUIDED and sends DO_SET_CUR_LANDING_ORBIT. If the operator switches to any other mode (RTL, LAND, STABILIZE, etc.), that's an override. If the operator switches to AUTO, that's also an override — it means "stop investigating, resume the mission."

**Implementation:** In `mission_app.py` `_handle_investigate_state`, expand the mode transition check from `if mode == AUTO` to `if mode != GUIDED_OR_LOITER` (i.e., any mode other than what the app set).

### R-UC11-2: Enable PASSIVE → SWEEP re-entry on AUTO after override

When the operator switches back to AUTO after overriding during INVESTIGATE, the app should re-enter SWEEP state (not INVESTIGATE). This prevents the app from automatically re-engaging classification on the same target.

**Implementation:** In `_handle_investigate_state`, when `mode == AUTO` and an override was detected, transition to SWEEP (or PASSIVE), not STRAFE. This requires a flag to distinguish "operator switched to AUTO" from "the app naturally finished the investigation."

### R-UC11-3: Alert on override

When an override is detected, emit a `STATUSTEXT` alert: `"[MISSION] OPERATOR_OVERRIDE — returning to SWEEP"`.

### R-UC11-4: Model update

Update `model.sysml` to reflect:
- UC-11 use case definition with operator override as a concrete scenario
- `FlightMode` transition from INVESTIGATE to any non-expected mode as an override
- State machine guard condition: `[overrideDetected] INVESTIGATE → SWEEP`

## SysML v2 Use Case Definition (Draft)

```
package UC_11_OperatorOverride {
    use case "Operator overrides autonomous investigation" {
        subject "Mission App";
        actor "Operator";
        
        scenario "Operator overrides investigation" {
            "Mission App" performs "Investigate target";
            "Operator" performs "Switch to non-investigation mode";
            "Mission App" performs "Abort investigation";
            "Mission App" performs "Log override alert";
            "Mission App" performs "Transition to SWEEP";
        }
    }
}
```

## CONOPS Table

| Phase | Operator action | App state | FC mode | Expected behavior |
|-------|----------------|-----------|---------|-------------------|
| Normal sweep | Monitoring | SWEEP | AUTO | No change |
| Detection reported | Observing | STRAFE | AUTO | Continue to INVESTIGATE |
| Investigating target | Decides to abort | INVESTIGATE | GUIDED + orbit | Override expected |
| Abort | Switches to RTL | INVESTIGATE → SWEEP | RTL | App logs override, transitions to SWEEP |
| Post-abort | Monitor | SWEEP | AUTO | Normal sweep resumes |
| Return to autonomous | Switches to AUTO | SWEEP | AUTO | Normal — SWEEP is the expected AUTO state |

## Key Decision Matrix

| Decision | Chosen | Alternative | Why |
|----------|--------|-------------|-----|
| Mechanism | QGC mode switch | Dedicated app button | Fail-safe, zero cost, operator familiar |
| Post-override state | SWEEP (not INVESTIGATE) | Re-enter INVESTIGATE on AUTO | Prevents re-classifying same target |
| Override detection | Any non-expected mode | Specific mode list | More robust — any mode change during investigation is an override |
| Alert severity | STATUSTEXT INFO | STATUSTEXT CRITICAL | Operator action, not system failure |

## Downstream Impacts

- **D2.13 (SITL suite):** Should add test cases for UC-11 — switch to RTL during INVESTIGATE, verify override is detected, verify SWEEP re-entry on AUTO.
- **mission_app.py:** `_handle_investigate_state` needs the mode-check expansion.
- **model.sysml:** UC-11 use case def + FlightMode transition.
