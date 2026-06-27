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
   as `VideoTransmitter` candidates (`VideoTransmitterCandidates` holds the analog
   VTX only). **No-double-VTX rule:** a configuration selecting an integrated
   cam+VTX (`vtxTypeRequired` = "Integrated…") must NOT also include a separate
   `VideoTransmitter` — its VTX mass and cost are already in the integrated unit. In
   the flight-time sweep this never occurs (FPV is held at a lightest representative
   and the VTX is swept separately), but the rule is documented for any future build
   that selects D1–D3. **Range vs R7 (2.8 km):** a new `FpvCamera.maxRange`
   attribute was added and populated for D1–D3 from research — DJI O4 Pro ~20 km,
   DJI O3 ~10 km, Walksnail Avatar ~4 km practical. **All three pass R7**; none are
   excluded on range (Walksnail is marginal). Rule going forward: if a future
   integrated cam+VTX cannot meet 2.8 km, that camera is not viable and is excluded.

7. **DECISION — new `part def TelemetryGroundLink`.** `telemetry_rx_candidates.csv`
   had no home in the architecture (telemetry is routed through the
   `RadioControlTransmitter` in the baseline). Added a definition to hold these
   options; it is **not** composed into `AerialThermalObservationSystem`.

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
      `SurveillanceDrone` are typed to their interface defs (`BatteryPowerInterface`,
      `VideoLink`). Data (UART/MAVLink) ports and the GNSS antenna port stay untyped
      (no compat rule); the wireless RF connects in `AerialThermalObservationSystem`
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
      composed into `GroundControlStation` as `laptopLink` (primary); `rcTx`
      (RadioControlTransmitter) is documented as backup; `subTotalCost` now =
      laptopLink + rcTx + videoRx + capture; `AerialThermalObservationSystem` wires
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
    (Requirements + `AerialThermalObservationSystem`), `logicalArchitecture`
    (system/drone/GCS decomposition), `interfaceBehavior` (the `Compatibility`
    layer + airborne connections), and `systemVerification` (the `Analysis` layer).
    Syside validates the structure; diagram/table rendering needs a SysML v2 viewer
    (none in the free Syside extension). **Lesson:** `verification` is a reserved
    keyword (like `interface`, `view`, `analysis`, `requirement`) — a bare usage
    named `verification` fails to parse ("Expected ';'"), so the usage is named
    `systemVerification`. View-def names (e.g. `VerificationView`) are fine since
    they don't collide. Optional future enhancement: add `viewpoint def`s
    (stakeholder concerns + `frame`/`require`) and `rendering`/`filter` clauses.

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

## E. Cross-reference note

**RESOLVED (2026-06-26).** Markdown prose now references the correct model element
names. `README.md`'s Architecture section was rewritten to drop the removed
`TelemetryTransmitter` / `TelemetryReceiver` parts (telemetry is carried by the
ELRS `RadioReceiver` / `RadioControlTransmitter`), fix the `SurveillanceDrone` and
`GroundControlStation` compositions, and add the current parts (`FpvCamera`,
`GpsModule`, `ThermalVideoRecorder`, `UsbVideoCapture`, the `Compatibility`
sub-package, and the thermal-detection analysis defs). The `CameraSubsystem` →
`CameraRequirements` package rename is reflected (README already listed
`CameraRequirements`). Requirement IDs `R3_CAM_*` are unchanged.
