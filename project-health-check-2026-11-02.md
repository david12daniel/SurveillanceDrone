# Project Health Check — 2026-11-02

## Executive Summary

The project is fully stalled at the Phase 0 CDR/ordering gate. Every single
task — hardware, firmware, software, and field validation — is blocked on one
or both of two root causes:

1. **Task #85 [0.1] Present CDR Briefing to Lisa** — the CDR presentation
   (status: Doing, due 2026-08-03, human_only, past due)
2. **Task #39 [2.1] Confirm the 18mm T13 variant's mass with the vendor**
   (status: Doing, human_only)

Nothing moves until the CDR is presented and approved, which unblocks all
ordering, which unblocks all hardware work, which unblocks all software and
field-validation tasks.

## Critical-Path Chain

```
[0.1] CDR Briefing [85] ─┬─→ [1.1] Order Chimera9 [16]
                          ├─→ [1.5] Order BAT10 [20]            ─┬─→ [2.10] Update candidates.sysml [48]
                          ├─→ [1.6] Order BAT22 [21]            │
                          ├─→ [1.9] Order ASF1 [24]             │
                          ├─→ [1.10] Order CHG1 [25]            │
                          ├─→ [1.7] Order VRX6 [22]             │
                          ├─→ [2.3] Order NanoPi M5 [41] ───────┤
                          ├─→ [2.2] Order T13 [40]              │
                          └─→ [2.4] Order UBEC [42]             │
                                                                │
[1.23] Caliper dims [38] ←─ [1.1]─┘                            │
    (human_only) ───────────────────────────────────────────────┤
                        └─→ [2.6] SBC deck design [44]         │
                                                                │
[1.12] Flash ArduPilot [27] ←─ [1.1]                           │
    └─→ [1.13] Bind ELRS [28]                                   │
    └─→ [1.14] Calibrate sensors [29]                           │
    └─→ [1.15] Configure failsafes [30]                         │
    └─→ [2.14] Wire SBC<>FC [52]                                │
    └─→ [D2.14] Verify mode numbers [71] (Done!)                │
```

## Downstream Software Tasks (What the Night Worked On)

These are the code tasks that the nightly agent COULD work once the project is
unstuck:

| Task | What | Depends on | Notes |
|------|------|------------|-------|
| [D2.5] UVC capture pipeline [65] | Python V4L2 capture, 640×512 @25 Hz | [2.15] hardware confirmation | Code can be drafted generically now |
| [D1.8] Field-validation protocol [63] | SSS §4 demonstration of R3_1/R3_2 | [2.17] field verify + [D1.7] benchmark | Protocol document can be written now |
| [D2.6] RKNN inference wrapper [66] | Implements Detector interface | [D1.6] + [D2.5] | Needs model first |
| [3.2] MAVLink detection mapping [73] | Detections → mission modification | [1.19] + [2.16] + [D2.8] + [3.1] | Needs system built |
| [D1.4] Training pipeline [60] | YOLO-nano fine-tune → ONNX | [D1.1] data collection | Data not collected yet |

## What Would Unblock the Software Tasks First

If CDR were approved and ordering happened, the fastest path to an agent-workable
software task would be:

1. Order Chimera9 + NanoPi M5 + T13 + UBEC (unblocks everything)
2. Flash ArduPilot (task 27, human_only)
3. [2.15] Confirm T13 enumerates (task 53, human_only)
4. → **Task [D2.5] UVC capture pipeline [65] becomes unblocked** ← first code task

## Recommendation

The single highest-leverage action is to present the CDR and get purchasing
approved. Once parts arrive, the bottleneck shifts to flashing ArduPilot and
confirming the thermal camera enumerates — both quick turnarounds that unblock
the first software task.