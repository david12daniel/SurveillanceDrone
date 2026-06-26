# Model Issues Log

Tracks problems found in the SysML v2 model and candidate data, the decisions
taken, and open items for review. Created 2026-06-25 while consolidating the
`analysis/*.csv` market/trade-study data into the SysML model
([model.sysml](model.sysml) schema + [candidates.sysml](candidates.sysml) data).

Status legend: **FIXED** (changed in-model) · **DECISION** (modeling choice made)
· **OPEN** (needs David's input) · **DATA GAP** (missing/uncertain source data).

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
   `CameraSubsystem` requirements package and the `Requirements` package were
   each missing a `}`, so `Architecture` and `Analysis` were being parsed as
   children of `Requirements::CameraSubsystem`. Added the two missing braces.

4. **FIXED — `power` name collision (attribute vs port).** Seven part defs
   (`CameraSubsystem`, `SingleBoardComputerPayload`, `FpvCamera`, `GpsModule`,
   `RadioReceiver`, `VideoTransmitter`, `ThermalVideoRecorder`) declared both
   `attribute power` and `port power`. Renamed the **port** to `power_in` and
   updated the seven `interface connect … to X.power;` lines in `SurveillanceDrone`
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

8. **FIXED — name collision `CameraSubsystem` (requirements package vs part
   def).** The requirements sub-package and the architecture part def shared the
   exact name, making the type unresolvable from `candidates.sysml`. Renamed the
   **requirements package** to `CameraRequirements`. The part def keeps the name
   `CameraSubsystem`. (Note: `README.md` prose still says "CameraSubsystem:
   7 requirements" — that now refers to package `CameraRequirements`.)

---

## B. Open items for review (David)

1. **OPEN — refinement relationship semantics.** `refines` was replaced with
   `subsets` (§A1). `subsets` means the child requirement is a specialization/
   subset of the parent (and inherits its features). If you instead want a pure
   *trace* without inheritance, the alternative is a package-level
   `dependency from <child> to <parent>;`. Both are valid; pick the intended one.

2. **OPEN — should the `analysis/*.csv` files be retired?** Their component data
   now lives in `candidates.sysml` (the single source of truth you asked for).
   The CSVs are currently kept for reference and not deleted. Recommend archiving
   them (or deleting once verified) to avoid two diverging sources.

3. **OPEN — derived analysis columns belong in the Analysis layer.** The big
   `thermal_camera_analysis_expanded.csv` is ~80% *computed* results (GSD,
   Johnson-criteria pixels-on-target, detection/recognition verdicts, SBC NPU
   load margins, pass/fail). These are NOT component attributes and were
   intentionally excluded from the candidate instances. They should be expressed
   as `constraint`/`calc`/`analysis` definitions in `DroneSystemModel::Analysis`
   that operate on the candidates, rather than precomputed in a spreadsheet.
   *(Partial precedent now exists — see §C8, the flight-time model, which reads
   the candidates and writes computed results back as SysML instances.)*

4. **OPEN — 7 airframes are excluded from the flight-time sweep for missing
   mass.** `flight_time_model.py` skips AF4a, AF5, AF6a, AF6b, AF7, AF9a, AF10
   because `candidates.sysml` has no bare-airframe `mass` for them (the §D data
   gap). Supplying those masses would let the sweep evaluate all 15 airframes.

5. **OPEN — `Airframe` has no `maxTakeoffMass` bound; feasibility is heuristic.**
   The sweep's `flyable` flag uses a rough max-thrust-by-prop-size lookup and a
   <60% hover-throttle margin, not a real thrust curve. Binding `maxTakeoffMass`
   (and ideally a thrust figure) per airframe would make feasibility rigorous.

6. **OPEN — adding *real* `Battery` candidates needs richer attributes.** The
   high-fidelity endurance model uses pack voltage, capacity, chemistry, and
   usable depth-of-discharge, but `Architecture::Battery` only has `cost_USD`,
   `mass`, and `energy`. For now the script SWEEPS *generic* generated packs (to
   inform the battery market search) and carries the rich params in the analysis
   output only. When real batteries are added to `candidates.sysml`, consider
   extending the `Battery` part def (a protected-model change) with
   `nominalVoltage`, `capacity_Ah`, `chemistry`, and `usableDoD` so the script can
   read actual packs instead of generated ones.

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

6. **DECISION — integrated digital cam+VTX modeled once.** DJI O4/O3 and
   Walksnail units are camera+VTX combos; they're modeled as `FpvCamera`
   candidates (D1–D3) and intentionally NOT duplicated as `VideoTransmitter`
   candidates. `VideoTransmitterCandidates` holds the analog VTX only.

7. **DECISION — new `part def TelemetryGroundLink`.** `telemetry_rx_candidates.csv`
   had no home in the architecture (telemetry is routed through the
   `RadioControlTransmitter` in the baseline). Added a definition to hold these
   options; it is **not** composed into `AerialThermalObservationSystem`.

8. **DECISION (2026-06-25) — high-fidelity flight-time model as a model-integrated
   script.** `analysis/flight_time_model.py` implements a momentum/actuator-disk
   endurance model (hover induced power + Glauert forward-flight induced velocity +
   parasitic drag + drivetrain efficiency + usable battery energy), the same
   physics family as eCalc/xcopterCalc. It is *integrated with the model*: it parses
   `model.sysml` + `candidates.sysml` for airframe and payload data, generates a
   grid of generic battery packs, runs a **holistic configuration sweep**
   (~137k configs: airframe × battery × SBC × VTX × thermal camera × DVR fully
   crossed; sub-1 W peripherals FPV/GPS/RX held at lightest representatives — a
   true all-brands Cartesian is ~85M and flight-time-redundant), and writes results
   back as `analysis/flight_time_results.csv` (every instance, all components +
   battery attrs + flight time) plus a SysML v2 **instance table**
   (`analysis/flight_time_instances.sysml`: a `FlightTimeResult` part def + bound
   instances for the baseline + top-100) and an `.md` summary. This is the chosen
   pattern for "compute outside SysML, document the result as model instances."
   Generated files are auto-built — never hand-edited.

   **Component-inclusion handling:** airframe-bundled VTX/FPV/GPS/RX add power only
   (mass already in the airframe weight); non-bundled peripherals add mass + power.
   RX power is derived from `currentDraw × 5 V` (RX candidates spec current, not
   power). Physics assumptions (FoM, η, ρ, C_d, frontal-area model) live in
   `PhysicsParams`; results are first-order **comparative** estimates. The *power
   bucket* in the output (cruise/wind endurance > hover) is real (translational
   lift), not an error. See OPEN items B4–B6 and DATA GAP below for gaps surfaced.

---

## D. Candidate data gaps & uncertainties (from the source CSVs)

- **DATA GAP — airframe mass/wheelbase often "N/A".** AF4a, AF5, AF6a/b, AF7
  (wheelbase given but mass N/A), AF9a, AF10 lack a bare-airframe weight; several
  lack wheelbase. `mass`/`wheelbase` were omitted for those candidates. These are
  skipped by the flight-time sweep (B4).
- **DATA GAP — BNF/PNP variants share one (bare-frame) mass.** The KOLAS7
  (AF2a/2b/2c), Chimera7 (AF8a/8b), and similar variants all carry the same
  `mass` even though the BNF builds physically include a VTX/FPV-cam/GPS/RX that
  the bare PNP does not. Because the flight-time model's inclusion logic treats a
  bundled peripheral's mass as already-in-the-airframe (adds power only), an
  understated BNF mass makes BNF variants look ~20–40 g lighter than reality and
  mildly inflates their ranking (e.g. AF2b/AF2c top the current sweep). Fix:
  record true *as-built* masses for BNF/PNP variants in `candidates.sysml`.
- **DATA GAP — Axisflying KOLAS7 BNF Analog (AF2b).** Product page names no VTX
  or FPV-camera model; `vtxModel` is "Unknown", `fpvCameraIncluded` set false
  pending seller confirmation. GPS module is manufacturer-unbranded.
- **DATA GAP — DarwinFPV X9 (AF4a) GPS** not confirmed; only 2 hardware UARTs
  (GPS via softserial is tight).
- **DATA GAP — unbranded GPS on bundled airframes** (AF2b/c, AF6a/b, AF10): exact
  module unknown ("DeepSpace/Axisflying unbranded").
- **DATA GAP — thermal module pricing is wide/uncertain** (factory-direct Chinese
  modules, InfiRay street pricing). Representative midpoints used.
- **DATA GAP — RunCam Mini DVR has two price points** ($17.99 direct / $29.99
  Amazon); modeled once at the direct price (DVR1).
- **DATA GAP — EasyCAP capture (VC4)** is only *partially* macOS-compatible
  (driver issues, not true UVC); modeled as `macOsCompatible = false`.
- **DATA GAP — several analog cameras** list estimated (`est`) illumination/power
  values; bound as given, treat as approximate.

---

## E. Cross-reference note

After the `CameraSubsystem` → `CameraRequirements` package rename (§A8), prose in
`README.md` and `CLAUDE.md` that enumerates requirement packages is slightly
stale (the package is now `CameraRequirements`; requirement IDs `R3_CAM_*` are
unchanged).
