# CDR Executive Summary — One-Page Briefing for Lisa

**Project:** Thermal Surveillance UAS (Autonomous Wildlife-Scouting Drone)
**Status:** Detailed design complete, verified by analysis. Next gate: procurement.
**Deck:** `CDR_Thermal_Surveillance_Drone.pptx` (41 slides, ~30 content slides)
**Read time:** 5 minutes

---

## Recommendation

> **Proceed to procurement, fabrication, and integration.**  
> The detailed design is complete, fully traced to requirements R1–R8, and verified by analysis with margin on cost, endurance, RF range, and thermal detection. The single gate to operations is empirical validation — which *requires building and flying first*.

---

## Three Decisions Needed

| # | Decision | My recommendation |
|---|----------|-------------------|
| 1 | **Approve the baseline design** — Chimera9 ECO frame, BLITZ F7 FC, T-Motor 2806.7 motors, 8× props, 6S 12 Ah battery, ELRS telemetry, analog FPV, PurpleRiver Mini 640 18mm thermal, NanoPi M5 SBC onboard | Approve — all analyses show compliance with margin |
| 2 | **Authorize Phase 1–3 procurement** — total committed system cost ≈ $1,848 (26% under the $2,500 R4 cap) | Authorize — best-value parts selected; no single point of failure |
| 3 | **Acknowledge three validation gates for operational release** — (a) instrumented Phase-1 hover to correlate endurance model, (b) field thermal capture to validate detection, (c) FAA BVLOS path | Acknowledge — these are normal for a first-build design review |

---

## Budget Snapshot

| Phase | Scope | Cost | Status |
|-------|-------|------|--------|
| Phase 1 | Airframe + FPV + waypoints | $1,371 | Committed |
| Phase 2 | Thermal camera + SBC | $809 | Committed |
| Phase 3 | AI detection (software only) | $0 | Committed |
| **Committed system** | Phases 1–3 | **≈ $1,848** | **26% margin** |
| Phase 4 (deferred) | OpenHD digital downlink | $159 | Future |
| **All four phases** | | **≈ $2,007** | **20% margin** |

Laptop (existing) and reusable support gear excluded from R4 basis per req. R4. The largest single line item is the thermal camera ($650).

---

## Top Risks (All Mitigated)

1. **Design not yet flown** (High) → Build Phase 1; instrumented hover correlates endurance model
2. **Species classification unproven** (High) → Field thermal capture at 90–120 m; train & validate YOLO-nano
3. **2.8 km range beyond VLOS** (Med) → Operate within VLOS or obtain BVLOS waiver / fly at approved site

---

## What Sign-Off Unlocks

Immediately after approval:
1. **All ordering tasks unblock** (~15 line items across airframe, electronics, tools)
2. **Build starts** once parts arrive (2–4 week lead time for most items)
3. **Phase 1 flight test** → endurance model correlation → thermal capture → Phase 2–3 integration

The design is ready. Signing off on a "build to verify" basis — not on a "proven operational system" — is the correct call at CDR.

---

*Full deck at `CDR_Thermal_Surveillance_Drone.pptx` (41 slides). Prep materials at `presentation/cdr_briefing_prep.md`.*