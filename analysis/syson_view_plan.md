# SysON diagram plan

Tracking checklist for the diagrams to build manually in SysON from `model.sysml`.
Scoped 2026-07-14 (see session context: SysON's textual `expose` import does not
materialize diagrams, and the documented GraphQL API has no representation/diagram
mutations — so diagrams are built by hand in the SysON UI and live in SysON's
project database, not in this repo).

**Tool access:** SysON imports the full `model.sysml` (all four pillars).
CATIA MSOSA Community imports only `model_community_balanced.sysml`, which omits
`Analysis`, `Views`, and `Behavior::UseCases` — rows marked **SysON-only** cover
content CATIA never sees.

**View types available:** SysON — General, Action Flow, Interconnection,
Requirements Table, State Transition. CATIA — same minus Requirements Table.

## Build tips (learned on the Drone diagram, 2026-07-13)

- For Interconnection Views, add **only the part usages** via "Add existing
  elements" and let the interface/connection edges draw themselves. Adding
  interface usages directly creates redundant floating "dangling" boxes —
  if present, remove them from the *diagram* (delete-from-view), never
  delete-from-model.
- Interconnection View is **unsynchronized**: elements must be added manually;
  the edges between on-canvas ports are synchronized automatically.
- To break out a part's internals (e.g. the SBC software), add its nested
  elements *into* the part's node, or make a dedicated view on the part def
  (row 7 below).
- Auto-layout: main toolbar → Flow or Compact.

## Tier 1 — core set

- [x] **0. Drone internals** — Interconnection View on `Architecture::Drone`.
      All 16 nested parts + power/video/RF/UART interface edges. *(SysON: built
      2026-07-13. CATIA: built — the `view Drone : DS_Views::SymbolicViews::iv`
      binding in `model_community_balanced.sysml`.)*
- [ ] **0b. System composition (BDD-equivalent)** — **General View** on
      `Architecture::AerialObservationSystem` (and optionally `Drone` / `GCS`).
      Add the `part def` + its nested `part` usages via "Add existing elements";
      the composition (the v1 black-diamond) renders from the nesting. This is the
      SysML v2 analog of a v1 **Block Definition Diagram** — the *what-it's-made-of*
      view, complementing the Interconnection Views' *how-it-wires* view. Export →
      `presentation/assets/diagrams/` to replace the hand-drawn "System Composition —
      Block-Definition View" slide in the CDR deck. *(SysON: not yet. CATIA MSOSA:
      General View works too, on the balanced export.)*
- [ ] **1. System context** — Interconnection View on
      `Architecture::AerialObservationSystem`. `drone` + `gcs` with the six
      cross-boundary connections (`videoDownlinkRf`, `elrsTelemetry`,
      `ctrlUplinkBackupRf`, `ohdDownlinkRfA/B`, `batteryCharge`). The
      first-five-minutes operational-context picture. *(CATIA: built
      2026-07-14 — the `view AerialObservationSystem :
      DS_Views::SymbolicViews::iv` binding in `model_community_balanced.sysml`;
      note the balanced export carries only 4 of the 6 connections — the
      Phase-4 OpenHD downlinks are omitted there. SysON: not yet.)*
- [ ] **2. GCS internals** — Interconnection View on `Architecture::GCS`.
      Laptop + laptopLink + rcTx + videoRx + capture + antennas + openHDRx +
      charger with the USB/RF/video wiring. Completes the part-level physical
      architecture alongside the Drone diagram. *(CATIA: built — the
      `view GCS : DS_Views::SymbolicViews::iv` binding in
      `model_community_balanced.sysml`. SysON: not yet.)*
- [ ] **3. Flight modes** — State Transition View on `Behavior::FlightMode`.
      disarmed → armed → flying (takeoff/cruise/loiter, cruise⇄loiter
      detect/investigate transitions) → RTL → land, + the two failsafe
      transitions out of `flying`. The SSS §3.1 flight-mode figure, from the
      model. *(CATIA: built 2026-07-14. SysON: not yet.)*
- [x] **4. Requirements table** — Requirements Table View on `Requirements`.
      **SysON-only.** R1–R8 + all subsystem requirements with doc text. If
      per-package scoping works, add per-subsystem tables (Camera, Battery,
      SBC, GCS, Airframe) as trade-study review artifacts. *(SysON: built
      2026-07-17. Known limitation: no traceability/subsets columns in the
      current SysON table — see the requirements_traceability.py idea if that
      matrix is ever needed.)*

## Tier 2 — mission behavior

- [ ] **5. Sortie thread** — Action Flow View on `Behavior::ConductSortie`.
      prepare → plan → launch → surveil → return, with `monitorMission`
      concurrent (UC-0). *(CATIA: built 2026-07-14. SysON: not yet.)*
- [ ] **6a. Sweep & detect** — Action Flow View on `Behavior::SweepAndDetect`.
      Inference loop, ≥90% decide node, POI/alert, terminal `send` (UC-5
      cruise half). *(CATIA: built 2026-07-14. SysON: not yet.)*
- [ ] **6b. Investigate & classify** — Action Flow View on
      `Behavior::InvestigateAndClassify`. Reroute, classify loop with ≥80%
      guard + `adjustOrbit` retry, resume route, terminal `send` (UC-5 loiter
      half). *(CATIA: built 2026-07-14. SysON: not yet.)*
- [ ] **6c. (optional) Detect/investigate cycle** — Action Flow View on
      `Behavior::DetectInvestigateClassify`. The two halves cycling.
      *(CATIA: built 2026-07-14, per the all-action-flows pass. SysON: not
      yet.)*
- [ ] **7. SBC software internals** — Interconnection View on
      `Architecture::SBCPayload`. **Effectively SysON-only.** `missionApp`,
      `mavlinkRouter`, `rknnRuntime`, `thermalModel`; `detectorSeam`,
      `appToRouter`, `uvcToApp`/`routerToUart` delegations. The entire D-1/D-2
      development scope on one page — key Phase 3 diagram.

## Tier 3 — worth having

- [ ] **8. Compatibility layer** — General View on
      `Architecture::Compatibility`. Port defs, enums, constraint defs, the
      three interface defs (P1 / VideoLink / RfLink). The *rules*,
      complementing the interconnection views' *instances*.
- [ ] **9. Analysis / verification** — General View on `Analysis`.
      **SysON-only.** Calc defs, constraint defs, analysis cases + subjects.
      The only place this pillar gets a picture at all.
- [ ] **10. Allocation view** — General View on `Behavior::missionContext`.
      **SysON-only.** perform/exhibit/allocate bindings (flyRoute→platform,
      detectLoop→sbc, planRoute→laptop…). Try once; if `allocate` edges render
      as spaghetti, drop it — the text carries this fine.

## Deliberately skipped

- Use-case diagrams — the `UseCases` veneer is intentionally thin; boxes would
  add nothing over the doc text.
- General View of all of `Architecture` — 20+ part defs × 30–60 attributes is
  unreadable (the CATIA element-cap experience already proved the shape).
- General-View duplicate of the Drone interconnection — row 0 is the real one.

## CATIA parity subset

If reproducing in CATIA MSOSA: rows **0, 1, 2, 3, 5, 6a/6b** (content that
survives into `model_community_balanced.sysml`). Rows **4, 7, 9, 10** are
SysON-exclusive value.
