# Thermal Surveillance Drone — MBSE Project

A **Model-Based Systems Engineering (MBSE)** project to architect, select, and build a
thermal surveillance drone for personal wildlife scouting. The "source" is engineering
documentation — a **SysML v2** textual model plus trade studies that evaluate real,
commercially-available components against it — with **git as the source of truth** for
engineering decisions. There is no build/lint/test toolchain.

## Mission & hard constraints

Detect and classify **deer, turkey, and humans** thermally at **90–120 m AGL**, subject to:

| Constraint | Target |
|---|---|
| Total system cost (R4) | **≤ $2,500** |
| Flight time (R6 / R8 stretch) | **≥ 30 min** (60 min stretch) |
| Range — control **and** video (R7 / R4_GCS_RANGE) | **≥ 2.8 km** (hard, both links) |
| Thermal detect / recognize (R3) | Johnson ≥1.5 px @120 m / ≥4 px @90 m |
| Build | minimize DIY soldering; laptop is the ground station |

## Current status

Past the early design phase — requirements, logical architecture, a full parametric
verification layer, and **extensive component trade studies** are complete. Components
are now being **locked in**:

- ✅ **Airframe — iFlight Chimera9 ECO (9")** · ✅ **Thermal — PurpleRiver Mini 640 (640×512, USB)** · ✅ **SBC — NanoPi M5 (RK3576)**
- 🔶 Open: battery (6S 12 Ah Amprius — Lumenier vs Upgrade Energy), and ground-station specifics.
- **Reference build:** Chimera9 ECO + Lumenier 6S 12 Ah Amprius + Mini 640 + NanoPi M5 → **~58.6 min hover, ~$1,645 system** (well under the $2,500 cap).

> **The authoritative, current list of selected vs open components is [`SELECTED_COMPONENTS.md`](SELECTED_COMPONENTS.md).** Read it first.

Next up: **physical integration** — designing a 3D-printed deck to mount the SBC + thermal
camera on the airframe (see [`reference/cad-resources.md`](reference/cad-resources.md)).

## Repository layout

| Path | What it is |
|---|---|
| [`model.sysml`](model.sysml) | Authoritative SysML v2 system model — requirements, component `part def`s, compatibility, analysis, views. **Protected** (changes need explicit approval). |
| [`candidates.sysml`](candidates.sysml) | ~110 **real, purchasable** component options as typed part usages — the single source of truth for market/trade-study data. |
| [`SELECTED_COMPONENTS.md`](SELECTED_COMPONENTS.md) | Single source of truth for **what is locked vs open**. |
| [`BOM.md`](BOM.md) | Phased bill of materials (product, part #, link, cost) sorted by phase, with per-phase subtotals. |
| [`REQUIREMENTS_EXPORT_26_06_30.md`](REQUIREMENTS_EXPORT_26_06_30.md) | System/Subsystem Specification (SSS) export — all requirements, traceability, qualification (DI-IPSC-81431 content). |
| [`INTERFACE_REQUIREMENTS_EXPORT_26_06_30.md`](INTERFACE_REQUIREMENTS_EXPORT_26_06_30.md) | Interface Requirements Specification (IRS) export — all system interfaces (DI-IPSC-81434 content). |
| [`analysis/`](analysis/) | The flight-time/trade-study engine (`flight_time_model.py`), its generated outputs, and the human-readable market-analysis / trade-study write-ups. |
| [`systems_engineering_plan.md`](systems_engineering_plan.md) | The 4-phase incremental build roadmap. |
| [`reference/`](reference/) | SysML v2 syntax cheat-sheet + validated examples, and CAD/3D-model resources + modeling pathway. |
| [`MODEL_ISSUES.md`](MODEL_ISSUES.md) | Chronological decisions log + open items / data gaps. |
| [`CLAUDE.md`](CLAUDE.md) | Operating guidance for AI assistants working in this repo. |
| `session-handoffs/` | Multi-session work logs (`YYYY-MM-DD.md`). |

## The system model (`model.sysml`)

One top-level `package DroneSystemModel` with **four** sub-packages:

### Requirements
System- and subsystem-level requirements with `subsets` traceability:
- **R1–R8** — top-level mission requirements (altitude, speed, thermal detection, cost, DIY minimization, flight time, range, stretch). Note: IDs use `R3_1`/`R3_2` (dots are invalid identifiers).
- Per-subsystem packages — `CameraRequirements`, `BatterySubsystem`, `SBCSubsystem`, `GCSSubsystem`, `AirframeSubsystem` — each tracing up to its parent mission requirement (e.g. `R3_CAM_FOV subsets R3`, cost reqs `subsets R4`). IDs follow `R<n>_<SUBSYS>_<NAME>`.

### Architecture
`part def`s with attributes, ports, and formal `satisfy` traceability:
- **SurveillanceDrone** — composes the airborne parts (Airframe, Battery, CameraSubsystem [thermal], FpvCamera, GpsModule, SingleBoardComputerPayload, RadioReceiver, VideoTransmitter) wired with typed power/video interfaces; derives `totalPower`.
- **AerialThermalObservationSystem** — composes SurveillanceDrone + GroundControlStation + ViewingComputer; connects the wireless RF links; derives `totalCost` (the MacBook Air `ViewingComputer` is an external actor, excluded from cost).
- **GroundControlStation** — two-tier, laptop-based: `laptopLink` (ELRS USB dongle — primary control + telemetry) + `rcTx` (handheld radio — Phase-1/backup) + `VideoReceiver` + `UsbVideoCapture` + `groundAntenna` (5.8 GHz directional patch for video-link range margin).
- Component defs — **Airframe** (incl. `minCells_s`/`maxCells_s`, `maxThrustPerMotor_g`, and a **physical-integration layer**: `payloadDeckLength_mm`/`payloadDeckWidth_mm`/`payloadCapacity_g`/`batteryMount`), **Battery** (energy, chemistry, cells, `length/width/height_mm`), **CameraSubsystem** (thermal), **FpvCamera**, **GpsModule**, **SingleBoardComputerPayload**, **RadioReceiver**, **VideoTransmitter**, **VideoReceiver**, **UsbVideoCapture**, **Antenna** (`gain_dBi`, band, polarization — feeds the RF link budget), **AntiSparkFilter** (inline XT60, in the drone power path), **Charger** (6S Li-ion/LiPo bench charger — ground-support equipment).
- **Compatibility** (sub-package) — typed `port def`s, `enum def`s (`VideoFormat`, `RfBand`), `constraint def`s, and `interface def`s declaring which pairings are real (battery↔airframe cell-count **and connector**, video-format chain, RF band). The structure is validated by Syside; the **rules are executed by the flight-time sweep**.

### Analysis
A parametric verification layer (structure validated by Syside; numeric execution needs a SysML v2 engine — the Python model below is the high-fidelity counterpart):
- `calc def` **FlightTimeCalc** (energy ÷ power) and **ScoreCalc** (endurance-per-dollar).
- `constraint def` **BudgetLimit** (≤ $2,500), **MinFlightTimeReq** (≥ 1800 s), **StretchFlightTimeReq** (≥ 3600 s).
- `analysis def` **MinFlightTimeCheck** (asserts R4 + R6, reports R8) and **TradeSpaceEvaluation** (scores + asserts budget).
- Thermal detection — `calc def` **GroundSampleDistance** / **PixelsAcrossTarget**; `constraint def` **DetectionCriterion** (≥1.5 px) / **RecognitionCriterion** (≥4 px); `analysis def` **ThermalDetectionCheck** (120 m) / **ThermalRecognitionCheck** (90 m). Battery energy is in joules `[J]` so `energy/power` → seconds.

### Views
`view def` + `view` presentations that `expose` model slices by concern: **operationalMission**, **logicalArchitecture**, **interfaceBehavior** (the Compatibility layer), and **systemVerification** (the Analysis layer). (`verification` is a reserved keyword, hence `systemVerification`.)

## Component candidates (`candidates.sysml`)

The market data — ~110 real options as typed usages with `:>>` value bindings, importing
the defs from `model.sysml`: **23 airframes** (22 with confirmed mass), **21 Li-ion battery
packs** (BAT01–BAT21), **16 thermal cameras**, **3 SBCs**, plus VTX, FPV cameras, GPS,
receivers, and ground video receivers. To add an option, add a typed usage here
(not a new def).

## Flight-time & trade-study analysis (`analysis/flight_time_model.py`)

A high-fidelity multirotor **endurance model integrated with the SysML model** — it *reads*
`candidates.sysml`, runs a holistic configuration sweep, and *writes back* ranked results.

- **Physics:** momentum / actuator-disk theory + a forward-flight parasitic-drag term (same family as eCalc; FoM 0.65, η 0.80, ρ 1.225, Cd 1.0). Reports hover, cruise, and headwind endurance + a per-motor thrust feasibility check.
- **Compatibility filtering (executes the model's rules):** **P1** battery↔airframe cell-count. DVR compatibility filter removed (DVR dropped from architecture 2026-07-05 — SBC handles recording).
- **Cost + ground station:** per-component + drone + total-system cost, with bundled BNF/PNP peripherals at $0. The **ground video receiver is matched per-airframe to the VTX video format** (analog VRX for analog VTX; DJI/Walksnail goggles for digital air units).
- **Physical-integration check:** whether the **SBC physically fits** the airframe's usable top deck — a 3-tier verdict (fits / marginal / no-fit) from the deck/SBC dimensions.
- **Design locks:** the sweep fixes the thermal (`T13`), SBC (`SBC3`), and airframe (`AF3a`/`AF3b`, Chimera9 ECO) to the locked selections via `FIXED_*` constants (set to `None` to re-open a dimension).

**Generated outputs (auto-generated — never hand-edit; rerun `python analysis/flight_time_model.py`):**
`flight_time_results.csv` (every config + full BOM + fit), `flight_time_instances.sysml`
(top-100 as SysML instances), `flight_time_results.md` (ranked by endurance),
`flight_time_value_ranking.md` / `.csv` (ranked by endurance-per-dollar, with full BOM),
and `cost_vs_flighttime.png`. The narrative `analysis/*_market_analysis.md` /
`*_trade_study.md` write-ups carry the human-readable rationale.

## Build roadmap (`systems_engineering_plan.md`)

Three incremental phases: **(1)** basic LOS manual flight + FPV/analog video downlink to the
laptop + GPS waypoint routes (airframe + ELRS + battery + VRX/antenna + GPS + dongle) →
**(2)** thermal camera + SBC onboard recording + OpenHD digital downlink → **(3)** AI detection/autonomous route modification (software-only, no new hardware).
+ autonomous route modification via MAVLink.

## Tooling

The model targets **SysML v2.0 Beta 4** and is authored with the **Syside Editor** VS Code
extension (live validation, no Java). Both `model.sysml` and `candidates.sysml` parse cleanly;
trust the live diagnostics over assumptions. See [`reference/sysml-v2-syntax.md`](reference/sysml-v2-syntax.md).
