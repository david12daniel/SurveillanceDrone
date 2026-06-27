# SurveillanceDrone Project

## Overview
This project aims to architect, design, and produce a thermal surveillance drone for personal use, targeting wildlife scouting applications.

We are currently in the design phase with high-level system requirements defined and an initial logical architecture established. The next steps involve executing trade studies to evaluate product solutions that meet the defined requirements and architecture.

## Project Structure

The system model (`model.sysml`) is a SysML v2 textual model organized into three top-level packages:

### Requirements
System-level and subsystem-level requirements with traceability:
- **R1–R8**: Top-level mission requirements (altitude, speed, thermal detection, cost, DIY minimization, flight time, range, stretch goal)
- **CameraRequirements**: 7 requirements (mass, power, FOV, NETD, resolution, cost, interface)
- **BatterySubsystem**: 7 requirements (voltage, energy x2, mass, discharge, cost, interface)
- **SBCSubsystem**: 6 requirements (power, mass, cost, video input, video processing, data interface, temperature)
- **GCSSubsystem**: 8 requirements (range, video display, telemetry, control, battery, portability, cost, interface)
- **AirframeSubsystem**: 8 requirements (payload, mass margin, propeller config, power distribution, assembly, stiffness, landing gear, cost)

### Architecture
Component part definitions with attributes, ports, and formal `satisfy` traceability to requirements:
- **SurveillanceDrone**: Composes Airframe, Battery, CameraSubsystem (thermal), FpvCamera, GpsModule, ThermalVideoRecorder, SingleBoardComputerPayload, RadioReceiver, and VideoTransmitter with defined power, video, and data interfaces; derives `totalPower`
- **AerialThermalObservationSystem**: Composes SurveillanceDrone + GroundControlStation + ViewingComputer; connects the wireless RF links (ELRS RC control + telemetry over one link; 5.8 GHz video downlink); derives `totalCost` (display computer excluded — existing MacBook Air, not procured)
- **ViewingComputer**: External actor — existing MacBook Air, not a procured component
- **Battery**: energy, mass, cost, specificEnergy, chemistry, cells_s, nominalVoltage, …; `satisfy` ×7
- **Airframe**: mass, power, maxTakeoffMass, propDiameter, minCells_s/maxCells_s, control/telemetry ports; `satisfy` ×8
- **CameraSubsystem** (thermal payload): mass, power, hfov, netd, resolution; `satisfy` ×7
- **FpvCamera**: piloting camera (analog, or integrated digital cam+VTX with `maxRange`)
- **GpsModule**: position/velocity/time to the flight controller
- **SingleBoardComputerPayload**: onboard inference (Phase 4); `satisfy` ×7
- **ThermalVideoRecorder** (onboard DVR): records thermal video in the earlier stages; CVBS + digital (HDMI/USB) variants
- **RadioReceiver** (onboard): ELRS — RC control + telemetry over one RF link; `maxRange`, `protocol`
- **VideoTransmitter** (onboard): 5.8 GHz FPV video downlink; `maxRange`
- **RadioControlTransmitter** (ground): pilot controls + telemetry forwarded to the GCS; `satisfy` R4_GCS_CTRL, R4_GCS_TELEM
- **VideoReceiver** (ground): 5.8 GHz video feed; `satisfy` R4_GCS_VIDEO_DISP
- **UsbVideoCapture** (ground): bridges the analog VRX to the laptop over USB-UVC
- **GroundControlStation**: Composes RadioControlTransmitter + VideoReceiver + UsbVideoCapture; `satisfy` ×8
- **Compatibility** (sub-package): typed ports + `enum`/`constraint`/`interface` defs declaring which component pairings are valid (battery↔airframe cell-count, video-format chain, RF band); enforced by the flight-time sweep

### Analysis
Parametric calculations, requirement constraints, and analysis cases for design
verification and trade studies:
- **FlightTimeCalc** (`calc def`): flight time = battery energy / total power
- **ScoreCalc** (`calc def`): endurance-per-dollar = flight-time magnitude / total cost
- **BudgetLimit** (`constraint def`): total cost ≤ $2,500 (R4)
- **MinFlightTimeReq** (`constraint def`): flight time ≥ 1800 s / 30 min (R6)
- **StretchFlightTimeReq** (`constraint def`): flight time ≥ 3600 s / 60 min (R8)
- **MinFlightTimeCheck** (`analysis def`): verifies a system instance — computes
  flight time, asserts budget (R4) + min flight time (R6), reports the R8 stretch
  goal, returns a pass/fail verdict
- **TradeSpaceEvaluation** (`analysis def`): scores a candidate configuration
  (flight time + endurance-per-dollar) and asserts the budget, for ranking alternatives
- **GroundSampleDistance / PixelsAcrossTarget** (`calc def`): thermal ground sample distance [m/px] and Johnson-criteria pixels-on-target
- **DetectionCriterion / RecognitionCriterion** (`constraint def`): ≥1.5 px (detect) / ≥4 px (recognize) across a target
- **ThermalDetectionCheck / ThermalRecognitionCheck** (`analysis def`): verify a thermal camera detects a 0.5 m target at 120 m (R3_1) and classifies it at 90 m (R3_2 / R3_CAM_RES)

Battery energy is expressed in joules `[J]` so `energy / power` reduces to seconds.
Syside validates the parametric structure; numeric execution of the `calc def`s
requires a SysML v2 execution engine.

### Views
SysML v2 `view def` + `view` presentations that `expose` model slices by stakeholder concern:
- **operationalMission** (`OperationalMissionView`): mission requirements (R1–R8 + decomposition) and the `AerialThermalObservationSystem` in its operating context
- **logicalArchitecture** (`LogicalArchitectureView`): the system / drone / GCS component decomposition
- **interfaceBehavior** (`InterfaceBehaviorView`): the `Compatibility` interface layer (typed ports, enums, interface defs, constraints) plus the airborne connections
- **systemVerification** (`VerificationView`): the Analysis layer (flight-time, budget, and thermal-detection calcs / constraints / cases)

Syside validates the view structure; diagram/table rendering needs a SysML v2 viewer. (`verification` is a reserved keyword, so the usage is `systemVerification`.)