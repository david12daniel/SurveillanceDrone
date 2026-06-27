# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **Model-Based Systems Engineering (MBSE)** project for a thermal surveillance drone (wildlife scouting), not a software codebase. There is no build, lint, or test toolchain — the "source" is engineering documentation: a SysML v2 textual model plus trade studies that evaluate real, commercially-available components against it. The work follows Agile MBSE with **git as the source of truth** for engineering decisions.

## SysML v2 authoring (tooling + syntax reference)

Before editing the model, lean on the installed tooling and the syntax reference:

- **Extension:** Syside Editor (`sensmetry.syside-editor`) is installed and gives live validation, completion, hover, and navigation for SysML v2 (language id `sysml`, free, no Java). The model targets **SysML v2.0 Beta 4**.
- **Syntax reference:** [`reference/sysml-v2-syntax.md`](reference/sysml-v2-syntax.md) is a project-tailored cheat sheet (def/usage, ports/connections, `subsets`/`satisfy` traceability, constraints/analysis, `:>`/`:>>`/`::>` operators). [`reference/sysml-v2-cheatsheet-examples.sysml`](reference/sysml-v2-cheatsheet-examples.sysml) is the canonical, extension-validated example of every construct — open it to confirm exact syntax.
- **The model files are `model.sysml` (schema) and [`candidates.sysml`](candidates.sysml) (data).** `model.sysml` holds requirements, the component `part def`s, and analysis. `candidates.sysml` holds the ~110 real component options (migrated from `analysis/*.csv`) as typed part usages with `:>>` value bindings — the single source of truth for market/trade-study data. It imports the defs via `DroneSystemModel::Architecture::*`.
- **Validation:** both files currently parse cleanly under Syside. `model.sysml` imports `ScalarValues`, `SI`, and (in `Architecture`) `Requirements::**` so primitives, units, and `satisfy` refs resolve. Keep it that way — run "Restart language server" if diagnostics look stale.
- **Trust the live diagnostics when editing** — the original model had several latent SysML v2 errors that only surfaced once the LSP was applied (see [`MODEL_ISSUES.md`](MODEL_ISSUES.md)). Don't assume a construct is valid because it "looks right"; the editor will tell you.

The hard design constraints driving everything: **≤ $2,500 total system cost**, **≥ 30 min flight time** (60 min stretch), **2.8 km range**, thermal detection/classification of deer/turkey/humans at 90–120 m AGL, and minimizing DIY soldering.

## Critical rule: do not modify `model.sysml` without approval

`model.sysml` is the authoritative system model and a protected artifact. **Never modify, move, or delete it without explicit prior approval from the user (David).** Changes require documented justification and a clear git commit. This is a standing policy — treat edits to `model.sysml` as requiring a formal request first, even for changes that look trivial.

## The system model (`model.sysml`)

A single SysML v2 textual file, one top-level `package DroneSystemModel` containing four sub-packages. Understanding how they interlock is the key to being productive here:

- **Requirements** — Top-level mission requirements `R1`–`R8` (note: `R3_1`/`R3_2`, not `R3.1`/`R3.2` — dots are invalid identifiers), plus per-subsystem requirement packages (`CameraRequirements`, `BatterySubsystem`, `SBCSubsystem`, `GCSSubsystem`, `AirframeSubsystem`). Subsystem requirements use `subsets` to trace up to the mission requirement they decompose (e.g. `R3_CAM_FOV subsets R3`, cost requirements `subsets R4`). Requirement IDs follow `R<n>_<SUBSYS>_<NAME>` (e.g. `R4_AF_PAYLOAD`). (The requirements package is `CameraRequirements`, deliberately distinct from the `CameraSubsystem` *part def* to avoid a name collision.)
- **Architecture** — `part def`s for each component (`Airframe`, `Battery`, `CameraSubsystem`, `FpvCamera`, `GpsModule`, `SingleBoardComputerPayload`, `RadioReceiver`, `VideoTransmitter`, `ThermalVideoRecorder`, `VideoReceiver`, `UsbVideoCapture`, etc.). Each part carries `attribute`s (cost_USD, mass, power…), `port`s, and formal `satisfy` statements linking it back to the requirements it fulfills. `SurveillanceDrone` composes the airborne parts and wires them with `interface connect`; `AerialThermalObservationSystem` composes drone + `GroundControlStation` + `ViewingComputer` and connects the wireless RF links. Derived attributes (`totalPower`, `totalCost`, `subTotalCost`) roll up from the leaf parts. A **`Compatibility`** sub-package (added 2026-06-26) declares which component pairings form a *real* configuration as formal SysML v2 — typed `port def`s, `enum def`s (`VideoFormat`, `RfBand`), `constraint def`s, and `interface def`s for the battery↔airframe cell-count rule (P1), the video-format chain (V1–V4), and RF band (R1–R2). `Airframe` carries `minCells_s`/`maxCells_s` for the voltage rule. The component part defs' power/video/RF ports are **typed** to these port defs, and the battery-power + video connects in `SurveillanceDrone` are typed to their interface defs (data/GNSS ports stay untyped). Syside validates the structure; the **rules are enforced by the flight-time sweep** (`model.sysml` declares, `flight_time_model.py` executes — see §C11-C12 in [`MODEL_ISSUES.md`](MODEL_ISSUES.md)).
- **Analysis** — A full parametric verification layer: `calc def`s `FlightTimeCalc` (energy / power → flight time, typed `ScalarQuantityValue` since ISQ `/` doesn't narrow to `DurationValue`) and `ScoreCalc` (flight-time magnitude / cost, via `QuantityCalculations::ToReal`); `constraint def`s `BudgetLimit` (R4, ≤ $2,500), `MinFlightTimeReq` (R6, ≥ 1800 s), `StretchFlightTimeReq` (R8, ≥ 3600 s); and two `analysis def` cases — `MinFlightTimeCheck` (subject = system; `assert constraint` on R4 + R6, returns a boolean verdict) and `TradeSpaceEvaluation` (subject = candidate; computes score + asserts budget). Thermal detection is also modeled (B3): `calc def`s `GroundSampleDistance`/`PixelsAcrossTarget`, `constraint def`s `DetectionCriterion` (≥1.5 px)/`RecognitionCriterion` (≥4 px), and `analysis def`s `ThermalDetectionCheck` (120 m, R3_1) / `ThermalRecognitionCheck` (90 m, R3_2/R3_CAM_RES) — Johnson-criteria pixels-on-target. Requirement checks compare dimensionally (`flightTime >= 1800 [s]`). Battery energy must be in joules `[J]` (`Wh × 3600`). Syside validates structure but does not execute the calcs — numeric verdicts need a SysML v2 execution engine (see [`MODEL_ISSUES.md`](MODEL_ISSUES.md) §A10).
- **Views** (added 2026-06-27) — Four SysML v2 `view def` + `view` presentations that `expose` model slices by stakeholder concern: `operationalMission` (mission requirements + system context), `logicalArchitecture` (system/drone/GCS decomposition), `interfaceBehavior` (the `Compatibility` interface layer + connections), and `systemVerification` (the Analysis layer). Syside validates the structure; diagram/table rendering needs a SysML v2 viewer. **Gotcha:** `verification` (like `interface`, `view`, `analysis`) is a reserved keyword, so the usage is named `systemVerification`, not `verification`.

When editing the model (after approval), preserve the traceability web: a new requirement should `subsets` its parent, and a new/changed part should `satisfy` the requirements it covers and feed the derived cost/power rollups. To add a component **option**, add a typed usage to the matching package in `candidates.sysml` (e.g. `part X : Airframe { :>> cost_USD = …; … }`) rather than editing the def.

Note on the `power` port: the seven payload part defs name their power input port `power_in` (not `power`, which would collide with the `attribute power` rollup). New connects should use `…power_in`.

Note: `ViewingComputer` is an existing MacBook Air — modeled as an external actor and **excluded from `totalCost`** because it is not procured. Components bundled with an airframe carry `includedWithAirframe : Boolean` and are costed as $0 in budget buildups.

## Architecture decisions baked into the model

- **Dual camera**: a non-IR `FpvCamera` for piloting plus the thermal `CameraSubsystem` for the mission (thermal is too low-res to fly by).
- **ELRS over a single RF link** handles both RC control uplink and telemetry downlink — there is deliberately no separate telemetry radio. `RadioReceiver`/`RadioControlTransmitter` absorb the telemetry role (a previous `TelemetryTransmitter`/`TelemetryReceiver` pair was merged away).
- **Onboard thermal recording** via an inline DVR (`ThermalVideoRecorder`) so footage survives RF signal loss, avoiding a second VTX. CVBS DVRs (DVR1-6, CVBS-in → microSD → pass-through to VTX) cover analog thermals; digital DVRs (DVR7-9: HDMI/USB-UVC) cover digital-output thermals. The DVR is an **earlier-stage (Phase 1-3) part only** — at the SBC stage (Phase 4) the SBC records, so the DVR is excluded from max-flight-time but retained for camera↔DVR compatibility and cost.

## `systems_engineering_plan.md` — the build roadmap

Defines four incremental phases, each listing the requirements satisfied, components required, and concrete build steps:
1. Basic LOS manual flight (airframe + ELRS + battery; ArduPilot/PX4).
2. FPV downlink + pre-programmed waypoint routes (adds FPV camera, VTX/VRX, QGroundControl).
3. EOIR thermal camera + onboard DVR recording.
4. On-board SBC detection (Jetson/RPi) + autonomous route modification via MAVLink.

## Trade studies (`analysis/`)

Each `*_market_analysis.md` / `*_trade_study.md` surveys real purchasable components against the relevant requirements. The established pattern: restate the requirement limits as a table (sourced from `model.sysml`), survey market options with specs and pass/fail per requirement, do a budget-impact check against the $2,500 cap, and end with next steps. `analysis/airframe-research.md` is the living airframe candidate down-select.

**Note:** the per-component spec data from the `analysis/*.csv` files has been consolidated into [`candidates.sysml`](candidates.sysml) (now the single source of truth for component options). The CSVs are kept for reference but may be retired — see [`MODEL_ISSUES.md`](MODEL_ISSUES.md). The narrative `*_market_analysis.md` / `*_trade_study.md` write-ups remain the human-readable rationale.

### Flight-time analysis (`analysis/flight_time_model.py`)

A high-fidelity multirotor **endurance** model that is *integrated with the SysML model*, not a standalone spreadsheet. It **reads** `candidates.sysml` (regex parser for `part X : T { :>> k = v [unit]; }` blocks — see `parse_part_blocks`), pulls every airframe, payload-component, and **real battery candidate** (BAT01–BAT21), runs a **holistic configuration sweep**, computes flight time with **momentum/actuator-disk theory + a forward-flight parasitic-drag term** (the same physics family as eCalc), and **writes back** results.

**Holistic sweep:** fully crosses the flight-time drivers — airframe × battery × SBC × VTX × thermal camera — holds the sub-1 W peripherals (FPV cam, GPS, RX) at lightest representatives, then **filters out incompatible pairings** per the model's `Compatibility` rules: **P1** battery↔airframe cell-count (drops e.g. a 4S pack on a 6S-only frame) and **V2** thermal↔DVR (a thermal no DVR can record — raw SPI/CMOS — is dropped). The **DVR is not crossed and is excluded from flight time**: it is an earlier-stage (Phase 1-3) part, so the headline endurance is the SBC-stage build (SBC present, DVR removed); the DVR is kept only for earlier-stage camera↔DVR compatibility and for cost. **Thermal camera locked to T13** (PurpleRiver Mini 640) via `FIXED_THERMAL_ID` and **SBC locked to SBC3** (NanoPi M5, RK3576) via `FIXED_SBC_ID` — David's design choices, so neither is swept (set either to `None` to sweep all again). With T13 + SBC3 fixed: **186 real configs** (all meet R4). Falls back to a generated generic LiPo/Li-ion grid only if no Battery candidates exist in `candidates.sysml`. **15 of 16 airframes participate** (AF5/EMAX Hawk 7 still lacks a confirmed mass; the discontinued KOLAS7 PNP and GEPRC MARK4 LR7 were removed 2026-06-27 — MARK4 replaced by the GEPRC MOZ7 V2 family: AF1a Analog / AF1b WTFPV / AF1c O4 Pro). **Recommended baseline:** DarwinFPV 129 (AF9a) + 4S 12Ah Amprius + T13 + SBC3 → 69.1 min hover, ~$1,505 system (well under the $2,500 R4 cap). (The earlier KOLAS7 "71 min winner" was a data artifact — its modeled mass omitted the 188 g of motors; corrected to as-built ~540–565 g, see `MODEL_ISSUES.md` §D.) See also `MODEL_ISSUES.md` §C11-C12.

**Battery source (as of 2026-06-25):** 21 real Li-ion candidates (BAT01–BAT21) in `candidates.sysml` `BatteryCandidates` package, covering all 8 cell-count/capacity types capable of >50 min hover. Voltage convention: Upgrade Energy packs use 21.6 V/14.4 V (3.6 V/cell); Lumenier/iFlight/GNB/Pyrodrone/DOGCOM use 22.2 V/14.8 V. Category 4S 12000mAh has only one confirmed product (Lumenier NAV Amprius, sold out).

**Component-inclusion logic (key):** some airframes are BNF/PNP bundles that already include a VTX/FPV-cam/GPS/RX. For a bundled peripheral the script adds **power only** (its mass is already in the airframe's as-built weight); non-bundled peripherals add **mass + power**. Driven off the airframe's `vtxIncluded`/`fpvCameraIncluded`/`gpsIncluded`/`receiverIncluded` flags. RX power is derived from `currentDraw × 5 V` (RX candidates spec current, not power).

**Outputs (auto-generated — never hand-edit; rerun the script):**
- [`analysis/flight_time_results.csv`](analysis/flight_time_results.csv) — **every** instance: all components (+ real battery attributes) and its max flight time. This is the complete dataset.
- [`analysis/flight_time_instances.sysml`](analysis/flight_time_instances.sysml) — SysML v2 **instance table** (`part def FlightTimeResult` + bound instances) for the **baseline + top-100**, validated clean in Syside.
- `analysis/flight_time_results.md` — ranked summary (by max flight time) + assumptions.
- `analysis/flight_time_value_ranking.md` — top-100 ranked by **endurance-per-dollar** (min hover per $1,000 of total system cost; R6-viable configs only).
- `analysis/cost_vs_flighttime.png` — scatter of every real config (total system cost vs flight time, coloured by airframe, with R4/R6/R8 reference lines). Generated via matplotlib if installed; skipped gracefully otherwise.

Cost is computed in the sweep too (per-component + drone total + total system incl. a fixed cheapest-GCS representative); bundled VTX/FPV/GPS/RX add $0 (already in the airframe price) and the DVR is included for cost. All top-100 endurance configs sit far under the R4 $2,500 cap (~$820–$1,360 system).

The naive `energy / power` calc in `DroneSystemModel::Analysis` (`FlightTimeCalc`) remains the in-model parametric expression; this script is the high-fidelity counterpart that produces actual numbers. Physics nuance: the **power bucket** (slow forward flight uses less power than hover via translational lift) means cruise/wind endurance can exceed hover — correct, not a bug. Assumptions (FoM 0.65, η 0.80, ρ 1.225, C_d 1.0) live in `PhysicsParams`. Airframes lacking `mass` are skipped (`MODEL_ISSUES.md` B4; AF5 only remaining gap). **BNF as-built masses corrected (2026-06-25):** all BNF variants now carry distinct masses reflecting bundled electronics (see `MODEL_ISSUES.md` §D); the KOLAS7 BNF estimates are ±20g (Axisflying does not publish as-built weights).

## Session handoffs (`session-handoffs/`)

Multi-session work is logged here as `YYYY-MM-DD.md` files. **When asked for the latest handoff, take the most recent by timestamp; when asked to save one, write it here.** A handoff captures accomplishments, design decisions (with rationale), open items/next steps, and files changed — read the latest before continuing in-flight design work.

## Agent-workspace files (context, not project work)

This repo doubles as an autonomous agent's home directory (an "OpenClaw" agent). `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `TOOLS.md`, `HEARTBEAT.md`, and `USER.md` define that agent persona and operating rules; `MEMORY.md` is its curated long-term memory. `memory/` is git-ignored. `MEMORY.md` contains personal context — treat it as private (load only in direct sessions with the user, not shared/group contexts). These files are background; the substantive engineering work lives in `model.sysml`, `systems_engineering_plan.md`, and `analysis/`.
