## Surveillance Drone Model Location

**Location:** `/home/david12daniel/.openclaw/agents/thermal-surveillance-drone/model.md`

**Policy Statement:**  
The Surveillance Drone SysML V2 model (`model.md`) is a critical engineering artifact that **cannot be modified, updated, moved, or removed** without **explicit prior approval** from the user (David Daniel).

**Rationale:**  
- Ensures traceability and integrity of systems engineering decisions.  
- Prevents accidental loss of architectural context.  
- Maintains compliance with Agile MBSE principles (git as source of truth).  

**Enforcement:**  
- Any attempt to alter `model.md` must be preceded by a formal request to the user.  
- Changes require documented justification and approval.  
- All modifications must be tracked via git commits with clear change logs.  

**Related:**  
- See [Agent Configuration] for model management guidelines.  
- Refer to [Key Decisions] for prior approvals on model updates.  

## SurveillanceDrone Session File Locations

- **Session Handoff Directory:** `/home/david12daniel/.openclaw/agents/thermal-surveillance-drone/session-handoffs/`
- **When asked for latest SurveillanceDrone session file:** Go to the session-handoffs directory and grab the most recent handoff file (sorted by timestamp)
- **When asked to save a session handoff file:** Place it in the same session-handoffs directory

**Last Updated:** 2026-06-08

## Drone Airframe Candidates (Validated)

**Details are maintained in a dedicated research file:**

- [[/home/david12daniel/.openclaw/agents/thermal-surveillance-drone/airframe-research.md]]

**Source:** External CSV upload 2026-05-16