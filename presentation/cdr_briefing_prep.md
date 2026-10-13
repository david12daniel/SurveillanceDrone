# CDR Briefing Preparation — Task [0.1] / #85

**Prepared:** 2026-09-17 · **Reconciled to the 41-slide deck:** 2026-10-12
**Purpose:** Prepare for the CDR briefing to Lisa. All ordering is blocked on this gate.
**Deck:** `presentation/build_cdr.py` → `CDR_Thermal_Surveillance_Drone.pptx` (41 slides)
**Due:** Original 2026-08-03. Deck is verified current as of 2026-10-11 (see §0); slide-numbering below is the PHYSICAL deck order (1–41), verified against the regenerated deck.

---

## 0. Deck Status (verified 2026-10-11, re-verified nightly 2026-10-12)

- `presentation/verify_cdr_deck.py` — automated verifier. **All checks PASS** on the current deck:
  deck opens cleanly (41 slides); slide 14 has exactly one picture, byte-identical to
  `presentation/assets/diagrams/system_composition.png` (md5 `4067545fb80e`), no legacy hand-drawn
  labels, caption/title preserved, no caption overlap, no dangling rels; RTM CSV 57 rows, 0 blank
  verification cells. Full writeup: `presentation/cdr_deck_verification.md`.
- `build_cdr.py` emits slide 14 natively (framed_image) — rebuilds are idempotent and preserve the
  diagram. PROJ resolves from `__file__`, so the deck builds from either checkout.
- **Nightly fix applied 2026-10-12:** Analysis-2 slide (30) and the camera hardware card (26) still
  showed the OLD 13 mm lens with 13 mm-nadir GSD / pixels-on-target. The model has used the **18 mm
  lens (HFOV 24.1°)** since the R3_CAM_FOV restatement, and the as-built **45° mount tilt**
  (OffNadirGsd, mountTilt_deg = 45, model.sysml) since 2026-08-12. Slides 26/30 now state 18 mm and
  show along-range pixels-on-target (4.2 px recognize @ 90 m / 3.1 px detect @ 120 m) — the honest
  as-built figures, matching model.sysml `ThermalRecognitionCheck` / `ThermalDetectionCheck`.
  Verdicts unchanged (R3.1 ✓ comfortable, R3.2 ✓ thin) — see slide 30 talking points.
- **Known remaining deck note (date stamp):** the deck's "CDR · 2026-07-26" date stamp on every
  slide is the *planned* review date, not today's date (the review is overdue — due 2026-08-03, not
  yet presented). It is now a **single source of truth**: `CDR_DATE` in `build_cdr.py`
  (env-overridable: `CDR_DATE=YYYY-MM-DD python3 presentation/build_cdr.py`). **Before presenting,
  set `CDR_DATE` to the actual meeting date and rebuild** — the verifier now checks all 35+ stamps
  are consistent with each other AND with the effective generator date (hard FAIL if they drift),
  and prints a loud WARNING when the stamped date is > 14 days old. Cosmetic; not a data issue —
  but presenting a deck stamped 3 months ago reads as stale, so set it.
  ⚠️ *Env-var gotcha:* if you set the date via `CDR_DATE=...` on the build, verify with the same
  env var (`CDR_DATE=... python3 presentation/verify_cdr_deck.py`); verifying without it reports a
  FAIL (the deck wouldn't match a plain rebuild — that's correct). Cleanest: edit the `CDR_DATE`
  default line in `build_cdr.py` once, then build+verify with no env var at all.

---

## 1. Pre-Briefing Checklist

Verify these BEFORE the meeting:

- [x] **Slide 14 (System Composition)** — CLOSED 2026-10-11. Diagram is model-derived
  (graphviz from model.sysml, General View of `Architecture::AerialObservationSystem`, 6 interface
  connections), embedded natively by `build_cdr.py`, md5-verified identical to
  `presentation/assets/diagrams/system_composition.png`. No manual step remains.
- [x] **Deck is current** — rebuilt 2026-10-11 from `build_cdr.py` (41 slides) and re-verified
  2026-10-12 after the Analysis-2 lens/GSD correction; `verify_cdr_deck.py` ALL PASS.
- [x] **Cost slide** — Analysis 5 (slide 33) shows **≈ $1,848 committed system cost, ≈ 26 % margin**
  under the $2,500 R4 cap; all four phases ≈ $2,007, also under cap. The old "$2,397 / $103 margin"
  figure in earlier prep notes is OBSOLETE (it predated the exclusion of the laptop + reusable
  support gear from the R4 basis).
- [x] **Open items slide** — slide 40 reflects the current board: 7 rows (RTL reserve value TBR,
  FC firmware RESOLVED, deck/battery dims TBR, SBC mount design, AF5 RETIRED, Phase 4 pricing TBD,
  empirical validation Action). Bootstrap dataset (D1.2) and labeling/augmentation (D1.3) are DONE
  and no longer listed.
- [x] **All RTM tables filling** — slides 10–12; RTM CSV 57 rows, 0 blank verification cells
  (verifier PASS). RTM now includes **R3_BHV_SBC_FAILSAFE** (allocated to fcSoftware).
- [x] **Date stamp integrity** — CLOSED 2026-10-13. The review-date stamp is now a single
  `CDR_DATE` constant in `build_cdr.py` (env-overridable); `verify_cdr_deck.py` checks all stamped
  dates are consistent with each other and with the effective generator date (hard FAIL on drift)
  and warns if > 14 days old. ⚠️ **Before presenting:** `CDR_DATE=<meeting date> python3
  presentation/build_cdr.py`, rebuild, re-verify (same env var on the verifier, or edit the
  `CDR_DATE` default line and use no env var). Current stamp: 2026-07-26 (the original planned
  date — update it to the real meeting date).
- [ ] **Lisa's background** — Who is Lisa? (Not documented in the repo.) If she's a domain-area
  stakeholder (not a project manager), tailor emphasis to her interest areas. If she's a
  funder/approver, emphasize budget, risk, and schedule.
- [ ] **Logistics** — deck is 41 slides incl. 5 section dividers; the ~30 content slides carry the
  briefing. Allow **45–60 min**; the recommended flow in §4 stays within that.

---

## 2. Slide-by-Slide Talking Points (physical slide numbers)

> Section dividers (slides 6, 13, 21, 24, 35) are one-line transitions — do not dwell.

### Section 0 — Introduction (slides 1–3)

**Slide 1: Title — CRITICAL DESIGN REVIEW (CDR)**
- Read the header data: detailed design baseline, requirements traceability, verifying analyses;
  MBSE (SysML v2); content per MIL-STD-1521B App. E / IEEE 15288.2; budget ≤ $2,500 (R4);
  design maturity "detailed design complete (pre-fabrication)".
- Key message: "This is a review of the COMPLETE design — we're asking for approval to procure and
  build, not for feedback on whether the design is ready."

**Slide 2: CDR Purpose & Agenda**
- Purpose: demonstrate the detailed design meets mission + derived requirements, interfaces defined,
  design verified by analysis, ready to proceed to fabrication/integration.
- Agenda: Overview → Requirements → Architecture → Behavior → Analyses → Risk/Closure.

**Slide 3: CDR Data-Item Content — Coverage Map**
- Maps the deck to MIL-STD-1521B / IEEE 15288.2 data items. Quick reference; don't dwell unless asked.

### Section 1 — System Overview (slides 4–5)

**Slide 4: Mission & Concept of Operations**
- Elevator pitch: "Autonomous thermal surveillance UAS — 30+ min endurance, 2.8 km range, detect
  deer/turkey/human thermal signatures at 90–120 m, classify via onboard AI, report back."
- Operating point: 90–120 m AGL (R1), 2.23 m/s ground speed (R2).

**Slide 5: Operational Concept (OV-1)**
- Walk the diagram: drone takes off → autonomous waypoints → thermal scanning → onboard
  detect/classify → POI report back. Callouts trace to R1 · R2 · R3 · R7. Frame at
  `presentation/assets/diagrams/` — verified to render.

### Section 1 — Requirements (slides 6–12)

**Slide 6: (Divider) Requirements & Traceability**
- One-liner: eight mission requirements decomposed into subsystem requirements, each allocated to a
  component via a formal satisfy link. Source: `analysis/requirements_traceability.csv` (SysML v2).

**Slide 7: Requirements — Decomposition by Subsystem**
- Top-down: system-level R1–R10 → subsystem packages; the traceability web is modeled, not manual.
- Highlight: R3_CAM_FOV (≥ 42 m swath at 120 m — T13 @ 18 mm gives 51.2 m, 22 % margin),
  R9/R10 (30/60 acres per sortie).

**Slide 8: Mission Requirements (R1–R8)**
- SysON export table; V-methods I/A/D/T; at CDR: A complete for all; T/D planned (see V&V).
- **Key callouts:**
  - **R4_BUDGET = $2,500** — committed system ≈ $1,848 (Analysis 5), 26 % margin
  - **R7_RANGE = 2.8 km** — 4/4 RF links pass with ≥ 10 dB margin (Analysis 3)
  - **R6_ENDURANCE = 30 min** — modeled at 58.4 min hover (Analysis 1)

**Slide 9: Traceability Approach & Coverage**
- Up-trace: each subsystem requirement subsets its mission requirement (e.g., R3_CAM_RES ⊂ R3,
  cost reqs ⊂ R4). Down-trace: each component part def carries satisfy links; the RTM is derived,
  not hand-maintained. All 10 requirements satisfied, no blanks.

**Slides 10–12: RTM Detail Tables (Airframe & Autonomy / Battery & Camera / SBC & Ground)**
- Reference tables — skip unless Lisa asks for detail.
- **Slide 10 note:** R3_BHV_SBC_FAILSAFE now appears (autonomous behavior reverts to a safe state;
  allocated to fcSoftware) — the formalized SBC-failure fallback (complete waypoint → RTL),
  developed 2026-08-15 and confirmed against ArduCopter 4.7.0 source + SITL probe.
- **Slide 11 note:** R3_CAM_COST restated to ≤ $720 (raised from $600) — the ordered T13 with 18 mm
  lens is $640 + $60 shipping = $700, inside the cap.
- **Slide 12 note:** R4_GCS_SWEEP_SPACING (line spacing ≤ 90 % of swath) is the new flight-planning
  requirement behind the R9/R10 area budget.

### Section 2 — System Architecture (slides 13–20)

**Slide 13: (Divider) System Architecture**
- One-liner: drone + laptop-based GCS joined by three wireless RF links; the drone integrates
  propulsion, power, thermal payload, and an onboard inference computer.

**Slide 14: System Composition — Block-Definition View**
- **The money architecture slide.** `AerialObservationSystem` = `Drone` + `GCS` with 6 interface
  connections (videoDownlinkRf, elrsTelemetry, ctrlUplinkBackupRf, ohdDownlinkRfA/B, batteryCharge).
- Key message: "SysML v2 analog of a BDD — model-derived, not hand-drawn." Phase-4 OpenHD parts
  omitted for the committed build.

**Slide 15: System Context — Aerial Observation System**
- IBD: drone ↔ GCS wireless interfaces + operator actor. MacBook Air is an existing external actor,
  excluded from system cost.

**Slide 16: Drone — Internal Block Diagram**
- Core architecture: FC (BLITZ F7) ↔ SBC (NanoPi M5) ↔ Thermal (PurpleRiver T13, nose-mounted).
- Paths: analog FPV → 5.8 GHz VTX; ELRS telemetry; MAVLink over UART. Power chain:
  6S Li-Ion → anti-spark (XT60) → UBEC (12 V → SBC) / direct (FC).

**Slide 17: Onboard Compute (SBC) — Software Architecture**
- The key Phase 2/3 slide. Stack: Ubuntu → V4L2 capture → RKNN inference → mission_app.py →
  pymavlink → FC. **No ROS, zero middleware overhead.** Amber boxes = to-be-developed software
  (D-1 thermalModel · D-2 missionApp). NanoPi M5: RK3576, 6 TOPS NPU, passive-cooled ≤ 10 W
  (R4_SBC_PWR / R4_SBC_TEMP).

**Slide 18: Ground Control Station — Internal Block Diagram**
- MacBook Air running QGroundControl 4.4+; VRX6 UVC video receiver + TrueRC patch; Hermes ELRS USB
  dongle (primary laptop link); TX12 Mark II as manual backup. No goggles in the architecture.

**Slide 19: Interface Design (Internal & External)**
- The big signal diagram: all RF links, baud rates, protocols. Highlight dual-redundant control
  links (ELRS laptop primary + TX12 backup) and the modeled compatibility rules (P1 cell-count rule
  etc.) enforced by the configuration sweep.

**Slide 20: Standards Profile (StdV-1)**
- Mature open/de-facto protocols (MAVLink, CRSF, UVC, WFB-ng, ELRS) — no proprietary lock-in on the
  committed build. Only dwell if asked about certification/compliance.

### Section 3 — Functional & Behavioral Design (slides 21–23)

**Slide 21: (Divider) Functional & Behavioral Design** — state machine + autonomy loop.

**Slide 22: Flight-Mode State Machine & Failsafes**
- Nominal path: disarmed → armed → flying (route execution) → returnToLaunch → land.
- Failsafe transitions: **link loss → RTL** (R7_BHV_LINKLOSS_RTL), **low battery → RTL**
  (R6_BHV_RTL_RESERVE). Realization: ArduPilot FS_* / BATT_* parameters; executeRtl /
  touchDownAndDisarm are modeled actions.
- **Open policy to name aloud:** the RTL reserve-energy threshold value is still TBR (tracked as an
  open item on slide 40) — policy set before first autonomous flight, per R6_BHV_RTL_RESERVE.
- **Decision needed:** Lisa verifies these behavior choices are acceptable.

**Slide 23: Autonomous Detect · Investigate · Classify Loop**
- SweepAndDetect (UC-5a) → InvestigateAndClassify (UC-5b): scan → detect candidate → reroute →
  loiter → classify → log → resume. 30-second loiter budget per investigation, then give up.
  Operator override via QGC mode switch at any point. (Both behaviors are implemented and
  contract-tested — D2.8/D2.9 in the mission app.)

### Section 4 — Engineering Analyses (slides 24–34)

**Slide 24: (Divider) Engineering Analyses** — four quantitative analyses + detail slides.

**Slide 25: Detailed Design — Selected Configuration**
- Reference build: Chimera9 ECO + 6S 12 Ah Amprius + Mini 640 + NanoPi M5 → ≈ 58 min hover,
  ≈ $1,850 committed system cost (≤ $2,500 R4), SBC fits the deck. Down-selected from ~110 real
  market candidates; version-controlled, machine-enforced in the analysis.

**Slide 26: Selected Hardware — Air Vehicle & Payload**
- Photo gallery: Chimera9 ECO 9" (PNP, 729 g, 6S, XING-E 2809) · Amprius 6S 12 Ah (XT60, ~57 min) ·
  **PurpleRiver Mini 640 — 640×512, 12 µm, 18 mm lens (corrected 2026-10-12), USB-UVC** ·
  NanoPi M5 (6 TOPS NPU, ≤ 10 W passive, 90×62 mm) · iFlight True-Diversity ELRS · iFlight
  Anti-Spark Filter (XT60, 150 A).

**Slide 27: Selected Hardware — Ground Control & Support**
- TX12 Mark II (ELRS 2.4 GHz, EdgeTX) · TrueRC X-AIR 5.8 MK II (10 dBic patch, 120°, RHCP) ·
  HOTA D6 Pro (AC 200 / DC 650 W dual). Also in kit: Skydroid 150CH UVC VRX ($44), Hermes ELRS
  dongle ($16), GPS (iFlight BLITZ M10, bundled), MacBook Air GCS (existing).

**Slide 28: Analysis 1 — Endurance (Flight Time)**
- Momentum/actuator-disk (blade-element) model, 34 compatible configs swept (T13 + M5 fixed).
- **58.4 min hover** at ~15 % throttle (16.85 W payload), 1,751 g AUW; slow cruise ≈ 60 min via
  translational lift. R6 ✓ (30 min), R8 ✗ (60 min stretch not met — documented).
- Fidelity: first-order comparative; **not yet validated against measured hover current** — the
  Phase-1 instrumented flight (task 1.22) is the correlation gate. Risk to flag: BAT10 Amprius is
  stock-fragile (BAT09 already OOS).

**Slide 29: Endurance vs. Cost — Full Configuration Trade Space**
- Scatter of every compatible real configuration; R4 vertical line + R6/R8 horizontals. Entire
  selected trade space sits left of $2,500 and above 30 min. Reference build ≈ $1,850 / 58 min.
  Quick reference — the decision is already made.

**Slide 30: Analysis 2 — Thermal Detection (Johnson Criteria)**
- **Corrected 2026-10-12 to the as-built geometry (18 mm lens, 45° mount tilt, along-range axis).**
  Nadir GSD: 6.0 cm @ 90 m / 8.0 cm @ 120 m. Pixels-on-target ALONG-RANGE (×2.0 vs nadir):
  - 0.5 m target @ 90 m: **4.2 px — Recognize ✓ (THIN — the tightest margin in the chain)**
  - 0.5 m target @ 120 m: 3.1 px — Detect ✓
  - **Deer @ 120 m (R3.1): 3.1 px — Detect ✓** (comfortable vs 1.5 px floor)
  - Deer @ 90 m: 4.2 px — detect/recog.; Human @ 90 m: 4.2 px — Detect ✓; Turkey @ 120 m: 1.9 px — Marginal
- Honest framing for Lisa: detection is comfortable across 90–120 m; **recognition of a 0.5 m
  target ~4.2 px vs the 4 px floor is thin — field capture (task 2.17) is the load-bearing check.**
  Species classification (R3.2) is the trained AI model's job, not geometry alone.
- (Old deck figures — 13 mm lens, 6.0/4.5 px nadir — overstated these margins; the deck now matches
  model.sysml ThermalRecognitionCheck / ThermalDetectionCheck.)

**Slide 31: Analysis 3 — RF Link Budget (2.8 km / R7)**
- FSPL at each link's frequency; design target ≥ 10 dB fade margin at 2.8 km. **4/4 links pass.**
  Control/telemetry (ELRS) close the range many times over; the BINDING link is analog FPV — the
  TrueRC X-AIR patch (10 dBic) is the enabling component (stock omni would fail). Phase 4 OpenHD
  shown for completeness (+11.3 dB with dual-diversity Foxeer panels).
- Not yet range-tested — task 1.21 is the field check.

**Slide 32: Analysis 4 — Physical Integration ("Does It Fit?")**
- Dimensional model, 3-tier fit verdict (±12 mm). Binding constraint: **NanoPi M5 footprint
  (90 × 62 mm)**; Chimera9 ECO deck ≈ 110 × 70 mm → SBC fits with ~8 mm spare (key reason it beat
  the endurance leader). 9–10" frames fit cleanly; the pure endurance winner (DarwinFPV 129) is
  NO-FIT. Deck dims are mostly ESTIMATES (≈ 0.27 × wheelbase) — confirm the real frame's deck pre-
  build (task 1.23).
- Endurance and fit trade against each other; the selected frame is the best endurance-per-dollar
  option that physically integrates the compute.

**Slide 33: Analysis 5 — Cost & Budget (R4 ≤ $2,500)**
- Method: phased BOM rolled up from candidates.sysml with actual quoted prices for locked parts;
  **laptop (existing) and reusable support gear (dev packs, charger) excluded from the R4 figure.**
- **≈ $1,848 committed system cost (~26 % margin); all four phases ≈ $2,007 — both under $2,500.
  R4 VERDICT: PASS.** Thermal camera ($650) is the single largest line.
- (The endurance sweep reports ≈ $1,674 using cost-representative radio/RX; the BOM figure uses the
  actual selected parts, hence higher.)
- **Decision needed:** Lisa approves the budget — now with a comfortable 26 % margin (the old
  96 %-of-budget "$103 margin" story is obsolete).

**Slide 34: Performance Measures (SV-7)**
- KPPs vs requirement thresholds with as-designed value and margin. All hard requirements met with
  margin; only R8 stretch endurance not met (documented). *Compute fit marginal (custom deck);
  speed is a control-tuned target verified by flight test.

### Section 5 — Verification, Risk & Closure (slides 35–41)

**Slide 35: (Divider) Verification, Risk & Closure.**

**Slide 36: Verification Cross-Reference Matrix (VCRM)**
- Every requirement → method (A/D/T/I) + status @ CDR: R1/R2/R6/R7 analysis ✓ test planned; R3.1
  analysis ✓ demo planned; R3.2 analysis ✓ AI test planned; R4/R5 verified by inspection; **R8 not
  met (documented).**
- At CDR: design compliance shown by analysis; demonstration/test gated at the Test Readiness Review.

**Slide 37: Manufacturing & Producibility**
- Minimize soldering (R5): PNP airframe pre-soldered; **the only solder joint in the committed
  build is the SBC UBEC's 12 V leads.** COTS-first (~110 real parts traded); only fabricated part is
  the 3D-printed SBC deck + 30 mm fan + heat-set hardware (~$15). Standardization: XT60 power chain,
  single ELRS ecosystem. Phased integration (1–3), each phase independently testable.

**Slide 38: Project Timeline (PV-2)**
- NOW — CDR: detailed design complete, verified by analysis. Next gate → **procurement**, then
  phased build & test. Phase 1 ≈ $1,371 (airframe, ELRS, battery, FPV, GPS, ArduPilot+QGC) ·
  Phase 2 ≈ $809 (Mini 640, M5, UBEC, mount) · Phase 3 $0 HW (AI software) · Phase 4 deferred.
- Critical path: **CDR approval → order → hardware arrival → bench assembly → field test.**
  Total remaining hands-on ~150 h + shipping leads + collection season.

**Slide 39: Risk Assessment**
- Top risks to voice:
  1. **Battery OOS** (HIGH): BAT09 gone; BAT10 Amprius stock-fragile — every week of delay raises risk.
  2. **Thermal data collection** (HIGH): season/opportunity dependent, ~40 h collection; October
     still viable in MI (pre-rut/rut activity improves thermal contrast), window narrows with cold.
  3. **R3.2 recognition margin is thin** (MEDIUM-HIGH): 4.2 px along-range vs 4 px floor — field
     capture (2.17) is the load-bearing check.
  4. **T13 shipping** (MEDIUM): long lead (Alibaba-class).
  5. **Endurance model unvalidated** (MEDIUM): 58.4 min is modeled, not measured — task 1.22.

**Slide 40: Open Items (TBD / TBR / Action)**
- 7 rows, none design-blocking: RTL reserve-energy value (TBR, set before first autonomous flight) ·
  FC firmware (RESOLVED) · deck/battery dims estimates (TBR, Phase 2 gate) · SBC mount design
  (Phase 2 gate) · AF5 mass gap (RETIRED) · Phase 4 pricing (TBD) · empirical validation (Action).
- **Key ask for Lisa:** authorization to proceed with ordering despite these items being carried
  forward — all bounded and assignable.

**Slide 41: CDR Exit Assessment & Recommendation** (final slide — close strong)
- Exit criteria: all ✓ (design complete & traced; interfaces defined; analyses show compliance with
  margin; R4 ✓ 26 % margin · R6 ✓ · R7 ✓ · thermal detect ✓); ▲ R8 stretch not met (documented);
  ▲ empirical validation pending (design gate, not yet test).
- **RECOMMENDATION: Proceed to procurement, fabrication & integration.** Gates to operations:
  (1) instrumented Phase-1 flight to correlate the endurance model, (2) field thermal capture to
  validate detection/classification, (3) established FAA BVLOS regulatory path (Part 107).
- This is the explicit "yes" slide — end the briefing here.

---

## 3. Key Decisions Lisa Needs to Make

1. **Approve the design → unlock ordering** — This is THE decision. Everything else is secondary.
2. **Accept the budget** — ≈ $1,848 committed of $2,500 (**26 % margin**); all four phases ≈ $2,007
   also under cap. The former tight-budget concern is resolved; contingency still wise if prices
   drift (see Risk #1).
3. **Acknowledge open-item carry-forward** — bolt-pattern caliper (1.23), vendor mass confirmation
   (2.1), SBC deck dims — none block ordering. Get explicit agreement that ordering proceeds before
   these close.
4. **Confirm failsafe behavior choices** — RTL on link loss, RTL on low battery, complete-waypoint-
   then-RTL on SBC failure (R7_BHV_LINKLOSS_RTL / R6_BHV_RTL_RESERVE / R3_BHV_SBC_FAILSAFE). The
   RTL reserve value itself remains TBR until first autonomous flight.
5. **Scope of review** — formal CDR sign-off or informal progress review? Set expectations at the start.

---

## 4. Recommended Presentation Flow

| Segment | Slides | Time |
|---------|--------|------|
| Intro + overview | 1–5 | 5 min |
| Requirements (highlights only) | 7–9 (skip 10–12 unless asked) | 5 min |
| Architecture (walk the key diagrams) | 14–19 | 10 min |
| Behavior (state machine + autonomy) | 22–23 | 5 min |
| Analyses (the numbers that matter) | 28, 30, 31, 32, 33 | 10 min |
| Risk + open items + exit assessment | 39–41 | 5 min |
| **Decision: approve to proceed** | — | 5–10 min |
| **Total** | | **~45–55 min** |

---

## 5. What This Briefing Unblocks

Approval of this CDR enables the following (in order):

1. **Ordering all Phase 1 hardware** (~$1,371): airframe, RX, TX, batteries, charger, VRX, patch
2. **Ordering Phase 2 hardware** (~$809): T13 thermal, SBC, UBEC, mount hardware
3. **Physical build and bench test** — the first time real hardware gets assembled
4. **Field flight tests** — LOS envelope, waypoint missions, range verification
5. **Phase 3 AI pipeline** — training with real thermal data, on-target benchmarking

Every remaining task (#16–#83) is blocked on this decision: ~40 tasks, ~150+ h of work that cannot
begin until the CDR briefing is delivered and Lisa signs off. The board-wide blocker is task #85.

---

## 6. Risk Flags for the Meeting

- **Deck accuracy:** the 2026-10-12 correction (slides 26/30: 18 mm lens, along-range px) makes the
  deck match the model — but be ready for a question on why recognition reads 4.2 px when older
  material said more; answer is the 45° mount tilt (×2.0 along-range GSD) — the honest as-built
  figure, and the reason task 2.17 is load-bearing.
- **Battery supply:** BAT09 is out of stock; BAT10 is the single most stock-fragile line in the BOM.
- **T13 thermal shipping:** long lead; highest-value single line in the BOM ($700).
- **Training data collection:** season-dependent; October in Michigan still viable (rut activity
  raises deer movement/thermal contrast), but the window narrows as temperatures drop.
- **Endurance figure is modeled, not measured** — say so; the instrumented Phase-1 flight (1.22)
  closes it.