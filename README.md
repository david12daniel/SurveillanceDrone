# SurveillanceDrone Project

## Overview
This project aims to architect, design, and produce a thermal surveillance drone for personal use, targeting wildlife scouting applications.

We are currently in the design phase with high-level system requirements defined and an initial logical architecture established. The next steps involve executing trade studies to evaluate product solutions that meet the defined requirements and architecture.

## Project Structure

The system model (`model.md`) is a SysML v2 textual model organized into three top-level packages:

### Requirements
System-level and subsystem-level requirements with traceability:
- **R1–R8**: Top-level mission requirements (altitude, speed, thermal detection, cost, DIY minimization, flight time, range, stretch goal)
- **CameraSubsystem**: 7 requirements (mass, power, FOV, NETD, resolution, cost, interface)
- **BatterySubsystem**: 7 requirements (voltage, energy x2, mass, discharge, cost, interface)
- **SBCSubsystem**: 6 requirements (power, mass, cost, video input, video processing, data interface, temperature)
- **GCSSubsystem**: 8 requirements (range, video display, telemetry, control, battery, portability, cost, interface)
- **AirframeSubsystem**: 8 requirements (payload, mass margin, propeller config, power distribution, assembly, stiffness, landing gear, cost)

### Architecture
Component part definitions with attributes, ports, and formal `satisfy` traceability to requirements:
- **SurveillanceDrone**: Composes Airframe, Battery, CameraSubsystem, SingleBoardComputerPayload, RadioReceiver, TelemetryTransmitter, and VideoTransmitter with defined power, signal, and data interfaces; derives `totalPower`
- **AerialThermalObservationSystem**: Composes SurveillanceDrone + GroundControlStation + ViewingComputer; connects wireless RF links (RC control, telemetry, video); derives `totalCost` (display computer excluded — existing MacBook Air, not procured)
- **ViewingComputer**: External actor — existing MacBook Air, not a procured component
- **Battery**: energy, mass, cost, specificEnergy; `satisfy` ×7
- **Airframe**: mass, power, maxTakeoffMass, propDiameter, control/telemetry ports; `satisfy` ×8
- **CameraSubsystem**: mass, power, hfov, netd; `satisfy` ×7
- **SingleBoardComputerPayload**: mass, power; `satisfy` ×7
- **RadioReceiver** (onboard): RC control input from ground; `maxRange`, `protocol`
- **TelemetryTransmitter** (onboard): Status broadcast to ground; `maxRange`
- **VideoTransmitter** (onboard): Thermal video downlink; `maxRange`
- **RadioControlTransmitter** (ground): Pilot controls; `satisfy` R4_GCS_CTRL
- **TelemetryReceiver** (ground): Telemetry display; `satisfy` R4_GCS_TELEM
- **VideoReceiver** (ground): Video feed; `satisfy` R4_GCS_VIDEO_DISP
- **GroundControlStation**: Composes RadioControlTransmitter + TelemetryReceiver + VideoReceiver; `satisfy` ×8

### Analysis
Executable constraints for design verification and trade studies:
- **BudgetLimit**: total cost ≤ $2,500
- **FlightTimeCalc**: flight time = battery energy / total power
- **ScoreCalc**: score = flight time / total cost
- **MinFlightTimeCheck**: Evaluates a system instance against budget, flight time, and cost constraints
- **TradeSpaceEvaluation**: Reusable analysis for comparing candidate configurations