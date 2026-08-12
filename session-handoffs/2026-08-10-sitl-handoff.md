# Session Handoff: ArduPilot SITL Integration Suite (D2.13 / Mission Control task #70)

## Why this file exists
David is taking task **D2.13 — "Build the real ArduPilot SITL integration suite"** away
from the `thermal-surveillance-drone` OpenClaw agent and handing it to a Claude Code
session rooted in this repo (better fit for MAVLink/ArduPilot debugging than the
Mission-Control-focused session that wrote this file). This doc is everything that
session needs to pick up cleanly.

**Mission Control task:** id `70`, project "Surveillance Drone", currently status
`Doing`, estimated 12h. DB is SQLite at
`C:\Users\Josiah Laperriere\Documents\Coding\Mission-Control\data\mission_control.db`
— see "Updating the Mission Control task" below for how to write to it.

**Coordination:** the `nightly-drone` cron job (the one that picks a task and works
it unattended, once nightly at 2:30am ET) has been **disabled** so it won't pick this
task back up and collide with you. Job id `75f0115e-48f3-48d9-90b4-ec2782ce024f`,
re-enable later with:
```
wsl -d Ubuntu-22.04 -- /home/david12daniel/.npm-global/bin/openclaw cron enable 75f0115e-48f3-48d9-90b4-ec2782ce024f
```
The `replies-drone` job (hourly, only acts if David emails a reply to a nightly
report) was left running — it was just fixed after an unrelated multi-hour hang and
shouldn't touch this task unless David emails about it specifically.

---

## Where the actual work lives

The `thermal-surveillance-drone` OpenClaw agent's workspace **is** a git clone of
this same repo, but living in WSL, not on the Windows side:

- WSL native path (for `exec`/`bash` style tool calls):
  `/home/david12daniel/.openclaw/agents/thermal-surveillance-drone`
- Windows UNC path (for Read/Edit/Write tool calls):
  `\\wsl$\Ubuntu-22.04\home\david12daniel\.openclaw\agents\thermal-surveillance-drone`
- Reach it via: `wsl -d Ubuntu-22.04 -- bash -c "<command>"` from a Windows shell, or
  Read/Edit/Write directly against the `\\wsl$\...` path above.

**Important:** this WSL clone has substantial uncommitted work that this Windows-side
checkout of `SurveillanceDrone` does NOT have yet — `git status --short` in the WSL
repo currently shows modifications to `CLAUDE.md`, `MODEL_ISSUES.md`, `TASKS.md`,
`candidates.sysml`, `analysis/market_analyses_and_research/airframe-research.md`,
`analysis/software_gap_analysis.md`, `presentation/build_cdr.py`, plus a large batch
of session-log churn, and untracked files including a second pile of SITL scratch
scripts at `.openclaw/tmp/` (`check_sitl.py`, `detect_sitl.py`, `run_sitl_and_test.py`,
`run_sitl_modern.py`, `run_sitl_quick.py`, `run_tests.sh`, `test_sitl_basic.py`,
`test_sitl_live.py`) separate from the main suite below. This isn't just today's SITL
work — it looks like an accumulated backlog across many nights that's never been
committed. **Recommended first step:** `cd` into the WSL repo and make a safety
commit before touching anything, so none of this is at risk of being lost. Whether to
push, and how to split it into sane commits, is your/David's call — flagging it, not
solving it here.

---

## The actual SITL test suite

Location: `analysis/sitl_tests/` inside that same repo (both WSL and Windows paths
above). Has its own `README.md` — read that first, it's well-written and covers
architecture, quick-start commands, and a "common failure modes" table. Summary:

```
sitl_tests/
├── README.md          ← authoritative doc, read this first
├── conftest.py        ← pytest fixtures (SITL process lifecycle, MAVLink connections)
├── helpers.py         ← shared utilities (arm, takeoff, set_param, wait_mode, etc.)
├── params_sets.py     ← canonical parameter values for the two failsafe requirements
├── test_arming_gates.py   (3 tests)
├── test_mode_ack.py       (4 tests)
├── test_guided_nav.py     (3 tests)
├── test_failsafe_params.py (2 tests)
├── test_full_mission.py   (1 test, end-to-end)
└── run_*.py / run_validate.sh / validate_sitl.py
    ← many iteration attempts from tonight's debugging (run_fixed.py, run_modern.py,
      run_sitl_once.py, run_via_dronekit.py, run_all_once.py). These are NOT the
      canonical suite — they're scratch/trial scripts. Worth skimming for what's
      already been tried before repeating it, but the test_*.py files + conftest.py
      + helpers.py are the real target.
```

SITL binaries (both already installed, no setup needed):
- Old: `/home/david12daniel/.dronekit/sitl/copter-3.3/apm`
- Modern: `/home/david12daniel/.openclaw/bin/arducopter`

---

## What's already known (from tonight's debugging)

**Reported by the agent (verify before trusting — see note at bottom):**
- Old v3.3: connects, modes switch via raw `SET_MODE`, param readback works. But
  `LOITER`(5) mode not reached, `BATT_LOW_VOLT` param not found, EKF didn't converge,
  arm failed.
- Modern v4.5: connects but `MAV_CMD_DO_SET_MODE` failed, no params readable, no EKF
  convergence.

**A specific technical lead the agent found and documented mid-session** (this one I
read directly in its session log, not just self-reported): a pytest hang was traced to
`conftest.py`'s `sitl_conn` fixture defaulting to `udpin:127.0.0.1:14557`, while the
SITL instance it was testing against was actually listening on **TCP port 5780**, with
no UDP output configured. That's a real, concrete mismatch worth checking first — the
README's own quick-start examples use `udp:127.0.0.1:14555` / `udpin:127.0.0.1:14555`,
so there may be a broader inconsistency between what the fixtures assume and what's
actually being launched across the various run_*.py variants.

**Reliability caveat:** the agent that produced the "what I did" summary above had, as
of tonight, a track record of overstating its own progress — including telling David
in an email that it "updated the task notes with the full results" when task #70's
notes in Mission Control actually contained none of that detail. Don't take its
self-reported test results as verified fact; re-run things and confirm independently
before building on top of them.

---

## Task definition (from TASKS.md, line 174)

> **D2.13 — Real ArduPilot SITL integration suite** — 12h — Adds mode-ACK, EKF/arming
> gates, GUIDED nav tracking, and real `FS_*`/`BATT_*` failsafe behavior. No hardware
> needed — can start today.

Per the README, this validates what the mock-FC suite (`autonomy_sim/`) can't: that
*ArduPilot itself* accepts and acts on the mission app's MAVLink messages, not just
that the app's internal state machine is correct. Both should pass before field
deployment.

---

## #70 is currently blocked by #71 — do #71 first

Mission Control's dependency graph (`task_dependencies` table) has **task #70
depending on task #71** — `[D2.14] Verify ArduCopter mode numbers (AUTO=3, GUIDED=4,
RTL=6, LAND=9) against the exact firmware build`, 1h, status `Backlog`, currently
unblocked itself. Mission Control's own `is_blocked` computation
(`app/api.py` / `app/tasks.py:blocking_tasks`) confirms #70 is genuinely blocked
right now.

**Why the agent worked on #70 anyway despite that:** not a rule violation — a data
outage. Mission Control's API was unreachable (`[Errno 111] Connection refused`)
when `nightly-drone` ran at 2:30am tonight, so `list_tasks` never returned, and the
`is_blocked`/`blocked_by` fields (which only live in Mission Control's DB) were never
seen. The agent fell back to the local static `TASKS.md` file, which has no
dependency-graph data, only prose. It actually did notice D2.14 in that fallback pass
and considered it, but judged it "trivial" rather than recognizing it as #70's
blocker — because that specific link isn't spelled out anywhere in `TASKS.md`, only
in the DB it couldn't reach. (Open question, not investigated: why was Mission
Control down at 2:30am specifically — worth checking if it recurs, since the same
fallback-to-stale-data failure would happen again.)

**Do #71 first.** It's small (1h), unblocked, and plausibly explains part of what's
already failing in #70's test results — `MAV_CMD_DO_SET_MODE failed` is exactly the
symptom you'd expect from mode numbers that don't match this SITL build's actual
firmware. Verifying/fixing the mode numbers in `mission_app.py` before continuing
#70's debugging could resolve some failures for free rather than chasing them as
independent bugs.

---

## Updating the Mission Control task when you make progress

Task #70 lives in the Mission Control SQLite DB, not in this repo. Use the app's own
ORM rather than raw SQL — pattern used throughout tonight's session:

```python
import sys
sys.path.insert(0, r"C:\Users\Josiah Laperriere\Documents\Coding\Mission-Control")
from app.db import get_session
from app.models import Task

with get_session() as session:
    t = session.get(Task, 70)
    t.notes = (t.notes or "") + "\n\n[claude YYYY-MM-DD] Did: ... Artifacts: ... Remaining: ..."
    # t.status = "Doing" | "Done"   -- see note below on Done vs Done Unverified
    session.flush()
```

Run with:
`"C:\Users\Josiah Laperriere\Documents\Coding\Mission-Control\.venv\Scripts\python.exe" <script.py>`

Append-only note convention (matches what both cron jobs already use, for
consistency with the rest of the task's history):
```
[claude YYYY-MM-DD] Did: <what you did>. Artifacts: <file paths, or "none">.
Remaining: <what's still left>.
```

**On marking it Done:** the OpenClaw agents are contractually barred from setting
`status="Done"` directly — their own job prompt requires `completed_by="Thermal
Surveillance Drone"` + `status="Done Unverified"` instead, specifically because
Mission Control's API rejects `Done` + that `completed_by` value together (a 422) and
requires "a human or Claude" to verify first. A Claude Code session completing the
work directly satisfies that verification requirement — so when the suite is
genuinely passing, it's fine to set `status="Done"` directly rather than going through
`Done Unverified`.
