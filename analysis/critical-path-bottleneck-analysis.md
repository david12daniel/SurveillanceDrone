# Critical Path & Bottleneck Analysis

**Date:** 2026-08-28
**Context:** 5th consecutive nightly run with no suitable agent-doable task found.
**Goal:** Identify the single bottleneck keeping the project stalled and clarify the path forward.

## The Core Problem

The project is gridlocked at a single point: **Task 14 → Task 85**, which blocks **all ordering** (tasks 16-25, 40-43, 77-78), which blocks **all hardware work** (tasks 27-38, 44-56), which blocks **everything downstream** (Phase 3+).

## Dependency Graph (Simplified)

```
Task 14 [0.11] Export SysON views [Doing]
  └── Blocks Task 85 [0.1] Present CDR Briefing to Lisa [To Do]
        └── Blocks ALL ordering tasks [Backlog]
              ├── [1.1]-[1.10] Phase 1 ordering (airframe, RX, TX, batteries, charger, etc.)
              └── [2.2]-[2.5] Phase 2 ordering (T13 camera, SBC, UBEC, mount hardware)
                    └── Blocks [1.12]-[1.23] + [2.6]-[2.18] + [3.x] + [4.x]
```

## What Blocks Task 14

Task 14 needs **one diagram**: a **General View** (BDD-equivalent) on `Architecture::AerialObservationSystem` in **CATIA MSoSA Community**, exported as PNG.

This is a **GUI desktop operation** that cannot be done in an unattended CI job. The automation tooling (`apply_row0b_export.py`) is ready and tested — it waits on the PNG.

## What Is Already Done (So You Don't Redo)

### Task 14 prep
- `apply_row0b_export.py` — tested against a scratch copy of the real CDR.pptx, correctly removes slide 14's 33 hand-drawn shapes and inserts the replacement PNG
- README with full usage instructions exists
- The CDR deck is identified and confirmed

### Task 39 (T13 mass)
- T13 mass estimated at 15.0g (midpoint of 12-17g range, 29% reduction from 21g ceiling)
- Vendor email found: `justin.lu@purpleriver.cn`
- Inquiry package written and ready to send
- **Impact:** 15.0g is sufficient for ordering; ±3g precision is nice-to-have

### Task 58 (Bootstrap dataset)
- BIRDSAI assembled: 21,209 frames, 87,199 boxes
- FLIR ADAS assembly scripts written, tested, ready
- Class balance analysis done (human=14.4%, other_animal=85.6%)
- **Missing:** FLIR ADAS v2 zip — requires David to fill out the Teledyne form or use Kaggle

## The Path Forward

### Option A: Bypass the CDR bottleneck (recommended)

**Problem:** Task 85 is set as a dependency for ALL ordering tasks. But the CDR briefing is a formality/review, not a technical prerequisite for ordering.

**Question for David:** Can the ordering tasks be decoupled from the CDR approval? The ordering is time-critical (BAT09 already went out of stock, Amprius BAT10 is stock-fragile). If the CDR is a necessary approval gate, then:
1. Building the MSoSA General View diagram is the #1 priority
2. It takes ~30 minutes in the CATIA GUI
3. The deck would then be ready to present

### Option B: Self-service the diagram

David needs to:
1. Open CATIA MSoSA Community
2. Import `model_community_balanced.sysml`
3. Create a **General View** on `Architecture::AerialObservationSystem`
4. Add the `part def` + nested `part` usages via "Add existing elements"
5. Export as PNG → save to `presentation/assets/diagrams/`
6. Run `python3 apply_row0b_export.py <path-to-png>`

This is **30 minutes of GUI work** that unblocks the entire project.

### Option C: Proceed with ordering at risk

If the CDR is a soft gate (not a hard stop), the ordering tasks could be unblocked by removing the `depends_on_ids: [85]` dependency. This would let the agent start placing orders immediately.

## Time Sensitivity

The critical items with time-sensitive supply:
| Item | Risk | Notes |
|------|------|-------|
| BAT10 (Amprius 12Ah) | **HIGH** | BAT09 already OOS; this is the most stock-fragile line |
| T13 (PurpleRiver 640) | **HIGH** | Long lead, custom variant (18mm, USB) |
| AF3a (Chimera9) | **MEDIUM** | Long lead, but widely stocked |
| VRX6 (Skydroid 150CH) | **MEDIUM** | Alibaba; long lead, unpredictable |

## Summary

The project is **one 30-minute diagram** away from being unblocked. Once Task 14 is done, Task 85 can proceed, and all ordering can begin. Two months of agent-side prep work (T13 mass research, BIRDSAI dataset assembly, FLIR ADAS tooling, SITL test suite, SysON view plan, deck automation) is already complete, waiting on this single GUI action.