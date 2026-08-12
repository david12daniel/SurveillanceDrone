# Model Issues Log

Tracks problems found in the SysML v2 model and candidate data, the decisions
taken, and open items for review. Created 2026-06-25 while consolidating the
`analysis/*.csv` market/trade-study data into the SysML model
([model.sysml](model.sysml) schema + [candidates.sysml](candidates.sysml) data).

Status legend: **FIXED** (defect changed in-model) · **DECISION** (a modeling
choice already made — *informational, no action needed from David*) · **RESOLVED**
(a formerly-open item now closed) · **OPEN** (needs David's input) · **DATA GAP**
(missing/uncertain source data).

---

## A. Pre-existing model defects (the model never parsed before this work)

The Syside language server revealed that `model.sysml` (formerly `model.md`) had
multiple SysML v2 syntax/structural errors and so had **never been valid**. All
were fixed; each is worth a look since the model couldn't have been validated by
any tool previously.

1. **FIXED — `refines` is not a SysML v2 keyword.** ~17 requirements used
   `refines Rx;` for parent traceability. The grammar has no such keyword.
   Replaced with `subsets Rx;` (requirement specialization), which is valid and
   machine-readable. **See OPEN item B1** — confirm `subsets` captures the intent.

2. **FIXED — invalid requirement identifiers `R3.1` / `R3.2`.** A `.` makes the
   lexer read `3.1` as a real number. Renamed to `R3_1` / `R3_2`. (Prose
   references to "R3.1/R3.2" inside `doc` text were left as-is.)

3. **FIXED — missing closing braces mis-nested the whole model.** The
   `IRCamera` requirements package and the `Requirements` package were
   each missing a `}`, so `Architecture` and `Analysis` were being parsed as
   children of `Requirements::IRCamera`. Added the two missing braces.

4. **FIXED — `power` name collision (attribute vs port).** Seven part defs
   (`IRCamera`, `SBCPayload`, `FpvCamera`, `GpsModule`,
   `RadioReceiver`, `Vtx`, `ThermalVideoRecorder`) declared both
   `attribute power` and `port power`. Renamed the **port** to `power_in` and
   updated the seven `interface connect … to X.power;` lines in `Drone`
   accordingly. (The `attribute power` rollup in `totalPower` is unchanged.)

5. **FIXED — constraint expression had a trailing `;`.** `flight_time_meets_req`
   was `computed_flight_time >= 1800.0;`. A constraint body holds a boolean
   expression with no terminating `;`. Removed it.

6. **FIXED — primitive type written as lowercase `string`.** The SysML v2
   primitive is `ScalarValues::String`. Changed all `: string` → `: String` and
   added `private import ScalarValues::*;` so `Boolean`/`String`/`Real`/`Integer`
   resolve unqualified.

7. **FIXED — missing standard-library imports.** Added `private import
   ScalarValues::*;` and `private import SI::*;` to `DroneSystemModel`, and
   `private import Requirements::**;` to `Architecture` so the `satisfy`
   statements resolve the requirement names.

8. **FIXED — name collision `IRCamera` (requirements package vs part
   def).** The requirements sub-package and the architecture part def shared the
   exact name, making the type unresolvable from `candidates.sysml`. Renamed the
   **requirements package** to `CameraRequirements`. The part def keeps the name
   `IRCamera`. (Note: `README.md` prose still says "IRCamera:
   7 requirements" — that now refers to package `CameraRequirements`.)

---

## B. Open items for review (David)

1. **RESOLVED (2026-06-26) — refinement + component trace.** `refines` → `subsets`
   (§A1) is confirmed correct (David: "subsets works perfectly"). For tracing each
   requirement to the **subsystem/component** it applies to, the model already
   carries that link two ways: (a) the per-subsystem requirement *packages*
   (`CameraRequirements`, `BatterySubsystem`, …) group requirements by subsystem;
   and (b) the **`satisfy`** statements in each component `part def` point back to
   the requirements it fulfills — e.g. `Battery satisfy R4_BAT_VOLT` means that
   requirement applies to `Battery`. A query/tool over the `satisfy` web yields, for
   any requirement, the responsible component(s), and vice-versa. (An explicit
   `subject : <ComponentType>` on each requirement is the other SysML v2 idiom, but
   it would make `Requirements` depend on `Architecture` — the reverse of the
   current `Architecture` → `Requirements` import direction — risking a circular
   import, so we rely on `satisfy` instead.)

2. **RESOLVED (2026-06-26) — `analysis/*.csv` source files retired.** David removed
   the per-component market CSVs; `candidates.sysml` is the single source of truth.
   The only CSVs left under `analysis/` are `thermal_camera_analysis_expanded.csv`
   (computed results — migrated into the Analysis layer, see B3) and the
   auto-generated `flight_time_results.csv` (a script *output*, not a source).

3. **RESOLVED (2026-06-26) — thermal detection analysis now in the model.** The
   core computed columns from `thermal_camera_analysis_expanded.csv` (GSD,
   Johnson-criteria pixels-on-target, detection/recognition verdicts) are now
   expressed in `DroneSystemModel::Analysis` as `calc def`s (`GroundSampleDistance`,
   `PixelsAcrossTarget`), `constraint def`s (`DetectionCriterion` ≥1.5 px,
   `RecognitionCriterion` ≥4 px), and `analysis def`s (`ThermalDetectionCheck`
   @120 m for R3_1; `ThermalRecognitionCheck` @90 m for R3_2 / R3_CAM_RES). Per
   David, these are modeled for documentation / future execution and the **existing
   numeric method is retained**: Syside validates the structure but does not execute
   calc defs, so the per-camera numbers stay in the CSV until a SysML v2 execution
   engine is available (same limitation as the flight-time calc, C10). SBC NPU
   load-margin columns can be added the same way if wanted.

4. **PARTIALLY RESOLVED (2026-06-25) — 6 of 7 missing airframe masses now
   filled; AF5 still missing.** Masses confirmed via web research and added to
   `candidates.sysml`: AF4a 747g (darwinfpv.com product page), AF6a 667g /
   AF6b 672g (RaceDayQuads listing; BNF with O4 Pro + GPS + ELRS RX = 672g;
   PNP+GPS approximated at 672 − 5g RX = 667g), AF7 597.5g (fpv24.com + multiple
   sources), AF9a 402g (Oscar Liang review), AF10 672g (same DeepSpace ROC7
   hardware as AF6b). **OPEN — AF5 (EMAX Hawk 7 BNF) needs a decision.** Research
   (2026-06-26) confirmed the EMAX Hawk ships in 7/8/9/10-inch sizes with "DC"
   (deadcat) and "X" frame geometries; the ~890 g (X) / ~920 g (DC) figures David
   found are for the **10-inch** version. AF5 is currently modeled as the **7-inch**
   Hawk 7 (propSize_in = 7), for which a reliable as-built mass is still not
   published (EMAX's page omits the spec table; a 7-inch BNF would be ~450–550 g,
   not ~900 g). **ACTION (David, 2026-06-26):** David is contacting EMAX to confirm
   the as-built mass of the 7-inch Hawk 7 (and, for reference, the 10-inch X 890 g /
   DC 920 g variants). AF5 stays modeled as 7-inch (propSize_in = 7) and skipped by
   the sweep until that mass is provided.

5. **RESOLVED (2026-06-26) — real per-motor thrust now drives feasibility.** Added
   `Airframe.maxThrustPerMotor_g` and bound it from manufacturer/thrust-table data:
   AF1 & AF7 2700 g (GEPRC 2806.5 1350KV), AF2a/b/c 2800 g (Axisflying C287 2807.5
   1350KV, ">2.8 kg"), AF3a/b 2933 g (iFlight XING-E 2809 800KV, confirmed),
   AF9a 1488 g (DarwinFPV 2507 1800KV @4S, confirmed). **RESEARCH-SOURCED
   (prop-dependent, approximate):** AF6a/b & AF10 2000 g (DeepSpace Redline 2807
   1350KV, ~1.9–2.0 kg @6S 7"), AF8a/b 2000 g (iFlight XING2 2809 1250KV @6S 7";
   ~2.5 kg @8"), AF4a 3245 g (DarwinFPV 2812 1100KV @6S 9" Gemfan 9045-3, full
   throttle — matches AF4a's actual prop). The sweep's
   `flyable`/throttle check now uses
   `maxThrustPerMotor_g` when present, falling back to the prop-size heuristic only
   if unset (AF5 only). **Caveat to watch:** the old prop-size heuristic badly
   *under-rated* 7-inch LR motors (~1750 g vs real ~2500–2800 g), so it was making
   heavy LR builds look less flyable than they are; the bound thrust corrects that.
   Treat the EST values as ±15 % until checked against full thrust tables. Rated
   per-frame MTOM is still unbound — thrust-to-weight (via `maxThrustPerMotor_g`) is
   used instead.

7. **OPEN (2026-07-01) — FC firmware choice: ArduPilot Copter vs PX4.**
   The BLITZ F7 on the Chimera9 ECO (AF3a) supports both ArduPilot Copter and PX4.
   Both satisfy the waypoint + MAVLink requirements; the choice affects GCS setup
   (Mission Planner / QGroundControl tuning profiles) and the Phase 3 SBC MAVLink
   integration. `AF3a.fcFirmware` is set to `"TBD"` in `candidates.sysml` until this
   is decided. **Action needed:** pick ArduPilot or PX4 before Phase 1 first flight
   (it is a configuration choice, not a procurement item).

6. **RESOLVED (2026-06-25) — real `Battery` candidates now in model.**
   `Architecture::Battery` was extended with `name`, `chemistry`, `cells_s`,
   `capacity_mAh`, `nominalVoltage` (`ISQElectromagnetism::ElectricPotentialDifferenceValue`),
   `usableDoD`, `cellModel`, `maxContinuousDischarge_A`, and `connector`. 21 real
   Li-ion battery candidates (BAT01–BAT21) were added to `candidates.sysml`
   (`BatteryCandidates` package) covering all 8 Li-ion capacity/cell-count types
   capable of >50 min hover. The flight-time script now reads real battery candidates
   directly from `candidates.sysml` via `load_model()`, falling back to the generic
   grid only if no Battery candidates are present. Voltage note: Upgrade Energy uses
   21.6 V/14.4 V (3.6 V/cell); Lumenier/iFlight/GNB/Pyrodrone/DOGCOM use
   22.2 V/14.8 V (3.7 V/cell average). 4S 12000mAh has only one confirmed product
   (Lumenier NAV Amprius, sold out as of 2026-06); alternatives exist at 4S 10Ah.

7. **RESOLVED (2026-08-11) — R3_CAM_FOV restated as a ground-swath floor; new mission
   requirement R9 (area coverage) added.** *(Was OPEN 2026-07-29: the ≥30° HFOV form was
   violated by the selected 18 mm lens.)*
   The thermal lens was changed **13 mm → 18 mm** (`T13`, `candidates.sysml`; see
   `SELECTED_COMPONENTS.md`, `BOM.md`, `analysis/thermal_detection_offnadir_analysis.md`).
   18 mm HFOV = **24.1°**, below the old R3_CAM_FOV ≥30°. This is a **deliberate trade**: the
   ≥30° figure was a *coverage/swath* floor, not a flight/controllability requirement (the FPV
   camera flies the drone, never the thermal), and 18 mm buys better on-target resolution
   (8.3 px @90 m) plus recognition at a 45° oblique tilt. All other camera requirements
   still pass (R3_CAM_RES improves).

   **Resolution (David approved 2026-08-11).** The old form stated a bare lens angle rather
   than the ground coverage it was meant to guarantee, and conflated a *sensor* property with
   a *route-planning* one. Four changes to `model.sysml`:
   - **NEW `R9` (mission requirement, hard):** survey a contiguous area of **at least 30 acres
     (12.1 ha) per sortie** at the R1 altitude / R2 speed with a 20% reserve.
   - **NEW `R10` (mission requirement, stretch):** **60 acres (24.3 ha) per sortie** — reported,
     not asserted, mirroring the R6 / R8 hard-versus-stretch pattern.
   - **`R3_CAM_FOV` restated (camera):** ≥ **42 m** across-track ground swath at 120 m AGL
     (`swath = 2·alt·tan(HFOV/2)`). Now `subsets R9` (was `R3`), since swath's real driver is
     area coverage, not detection performance (which R3_CAM_RES owns). The selected T13 @18 mm
     yields **51.2 m → 22% margin**, so the def-level `satisfy R3_CAM_FOV` on `IRCamera` is
     **true again** and was left in place.
   - **NEW `R4_GCS_SWEEP_SPACING` (flight-planning software):** generated line spacing
     ≤ 90% of camera swath (≥10% overlap). `subsets R9`; satisfied by `ConductSortie.planRoute`
     (allocated to QGroundControl). This is where the "no gaps between passes" obligation
     actually belongs — it is operational, not a sensor property.

   **Why 30 acres hard / 60 stretch (and not 60 hard).** A 60-acre hard floor would have made
   **R9 outrank R6 as the endurance driver**: at 2.23 m/s and 46.1 m spacing, 60 acres needs
   ≈5,270 m of swept track ≈ **49 min** usable endurance, well above the R6 30-min floor — so a
   design that merely satisfied R6 would cover only ~36.6 acres and *fail* R9. Setting the hard
   requirement at **30 acres** keeps R6 governing: R6's 30 min yields ~3,210 m of track →
   **36.6 acres**, clearing R9 with margin. The 60-acre case moves to **R10**, which needs
   ~49 min — inside the **R8** 60-min stretch (~73.2 acres). Hard and stretch now pair
   coherently: **R6↔R9** and **R8↔R10**.

   *Consistency check:* both pairs (30 ac @ 30 min, 60 ac @ 60 min) share the same
   area-per-minute ratio and therefore derive the **same 42 m swath floor** — the R3_CAM_FOV
   value is stable whether taken from the hard or the stretch pair.

   *Derived artifacts regenerated:* `analysis/requirements_traceability.csv` (54 requirements).
   *No `model_community_balanced.sysml` change needed* — that export deliberately omits the
   Requirements pillar and all `satisfy` statements (see its header), and this change touched
   nothing else. *Still to sync:* the SSS export `REQUIREMENTS_EXPORT_26_06_30.md`.

8. **RESOLVED (2026-08-11) — the two SSS §3.7 failsafe parameter sets captured as
   requirements: new `R6_FS_BATT` / `R7_FS_LINK`.** *(Closes TASKS.md 0.2/0.3; both had
   sat as "TBD"/"open" since the requirements were first written.)*

   **Source.** An OpenClaw nightly-agent session (WSL clone of this repo, uncommitted)
   had already worked out the low-battery reserve policy decision (0.3) in
   `analysis/low_battery_reserve_analysis.md` and a companion `params_sets.py`
   (ArduPilot parameter values for both failsafes). That file was ported into this
   (Windows) checkout's `analysis/` — it did not exist here before. David reviewed the
   values 2026-08-11 before they were written into the model.

   **`R6_FS_BATT` (subsets `R6_BHV_RTL_RESERVE`):** `BATT_LOW_MAH = 700` mAh (30% margin
   over the 555 mAh bare-RTL cost of the worst-case 2.8 km return (R7) at `RTL_SPEED =
   12` m/s — the multirotor power-bucket minimum; a slow 2.23 m/s return would need
   ~1950 mAh instead), `BATT_CRT_MAH = 350`, `BATT_LOW_VOLT = 20.4` V (3.4 V/cell),
   `BATT_CRT_VOLT = 19.2` V (3.2 V/cell), `BATT_FS_LOW_ACT = 2` (RTL),
   `BATT_FS_CRT_ACT = 1` (Land), `BATT_MONITOR = 4` (fuel level + voltage). Static,
   worst-case-distance reserve — **not** distance-adaptive.

   **`R7_FS_LINK` (subsets `R7_BHV_LINKLOSS_RTL`):** `FS_THR_ENABLE = 1` (RTL on
   throttle failsafe), `FS_THR_VALUE = 900` (ELRS RX outputs a below-range throttle
   value on TX signal loss; ArduPilot reads that as link loss), `FS_OPTIONS = 0` (no
   continue-on-failsafe exceptions — RTL fires unconditionally, even mid-investigation
   in GUIDED mode).

   **Two design forks surfaced with David during review, both resolved to the simpler
   option for now:**
   - **Low-battery: static vs. distance-adaptive reserve.** David asked whether the
     reserve could shrink dynamically as the vehicle nears the launch point, instead of
     always reserving for the worst-case 2.8 km — a real efficiency gain (a drone close
     to home with the static 700 mAh reserve still has far more margin than it needs)
     but it requires new software (SBC or FC Lua logic computing energy-needed-to-return
     from live GPS distance each cycle), not a firmware parameter, so it doesn't fit the
     "config-as-requirement" scope of 0.2. **Decision: keep `R6_FS_BATT` static for
     Phase 1** (zero new software, and `BATT_CRT_MAH` remains an absolute hard-floor
     backstop regardless); track the dynamic version as a new Phase 3 follow-up —
     **TASKS.md D2.17** (Mission Control task id 142).
   - **Link-loss: abort mid-investigation vs. finish it first.** `FS_OPTIONS` has a bit
     to continue the current GUIDED action on RC failsafe (finish classifying before
     RTLing) instead of aborting immediately. **Decision: unconditional abort
     (`FS_OPTIONS = 0`)** — simpler and safer; matches the values already in the
     ported analysis.

   **Other `model.sysml` changes:** `fcSoftware` now also `satisfy`s `R6_FS_BATT` /
   `R7_FS_LINK` (in addition to the existing `R6_BHV_RTL_RESERVE` /
   `R7_BHV_LINKLOSS_RTL`). The now-stale "TBD"/"open requirement" doc text was updated
   in four other spots that referenced the gap: `R6_BHV_RTL_RESERVE`'s doc, the
   `LinkLossDetected`/`LowBatteryReached` attribute defs (Behavior pillar), and the
   `HandleLinkLossUC`/`HandleLowBatteryUC` objective docs (UseCases veneer).

   *Derived artifacts regenerated:* `analysis/requirements_traceability.csv` (56
   requirements). *No `model_community_balanced.sysml` change needed* — same reasoning
   as item 7 above (Requirements pillar + `satisfy` statements are excluded from that
   export). TASKS.md 0.2 and 0.3 marked done; a new D2.17 task added for the deferred
   dynamic-reserve idea.

9. **RESOLVED (2026-08-12) — UC-11 operator override authority modeled and
   implemented.** *(Closes TASKS.md 0.5 / Mission Control task #8; decision itself
   was made 2026-08-06 in `analysis/operator_override_UC11.md`, David approved
   proceeding to modeling + implementation 2026-08-12.)*

   **The decision (unchanged from the 2026-08-06 analysis):** the operator can abort
   an autonomous investigation, and the mechanism is a plain QGC flight-mode switch —
   not a dedicated app input. Chosen because it works even if the SBC mission app has
   crashed, needs zero new UI, and the operator already knows how to use it.

   **`model.sysml` changes (Behavior pillar):** new `attribute def OperatorOverride`
   trigger signal (external/unmodeled-sender, same category as `ArmCommand`/
   `LaunchCommand` — it originates with the operator, not an onboard action def);
   new `FlightMode.flying.loiterToCruiseOnOverride` transition (`first loiter, accept
   overrideCmd : OperatorOverride, then cruise`), sitting alongside the existing
   `loiterToCruise` (on `InvestigationComplete`); new `UseCases::OperatorOverrideUC`
   (UC-11), modeled — like UC-9/UC-10 — as a standalone exceptional-flow use case def
   realized by a `FlightMode` transition and deliberately not `include`d by
   `ConductSortieUC`, but *with* an `actor operator : Operator` (unlike UC-9/UC-10,
   this one is operator-initiated, not a system-internal failsafe). Updated the two
   stale "UC-11 not yet modeled" doc comments (`ConductSortie`, `UseCases` package
   header). Mirrored the state-machine pieces (not `OperatorOverrideUC` — `UseCases`
   is excluded from that export) into `model_community_balanced.sysml`.

   **Scope note — RTL/LAND are NOT the override trigger.** The original CONOPS table
   in the analysis doc listed "operator switches to RTL" as an override case
   resuming SWEEP, but that would fight the *already-modeled and tested* failsafe
   stand-down (`flyingToRtlOnLinkLoss`/`flyingToRtlOnLowBattery`-style handling): if
   the operator explicitly commands RTL, the vehicle should go fully passive, not
   silently resume autonomous SWEEP mid-return. `OperatorOverride` therefore covers
   every non-GUIDED mode *except* RTL/LAND (including a direct switch back to AUTO),
   which is exactly what fires in the software (see below) since the RTL/LAND check
   in `mission_app.py`'s `step()` already runs first and intercepts those two modes.

   **`DroneMissionApp` changes (the live repo — `SurveillanceDrone/analysis/
   autonomy_sim/` is the frozen prototype, not touched):**
   - `mission_app.py` — the `INVESTIGATE` handler now checks `fc_mode != GUIDED` as
     its first line; on a mismatch it alerts, logs an `("operator_override",
     <mode>)` event, and transitions to `SWEEP` (which already gates on `fc_mode ==
     AUTO`, so re-entry on a switch back to AUTO needs no extra logic — R-UC11-2 from
     the analysis doc falls out for free).
   - `alerts.py` — new `OVR` `STATUSTEXT` kind (`override()` constructor,
     `SEV_OVERRIDE = MAV_SEVERITY_INFO` per the analysis doc's severity matrix,
     `parse()` allow-list). Deliberately reuses the existing D2.10 structured
     `KIND|species|lat,lon|alt|conf` wire schema rather than the illustrative
     free-text `"[MISSION] OPERATOR_OVERRIDE"` string sketched in the original
     analysis draft — that draft predates the structured-schema task (D2.10), and
     the structured form is parseable/consistent with `DET`/`CLS`/`UNK`.
   - `test_autonomy_loop.py` — new `test_operator_override_during_investigate`
     (drives a real `FakeFC`, forces `STABILIZE` mid-`INVESTIGATE`, asserts the
     override event, the `OVR` alert, and no spurious `AUTO` mode request). All 16
     tests pass. Note for whoever builds D2.13: the override path never reaches
     `PASSIVE`, so a `run()`-in-thread test must bound `max_ticks` tightly or the
     background thread can outlive a short `join()` timeout — cost me one flaky
     iteration before landing on `max_ticks=100`.

   **Not done:** field-testing this against real ArduPilot SITL (tracked as a
   D2.13 follow-up, TASKS.md); no new `R#` requirement was added (`R-UC11-1..4` in
   the analysis doc are implementation notes, not formal model requirements), so
   `analysis/requirements_traceability.csv` needed no regeneration.

---

## C. Modeling decisions (SysML v2 representation choices)

1. **DECISION — sub-units absent from the SI library.** `mW`, `mA`, `mK`, and
   `µm` are not predefined unit symbols in the bundled SI library, so values are
   bound in base SI units with the original in a comment: e.g. `100 mW` →
   `0.1 [W]`, `120 mA` → `0.12 [A]`, `50 mK` → `0.05 [K]`, `12 µm` →
   `0.012 [mm]`. (Predefined and used directly: `g, mm, cm, km, nm, m, s, W, V,
   A, K, Hz`.)

2. **DECISION — absolute temperature in °C kept as `Real`.** Celsius is an
   offset unit that the bracket-unit notation doesn't handle cleanly, so
   `operatingTempMin_C` / `operatingTempMax_C` are unitless `Real` (documented).
   NETD (a temperature *difference* in mK) uses `TemperatureValue` as `[K]`.

3. **DECISION — quantity-kind type names** (verified against the bundled ISQ
   library): voltage = `ISQElectromagnetism::ElectricPotentialDifferenceValue`;
   current = `ISQBase::ElectricCurrentValue`; specific energy =
   `ISQThermodynamics::SpecificEnergyValue` (NOT `ISQMechanics::SpecificEnergyValue`
   — that type does not exist; battery-specific energy is a thermodynamic quantity).
   Frequency would be `ISQSpaceTime::FrequencyValue` (rates/frame-rates modeled as
   `Real` with a `_Hz`/`_fps` suffix instead, to avoid over-constraining).

9. **FIXED (2026-06-25) — `ISQMechanics::SpecificEnergyValue` does not exist.**
   `Battery.specificEnergy` used the wrong namespace. Corrected to
   `ISQThermodynamics::SpecificEnergyValue`.

10. **RESOLVED (2026-06-25) — full flight-time verification now modeled
    parametrically.** Earlier blocker: the `'/'` operator in
    `QuantityCalculations.sysml` returns the generic `ScalarQuantityValue[1]`, so
    `energy / power` cannot be assigned to a narrower `ISQBase::DurationValue`
    attribute (the prior `FlightTimeCalc`/`ScoreCalc` *constraint* defs also
    misused `constraint def`, which must return Boolean). **Fix — three changes:**
    (a) the calculations are now `calc def`s (the correct SysML v2 construct for a
    parametric function with a `return`), not constraint defs;
    (b) the flight-time result is typed `ScalarQuantityValue` (matching the `'/'`
    return), and requirement checks compare it dimensionally — `flightTime >= 1800
    [s]` type-checks because the comparison operators take two
    `ScalarQuantityValue`s and return Boolean;
    (c) scoring extracts a magnitude via `QuantityCalculations::ToReal`.
    The Analysis package now contains: `calc def FlightTimeCalc` (energy/power →
    flight time), `calc def ScoreCalc` (flight time / cost → endurance-per-dollar),
    `constraint def`s `BudgetLimit` (R4), `MinFlightTimeReq` (R6, ≥ 1800 s),
    `StretchFlightTimeReq` (R8, ≥ 3600 s), and two `analysis def` cases —
    `MinFlightTimeCheck` (subject = system; asserts R4 + R6, reports R8, returns a
    boolean verdict) and `TradeSpaceEvaluation` (subject = candidate; computes the
    score and asserts the budget). All validate cleanly under Syside.

    **Convention:** battery energy must be expressed in joules `[J]` (`Wh × 3600`)
    so `energy [J] / power [W]` reduces to seconds; `Wh` is not a predefined SI
    symbol. Note Syside validates the parametric *structure* but does not execute
    calc defs to produce numeric verdicts — numeric evaluation still needs an
    execution engine (e.g. the SysML v2 API/Pilot Implementation or a tool bound
    via `AnalysisTooling::ToolExecution`).

4. **DECISION — cost ranges bound to a representative value.** Where a CSV gave a
   price range (e.g. "240-330"), a single representative `cost_USD` is bound and
   the full range noted in a trailing comment.

5. **DECISION — thermal lens variants collapsed.** `candidates.sysml` models the
   16 base thermal modules (T1–T16) from `thermal_camera_candidates.csv`, not the
   per-lens rows of the expanded analysis CSV. Lens choice is a configuration of
   the module and belongs to the Analysis layer (see B3).

6. **DECISION (updated 2026-06-26) — integrated digital cam+VTX: single part, no
   separate VTX, range-checked.** DJI O4/O3 and Walksnail units are camera+VTX
   combos modeled as `FpvCamera` candidates (D1–D3) and intentionally NOT duplicated
   as `Vtx` candidates (`VideoTransmitterCandidates` holds the analog
   VTX only). **No-double-VTX rule:** a configuration selecting an integrated
   cam+VTX (`vtxTypeRequired` = "Integrated…") must NOT also include a separate
   `Vtx` — its VTX mass and cost are already in the integrated unit. In
   the flight-time sweep this never occurs (FPV is held at a lightest representative
   and the VTX is swept separately), but the rule is documented for any future build
   that selects D1–D3. **Range vs R7 (2.8 km):** a new `FpvCamera.maxRange`
   attribute was added and populated for D1–D3 from research — DJI O4 Pro ~20 km,
   DJI O3 ~10 km, Walksnail Avatar ~4 km practical. **All three pass R7**; none are
   excluded on range (Walksnail is marginal). Rule going forward: if a future
   integrated cam+VTX cannot meet 2.8 km, that camera is not viable and is excluded.

7. **DECISION — new `part def TelemetryGroundLink`.** `telemetry_rx_candidates.csv`
   had no home in the architecture (telemetry is routed through the
   `RcTx` in the baseline). Added a definition to hold these
   options; it is **not** composed into `AerialObservationSystem`.

8. **DECISION (2026-06-25, updated 2026-06-25) — high-fidelity flight-time model as
   a model-integrated script.** `analysis/flight_time_model.py` implements a
   momentum/actuator-disk endurance model (hover induced power + Glauert
   forward-flight induced velocity + parasitic drag + drivetrain efficiency +
   usable battery energy), the same physics family as eCalc/xcopterCalc. It is
   *integrated with the model*: it parses `candidates.sysml` for airframe, payload,
   and **real battery candidates** (BAT01–BAT21), runs a **holistic configuration
   sweep** (139,104 raw pairings, filtered to 60,480 interface-compatible "real"
   configs — see C11: airframe × battery × SBC × VTX × thermal camera × DVR fully
   crossed; sub-1 W peripherals FPV/GPS/RX held at lightest representatives), and
   writes results back as
   `analysis/flight_time_results.csv` (every instance) plus a SysML v2 **instance
   table** (`analysis/flight_time_instances.sysml`) and an `.md` summary. Falls
   back to a generated generic grid only if no Battery candidates are found.

   **Component-inclusion handling:** airframe-bundled VTX/FPV/GPS/RX add power only
   (mass already in the airframe weight); non-bundled peripherals add mass + power.
   RX power is derived from `currentDraw × 5 V` (RX candidates spec current, not
   power). Physics assumptions (FoM, η, ρ, C_d, frontal-area model) live in
   `PhysicsParams`; results are first-order **comparative** estimates. The *power
   bucket* in the output (cruise/wind endurance > hover) is real (translational
   lift), not an error. See OPEN items B4–B5 and DATA GAP below for gaps surfaced.

11. **DECISION (2026-06-26) — interface compatibility layer + sweep filtering.**
    Added a `Compatibility` sub-package to `model.sysml`'s `Architecture` package
    that declares, as formal SysML v2, which component pairings form a *real*
    configuration: typed `port def`s (PowerSourcePort/PowerSinkPort,
    VideoSourcePort/VideoSinkPort, RfSourcePort/RfSinkPort), `enum def`s
    (VideoFormat, RfBand), `constraint def`s (BatteryVoltageCompatible,
    VideoFormatCompatible, RfBandCompatible), and `interface def`s
    (BatteryPowerInterface, VideoLink, RfLink) binding source↔sink ports and
    asserting the matching constraint. Syside validates the *structure*; it does
    not execute the constraints, so the actual pruning lives in
    `flight_time_model.py` — the same READ-model / EXECUTE-in-Python split used by
    the flight-time calc. New `Airframe` attributes `minCells_s`/`maxCells_s`
    carry the ESC/motor cell-count window (researched per airframe: all candidates
    are 6S **except** the DarwinFPV 129 / AF9a, which is 3–5S — 2507 1800KV motors
    rated ≤5S, 4S recommended). The sweep now drops:
      • **P1 battery↔airframe** — `cells_s` outside `[minCells_s, maxCells_s]`
        (42,336 configs; e.g. the previously top-ranked KOLAS7 + 4S 12Ah Amprius,
        which is **not real** because KOLAS7 is 6S-only).
      • **V2 thermal↔DVR** — a thermal whose video output can be recorded by no
        DVR is dropped (initially CVBS-only; relaxed in **C12** with digital DVRs).
    Result (initial, CVBS-only DVRs swept): 139,104 → 60,480 real configs.
    **Superseded by C12** — once digital DVRs were added and the DVR was removed
    from the flight-time calc, the final figures are 14,112 real configs with the
    baseline KOLAS7 + 6S 12Ah Amprius → 74.6 min.

    The R1/R2 RF links and D-series data links are declared in the model for
    completeness but do not prune the current sweep (all VTX/VRX are analog 5.8
    GHz; RX/TX are held at representatives).

12. **DECISION (2026-06-26) — digital DVRs, DVR staging, and last-mile port typing.**
    Refines C11 after review:
    - **Digital DVR candidates added** (`candidates.sysml` DVR7-9): ezcap273
      (HDMI, 180 g), Zowietek megaDVR III (HDMI/SDI, ~430 g est), and the Monster
      UVC Recorder (standalone USB-UVC, specs **estimated** — emerging 2026
      product). DVR1-6 remain the CVBS analog FPV DVRs. This removes the CVBS-only
      exclusion: USB-output thermals (FLIR Lepton, USB-UVC modules) are recorded by
      DVR9, so **14 of 16 thermals are now viable**. Only T7 (raw SPI) and T16 (raw
      CMOS) stay excluded — no standalone recorder can read a raw sensor bus; those
      require SBC integration and are effectively SBC-stage-only cameras.
    - **DVR excluded from max-flight-time.** The headline endurance is the SBC-
      stage build (Phase 4: SBC present, no DVR). Per the staged plan the DVR is
      used only in the earlier (Phase 1-3) stages, so it is no longer a flight-time
      sweep dimension and its mass/power are excluded from the endurance calc. It is
      still required for earlier-stage camera↔DVR compatibility (each thermal must
      have a compatible recorder) and still contributes to overall cost (the SysML
      model's `totalCost` includes `drone.recorder.cost_USD`). The flight-time CSV
      carries the lightest compatible DVR per thermal for reference only. Effect:
      the sweep no longer crosses DVR (139,104 → 23,184 raw pairings); after P1
      (7,056) and V2 (2,016) pruning → **14,112 real configs**; baseline 73.8 →
      **74.6 min** (DVR mass removed, SBC retained).
    - **Last-mile port typing.** The power/video/RF ports on the component part
      defs are now typed to the Compatibility port defs (`PowerSourcePort`/
      `PowerSinkPort`, `VideoSourcePort`/`VideoSinkPort`, `RfSourcePort`/
      `RfSinkPort`), and the battery-power + four video connects in
      `Drone` are typed to their interface defs (`BatteryPowerInterface`,
      `VideoLink`). Data (UART/MAVLink) ports and the GNSS antenna port stay untyped
      (no compat rule); the wireless RF connects in `AerialObservationSystem`
      keep `connection connect` (their ports are typed).

13. **DECISION (2026-06-26) — cost in the sweep + laptop-based GCS.** The flight
    model now computes cost alongside endurance:
    - **Per-config cost** (drone + total system) with bundled-inclusion: a BNF/PNP
      airframe's price already includes its VTX/FPV/GPS/RX, so those add $0; the DVR
      IS included (earlier-stage part, R4 cost). New CSV columns
      (`*_cost_usd`, `drone_cost_usd`, `gcs_cost_usd`, `total_system_cost_usd`,
      `endurance_per_1000usd`, `meets_budget_r4`) + SysML instance attrs. Outputs
      added: `flight_time_value_ranking.md` (top-100 by endurance-per-dollar) and
      `cost_vs_flighttime.png` (scatter). **All top-100 endurance configs are far
      under R4** ($820–$1,360 system; ~$1,100–1,700 headroom).
    - **GCS = the laptop, two-tier** (David's decision, refined 2026-06-27). The
      laptop is the ground station. **PRIMARY (Phase 2+):** an ELRS USB dongle
      (control + telemetry) + analog VRX/capture (live video) — all through the
      laptop. **BACKUP / Phase 1:** a cheap handheld ELRS radio for manual control
      if the laptop link fails. **Model updated** (`model.sysml`): `TelemetryGroundLink`
      gained an `rf_out : RfSourcePort` (combined ELRS control+telemetry) and is now
      composed into `GCS` as `laptopLink` (primary); `rcTx`
      (RcTx) is documented as backup; `subTotalCost` now =
      laptopLink + rcTx + videoRx + capture; `AerialObservationSystem` wires
      the dongle as primary control/telemetry (drone RX ↔ laptopLink → laptop) with
      the radio path retained as backup. The sweep's GCS cost basis = cheapest
      integrated handheld radio (backup) + cheapest standalone ELRS dongle
      (`extraHardwareNeeded = None`, e.g. TLM2 $16) + cheapest 5.8 GHz VRX+capture
      (VRX1 $40) ≈ **$121** (was a $47/$56 estimate).
    - **Range (R7 / R4_GCS_RANGE) — BOTH links hard at 2.8 km** (David, 2026-06-27:
      video is a hard requirement, not best-effort, so `R4_GCS_RANGE` stands as
      written). **Control + telemetry (ELRS):** trivially met (2.4 GHz: 25 mW =
      3.5–4.6 km, 100 mW = 10 km; all onboard RX candidates ≥ 3 km; dongles
      TLM2/TLM3 flagged range-OK). **Video (5.8 GHz analog):** all 10 VTX candidates
      were checked — every one is ≥ 4.0 km (V1/V3/V5/V8/V10 = 4.0; V7 = 5.0; V2/V4 =
      6.5; V11 = 7.0; V6 = 8.0), and the integrated cam+VTX (D1–D3 = 4–20 km) and
      bundled VTX all pass — so **no VTX candidate was removed**. The binding element
      is the **ground VRX + antenna**: VRX1 is rated exactly 2.8 km *and only with a
      patch/directional antenna* (zero margin) — a better ground antenna is
      recommended for headroom. Going forward, any VTX with maxRange < 2.8 km is not
      viable and must be dropped.
    - **Better-range ground VRX (market research 2026-06-27).** Because the video
      link is gated by the ground receiver, added margin options to `candidates.sysml`:
      **VRX6 — Skydroid 150CH true-diversity UVC** (~$45, ~5 km, dual-antenna,
      laptop-direct via USB/UVC, confirmed working on macOS via QuickTime) and
      **VRX7 — TBS Fusion + UVC capture** (~$137, ~8 km, top-tier sensitivity, macOS
      via the capture dongle). A high-gain **patch antenna (9–13 dBi)** is the single
      biggest range lever. The sweep's GCS cost basis now selects the cheapest VRX
      with **≥ 4 km margin** (Skydroid $45) rather than the zero-margin VRX1 (2.8 km),
      so GCS ≈ **$126** (radio $65 + dongle $16 + diversity VRX $45). VRX1 remains a
      budget floor option but is no longer the costed default.

14. **DECISION (2026-06-27) — model views added (`DroneSystemModel::Views`).** A
    fourth sub-package holds four SysML v2 `view def` + `view` presentations that
    `expose` model slices by stakeholder concern: `operationalMission`
    (Requirements + `AerialObservationSystem`), `logicalArchitecture`
    (system/drone/GCS decomposition), `interfaceBehavior` (the `Compatibility`
    layer + airborne connections), and `systemVerification` (the `Analysis` layer).
    Syside validates the structure; diagram/table rendering needs a SysML v2 viewer
    (none in the free Syside extension). **Lesson:** `verification` is a reserved
    keyword (like `interface`, `view`, `analysis`, `requirement`) — a bare usage
    named `verification` fails to parse ("Expected ';'"), so the usage is named
    `systemVerification`. View-def names (e.g. `VerificationView`) are fine since
    they don't collide. Optional future enhancement: add `viewpoint def`s
    (stakeholder concerns + `frame`/`require`) and `rendering`/`filter` clauses.

15. **DECISION (2026-06-28) — ground VRX matched per-airframe to the VTX video
    format.** Previously the sweep added a single fixed analog VRX (Skydroid $45)
    to every config's GCS cost, which silently mis-costed the airframes that
    bundle a **digital** air unit (DJI O3/O4, Walksnail) — an analog 5.8 GHz VRX
    cannot decode those. The flight-time model now derives each airframe's VTX
    video standard (`Airframe.vtx_format`, from `vtxModel`/`fpvCameraType`/
    `purchaseType`; a swept VTX uses its own format) and **matches the cheapest
    compatible ground receiver per format** (`vrx_by_format`, range ≥ 4 km):
    **CVBS → Skydroid 150CH ($45), DJI → DJI Goggles N3 ($230), Walksnail →
    Walksnail Avatar HD Goggles L ($199)**. Added `candidates.sysml` VRX8 (DJI
    Goggles N3) + VRX9 (Walksnail Goggles L); new CSV columns `video_format`,
    `gcs_vrx_name`, `gcs_vrx_cost`; `gcs_cost_usd` is now per-config. GCS = base
    **$81** (backup radio + ELRS control dongle) + matched VRX. **Effect:** analog
    frames unchanged ($126 GCS, baseline AF9a still $1,505); the 7 DJI-air-unit
    frames (AF1c, AF2c, AF6a, AF6b, AF10, AF12, AF14) each +$185 system ($311
    GCS). Endurance ranking unaffected (the VRX is ground-side). **AF12 (CineLR 7
    O4) now tops out at ~$2,497 — essentially at the R4 $2,500 cap.** NB: digital
    frames realistically use **goggles** as the ground receiver (HDMI/USB out to a
    laptop), not a laptop UVC dongle — so a DJI/Walksnail choice partly walks back
    the pure "laptop-is-the-GCS" model (still laptop for control via ELRS). All 447
    configs re-audited: **0 compatibility violations**.

16. **DECISION (2026-06-29) — physical-integration layer ("does it fit?").** The
    trade study now checks whether the **SBC physically fits** on each airframe,
    not just whether the config is electrically compatible and flyable. New
    attributes were added to the protected `model.sysml` defs (with David's
    approval): `Airframe.payloadDeckLength_mm` / `payloadDeckWidth_mm` /
    `payloadCapacity_g` / `batteryMount`, and `Battery.length_mm` / `width_mm` /
    `height_mm`; values are bound per-unit in `candidates.sysml`. **Most deck dims
    are ESTIMATES** (`deckLen ≈ 0.27·wheelbase`, `deckWid ≈ 0.17·wheelbase`,
    calibrated so a 9" Chimera9 → ~110×70 and a 7" DarwinFPV129 → ~75×50); battery
    envelopes are an upright-21700/18650 cell-grid estimate validated against the
    one confirmed pack (BAT04 4S 12Ah Amprius = 80×45×70 mm). `flight_time_model.py`
    parses these + the SBC/thermal `dimensions` strings and emits a **3-tier
    verdict** (`sbc_fit_status` = fits / marginal / no_fit; tolerant of ±12 mm
    estimate error) plus `deck_margin_mm`, `payload_weight_g`, `physical_fit_note`,
    and new CSV columns. The thermal cam (17×17×35 mm, nose-mounted) is never the
    constraint — the **90×62 mm NanoPi M5 footprint** is. **Result (T13+SBC3,
    657 configs): 45 fit / 606 marginal / 6 no-fit.** Only the **9–10" frames
    (AF3a/b Chimera9, AF15 Nazgul XL10) fit cleanly**; the 7.5–9" and larger 7"
    frames are **marginal** (need a snug/custom 3D-printed deck); **AF9a DarwinFPV
    129 — the endurance/value winner — is NO-FIT** (90×62 SBC vs ~75×50 deck;
    needs a larger frame or belly pod). The check is **informational, not a filter**
    (configs are flagged, not dropped) so the fit tension stays visible in the
    ranking. Still 0 compatibility violations.

17. **DECISION (2026-06-29) — airframe LOCKED = iFlight Chimera9 ECO (9").** David
    selected the Chimera9 ECO (`AF3a` PNP / `AF3b` BNF) — best endurance-per-dollar
    of the SBC-capable frames **and** it fits the 90×62 mm SBC cleanly (its ~110×70
    deck, 8 mm spare; §C16). Enforced by `FIXED_AIRFRAME_IDS = ["AF3a","AF3b"]` in
    `flight_time_model.py` (sweep now = 30 Chimera9 configs, the open variable being
    the battery + PNP/BNF). PNP-vs-BNF sub-choice still open (PNP = best value; BNF
    bundles a TBS Crossfire Nano RX). **Created [`SELECTED_COMPONENTS.md`](SELECTED_COMPONENTS.md)
    as the single authoritative record of locked vs open selections** (the prior
    state — locks buried in `FIXED_*` constants + git-ignored agent memory — was not
    visible to outside collaborators). `CLAUDE.md` now points to it first.

18. **DECISION (2026-06-30) — Phase-1 video on the laptop + ground antenna + RF link
    budget.** Pulled the video downlink forward into Phase 1 (the Chimera9 PNP already
    bundles the air-side analog VTX + FPV cam, so only the **Skydroid 150CH UVC VRX**
    (`VRX6`, laptop-direct UVC) is procured). Added a new **`part def Antenna`** to
    `model.sysml` (gain/band/polarization/beamwidth) composed into `GCS`
    as `groundAntenna` (`satisfy R4_GCS_RANGE`), and a single candidate **`PATCH1` =
    TrueRC X-AIR 5.8 MK II patch (~10 dBic, 120°, RHCP, RP-SMA, $45)** in
    `candidates.sysml`. `flight_time_model.py` now folds the cheapest antenna into the
    GCS base cost (GCS base $81 → **$126** = radio + dongle + patch; baseline system
    $1,645 → **$1,690**; still ≪ R4). New **`analysis/rf_link_budget.py` → `rf_link_budget.md`**
    verifies all RF links vs the 2.8 km hard requirement (FSPL + 10 dB fade margin):
    **control (ELRS 1 W) +29 dB / ~25 km, telemetry +19 dB / ~7.9 km, video (2.5 W +
    patch) +17 dB / ~6.5 km — all PASS.** The video link is the binding one: on the
    VRX's **stock omni** it is only +9.3 dB / ~2.6 km — **below** the requirement, which
    is exactly why the patch antenna is required. Sweep re-audited: 0 violations.

19. **DECISION (2026-06-30 / 07-01) — power interface, support equipment, battery
    selection, and phase restructure.**
    - **Battery power interface + anti-spark:** refined `BatteryPowerInterface` with a
      `ConnectorCompatible` constraint + `connector` on the power ports +
      `Airframe.batteryConnector`. The whole power chain is **XT60**
      (battery → anti-spark → airframe) for all real contenders (BAT09/BAT10/BAT22).
      Added `part def AntiSparkFilter` (composed inline in `Drone`) +
      candidate `ASF1` (iFlight Anti Spark, XT60, $15).
    - **Charger:** added `part def Charger` composed into `AerialObservationSystem`
      as ground-support (excluded from the per-drone R4 cost, like the laptop) +
      `ChargerCandidates` (CHG1–CHG4); **selected `CHG1` HOTA D6 Pro**.
    - **Battery selected:** **`BAT10`** (Upgrade Energy 6S 12 Ah Amprius) is the flight
      default — `BAT09` (the top-endurance pick) is **out of stock**; **2× `BAT22`**
      (GNB) procured as development / shakedown packs.
    - **Phase restructure (4 → 3):** merged old Phase 1 (basic flight) + Phase 2
      (FPV/waypoints) into a single **Phase 1**, and **pulled GPS + the ELRS laptop
      dongle into Phase 1**. Old Phase 3 (thermal + DVR) → **Phase 2**; old Phase 4
      (SBC) → **Phase 3**. The DVR is now a Phase 1–2 part; the SBC records at Phase 3.
      Updated the SE plan, SELECTED_COMPONENTS, REQUIREMENTS_EXPORT §3.1, README,
      CLAUDE.md, and the model.sysml doc comments.
    - **New artifact — [`BOM.md`](BOM.md):** phased bill of materials (product / part # /
      link / cost, per-phase subtotals). Grand total ~$2,125 all-in (~$1,805 R4
      flight-system, both ≤ the $2,500 R4 cap).

20. **DECISION (2026-07-09) — build-phase tags on all requirements (`Phasing::PhaseTag`).**
    All 47 requirements in `model.sysml` now carry an `@PhaseTag` metadata annotation
    (edit to the protected model requested by David) marking the phase — per
    `systems_engineering_plan.md` — in which the requirement is expected to be **fully**
    implemented: satisfied in the as-fielded configuration of that phase and remaining
    satisfied in every later phase. New top-level **`package Phasing`** (`enum def Phase`
    Phase1–Phase4 + `metadata def PhaseTag`), privately imported into `Requirements`;
    validates clean in Syside. Tagging rule: requirements over **total-system
    quantities** (endurance R6/R7/R8; payload/TOM; all cost sums incl. R4) bind at
    **Phase 2**, the last hardware phase — Phase 3 is software-only, so the final
    mass/power/BOM configuration exists at end of Phase 2. **SBC workload requirements**
    (R4_SBC_PWR / R4_SBC_TEMP / R4_SBC_DATA_AF) bind at **Phase 3** (sustained NPU
    inference is the binding load; MAVLink integration is a Phase 3 build step). Pure
    Phase-1 hardware/interface requirements (flight regime R1/R2, ELRS/analog-video GCS
    links, battery voltage/connector) bind at **Phase 1**. **David's ruling on the R3
    family (2026-07-09):** R3 / R3_1 / R3_2 = **Phase 3** — in the committed build the
    detect/classify mission is fulfilled by onboard inference + telemetry alerts, not by
    an operator viewing live thermal video; R4_SBC_VIDEO_PROC and R4_GCS_VIDEO_DISP =
    **Phase 4** (both are explicitly about the live-video-to-GCS chain, deferred with
    OpenHD). **Follow-up (open):** reword R3_1/R3_2 ("operator viewing the live video
    feed") and R4_SBC_VIDEO_PROC ("for live transmission to the ground control
    station") to match the onboard-inference CONOPS — pending David's approval; until
    then the tags encode intent and the wording lags. Distribution: Phase 1 ×12,
    Phase 2 ×27, Phase 3 ×6, Phase 4 ×2.

21. **DECISION (2026-07-10) — behavioral layer scaffolded in new sibling file
    [`behavior.sysml`](behavior.sysml) (`package DroneSystemBehavior`); model-fork
    namespace collision found.** First two layers of the functional architecture
    from the use-case brainstorm, kept OUT of the protected `model.sysml` (same
    sibling-file pattern as `candidates.sysml`; imports
    `DroneSystemModel::Architecture::*`). **(1) Functions as `action def`s:**
    `ConductSortie` (UC-0 thread prepare → plan → launch → surveil → recover, with
    the UC-6 monitor and both failsafe handlers as concurrent members);
    `ExecuteSurveillance` (UC-4: concurrent flyRoute / streamThermal / detectLoop);
    `DetectInvestigateClassify` (UC-5: merge-loop sweep at 120 m → decide on
    detectionConfidence ≥ 0.90 (R3_1) → POI + telemetry alert → reroute/descend to
    90 m → classify loop ≥ 0.80 (R3_2) → resume route; thresholds as attributes);
    accept-triggered `HandleLinkLoss` / `HandleLowBattery` (UC-9/UC-10 — both still
    lack formal requirements, SSS §3.7; low-battery reserve threshold TBD).
    **(2) Allocation:** `part missionContext : AerialObservationSystem` performs the
    sortie and `allocate`s each function to its component (a new `operator :
    Operator` usage — first use of that def — plus laptop/QGC, FC/platform, camera,
    SBC). All action + allocation constructs (guarded decides, accepts, 3-deep
    allocate feature chains) validated clean in Syside on first pass. **FINDING —
    model fork:** three files declare `package DroneSystemModel` (`model.sysml`,
    `model_community_balanced.sysml`, `model_community_balanced_CATIA_backup.sysml`);
    Syside binds cross-file qualified names to a variant that predates `Phasing`,
    so the `@PhaseTag` annotations in `behavior.sysml` are **parked as
    `// phase: PhaseN` comments** (restore = resolve fork, uncomment the import,
    swap comments back). **RESOLVED (David, 2026-07-10): `model.sysml` stays the
    authoritative model.** Agreed sequence: (a) port the community file's newer
    interface work (typed `vrxToCapture`/`capToLaptop` VideoLinks, `UsbCap`/`Laptop`
    nested vid ports) into `model.sysml` as a reviewed, approved change; (b)
    de-conflict the variants once David's CATIA session allows (rename their
    top-level package or park the files as `.sysml.bak` so Syside stops indexing
    them); (c) restore the parked `@PhaseTag`s in `behavior.sysml`.

22. **DECISION (2026-07-10) — Layer 4 flight-mode state machine added; UC-9/UC-10
    handler action defs retired.** Added `state def FlightMode` to `behavior.sysml`
    (verbose) and `test.sysml` (minified), formalizing the SSS §3.1 flight states
    as a real state machine: top-level `disarmed → armed → flying → returnToLaunch
    → land → disarmed`, with `flying` a **superstate** over `takeoff/cruise/loiter`
    (each carrying a `do action`) and internal transitions `takeoff → cruise`,
    `cruise ⇄ loiter` (on `TargetDetected` / `InvestigationComplete`). Four new
    trigger `attribute def`s added (`ArmCommand`, `LaunchCommand`, `TargetDetected`,
    `InvestigationComplete`) alongside the existing `LinkLossDetected` /
    `LowBatteryReached`. Bound to the physical architecture via
    `exhibit state flightMode : FlightMode` on `missionContext`. **This retires the
    Layer-1 `HandleLinkLoss` / `HandleLowBattery` action defs** (and their
    `linkLossHandler`/`lowBatteryHandler` usages + allocations): link-loss and
    low-battery are now `accept`-triggered transitions out of the `flying`
    superstate, declared once and giving **real preemptive semantics** (exiting
    `flying` terminates the running `cruise`/`loiter` do-activity) — the fix for the
    disconnected-concurrent-actions problem David flagged. Both files validate clean
    in Syside (the minified `transition <src> then <tgt>` / `transition first <src>
    accept <sig> then <tgt>` forms parse). **KNOWN SEAM (documented in-file, future
    work):** `DetectInvestigateClassify` (UC-5) is one action spanning both `cruise`
    (sweep) and `loiter` (investigate/classify) and does not split 1:1 onto the
    `do` actions, so those are independent stand-ins cross-referenced by doc, not
    formally typed against it; `TargetDetected`/`InvestigationComplete` are likewise
    conceptual triggers with no modeled sender (same fidelity as the failsafe
    signals). Reconciling the action-flow and state-machine representations is
    deferred. Layer 3 (use-case veneer) remains the only unbuilt behavioral layer.

23. **DECISION (2026-07-10) — Layer 3 use-case veneer added; behavioral model
    complete.** Added a `package UseCases` to `behavior.sysml` (verbose) and
    `test.sysml` (minified) giving the 2026-07-09 brainstorm use cases a formal
    SysML v2 home. Ten `use case def`s: umbrella `ConductSortieUC` (UC-0) with
    `subject : AerialObservationSystem`, `actor operator : Operator`, an
    `objective` doc tracing to R1/R2/R3/R6/R7, and `include use case` for the six
    always-performed sub-use-cases (UC-1 Prepare, UC-2 Plan, UC-3 Launch, UC-4
    ExecuteSurveillance — itself including UC-5 DetectInvestigateClassify, UC-6
    Monitor, UC-7 ReturnAndRecover); plus a top-level `use case conductSortie :
    ConductSortieUC` instance. Each leaf carries its subject, an operator actor
    where the operator actively participates, and an objective doc citing the
    requirement IDs + the Layer-1/Layer-4 element that realizes it. **This is the
    layer that gives `part def Operator` an explicit operational role** (beyond the
    Layer-2 allocation target). **Design choice — failsafes as exceptional flows:**
    UC-9 (HandleLinkLossUC) and UC-10 (HandleLowBatteryUC) are UML-«extend»-style
    exceptional flows, but SysML v2 use cases offer only `include` (always-
    performed) — so they are modeled as standalone `use case def`s (realized by the
    FlightMode failsafe transitions) and deliberately **not** `include`d by the
    umbrella. Secondary actors (observed wildlife/humans; GNSS constellation) are
    named in doc only — the thin veneer adds no part def for them. NOT modeled (no
    backing behavior): UC-8 turnaround, UC-11 operator override, UC-12 GNSS
    degradation, UC-13 Phase-4 downlink. Both files validate clean in Syside
    (`use case def`/`use case`, `subject`, `actor`, `objective { doc }`,
    `include use case` all parse). **All four behavioral layers (1 functions,
    2 allocation, 3 use-case veneer, 4 state machine) are now in place**; the
    open behavioral items are the KNOWN SEAM from §C22 (action-flow ⇄ state-machine
    reconciliation) and the parked `@PhaseTag`s pending the §C21 model-fork cleanup.

24. **DECISION (2026-07-10) — CATIA export (`test.sysml`) curated to fit the ~500-
    element cap; Analysis + Views packages omitted from the export only.** Adding
    the behavioral layers pushed the merged `test.sysml` past the CATIA
    Community/No-Magic ~500-element limit (David hit it before Layer 4 was even
    added). An element census (scratch script over `test.sysml`) put the merged
    file at ~459 by a conservative per-line proxy — CATIA's own counter runs higher
    (it also counts successions, connector ends, control nodes `start`/`done`/`merge`/
    `decide`, and doc elements), consistent with David's >500 reading. Distribution:
    **Architecture ~212 (46%)**, Behavior ~90, **Analysis ~88 (19%)**, Requirements
    ~53, Views ~9. **Chosen fix (David, 2026-07-10): omit the `Analysis` and `Views`
    packages from `test.sysml` only** — they remain complete in `model.sysml`
    (authoritative) and are unaffected in `behavior.sysml`. Rationale: the Analysis
    layer is the lowest-value-per-element in a CATIA *diagramming* context — Syside
    can't execute its `calc def`s (A10/B3) and the real endurance/Johnson/budget
    numbers are produced by `analysis/flight_time_model.py`; the `Views` package is
    redundant scaffolding where CATIA manages its own diagrams. Removing both dropped
    a clean 143 lines with **no dangling references** (the only cross-ref was
    `systemVerification` exposing `Analysis::**`, and that view lives inside the
    removed `Views` package); `test.sysml` re-validates clean in Syside at **~362**
    (my proxy), ≈ −97, clearing the cap with margin while keeping ALL structure,
    requirements, and the full four-layer behavior model. The `test.sysml` header
    now documents the omission. **Levers still in reserve if the cap is threatened
    again** (not applied): drop the 26 spec-only Architecture attributes used only by
    `candidates.sysml` + Python (`connector`, `maxRange`, `netd`, `resolutionH/V`,
    `pixelPitch`, …); or hold the Layer-3 use-case veneer as Syside-only; or split the
    CATIA import into two projects (structure vs behavior). NB: `test.sysml` is a
    generated export — no generator script exists in-repo yet, so this curation is a
    manual maintenance rule to reapply on any future regeneration.

25. **DECISION (2026-07-10) — §C22 seam CLOSED: UC-5 split into state-aligned
    halves with formal signal emission.** In `behavior.sysml` (verbose) and
    `test.sysml` (minified): `DetectInvestigateClassify` was refactored into
    **`SweepAndDetect`** (cruise half: 120 m infer loop → detect ≥0.90 → markPoi →
    alertOperator → **`send targetDetectedEvt to missionContext`**) and
    **`InvestigateAndClassify`** (loiter half: rerouteToTarget/descend →
    classify ≥0.80 w/ retry loop → reportClassification → resumeRoute →
    **`send investigationCompleteEvt to missionContext`**), with
    `DetectInvestigateClassify` retained as the umbrella that cycles the two
    (so `ExecuteSurveillance.detectLoop` and the SBC allocation are unchanged).
    `FlightMode.cruise`'s do action is now **typed `: SweepAndDetect`** and
    `loiter`'s **`: InvestigateAndClassify`** — the same defs the action flow
    composes: **one definition, two views**, which is the SysML v2 reconciliation
    of the action-flow ⇄ state-machine seam. The `cruise⇄loiter` transitions now
    have **modeled senders**; sends target `missionContext` because it is the part
    that `exhibit`s FlightMode. The send in each half is deliberately the LAST
    step (exiting a state terminates its do-activity, so the trigger must not
    fire before resumeRoute completes). **Syside syntax rules learned** (added to
    `reference/sysml-v2-syntax.md`): a send action requires **payload AND
    receiver** ("at least 2 owned input parameters" — bare `send X();` fails),
    and the payload **cannot be a datatype invocation** (`TargetDetected()` →
    "Invocation expression must invoke a Behavior") — idiom: declare a named
    `attribute <evt> : <SignalType>;` and `send <evt> to <receiver>;`.
    Element cost in the CATIA export: +4 (≈366 proxy, ~450 CATIA-equivalent —
    still under the 500 cap). Still stand-ins by intent: takeoff/RTL/land do
    actions (ArduPilot behavior, not custom software) and the
    LinkLossDetected/LowBatteryReached triggers (FC/environment-originated).
    Software significance (David's stated end goal): the two halves + their
    sends are the design spec of the custom SBC application — the signals map
    to MAVLink AUTO→GUIDED→AUTO mode switches.

26. **DECISION (2026-07-10) — autonomy-loop control contract DE-RISKED with an
    executable SITL/mock harness ([`analysis/autonomy_sim/`](analysis/autonomy_sim/)).**
    Built the onboard mission-app skeleton + a mock MAVLink FC + passing contract
    tests that exercise the UC-5 loop **without ArduPilot installed** and **without
    the CV model** (the detector is injected — `ScriptedDetector` now, RKNN later).
    `mission_app.py` `MissionApp` is the executable form of `SweepAndDetect` /
    `InvestigateAndClassify` / `FlightMode`: SWEEP polls the detector in AUTO →
    on ≥0.90 it geotags + `STATUSTEXT`-alerts + switches **GUIDED** (=send
    TargetDetected) + commands `SET_POSITION_TARGET_GLOBAL_INT` descent to 90 m →
    INVESTIGATE classifies with retries → on ≥0.80 reports + switches **AUTO**
    (=send InvestigationComplete). FC-commanded RTL/LAND drives the app to PASSIVE
    (the external LinkLossDetected/LowBatteryReached path — app does not self-
    trigger). `fake_fc.py` streams HEARTBEAT/GLOBAL_POSITION_INT and records what
    it receives so `test_autonomy_loop.py` asserts the contract **on the wire**:
    `mode_cmds == [GUIDED, AUTO]`, a 90 m descent target, DETECT/CLASSIFY alerts,
    and failsafe stand-down. **Both tests pass (~7.5 s); `run_demo.py` narrates one
    cycle.** Dev deps: `pymavlink`, `pytest` (installed this session). Bug found +
    fixed: `threading.Thread` has an internal `_stop()` method — a `self._stop`
    Event shadowed it and broke `join()`; renamed to `_stop_evt`. **Significance:**
    the mission-defining autonomy loop is now proven correct at the control level
    before any flight or CV effort; the same `MissionApp` runs unchanged against
    real ArduPilot SITL by swapping the connection string (README documents it).
    Remaining validation (needs SITL/real FC): mode-ACK handling, GUIDED nav,
    arming/EKF gates, real `FS_*`/`BATT_*` failsafe params; then swap in the RKNN
    detector. NB: `analysis/autonomy_sim/` is the repo's first test suite — the
    project is otherwise MBSE docs, not code (CLAUDE.md).

27. **ARTIFACT (2026-07-10) — per-component software register:
    [`analysis/software_by_component.md`](analysis/software_by_component.md).**
    For each programmable component (laptop GCS / flight controller / SBC): the
    full function list needed to execute the mission, the existing software per
    function, and a **D-register** of capabilities that do not exist and must be
    developed. Result: **laptop = 0 to develop** (QGroundControl covers all of it;
    macOS/MacBook-Air constraint rules out Mission Planner), **FC = 0 to develop**
    (all ArduPilot; the link-loss + battery failsafe *parameter values* are the
    two open §3.7 requirements — config-as-requirement), **SBC = the entire
    development scope**: **D-1** thermal wildlife detection/classification model
    (R3_1/R3_2 burden; largely self-collected LWIR deer/turkey data — the long
    pole) and **D-2** the onboard mission app (control contract already tested per
    §C26; capture/inference integration + retry/timeout policy + hardening
    remain). **D-3 (optional)**: QGC map-POI display beyond STATUSTEXT — decide
    after Phase-3 field trials. Recording is explicitly out of scope (DVR removed
    2026-07-05). Cross-linked with `software_gap_analysis.md` (function-oriented
    adopt/build + interface contract).

28. **DECISION (2026-07-10) — software recorded IN THE MODEL (`Architecture::
    Software` register); FC firmware TBD resolved = ArduPilot; fork now
    demonstrably breaking `candidates.sysml` validation.** Per David's request
    (explicit approval for the protected-file edit): added `package Software`
    (`enum def SwStatus { EXISTS; TO_DEVELOP; }` + `part def SoftwareItem`
    {productName, version, license, status}) to **`model.sysml`**,
    **`model_community_balanced.sysml`** (full fidelity), and **`test.sysml`**
    (lean: name+status; export now ~379 proxy / ~466 CATIA-equivalent — under the
    500 cap). Product usages composed into the executing components:
    `Laptop.gcsApp` = QGroundControl 4.4+ (EXISTS); `Airframe.fcSoftware` =
    ArduPilot ArduCopter ≥4.5 (EXISTS); `SBCPayload.rknnRuntime` +
    `.mavlinkRouter` (EXISTS) + **`.missionApp` (D-2, TO_DEVELOP)** +
    **`.thermalModel` (D-1, TO_DEVELOP, `satisfy R3_1; satisfy R3_2;`)**. The
    register complements (does not replace) the per-candidate software spec
    strings on the defs. **Name collision fixed:** `Airframe` already had
    `attribute fcFirmware : String` (candidate data) — the register part is named
    `fcSoftware`. **FC-firmware TBD RESOLVED:** `candidates.sysml`
    `AF3a.fcFirmware` updated from "TBD — ArduPilot or PX4" to **ArduPilot
    ArduCopter ≥4.5, SELECTED** (the §C26 autonomy contract is built on
    ArduCopter AUTO/GUIDED); `SELECTED_COMPONENTS.md` gained FC-firmware +
    GCS-application rows. Function-level D-1/D-2 development breakdown
    (D1.1–D1.8, D2.1–D2.13 with build status) added to
    `software_by_component.md`. **FINDING — fork escalation:** the first-ever
    edit of `candidates.sysml` this session surfaced **187 pre-existing
    reference errors** (lines 3142–3643: BAT04–BAT23 + WLAN_AIR/GND blocks —
    "No Feature named 'usableDoD'/'name'/'chipset'…"). Those features DO exist
    in `model.sysml`'s rich defs (e.g. `Battery.usableDoD`) but not in the lean
    variant defs — i.e. Syside resolves those candidates' types against a fork
    variant (FOUR files now declare `package DroneSystemModel`: model.sysml,
    community_balanced, CATIA backup, test.sysml). NOT caused by today's
    content changes. **The §C21 de-conflict is now urgent** — the fork is
    silently invalidating validation of the single source of truth for
    component data. Quickest safe first step: park the CATIA backup as
    `.sysml.bak`; full fix per §C21 (a)–(c).

29. **ARTIFACT (2026-07-11) — software trade studies for the adopt/EXISTS items:
    [`analysis/software_trade_studies.md`](analysis/software_trade_studies.md).**
    Per David's request, surveyed free + paid alternatives for each `status =
    EXISTS` register item and traded them against the project's constraints
    (web-researched 2026-07-11). **Six trade studies (TS-1..TS-6): GCS app, FC
    firmware, NPU runtime, MAVLink library, MAVLink router, video capture.**
    **Result: all six selections CONFIRMED — no changes.** Two winners are
    *forced* by prior locks (RKNN by the RK3576 NPU — every alternative misses
    the NPU and busts R4_SBC power/thermal; QGroundControl by the macOS/MacBook-
    Air constraint among full GCSs — Mission Planner is Windows-only). Notable
    findings: **ArduDeck** (native Apple-Silicon ArduPilot GCS) is a real QGC
    backup worth trialing; **mavp2p** is a dependency-free router alternative to
    mavlink-router; **dronekit-python is maintainer-orphaned (2025)** → stay on
    pymavlink (already in `autonomy_sim`); the sole open sub-decision is the
    capture method (OpenCV now, GStreamer if Phase-4 downlink). Currency: current
    ArduPilot stable = **Copter 4.6.3** (Nov 2025) — model's `">= 4.5"` stays
    valid. Cost impact $0 (all free/OSS; only paid option surveyed, UgCS, adds
    nothing). No model edits (selections unchanged); cross-linked into the
    software doc set (gap analysis + per-component register).

30. **DECISION (2026-07-11) — behavior MERGED into `model.sysml` (single-root,
    standard four-pillar model); §C21/§C28 fork RESOLVED; `behavior.sysml` +
    `test.sysml` retired.** Per David ("implement all 5 parts"; explicit approval
    for the protected-model edit). The behavioral layer no longer lives in a
    separate `DroneSystemBehavior` root — it is now **`DroneSystemModel::Behavior`**,
    a peer of Requirements / Architecture / Analysis, so the model reads as the
    canonical pillars **Requirements · Architecture · Behavior · Analysis** (+ Views,
    Phasing). All validated clean in Syside.
    - **(1) Merge:** `behavior.sysml`'s content moved into `model.sysml` as
      `package Behavior` (verbose docs retained). The parked `@PhaseTag`s are
      **restored** (15 tags: Phasing now resolves from inside the same root) — the
      §C21 payoff. `missionContext : AerialObservationSystem` was KEPT (not replaced
      by raw perform/exhibit on AOS): it is the standard behavioral-context block
      and, critically, the **receiver for the UC-5 seam-closure `send`s** (§C25) —
      pure AOS-ownership would have forced re-wiring those as ports/flows.
      `AerialObservationSystem` therefore needed **no edits**.
    - **(2) Fork de-conflict:** four files declared `package DroneSystemModel`.
      Now **only `model.sysml` does**. The CATIA backup (`…_CATIA_backup.sysml`)
      was already gone; **`model_community_balanced.sysml`'s root renamed to
      `DroneSystemModel_Community`**; `behavior.sysml` and `test.sysml` deleted
      (their content lives in model.sysml + balanced). **`candidates.sysml`'s 187
      pre-existing reference errors (§C28) are GONE** — it now resolves against
      model.sysml's rich defs. *CATIA note: re-importing balanced will show the
      root as `DroneSystemModel_Community`; if that disrupts the CATIA project,
      the alternative is de-indexing the export from Syside instead of renaming.*
    - **(3) Balanced = the single CATIA export**, now WITH behavior. To stay under
      the element/char caps, applied the §C24-consistent cuts: **Analysis + Views
      removed** (already the approved CATIA cut) and, since balanced was becoming
      the capped import (~460 proxy ≈ at the 500 cap), the **use-case veneer
      (`UseCases`) trimmed from the export** (kept in full in model.sysml) plus
      behavior inline-comments stripped. **Net: balanced 463→431 elements and
      22 227→21 993 chars — SMALLER on BOTH axes than before, so under whatever
      limits it previously satisfied**, while now carrying the behavior. (If David
      prefers use-case *diagrams* in CATIA, the alternative is to keep `UseCases`
      and instead minify balanced's Architecture attributes — the §C24 reserve
      lever — to recover the elements.) **FOLLOW-UP (2026-07-11): David still hit
      the CATIA *character* limit at ~22 k**, so balanced was fully **minified —
      ALL `//` comments + blank lines stripped** (CATIA never imports `//`
      comments — only `doc /* */` — so this drops zero model content). **Result:
      21 993→17 216 chars (−22%), 431 elements unchanged.** balanced is now a
      generated minified export (header says so); the readable source is
      model.sysml. A regenerator script is the obvious next automation.
      **FOLLOW-UP 2 (2026-07-11): then hit the ELEMENT limit** (comments aren't
      elements, so the char minify didn't help there). Stripped the **76 empty
      component data-attribute declarations (cost/mass/power/specs) + the
      cost/power rollups** — they carry NO values in balanced (the `:>>` bindings
      live in `candidates.sysml`, which CATIA never imports), so this is zero
      content loss; every value remains in model.sysml. **Kept** the structural
      skeleton (parts, ports, connects, interfaces, satisfy), Requirements,
      Behavior, and the Software register. **Result: 431→354 elements (proxy;
      ≈ −18%), 17 216→14 154 chars.** If David hits the cap yet again, the next
      levers (in order) are: drop the deferred **Phase-4 OpenHD parts** (OhdWifiTx/
      OhdGndRx + wifi antennas — not in the committed build), then the Software
      register, then thin the subsystem requirement packages.
      **FOLLOW-UP 3 (2026-07-11): added the system-level requirement doc text back**
      (R1–R8, R3_1, R3_2 — the `shall` statements, pulled verbatim from model.sysml
      so the two stay consistent) so CATIA requirement diagrams/tables show real
      text instead of empty IDs. Cost as predicted: **+1 417 chars (14 384→15 901),
      +0 elements** — a `doc` attaches as the requirement's documentation property,
      not a counted model element in MSOSA. Subsystem-requirement docs stay stripped
      (adding all 47 would be +7 k chars, back near the char cap).
    - **File roles now:** `model.sysml` = authoritative full model (all pillars);
      `candidates.sysml` = data (`DroneCandidates`, resolves to model.sysml);
      `model_community_balanced.sysml` = lean CATIA export (`DroneSystemModel_Community`,
      no Analysis/Views/UseCases). `behavior.sysml`, `test.sysml`, and the CATIA
      backup are gone.

31. **DECISION (2026-07-12) — software interconnection layer added (`Architecture::
    Software` register parts now have ports + connections + allocations).** Per
    David: gave the six software items MAVLink/inference ports and wired them, in
    both `model.sysml` (full, doc'd) and `model_community_balanced.sysml` (lean).
    **SBC-internal (on-board IPC, no wire):** `missionApp.mav ↔ mavlinkRouter.app`;
    `missionApp.infer ↔ rknnRuntime.infer` (the Detector seam); `allocate
    thermalModel to rknnRuntime` (the .rknn is executed by the runtime).
    **Cross-component MAVLink, each allocated to the physical bearer it rides:**
    `sbc.mavlinkRouter.fc ↔ platform.fcSoftware.sbc_mav` (in `Drone`) **allocated
    to the named `sbcMavUart` interface** (the FC↔SBC UART, `sbc_dta↔uart_dta`);
    `drone.platform.fcSoftware.gcs_mav ↔ gcs.viewingComputer.gcsApp.mav` (in
    `AerialObservationSystem`) **allocated to the named `elrsTelemetry` link**
    (carries FC telemetry + the SBC's STATUSTEXT alerts to QGC). The two
    previously-unnamed physical interfaces were **named** so the allocations can
    target them. **SysML learned:** `allocate <connection> to <interface>`
    validates in Syside; a part *usage* can add its own `port`s alongside its
    `:>>` redefinitions. All clean in Syside (only the standing `DS_Views` errors
    remain). **Cap impact on the export:** +15 elements (354→**369**, ≪ 500) and
    +550 chars (15 901→**16 452**, ≪ ~22 k) — both comfortably under. (NB: the
    first scripted pass silently dropped the two cross-component connections
    because their insertion anchors were the `totalPower`/`totalCost` rollups,
    which had already been stripped from the lean export; caught + fixed.) Typed item
    flows (MavlinkStream/VideoFrame/Detections) were deliberately NOT added — the
    ports are untyped to keep the element count down; the "what flows" is in the
    port names + model.sysml doc comments. Not in candidates.sysml (schema only).

32. **DECISION (2026-07-13) — item-flow layer added to `model.sysml` (typed
    messages/flows on every connection).** Per David: document *all* the messages
    and flows in the system as first-class SysML v2, where each transfer has a
    from, a to, and the connection it rides over. This **supersedes the C31
    deferral** ("typed item flows deliberately NOT added") — but **only in
    `model.sysml`**. `model_community_balanced.sysml` is **left untouched** and
    deliberately continues to omit this layer to stay under the CATIA Community
    ~500-element cap (David's explicit instruction). When regenerating the lean
    export, **strip the `Flows` package, the port item features, the nested
    signal sub-ports, and every `flow`** — the balanced export keeps only the
    untyped-port + named-connection form from C31.
    **What was added (all in `Architecture`):**
    - A new **`package Flows`** with 7 payload `item def`s — physical carriers
      `ElectricalPower` / `RfSignal` / `VideoSignal`, and logical messages
      `MavlinkData` / `CrsfData` / `GnssData` / `InferenceData` — plus the
      data-bearing `port def`s (`PowerOut`/`PowerIn`, `MavlinkSerial`,
      `CrsfSerial`, `GnssSerial`, `InferClient`/`InferServer`).
    - **Directed `in`/`out` item features** added to the existing `Compatibility`
      power/video/RF port defs (e.g. `VideoSourcePort { …; out video : VideoSignal; }`).
    - **Nested signal sub-ports** on the combined physical connectors (a plug that
      carries 9 V + video + UART now exposes `pwr` / `vid` / data sub-ports),
      extending the pre-existing nested-`vid` idiom.
    - A **named `flow` inside the body of every connection** it rides over —
      `interface camToSbc : VideoLink connect … { flow thermalVideo from
      camera.…vid.video to sbc.…vid.video; }` — covering power buses, the video
      chain, the ELRS/OpenHD RF hops, GNSS, CRSF, the MAVLink UART/RF/localhost
      links, and the SBC detector seam (~50 flows total).
    **SysML v2 constructs used (all validated clean in Syside via the live LSP):**
    the `flow <name> from <out feature> to <in feature>;` form **written inside a
    connection body** (the official-release idiom — the flow's owning connection
    *is* the one it flows over); directed item features on port defs; and **port
    conjugation** (`~Flows::GnssSerial`) for one-way sink sides. Only the standing
    `DS_Views` reference errors remain. See the `Flows` banner comment in
    `model.sysml` and item 31 above for the layered (physical bearer ← logical
    message) relationship that the software `allocate`s already expressed.
    - **Follow-up (2026-07-13) — SBC frame-capture delegation.** Reviewing the
      MSOSA diagram, the SBC software was internally wired but had no link to the
      SBC's own I/O ports — so the Detector-seam "frames" had no visible source.
      Added a `frameIn : VideoSinkPort` to `missionApp` and a **port-delegation
      connector** `uvcToApp` from `usba1_pwr_vid.vid` to `missionApp.frameIn`,
      closing the pipeline camera → usba1 (UVC) → missionApp → infer seam →
      rknnRuntime. It is a *delegation* (boundary-in → child-in), so it carries
      **no own `flow`** (a flow can't go `in`→`in`; the VideoSignal already flows
      onto usba1 via `camToSbc`). Unlike the rest of the C32 item-flow layer, this
      single structural connection **WAS added to `model_community_balanced.sysml`
      too** (per David) — it's a plain connector, ~2 elements, no cap concern.
    - **Follow-up 2 (2026-07-13) — MAVLink FC↔SBC re-routed through the physical
      UART (supersedes C31's `swRouterToFc`).** David: "the mavlink SW doesn't
      directly interface with the FC." Correct — `mavlink-router` opens the SBC's
      serial device and writes bytes onto the UART; there is no direct IPC to
      ArduPilot. So the direct SW-to-SW `swRouterToFc` (`sbc.mavlinkRouter.fc ↔
      platform.fcSoftware.sbc_mav`, allocated to `sbcMavUart`) and its allocate
      were **removed**, replaced by two **port delegations**: `routerToUart`
      (`mavlinkRouter.fc → uart_dta`, in `SBCPayload`) and `fcMavToUart`
      (`fcSoftware.sbc_mav → sbc_dta`, in `Airframe`). The end-to-end MAVLink is
      now continuous through the hardware — `mavlinkRouter.fc → uart_dta →
      [sbcMavUart wire, carries the MavlinkData flows] → sbc_dta →
      fcSoftware.sbc_mav` — with no fictitious direct software link. Applied to
      **both** `model.sysml` and the balanced export.
    - **Follow-up 3 (2026-07-13) — MAVLink FC↔GCS re-routed through the physical
      ELRS chain (supersedes C31's `swFcToGcs`).** Same treatment as follow-up 2,
      for the telemetry link. Removed the direct `swFcToGcs` (`fcSoftware.gcs_mav
      ↔ gcsApp.mav`, allocated to `elrsTelemetry`) and replaced it with two
      delegations onto the physical chain that was already fully wired:
      `fcTelemToRx` (`fcSoftware.gcs_mav → rx_pwr_dta`, in `Airframe` — MAVLink is
      tunneled MAVLink-over-CRSF to the ELRS RX; in `model.sysml` it targets the
      `.crsf` sub-port the `telemToRx` flow already rides) and `gcsMavFromDongle`
      (`gcsApp.mav → usb_elrs_pwr_dta`, in `Laptop` — QGC reads it from the ELRS
      USB dongle; `.mav` sub-port in `model.sysml`). The end-to-end telemetry path
      is now continuous through hardware: `fcSoftware.gcs_mav → rx_pwr_dta →
      [rxLink] → rx → [rxRfA/elrsTelemetry RF] → laptopLink dongle → [elrsDongleUsb]
      → usb_elrs_pwr_dta → gcsApp.mav`, the RX and dongle being the (implicit)
      CRSF↔RF↔USB tunneling hardware. Applied to **both** files. With this, **no
      software register port crosses a device boundary via a fictitious direct
      link** — every SW port delegates to the physical port it uses. (`model.sysml`
      targets the typed `.crsf`/`.mav` sub-ports; the balanced export, which omits
      the flow-layer sub-ports, delegates to the bare `rx_pwr_dta`/`usb_elrs_pwr_dta`
      connectors.)
    - **Follow-up 4 (2026-07-13) — balanced export element-budget trims (~497 →
      ~438).** The delegations above pushed the lean export to ~3 elements under
      the CATIA Community ~500-element cap. Per David ("keep all pillars, trim
      fat"), two **balanced-only** cuts were applied (model.sysml keeps
      everything): (1) **deferred Phase-4/OpenHD hardware omitted** — `OhdWifiTx`,
      `OhdGndRx`, the wifi/openHD antenna usages, their ports/`satisfy`, and the
      OpenHD connects (SBC `usba2_pwr_dta`, Laptop `usb_ohd_pwr_dta`); it is a
      non-committed future capability (Phase 1–3 unaffected). (2) **software-register
      attributes stripped** — the `SoftwareItem` def's 4 attributes + `SwStatus`
      enum + all 24 `:>>` product/version/license/status bindings; the usage names
      (`mavlinkRouter`, `missionApp`, …) still carry identity, and the values live
      in `model.sysml`. Together ~59 fewer elements → ~62 of headroom. **Held back**
      (offered, not applied): collapsing the RX diversity antennas `rxAntennaA/B`
      to one (~5 more) — after Phase-4 removal that pair is the model's distinct
      primary-dongle vs backup-handheld path, a real feature not worth losing for 5
      elements when the target was already met. Requirements still satisfied (the
      OpenHD `satisfy R4_GCS_VIDEO_DISP/RANGE` were redundant with `Vrx`/`Antenna`).
      The export header comment + this file are the record of what the lean export
      now omits; regeneration must reapply these cuts.

---

## D. Candidate data gaps & uncertainties (from the source CSVs)

- **FIXED (2026-06-27) — KOLAS7 masses were frame-kit weights, not as-built; PNP
  removed.** David found the KOLAS7 "PNP" no longer exists (only the frame kit +
  BNF variants ship), and that the modeled 257 g is the **bare frame kit** (carbon
  + TPU, no motors/ESC/FC). The C287 2807.5 motors are **47 g each (4 = 188 g)**, so
  every KOLAS7 mass (AF2a 257 g, AF2b 300 g, AF2c 333 g) omitted the entire
  drivetrain — making KOLAS7 ~240 g too light and the artificial endurance
  "winner." **Corrections:** AF2a (PNP) removed; AF2b (BNF analog) 300 → **540 g**,
  AF2c (BNF HD) 333 → **565 g** (frame 257 + motors 188 + ESC/FC/props/wiring ~53 +
  bundled VTX/GPS/RX[/cam]). This supersedes the "±20 g" claim in the 2026-06-25
  note below. Effect: KOLAS7 drops from ~71 min (#1) to ~53–54 min (mid-pack); the
  new endurance leader is **AF9a DarwinFPV 129** (~69 min). Other airframes were
  spot-checked and use genuine as-built (with-motor) weights — this error was
  KOLAS7-specific.
- **FIXED (2026-06-27) — GEPRC MARK4 LR7 (AF1) discontinued; replaced by MOZ7 V2.**
  AF1 removed; added **AF1a** (MOZ7 V2 Analog, 782 g, analog VTX+cam+GPS), **AF1b**
  (WTFPV / Walksnail-ready, 764 g, no bundled VTX/cam), **AF1c** (O4 Pro, 750 g, DJI
  O4 digital + GPS) — one platform: 336 mm, 7.5″ HQ props, SPEEDX2 2809 1280KV,
  TAKER H743 BT FC, H65 8S 65A ESC, **6S LiPo / 8S Li-ion** (minCells 6, maxCells 8).
  As-built weights from geprc.com. Heavy 7.5″ frames → ~47–49 min hover (near the
  ROC7 group); thrust 3000 g/motor is EST (GEPRC publishes no grams). Baseline
  unchanged: AF9a DarwinFPV 129, 69.1 min.
- **MOSTLY RESOLVED (2026-06-26) — airframe masses filled (AF5 pending).** All
  airframe `mass` values are now populated except AF5 (see B4 — pending a
  7-inch-vs-10-inch decision). Wheelbase is still absent for a few BNF-only entries
  (AF5, AF6a/b, AF10); the flight-time model falls back to a 250 mm default
  frontal-area width when wheelbase is missing, so the effect is minor.
- **RESOLVED (2026-06-25) — BNF/PNP as-built masses corrected.** BNF variants
  now carry distinct masses reflecting their bundled electronics. Confirmed from
  official manufacturer pages or peer reviews:
  - AF3b (Chimera9 ECO BNF): 721g PNP → 727g (+ TBS Nano RX 5.5g)
  - AF8a (Chimera7 Pro V2 PNP): 725g → **705g** (iFlight shop; 725g is the HD/O3 variant)
  - AF8b (Chimera7 Pro V2 BNF): 725g → 711g (705g + TBS Nano RX 5.5g)
  - AF2b (KOLAS7 BNF Analog): 257g → **300g est.** (257g base + ~15g analog VTX
    + ~20g GPS + ~5.5g TBS Nano RX + ~2.5g misc; VTX model unknown)
  - AF2c (KOLAS7 BNF HD): 257g → **333g est.** (257g base + ~48g DJI O3 full
    assembly [36.4g module+cam + 3g ant + 8.3g cable] + ~20g GPS + ~5.5g RX)
  The KOLAS7 BNF estimates remain approximate because Axisflying does not publish
  as-built masses; treat them as ±20g.
- **RESOLVED (2026-06-25) — AF4a and AF9a had wrong `vtxIncluded` /
  `fpvCameraIncluded` flags.** Both were set to `false` from earlier CSV
  uncertainty. Web research confirmed: DarwinFPV X9 (AF4a) integrates a 1000mW
  analog VTX and "Darwin cement" waterproof FPV camera (confirmed at fpvfaster.com;
  "GPS: Non" also confirmed). DarwinFPV 129 (AF9a) integrates an 800mW VTX and
  FPV camera (Oscar Liang review lists both in the 402g all-up weight). Both flags
  corrected to `true` in `candidates.sysml`; flight-time model now correctly treats
  these as bundled (power-only, no added mass).

- **DATA GAP — Axisflying KOLAS7 BNF Analog (AF2b).** Product page names no VTX
  or FPV-camera model; `vtxModel` is "Unknown", `fpvCameraIncluded` set false
  pending seller confirmation. GPS module is manufacturer-unbranded.
- **DATA GAP — DarwinFPV X9 (AF4a) GPS** not confirmed; only 2 hardware UARTs
  (GPS via softserial is tight).
- **DATA GAP — unbranded GPS on bundled airframes** (AF2b/c, AF6a/b, AF10): exact
  module unknown ("DeepSpace/Axisflying unbranded").
- **DATA GAP — thermal module pricing is wide/uncertain** (factory-direct Chinese
  modules, InfiRay street pricing). Representative midpoints used.
- **RESOLVED (documented) — RunCam Mini DVR two price points** ($17.99 direct /
  $29.99 Amazon); modeled once at the direct price (DVR1). No further action.
- **RESOLVED (documented) — EasyCAP capture (VC4)** is only *partially* macOS-
  compatible (driver issues, not true UVC); modeled as `macOsCompatible = false`.
- **DATA GAP — several analog cameras** list estimated (`est`) illumination/power
  values; bound as given, treat as approximate.

---

## F. Architectural changes

14. **DECISION (2026-07-27) — R3 operating condition reworded night → daytime.**
    David confirmed the concept flies **daytime**, not at night: the thermal camera
    detects/classifies by IR signature, which works in daylight, so night operation
    is not required. `R3`'s doc text was changed from *"under clear-night conditions"*
    to *"under clear daytime conditions"* (the ≥ 5 °C target-to-background differential
    is unchanged). Propagated to every source artifact: `model.sysml` (R3),
    `REQUIREMENTS_EXPORT_26_06_30.md` (R3 + §3.9), and the AI data-collection notes in
    `analysis/software_by_component.md` (D1.1) / `analysis/software_gap_analysis.md`;
    `analysis/requirements_traceability.csv` was regenerated from the model. **Not yet
    regenerated (David's action):** the SysON **Requirements Table View** PNG
    (`system_level_requirements.png`) — it is rendered from the model in SysON and lives
    in SysON's project DB, so it must be re-exported by hand and re-dropped into
    `presentation/assets/diagrams/` before the CDR deck's slide 6 shows the new wording.
    **Engineering note to validate:** daytime thermal contrast can be *lower* than at
    night (solar loading warms the background), so the ≥ 5 °C differential is the
    condition to confirm during field thermal capture (D1.1).

13. **DECISION (2026-07-05) — DVR removed; SBC moved to Phase 2.**

    - **Context:** David requested the standalone Monster UVC Recorder (`DVR9`) be
      removed from the architecture entirely. Instead of a separate DVR, the SBC
      (`SBC3`, NanoPi M5) handles onboard recording via USB-UVC from the T13
      thermal camera — eliminating a $129 part and ~430 g of mass.
    - **Phase restructure:**
      - **Phase 2** (was: thermal + DVR + OpenHD) → becomes **thermal + SBC +
        OpenHD**. The SBC and its mount/cooling are procured in Phase 2 alongside
        the T13 and OpenHD hardware. Phase 2 subtotal: ~$936 (+$12 net from
        dropping DVR $129 and adding SBC $141).
      - **Phase 3** (was: SBC procurement → becomes: **AI software deployment**,
        no new hardware procurement). All hardware is on-board since Phase 2.
    - **Files changed (2026-07-05):**
      - `model.sysml` — removed `part def ThermalVideoRecorder` and the
        `recorder : ThermalVideoRecorder` part from `Drone`;
        removed `camToRec` and `recToVtx` video interfaces; removed
        `recorder` from `totalPower` rollup.
      - `BOM.md` — DVR9 row removed; SBC3 + mount moved to Phase 2; Phase 3
        marked as $0 software; totals recalculated.
      - `systems_engineering_plan.md` — Phase 2 steps now include SBC mounting
        + OpenHD config; Phase 3 is software-only.
      - `SELECTED_COMPONENTS.md` — DVR open item replaced with SBC-recording
        note.
      - `REQUIREMENTS_EXPORT_26_06_30.md` — phase descriptions updated.
      - `CLAUDE.md`, `README.md` — architecture description updated.
      - `analysis/flight_time_results.md`,
        `analysis/flight_time_value_ranking.md` — prose updated to reflect
        DVR removal.
      - `candidates.sysml` — `part DVR9` retained as unused historical
        candidate (no active references in the architecture).
    - **Budget impact:** R4 system cost dropped from ~$2,088 to ~$1,960 (savings
      of ~$128 from DVR removal, partially offset by SBC moving to Phase 2
      costing). Grand total ~$2,290.75 vs ~$2,419.75 previously.

14. **DECISION (2026-07-07) — Thermal = USB (live inference, not recorded); OpenHD downlink deferred to a new Phase 4.**

    - **Context:** David finalized the thermal architecture. The thermal feed is **not
      recorded** — it streams live from the T13 (USB-UVC) directly to the SBC (`SBC3`),
      which runs **real-time inference** that drives autonomous actions (Phase 3). The
      OpenHD digital video downlink to the ground is **no longer part of the committed
      build**; it becomes a deferred **Phase 4** future capability.
    - **Thermal interface — USB chosen; MIPI and CVBS rejected:**
      - **USB (UVC)** — selected. Plug-and-play (`/dev/video0`), full-fidelity for the NPU
        (640×512 @ 25 Hz uncompressed YUV ≈ 16 MB/s fits USB 2.0), zero driver work.
      - **MIPI** — rejected. Its only advantages (bandwidth, ~30 ms lower latency) are
        immaterial for a feed whose cadence is set by the 25 Hz frame interval (40 ms) and
        flight dynamics (hundreds of ms), not transport. PurpleRiver's MIPI enablement targets
        Jetson, not Rockchip; a non-vendor MIPI camera on the RK3576 is a kernel driver-porting
        project (vendor 6.1 kernel + device tree; only FriendlyElec's CAM415 supported out of
        box). High integration risk for no usable benefit.
      - **CVBS (+ USB analog dongle)** — rejected. Only had value for an analog/HD downlink,
        which is gone; analog conversion degrades the image and adds a part vs USB.
    - **Phase restructure (Phase 4 added):**
      - **Phase 2** (was: thermal + SBC + OpenHD) → **thermal (USB) + SBC only.** No recording,
        no downlink hardware. Subtotal ~$967.97 → **~$808.98** (OpenHD −$158.99 out).
      - **Phase 3** — unchanged scope (AI + MAVLink), now explicitly **real-time inference on
        the live USB thermal feed.**
      - **Phase 4 (NEW, deferred future)** — OpenHD downlink: `WLAN_AIR1`, air cloverleaf
        antennas ×2, `WLAN_GND1`, Foxeer Echo 2 Max ×2, VMware VM. Subtotal **~$158.99** (the
        air module's 5 V power reuses the spare 2nd unit of the Phase 2 UBEC 2-pack, $0).
    - **Budget impact:** committed **R4 (Phases 1–3) ≈ $1,832** (was ~$1,991 with OpenHD in
      Phase 2); with Phase 4 built it returns to ~$1,991. Grand total unchanged at ~$2,322.72
      (redistributed across four phases). All under the $2,500 R4 cap.
    - **Note on HDZero:** an HDZero digital-FPV path (switchable FPV↔thermal on one link) was
      explored in depth and **not adopted** — the committed build keeps the bundled analog FPV
      for piloting and takes the thermal onboard-only. No HDZero parts entered the model/BOM.
    - **Files changed (2026-07-07):** `BOM.md` (Phase 2 trimmed, Phase 4 added, totals),
      `systems_engineering_plan.md` (Phase 2 reworded, Phase 4 added), `SELECTED_COMPONENTS.md`
      (OpenHD rows → Phase 4, port inventory, recording note, SBC-power load), `candidates.sysml`
      (OpenHD package phase comments). **`model.sysml` not modified** — phases are a planning
      artifact, not in the formal model, and the OpenHD parts live in `candidates.sysml`.

---

## E. Cross-reference note

**RESOLVED (2026-06-26).** Markdown prose now references the correct model element
names. `README.md`'s Architecture section was rewritten to drop the removed
`TelemetryTransmitter` / `TelemetryReceiver` parts (telemetry is carried by the
ELRS `RadioReceiver` / `RcTx`), fix the `Drone` and
`GCS` compositions, and add the current parts (`FpvCamera`,
`GpsModule`, `ThermalVideoRecorder`, `UsbCap`, the `Compatibility`
sub-package, and the thermal-detection analysis defs). The `IRCamera` →
`CameraRequirements` package rename is reflected (README already listed
`CameraRequirements`). Requirement IDs `R3_CAM_*` are unchanged.

---

## G. Attribute pruning — analytically-inert attributes removed (2026-07-10)

**Context (David).** Audited every attribute in the model against its actual
consumers: the `Analysis` package calcs/constraints, the derived rollups
(`totalPower`/`totalCost`/`subTotalCost`), the `VideoFormatCompatible`
constraint, and the external `analysis/flight_time_model.py` endurance/detection
sweep. Goal: drop attributes that no analysis reads (also buys headroom under the
CATIA Community **~500-element** import limit — see the balanced-export notes).

**Verification performed first (per David's instruction):** grepped all five
`analysis/*.py` + `.openclaw/tmp/*.py` scripts and confirmed there are **no
hooks/settings** in the repo. This caught two attributes that *are* consumed and
were therefore **kept**:
- **`Battery.nominalVoltage`** and **`Battery.capacity_mAh`** — read by
  `flight_time_model.py` (battery parser: `v_nom`, `cap_mah`, lines ~474–478).
- Also confirmed `flight_time_model.py` reads **only `candidates.sysml`**
  (`MODEL_SYSML` is declared but never `read_text()`), so edits to `model.sysml`
  cannot affect the sweep. Script re-run end-to-end after the edits: **exit OK**,
  baseline unchanged (iFlight Chimera9 ECO → 58.4 min, ~$1,674 system).

**Removed from `model.sysml` AND `model_community_balanced.sysml` (7 attributes,
zero `candidates.sysml` bindings, nothing reads them):**

| Attribute | Part | Why inert |
| --- | --- | --- |
| `specificEnergy` (derived `energy/mass`) | `Battery` | computed, never consumed |
| `outputVoltage` | `Ubec` | UBEC is a fixed pass-through in every analysis |
| `maxTakeoffMass` | `Airframe` | no in-model mass rollup compares against it |
| `cost_USD`, `mass`, `power`, `maxRange` | `GCS` | superseded — `totalCost` uses `gcs.subTotalCost`; no mass/power/range rollup reads the GCS's own scalars |

`GCS.batteryEnergy` (exists only in `model.sysml`) was **left in place** — not in
the audited-inert set.

**Deliberately NOT removed (candidate-bound; hold real trade-study spec data).**
`connector`(×37), `maxRange`(×39 on components), `maxCells_s`(×28),
`netd`/`pixelPitch`/`resolutionV`(×15 each), `detectionRange`(×14),
`maxCurrent_A`(×4), `batteryConnector`(×1) are all `:>>`-bound in
`candidates.sysml`; removing them from the defs would invalidate those bindings
and delete market data. David chose **"clean set only."** Note on
**`resolutionV`**: the GSD calc uses only `resolutionH` because thermal pixels are
square → GSD is isotropic (`hfov/resolutionH` ≡ `vfov/resolutionV`), so
`resolutionV` is redundant *for the calc* — but it stays for now as candidate data.

**Follow-up worth considering:** add a `totalMass` rollup so `mass` (currently the
#1 driver of the *external* endurance model but analytically inert *in-model*) and
`maxTakeoffMass`/payload requirements become load-bearing SysML.
