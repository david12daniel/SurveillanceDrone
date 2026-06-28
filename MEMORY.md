## Surveillance Drone Model Location

**File:** `model.sysml` (renamed from `model.md` on 2026-06-25 so the Syside VS Code extension activates natively on the `.sysml` extension; still raw SysML v2 textual notation).

**Locations (same repo, two checkouts):**
- **Linux (OpenClaw agent):** `/home/david12daniel/.openclaw/agents/thermal-surveillance-drone/model.sysml`
- **Windows:** `c:\Users\Josiah Laperriere\Documents\Coding\SurveillanceDrone\SurveillanceDrone\model.sysml`

This project is worked on from both locations. **Git is the single source of truth** — sync via git, not by copying files. Only one user (David) works on the file at a time, so there is no concern about concurrent-edit conflicts; just pull before starting and push when done.

**Policy Statement:**  
The Surveillance Drone SysML V2 model (`model.sysml`) is a critical engineering artifact that **cannot be modified, updated, moved, or removed** without **explicit prior approval** from the user (David Daniel).

**Rationale:**  
- Ensures traceability and integrity of systems engineering decisions.  
- Prevents accidental loss of architectural context.  
- Maintains compliance with Agile MBSE principles (git as source of truth).  

**Enforcement:**  
- Any attempt to alter `model.sysml` must be preceded by a formal request to the user.  
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

- [[airframe-research]]

**Source:** External CSV upload 2026-05-16

## GitHub Credential Cache

- **Location:** `.git/git-creds` inside the repo (stored via `git config credential.helper 'store --file .git/git-creds'`)
- **Token type:** Classic PAT with `repo` scope
- **Reference:** See `TOOLS.md` for re-issuance instructions
- **Important:** DO NOT commit `.git/git-creds` to the repo. It's in `.gitignore` implicitly via `.git/`.