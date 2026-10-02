# CDR Briefing Preparation — Task [0.1] / #85

**Prepared:** 2026-09-17
**Purpose:** Prepare for the CDR briefing to Lisa. All ordering is blocked on this gate.
**Deck:** `presentation/build_cdr.py` → `CDR_Thermal_Surveillance_Drone.pptx`
**Due:** Original 2026-08-03 (now 45 days overdue — slide 14 bottleneck just cleared Sep 15)

---

## 1. Pre-Briefing Checklist

Verify these BEFORE the meeting:

- [ ] **Slide 14 (System Composition)** — The image was replaced Sep 15 via `apply_slide14_diagram.py`. Confirm the replacement looks correct in the real deck (open the .pptx, verify the graphviz-rendered diagram is present, the 33 old hand-drawn shapes are gone, and the caption text is preserved).
- [ ] **Deck is current** — `build_cdr.py` generates the full deck. If you modified the model, requirements, or BOM since the last build, re-run `build_cdr.py` to pick up changes.
- [ ] **Cost slide** — Verify the $2,500 budget constraint is still met (BOM prices can drift). Run `analysis/flight_time_model.py` to confirm the latest selected-configuration cost.
- [ ] **Open items slide** — Check that resolved items have been cleared from the open-items list. Task 14 (diagram export) is done — remove from open items.
- [ ] **All RTM tables filling** — Verify `analysis/requirements_traceability.csv` has no blank verification-status cells.
- [ ] **Lisa's background** — Who is Lisa? (Not documented in the repo.) If she's a domain-area stakeholder (not a project manager), tailor emphasis to her interest areas. If she's a funder/approver, emphasize budget, risk, and schedule.
- [ ] **Logistics** — Confirm meeting duration. The deck has ~30 slides; allow 45–60 min.

---

## 2. Slide-by-Slide Talking Points

### Section 0 — Introduction (3 slides)

**Slide 1: CDR Purpose & Agenda**
- Key message: "This is a review of the COMPLETE design — we're asking for approval to procure and build, not for feedback on whether the design is ready."
- Agenda: Overview → Requirements → Architecture → Behavior → Analyses → Risk/Closure
- Duration expectation: 45-60 min

**Slide 2: CDR Data-Item Content — Coverage Map**
- Map the deck to MIL-STD-1521B / IEEE 15288.2 data items
- Show that every required CDR data item has a slide
- Quick reference; don't dwell unless asked

**Slide 3: Mission & Concept of Operations**
- Single-paragraph elevator pitch: "Autonomous thermal surveillance UAS — 30+ min endurance, 2.8 km range, detect deer/turkey/human thermal signatures at 90-120 m, classify via onboard AI, report back via WFB-ng digital datalink"
- Reference the OV-1 graphic on the next slide

### Section 1 — System Overview (1 slide)

**Slide 4: Operational Concept (OV-1)**
- Walk the diagram: drone takes off → autonomous waypoints → thermal scanning → onboard detect/classify → POI report back
- Key constraint: the OV-1 image is at `presentation/assets/diagrams/` — verify it exists and renders correctly

### Section 1 — Requirements (5 slides)

**Slide 5: Requirements — Decomposition by Subsystem**
- Top-down: system-level R1-R10 → subsystem allocation
- Show the traceability web is modeled, not manual
- Highlight: R3_CAM_FOV (swath ≥42 m at 120 m), R9/R10 (30/60 acres per sortie)

**Slide 6: Mission Requirements (R1-R8)**
- Read the eight top-level requirements
- Each with: requirement text, allocated-to, verification method
- Point out which are HARD vs. STRETCH (R9/R10, R8)
- **Key callouts:**
  - **R4_BUDGET = $2,500** — we're at ~$2,397 (Analysis 5)
  - **R7_RANGE = 2.8 km** — RF link budget shows +11.3 dB margin (Analysis 3)
  - **R6_ENDURANCE = 30 min** — modeled at ~58.6 min hover (Analysis 1)

**Slide 7: Traceability Approach & Coverage**
- Show the SysML-modeled RTM (not hand-maintained)
- Down-trace: requirements → part defs with satisfy links
- Up-trace: every component → which requirements it fulfills
- Coverage: all 10 requirements satisfied (verify no blanks)

**Slide 8-10: RTM Detail Tables**
- Grouped by subsystem (airframe/propulsion, avionics/GCS, payload/software)
- Reference tables, not presentation material — skip unless Lisa asks for detail

### Section 2 — System Architecture (7 slides)

**Slide 11: System Composition — Block-Definition View**
- **This is Slide 14 of the actual deck** (just updated Sep 15)
- Shows: `AerialObservationSystem` composed of `Drone` + `GCS` with 6 interface connections
- Key message: "This is the SysML v2 analog of a BDD — model-derived, not hand-drawn"
- The diagram is graphviz-rendered from `model.sysml`; the GitHub reference is `presentation/assets/diagrams/system_composition.png`

**Slide 12: System Context — Aerial Observation System**
- IBD showing external actors (environment, operator, airspace)
- Focus on the external interfaces (RF links, GPS constellation)

**Slide 13: Drone — Internal Block Diagram**
- The core architecture: FC (BLITZ F7) ↔ SBC (NanoPi M5) ↔ Thermal (PurpleRiver T13)
- Three serial/PWM paths: analog FPV → 5.8 GHz VTX, ELRS telemetry, MAVLink over UART
- Power chain: 6S Li-Ion → anti-spark → UBEC (12V → SBC) / direct (FC)

**Slide 14: Onboard Compute (SBC) — Software Architecture**
- The key Phase 2/3 slide
- Show the software stack: Ubuntu → V4L2 capture → RKNN inference → mission_app.py → pymavlink → FC
- Highlight: no ROS needed, zero middleware overhead
- This diagram should show the D-2/D-1 software partition

**Slide 15: GCS — Internal Block Diagram**
- MacBook running QGC + WFB-ng decode
- VRX6 UVC receiver + patch antenna
- Hermes ELRS USB dongle for laptop telemetry link
- TX12 Mark II as manual backup

**Slide 16: Interface Design**
- The big signal diagram: all RF links, baud rates, protocols
- Highlight: dual-redundant control links (ELRS laptop primary + TX12 backup)

**Slide 17: Standards Profile (StdV-1)**
- Quick reference to standards used (MAVLink, CRSF, UVC, WFB-ng, etc.)
- Only dwell if asked about certification/compliance

### Section 3 — Functional & Behavioral Design (2 slides)

**Slide 18: Flight-Mode State Machine & Failsafes**
- State machine: MANUAL → GUIDED (takeoff) → AUTO (waypoints) → LOITER (investigate) → RTL
- Failsafe transitions: link loss → RTL, low battery → RTL, SBC heartbeat loss → complete waypoint → RTL
- **Decision needed:** Lisa verifies these behavior choices are acceptable

**Slide 19: Autonomous Detect · Investigate · Classify Loop**
- The autonomy loop: scan → detect candidate → loiter → classify → log → resume
- 30-second loiter budget per investigation, then give up
- Operator override via QGC mode switch at any point

### Section 4 — Engineering Analyses (9 slides)

**Slide 20: Detailed Design — Selected Configuration**
- Photo gallery of selected hardware (airframe, thermal, SBC, radio, battery)
- Show the actual components so Lisa can visualize the build

**Slide 21: Photo Gallery (continued)**
- Remaining components

**Slide 22: Analysis 1 — Endurance (Flight Time)**
- **~58.6 min hover** (BAT10 Amprius 12 Ah, 6S)
- The key assumptions: 950 g all-up mass, 193 W hover power
- Sensitivity: +100 g → -4.6 min; wind adds 15-25% drag power
- 2x GNB dev packs (BAT22) will be used for shakedown; Amprius saved for mission flights
- **Risk to flag:** BAT09 already OOS; BAT10 Amprius is stock-fragile

**Slide 23: Endurance vs. Cost — Full Configuration Trade Space**
- The scatter plot from the model sweep
- Our pick is on the Pareto frontier
- Quick reference — the decision is already made

**Slide 24: Analysis 2 — Thermal Detection (Johnson Criteria)**
- **R3_1 (detect @120 m): 6.25 px** nadir → **3.13 px** along-range at 45° tilt → PASS (3 px threshold)
- **R3_2 (recognize @90 m): 8.33 px** nadir → **4.17 px** along-range at 45° tilt → PASS (4 px threshold)
- Key caveat: the along-range numbers are thin — field verification is critical (TBD task 2.17)
- The 45° mount tilt was modeled 2026-08-12 per TASKS.md 0.15; margin is honest now

**Slide 25: Analysis 3 — RF Link Budget (2.8 km / R7)**
- ELRS (control/telemetry): +11.8 dB margin @ 2.8 km
- Analog FPV (video): +15 dB margin with patch antenna
- WFB-ng (future digital): +11.3 dB margin, reliable to ~3.3 km
- **Worst-case:** Largest Free-Space Path Loss at 2.8 km for 5.8 GHz = 116.5 dB — all three links stack positive margin

**Slide 26: Analysis 4 — Physical Integration ("Does It Fit?")**
- Top-plate bolt pattern: assumed 30.5 mm (standard 30.5×30.5 stack)
- SBC deck clearance above battery: ~8 mm spare
- Thermal mount: lens tip ~31 mm below plate — verify landing gear clearance
- **Open:** bolt pattern needs caliper confirmation (task 1.23)

**Slide 27: Analysis 5 — Cost & Budget (R4 ≤ $2,500)**
- Current total: **~$2,397 of $2,500** (96% — tight)
- Top 3 cost drivers: T13 thermal ($700), Chimera9 airframe ($491), Amprius BAT10 ($275)
- Remaining $103 margin — no room for unplanned purchases
- **Decision needed:** Lisa approves budget — acknowledge it's tight

**Slide 28: Performance Measures (SV-7)**
- Key metrics table: endurance, range, detection range, classification accuracy (TBD), coverage per sortie
- Some values have TBD (classification accuracy) — honest about what's not yet measured

### Section 5 — Verification, Risk & Closure (5 slides)

**Slide 29: Verification Cross-Reference Matrix (VCRM)**
- Every requirement → verification method (Analysis, Demonstration, Test, Inspection)
- Highlight which are analysis-only (will need TBD field test)
- **Open:** R3_1/R3_2 field verification (task 2.17)

**Slide 30: Manufacturing & Producibility**
- Build steps: Phase 1 (flight+FPV) → Phase 2 (thermal+SBC) → Phase 3 (AI) → Phase 4 (digital downlink)
- Key dependencies: ordering → hardware arrival → bench assembly → field test
- No exotic tooling — standard 3D printer, soldering iron, heat-set insert tool

**Slide 31: Project Timeline (PV-2)**
- Gantt-style overview
- Current status: gridlocked at task 85 → ordering → hardware
- Total remaining: ~150 h hands-on + shipping leads + collection season
- **Critical path:** CDR approval → order Phase 1 → bench build Phase 1 → field test → Phase 2 → Phase 3

**Slide 32: Risk Assessment**
- Top risks:
  1. **Battery OOS** (HIGH, ~55%): BAT09 already gone; BAT10 stock-fragile
  2. **Thermal data collection** (HIGH): season/opportunity dependent, 40+ h collection
  3. **T13 shipping** (MEDIUM): long lead, Alibaba
  4. **Shutdown at range** (MEDIUM): 58.6 min is borderline on a 30 min mission

**Slide 33: Open Items (TBD / TBR / Action)**
- Remaining open items from the design phase (tasks not yet Done):
  - Caliper top-plate bolt pattern
  - Confirm T13 18mm mass with vendor (15.0g estimate sufficient)
  - Field-test thermal detection range
  - Collect deer/turkey/human LWIR training data
  - Bootstrap ML dataset assembly (BIRDSAI done, need FLIR ADAS download)
- **Key ask for Lisa:** authorization to proceed with ordering despite these open items being carried forward

---

## 3. Key Decisions Lisa Needs to Make

1. **Approve the design → unlock ordering** — This is THE decision. Everything else is secondary.
2. **Accept the $2,397 of $2,500 budget** — $103 margin is tight. Acknowledge it; propose contingency plan if prices drift.
3. **Acknowledge open-item carry-forward** — Some open items (bolt-pattern caliper, vendor mass confirmation) don't block ordering. Get explicit agreement that ordering can proceed before these are closed.
4. **Confirm failsafe behavior choices** — RTL on link loss, RTL on low battery, complete-waypoint-then-RTL on SBC failure. These are the safety-critical R6_FS_BATT / R7_FS_LINK decisions.
5. **Scope of review** — Is this a formal CDR sign-off or an informal progress review? Set expectations at the start.

---

## 4. Recommended Presentation Flow

| Segment | Slides | Time |
|---------|--------|------|
| Intro + overview | 1–4 | 5 min |
| Requirements (highlights only) | 5–7 | 5 min |
| Architecture (walk the key diagrams) | 11–16 | 10 min |
| Behavior (state machine + autonomy) | 18–19 | 5 min |
| Analyses (the numbers that matter) | 22–28 | 10 min |
| Risk + open items | 29–33 | 5 min |
| **Decision: approve to proceed** | — | 5–10 min |
| **Total** | | **~45–55 min** |

---

## 5. What This Briefing Unblocks

Approval of this CDR enables the following (in order):

1. **Ordering all Phase 1 hardware** ($1,371): airframe, RX, TX, batteries, charger
2. **Ordering Phase 2 hardware** ($958): T13 thermal, SBC, UBEC
3. **Physical build and bench test** — the first time real hardware gets assembled
4. **Field flight tests** — LOS envelope, waypoint missions, range verification
5. **Phase 3 AI pipeline** — training with real thermal data, on-target benchmarking

Every task from #16 through #83 is blocked on this decision. There are ~40 tasks totaling ~150+ h of remaining work that cannot begin until the CDR briefing is delivered and Lisa signs off.

---

## 6. Risk Flags for the Meeting

- **Task 14 export is done** but re-verify the deck opens cleanly — the Sep 15 change modified slide 14
- **Battery supply:** BAT09 (Amprius predecessor) is already out of stock. BAT10 is the single most stock-fragile line in the BOM. Every week of delay increases risk of having no flight battery.
- **T13 thermal shipping:** Alibaba — 3–6 week typical lead. This is the highest-value single line in the BOM ($700).
- **Training data collection:** Season-dependent. September is still viable for deer/turkey thermal collection in Michigan, but the window narrows as temperatures drop.