package DroneSystemModel {
 // Standard library imports — primitive value types (Boolean, String, Real, Integer)
 // via ScalarValues; units via SI; ISQ quantity value types (MassValue, PowerValue,
 // EnergyValue, …) via the four ISQ sub-package imports so they resolve unqualified.
 // (Fully-qualified ISQ prefixes were dropped to save characters for the CATIA MSOSA
 // Community export; the import approach was validated in CATIA.)
 private import ScalarValues::*;
 private import SI::*;
 private import ISQBase::*;
 private import ISQMechanics::*;
 private import ISQThermodynamics::*;
 private import ISQElectromagnetism::*;

 // ── Build-phase tagging (added 2026-07-09) ──
 // PhaseTag marks the phase (per systems_engineering_plan.md) in which the
 // annotated element is expected to be FULLY implemented: satisfied in the
 // as-fielded configuration of that phase and remaining satisfied in every
 // later phase. Phase1-Phase3 = the committed build; Phase4 = the deferred
 // OpenHD video-downlink capability. Rationale for the tag assignments is
 // logged in MODEL_ISSUES.md (2026-07-09 entry).
 package Phasing {
 enum def Phase { Phase1; Phase2; Phase3; Phase4; }
 metadata def PhaseTag {
 attribute phase : Phase;
 }
 }

 package Requirements {
 private import Phasing::*;

 requirement R1 {
 doc /* The system shall operate at a nominal cruising altitude relative to ground level between 90 meters and 120 meters. */
 @PhaseTag { phase = Phase::Phase1; }
 }

 requirement R1_BHV_ALT_HOLD {
 doc /* The autonomous flight behavior (waypoint AUTO-mode route execution) shall hold the vehicle's actual altitude within the commanded 90-120m AGL survey band throughout the cruise phase of the sortie, correcting for wind and terrain variation. */
 @PhaseTag { phase = Phase::Phase1; }
 subsets R1;
 }

 requirement R2 {
 doc /* The drone shall maintain a steady ground speed of 2.23 meters/second. */
 @PhaseTag { phase = Phase::Phase1; }
 }

 requirement R2_BHV_SPEED_HOLD {
 doc /* The autonomous flight behavior (waypoint AUTO-mode route execution) shall hold the vehicle's actual ground speed at 2.23 m/s throughout the cruise phase of the sortie, correcting for sustained wind up to 4.5 m/s (R7). */
 @PhaseTag { phase = Phase::Phase1; }
 subsets R2;
 }

 requirement R3 {
 doc /* At nominal cruising altitude (90m to 120m AGL), the thermal imaging system shall enable a remote operator to detect and classify heat signatures to distinguish deer, turkey, other animals, and humans under clear daytime conditions with a minimum target-to-background temperature differential of 5°C. */
 @PhaseTag { phase = Phase::Phase3; } // fulfilled by onboard inference + telemetry alerts in the committed build (David 2026-07-09; see MODEL_ISSUES.md)
 }

 requirement R3_1 {
 doc /* Detection: A human operator viewing the live video feed shall be able to identify the presence of a deer-, turkey-, or human-sized heat source at 120m AGL with a confidence level of at least 90%. */
 @PhaseTag { phase = Phase::Phase3; } // 'operator viewing' wording predates the Phase-4 downlink deferral — rewording is a logged follow-up
 }

 requirement R3_2 {
 doc /* Classification: A human operator viewing the live video feed shall be able to correctly classify a detected heat source as deer, turkey, other animal, or human at 90m AGL with a confidence level of at least 80%. */
 @PhaseTag { phase = Phase::Phase3; } // 'operator viewing' wording predates the Phase-4 downlink deferral — rewording is a logged follow-up
 }

 requirement R4 {
 doc /* The total cost for the entire integrated system shall be under $2,500. */
 @PhaseTag { phase = Phase::Phase2; } // procurement completes with Phase 2 hardware (Phase 3 is software-only)
 }

 requirement R5 {
 doc /* The system shall minimize DIY soldering. */
 @PhaseTag { phase = Phase::Phase2; } // spans all hardware assembly; last install is Phase 2
 }

 requirement R6 {
 doc /* Minimum sustained flight time: 30 minutes in non-wind (0 m/s) conditions. */
 @PhaseTag { phase = Phase::Phase2; } // binds at the full-mission-payload configuration (final mass/power = Phase 2)
 }

 requirement R6_BHV_RTL_RESERVE {
 doc /* The autonomous flight behavior shall command an automatic return-to-launch (RTL) when usable battery energy reaches a return-energy reserve threshold sufficient to guarantee the vehicle can return to the launch point and land before energy is depleted. Reserve threshold value: see R6_FS_BATT (static worst-case parameter set, closing the former SSS §3.7 gap). */
 @PhaseTag { phase = Phase::Phase1; }
 subsets R6;
 }

 requirement R6_FS_BATT {
 doc /* Low-battery failsafe parameter set realizing R6_BHV_RTL_RESERVE's return-energy reserve threshold: a static, worst-case-distance reserve (David 2026-08-11 - a distance-adaptive reserve that shrinks as the vehicle nears the launch point was considered and deferred to Phase 3 as new SBC/Lua behavior rather than folded into this Phase 1 config item; see TASKS.md D2.17). BATT_LOW_MAH = 700 mAh (RTL trigger; a 30 percent margin over the 555 mAh bare-RTL energy cost of the worst-case 2.8 km return (R7) at RTL_SPEED = 12 m/s, the power-bucket-minimum return speed - see analysis/low_battery_reserve_analysis.md). BATT_CRT_MAH = 350 mAh (critical-landing trigger, half the low threshold - the absolute hard-floor backstop regardless of any dynamic logic added later). BATT_LOW_VOLT = 20.4 V (3.4 V/cell first-stage warning). BATT_CRT_VOLT = 19.2 V (3.2 V/cell critical stage). BATT_FS_LOW_ACT = 2 (RTL on low). BATT_FS_CRT_ACT = 1 (Land on critical). BATT_MONITOR = 4 (fuel level + voltage). RTL_SPEED = 12 m/s (the power-bucket return speed that makes the 700 mAh reserve sufficient; a slow 2.23 m/s return would need roughly 1950 mAh instead). Closes the SSS §3.7 low-battery-failsafe gap. */
 @PhaseTag { phase = Phase::Phase1; }
 subsets R6_BHV_RTL_RESERVE;
 }

 requirement R7 {
 doc /* Maximum operating range: the drone shall maintain control-link and video-link connectivity, and shall be capable of recovering under its own power, from a straight-line distance of at least 2800 meters from the GCS launch point. At this range the drone shall be able to perform surveillance at 2.2 m/s ground speed in sustained wind of 4.5 m/s. (The range drives the GCS link budget (R4_GCS_RANGE), the return-energy reserve (R6_BHV_RTL_RESERVE), and the link-loss failsafe design (R7_BHV_LINKLOSS_RTL). The sortie track length derived from R6 endurance is governed by R9.) */
 @PhaseTag { phase = Phase::Phase2; }
 }

 requirement R7_BHV_LINKLOSS_RTL {
 doc /* The autonomous flight behavior shall command an automatic return-to-launch (RTL) when the control link (ELRS) is lost beyond the flight controller's failsafe timeout, so a surveillance sortie fails safe rather than continuing uncommanded. Realization parameter set: see R7_FS_LINK (closing the former SSS §3.7 gap). */
 @PhaseTag { phase = Phase::Phase1; }
 subsets R7;
 }

 requirement R7_FS_LINK {
 doc /* Link-loss failsafe parameter set realizing R7_BHV_LINKLOSS_RTL's control-link-loss RTL trigger. FS_THR_ENABLE = 1 (enable throttle-based RC failsafe, action = RTL). FS_THR_VALUE = 900 (the ELRS receiver outputs a throttle-channel value below 900, out of the ~1000-2000 PWM range, when it has lost the transmitter signal; ArduPilot reads that as link loss). FS_OPTIONS = 0 (no continue-on-failsafe exceptions - RTL fires unconditionally on link loss, even if the vehicle is mid-investigation in GUIDED mode; David 2026-08-11 - finishing the current investigation before RTLing was considered and rejected in favor of the simpler, safer unconditional abort). Closes the SSS §3.7 link-loss-failsafe gap. */
 @PhaseTag { phase = Phase::Phase1; }
 subsets R7_BHV_LINKLOSS_RTL;
 }

 requirement R8 {
 doc /* Stretch Goal: sustained flight time of 60 minutes in non-wind (0 m/s) conditions. */
 @PhaseTag { phase = Phase::Phase2; }
 }

 requirement R9 {
 doc /* Area coverage: the system shall survey a contiguous area of at least 30 acres (12.1 hectares) in a single sortie, at the R1 nominal survey altitude and the R2 survey speed of 2.23 m/s, holding a 20 percent battery reserve. Covered area = usable swept track length x across-track flight-line spacing; the two contributing requirements are R3_CAM_FOV (sensor swath) and R4_GCS_SWEEP_SPACING (route spacing). Consistency with R6: at the R6 minimum endurance of 30 minutes the usable swept track is approximately 3210 m, which at the 46.1 m line spacing afforded by the selected 24.1 degree thermal lens covers approximately 36.6 acres. R9 is therefore satisfied by any design that meets R6, and R6 remains the governing endurance floor. R10 is the 60-acre stretch goal. */
 @PhaseTag { phase = Phase::Phase2; }
 }

 requirement R10 {
 doc /* Stretch Goal: survey a contiguous area of 60 acres (24.3 hectares) in a single sortie, at the R1 nominal survey altitude and the R2 survey speed with a 20 percent reserve. Requires approximately 49 minutes of usable endurance - above the R6 30-minute floor, but within the R8 60-minute stretch goal, which delivers approximately 73.2 acres. The reference build (Chimera9 ECO + 6S3P 12Ah Amprius, 58.4 min cruise) achieves approximately 71.2 acres and therefore already meets R10. Reported, not asserted - mirroring the R6 / R8 hard-versus-stretch pattern. */
 @PhaseTag { phase = Phase::Phase2; }
 }

 package CameraRequirements {
 requirement R3_CAM_WT {
 doc /* The camera subsystem (sensor + lens + housing + cabling) shall not exceed 200g total mass. */
 @PhaseTag { phase = Phase::Phase2; }
 }

 requirement R3_CAM_PWR {
 doc /* The camera subsystem shall consume no more than 4.5W average during continuous operation. */
 @PhaseTag { phase = Phase::Phase2; }
 }

 requirement R3_CAM_FOV {
 doc /* The thermal camera shall image a continuous across-track ground swath of at least 42 meters at the 120m AGL nominal detection altitude, where swath = 2 x altitude x tan(HFOV/2). Derived from R9 (30 acres per sortie) at the R6 minimum endurance of 30 minutes, the R2 survey speed and a 20 percent reserve: 3210 m of usable track needs 37.8 m of line spacing, hence >= 42 m of swath at the 10 percent overlap required by R4_GCS_SWEEP_SPACING. The R10 / R8 stretch pair (60 acres at 60 minutes) yields the same 42 m floor, since both pairs share the same area-per-minute ratio. Verified by analysis from the camera's specified HFOV: the selected T13 at 18 mm (HFOV 24.1 degrees) yields 51.2 m, a 22 percent margin. Supersedes the former "at least 30 degrees" form, which stated a bare lens angle rather than the ground coverage it was intended to guarantee - and which the selected 18 mm lens failed while still meeting the coverage intent. */
 @PhaseTag { phase = Phase::Phase2; }
 subsets R9;
 }

 requirement R3_CAM_NETD {
 doc /* The thermal sensor NETD (noise equivalent temperature difference) shall not exceed 50mK. */
 @PhaseTag { phase = Phase::Phase2; }
 subsets R3;   // refinement traceability (was 'refines')
 }

 requirement R3_CAM_RES {
 doc /* The thermal sensor shall provide sufficient spatial resolution such that at 90m AGL a 0.5m x 0.5m target occupies at least 4 contiguous pixels in each dimension, enabling Johnson-criteria recognition. */
 @PhaseTag { phase = Phase::Phase2; }
 subsets R3;   // refinement traceability (was 'refines')
 }

 requirement R3_CAM_COST {
 doc /* The camera subsystem cost shall not exceed 720 USD. Raised from the original 600 USD cap
 (David, 2026-08-12) after the locked T13 selection (700 USD: 640 USD base incl. the +50 USD 18mm
 lens, +60 USD shipping) exceeded it by 100 USD - tracked as a "NOT MET - waiver required" line in
 analysis/requirements_traceability.csv and analysis/verification_methods.csv since the 18mm lens
 was selected (2026-07-29). 720 USD keeps a small margin over the as-purchased 700 USD rather than
 setting the cap exactly at cost. The R4 system-level $2,500 cap is unaffected and remains well
 clear (system total ~$1,724 per analysis/flight_time_model.py). */
 @PhaseTag { phase = Phase::Phase2; }
 subsets R4;   // refinement traceability (was 'refines')
 }

 requirement R3_CAM_IF {
 doc /* The camera shall output analog CVBS or digital video (HDMI / CSI / USB) compatible with the selected SBC or VTX video input port. */
 @PhaseTag { phase = Phase::Phase2; }
 }
 }

 package BatterySubsystem {
 requirement R4_BAT_VOLT {
 doc /* The battery nominal voltage shall be within the operating input voltage range of the airframe's flight controller, ESC, and payload voltage regulators. */
 @PhaseTag { phase = Phase::Phase1; }
 }

 requirement R4_BAT_ENERGY {
 doc /* The battery shall store sufficient usable energy such that, when combined with the system total power draw as computed by FlightTimeCalc, the minimum sustained flight time of 1800 seconds (R6) is achieved. */
 @PhaseTag { phase = Phase::Phase2; } // 'system total power draw' binds at the full Phase 2 payload
 subsets R6;   // refinement traceability (was 'refines')
 }

 requirement R4_BAT_ENERGY_STRETCH {
 doc /* The battery shall store sufficient usable energy such that the stretch-goal sustained flight time of 3600 seconds (R8) is achievable. */
 @PhaseTag { phase = Phase::Phase2; }
 subsets R8;   // refinement traceability (was 'refines')
 }

 requirement R4_BAT_WT {
 doc /* The battery mass shall not exceed the payload capacity of the selected airframe when combined with all other onboard subsystems. */
 @PhaseTag { phase = Phase::Phase2; } // 'combined with all other onboard subsystems' binds at the full Phase 2 payload
 }

 requirement R4_BAT_DISCHARGE {
 doc /* The battery shall sustain continuous discharge at the system maximum current draw without triggering the airframe ESC's low-voltage cutoff or causing voltage sag that degrades flight performance. */
 @PhaseTag { phase = Phase::Phase2; } // 'system maximum current draw' includes the Phase 2 payload (motor-dominated; near-met at Phase 1)
 }

 requirement R4_BAT_COST {
 doc /* The battery cost, when summed with all other subsystem costs, shall not cause the system total cost to exceed 2500 USD (R4). */
 @PhaseTag { phase = Phase::Phase2; } // cost-sum requirements finalize when procurement completes (Phase 2)
 subsets R4;   // refinement traceability (was 'refines')
 }

 requirement R4_BAT_IF {
 doc /* The battery connector and form factor shall be physically compatible with the selected airframe's power input leads and battery mounting bay. */
 @PhaseTag { phase = Phase::Phase1; }
 }
 }

 package SBCSubsystem {
 requirement R4_SBC_PWR {
 doc /* The SBC shall consume no more than 10W average during continuous operation at cruise. */
 @PhaseTag { phase = Phase::Phase3; } // binding workload = Phase 3 NPU inference under sustained load
 }

 requirement R4_SBC_WT {
 doc /* The SBC (board + cabling + any enclosure) shall not exceed 100g total mass. */
 @PhaseTag { phase = Phase::Phase2; }
 }

 requirement R4_SBC_COST {
 doc /* The SBC cost shall not exceed 150 USD. */
 @PhaseTag { phase = Phase::Phase2; }
 subsets R4;   // refinement traceability (was 'refines')
 }

 requirement R4_SBC_VIDEO_IN {
 doc /* The SBC shall accept a video input from the thermal camera that matches the camera's video output format. */
 @PhaseTag { phase = Phase::Phase2; }
 }

 requirement R4_SBC_VIDEO_PROC {
 doc /* The SBC shall process the incoming video stream for live transmission to the ground control station without introducing a processing delay that degrades the operator's ability to detect and classify targets per R3.1 and R3.2. */
 @PhaseTag { phase = Phase::Phase4; } // live-video-to-GCS chain — deferred OpenHD downlink (David 2026-07-09)
 subsets R3;   // refinement traceability (was 'refines')
 }

 requirement R4_SBC_DATA_AF {
 doc /* The SBC shall exchange telemetry and status data with the flight controller (airframe) through the data_af interface. */
 @PhaseTag { phase = Phase::Phase3; } // FC<->SBC MAVLink integration is a Phase 3 build step
 }

 requirement R4_SBC_TEMP {
 doc /* The SBC shall operate within the full environmental temperature range of the drone system without active cooling. */
 @PhaseTag { phase = Phase::Phase3; } // worst-case thermal = sustained Phase 3 inference on passive cooling
 }
 }

 package GCSSubsystem {
 requirement R4_GCS_RANGE {
 doc /* The GCS control link and video receiver shall maintain a reliable connection with the drone at a slant range of at least 2800 meters under clear line-of-sight conditions. */
 @PhaseTag { phase = Phase::Phase1; } // ELRS control + analog FPV video links are Phase 1 hardware
 subsets R7;   // refinement traceability (was 'refines')
 }

 requirement R4_GCS_VIDEO_DISP {
 doc /* The GCS display shall render the thermal video feed at sufficient resolution, brightness, and size such that the operator can perform detection (R3.1) and classification (R3.2) tasks. */
 @PhaseTag { phase = Phase::Phase4; } // live-video-to-GCS chain — deferred OpenHD downlink (David 2026-07-09)
 subsets R3;   // refinement traceability (was 'refines')
 }

 requirement R4_GCS_SWEEP_SPACING {
 doc /* The flight planning software shall generate survey routes whose across-track flight-line spacing does not exceed 90 percent of the thermal camera's ground swath at the planned survey altitude, guaranteeing at least 10 percent overlap between adjacent passes and gap-free ground coverage of the area of interest. Verified by demonstration: plan a survey grid in the GCS application and compare the generated line spacing against 0.9 x (2 x altitude x tan(HFOV/2)). The selected GCS application (QGroundControl 4.4+) computes this natively from camera FOV and a side-overlap setting. */
 @PhaseTag { phase = Phase::Phase1; }
 subsets R9;
 }

 requirement R4_GCS_TELEM {
 doc /* The GCS display shall present real-time drone telemetry data (altitude, position, battery voltage, heading, speed) to the operator. */
 @PhaseTag { phase = Phase::Phase1; }
 }

 requirement R4_GCS_CTRL {
 doc /* The GCS shall provide flight control inputs (throttle, roll, pitch, yaw, arming, flight mode selection) with sufficient latency and resolution for safe manual operation at 2800m range. */
 @PhaseTag { phase = Phase::Phase1; }
 }

 requirement R4_GCS_BAT {
 doc /* The GCS shall operate on internal battery power for a duration matching or exceeding the drone's maximum planned flight time, without requiring external AC power during field operation. */
 @PhaseTag { phase = Phase::Phase1; }
 }

 requirement R4_GCS_WT {
 doc /* The GCS system (transmitter, display, antennas, battery) shall be portable and hand-held for field operation. */
 @PhaseTag { phase = Phase::Phase1; }
 }

 requirement R4_GCS_COST {
 doc /* The GCS cost, when summed with all other subsystem costs, shall not cause the system total cost to exceed 2500 USD (R4). */
 @PhaseTag { phase = Phase::Phase2; } // cost-sum requirements finalize when procurement completes (Phase 2)
 subsets R4;   // refinement traceability (was 'refines')
 }

 requirement R4_GCS_IF {
 doc /* The GCS receiver and transmitter shall be compatible with the drone's video transmitter and telemetry radio operating frequencies and protocols. */
 @PhaseTag { phase = Phase::Phase1; }
 }
 }

 package AirframeSubsystem {
 requirement R4_AF_PAYLOAD {
 doc /* The airframe (frame + motors + ESCs + propellers + power distribution) shall have sufficient payload capacity to carry the combined mass of all onboard subsystems (battery, camera, SBC, cabling) while maintaining stable flight. */
 @PhaseTag { phase = Phase::Phase2; } // full payload (camera + SBC) is aboard from Phase 2
 }

 requirement R4_AF_WT {
 doc /* The bare airframe mass (frame only, excluding motors, ESCs, and propellers) shall leave adequate margin such that the total takeoff mass does not exceed 80% of the airframe's rated maximum takeoff mass. */
 @PhaseTag { phase = Phase::Phase2; } // total takeoff mass finalizes with the Phase 2 payload
 }

 requirement R4_AF_PROP_CFG {
 doc /* The airframe shall accommodate propeller diameters and motor mounting patterns suitable for efficient cruise at 2.23 m/s and 90-120m AGL. */
 @PhaseTag { phase = Phase::Phase1; }
 subsets R1;   // refinement traceability (was 'refines')
 subsets R2;   // refinement traceability (was 'refines')
 }

 requirement R4_AF_PWR_DIST {
 doc /* The airframe's power distribution wiring and connectors shall supply regulated voltage to the payload subsystems (camera, SBC) and unfiltered battery voltage to the ESCs. */
 @PhaseTag { phase = Phase::Phase2; } // payload rails (SBC/camera power) are exercised from Phase 2
 }

 requirement R4_AF_ASSY {
 doc /* The airframe assembly shall minimize DIY soldering, preferring pre-soldered power distribution boards, plug-in connectors, and screw-terminal motor connections. */
 @PhaseTag { phase = Phase::Phase1; } // the airframe build itself is a Phase 1 activity (system-wide R5 completes Phase 2)
 subsets R5;   // refinement traceability (was 'refines')
 }

 requirement R4_AF_STIFF {
 doc /* The airframe structure shall be sufficiently rigid to prevent vibration-induced degradation of thermal image quality during cruise. */
 @PhaseTag { phase = Phase::Phase2; } // verifiable once the thermal camera flies (Phase 2)
 subsets R3;   // refinement traceability (was 'refines')
 }

 requirement R4_AF_LANDING {
 doc /* The airframe shall provide landing gear or structural clearance of at least 30mm below the lowest payload component to prevent ground contact during landing and takeoff. */
 @PhaseTag { phase = Phase::Phase2; } // 'lowest payload component' set by the Phase 2 camera/SBC installation
 }

 requirement R4_AF_COST {
 doc /* The complete airframe subsystem cost (frame + motors + ESCs + propellers + power distribution) shall not cause the system total cost to exceed 2500 USD (R4). */
 @PhaseTag { phase = Phase::Phase2; } // cost-sum requirements finalize when procurement completes (Phase 2)
 subsets R4;   // refinement traceability (was 'refines')
 }
 }
 }

 package Architecture {
 // Bring requirement names into scope so satisfy statements resolve unqualified.
 private import Requirements::**;

 // ── Software allocation layer (added 2026-07-10) ──
 // Existing software products (adopt/configure) and to-be-developed software,
 // composed into the component that executes them (usages in Laptop, Airframe,
 // SBCPayload). status = TO_DEVELOP marks the D-register items (D-1 thermal
 // model, D-2 mission app) from analysis/software_by_component.md; see also
 // analysis/software_gap_analysis.md and MODEL_ISSUES.md §C27–C28. This
 // register COMPLEMENTS the per-candidate software spec strings already on
 // SBCPayload/Laptop (osVersion, mlRuntime, detectionModel, gcsSoftware, …):
 // those are candidate data bound in candidates.sysml; these are the
 // product/status/traceability records.
 package Software {
 enum def SwStatus { EXISTS; TO_DEVELOP; }
 part def SoftwareItem {
 attribute productName : String;
 attribute version : String;
 attribute license : String;
 attribute status : SwStatus;
 }
 }

 // ════════════════════════════════════════════════════════════════════
 // Interface compatibility layer  (added 2026-06-26)
 // ════════════════════════════════════════════════════════════════════
 // Typed ports, constraint defs, and interface defs declare which component
 // pairings form a REAL configuration. Syside validates the structure; the
 // executable filtering that prunes the configuration sweep lives in
 // analysis/flight_time_model.py, which reads these attributes. Interfaces
 // are formalized one at a time — see the interface inventory in the latest
 // session handoff.
 package Compatibility {

 // ── Interface P1: Battery -> Airframe power  (R4_BAT_VOLT, R4_BAT_IF) ──
 // The battery pack's series-cell count must fall within the cell-count
 // window the airframe's ESC and motors are rated for. Cell count (not raw
 // voltage) is the market-standard compatibility key for FPV gear and avoids
 // the 3.6 vs 3.7 V/cell nominal-voltage ambiguity.

 // Typed power ports: a source advertises its pack cell count; a sink
 // advertises the cell-count window it accepts.
 port def PowerSourcePort {
 attribute cells_s : ScalarValues::Integer;
 attribute connector : String;                  // battery discharge connector (XT60 / XT90 / EC5)
 out power : Flows::ElectricalPower;             // the DC power this source delivers
 }
 port def PowerSinkPort {
 attribute minCells_s : ScalarValues::Integer;
 attribute maxCells_s : ScalarValues::Integer;
 attribute connector : String;                  // airframe battery-lead connector
 in power : Flows::ElectricalPower;              // the DC power this sink draws
 }

 // Compatibility predicate (boolean body — no trailing ';').
 constraint def BatteryVoltageCompatible {
 in batteryCells : ScalarValues::Integer;
 in afMinCells : ScalarValues::Integer;
 in afMaxCells : ScalarValues::Integer;
 (batteryCells >= afMinCells) and (batteryCells <= afMaxCells)
 }

 // The battery's discharge connector must match the airframe's battery-lead
 // connector (R4_BAT_IF). Different families (XT60 vs XT90 vs EC5) require an
 // adapter or re-pigtailing — flagged so the build is connector-consistent.
 constraint def ConnectorCompatible {
 in srcConn : String;
 in snkConn : String;
 srcConn == snkConn
 }

 // Interface binds a source port to a sink port and asserts the rule.
 interface def BatteryPowerInterface {
 end source : PowerSourcePort;
 end sink : PowerSinkPort;
 constraint voltageOk : BatteryVoltageCompatible {
 in batteryCells = source.cells_s;
 in afMinCells = sink.minCells_s;
 in afMaxCells = sink.maxCells_s;
 }
 constraint connectorOk : ConnectorCompatible {
 in srcConn = source.connector;
 in snkConn = sink.connector;
 }
 }

 // ── Interface V1-V4: Video signal chain  (R3_CAM_IF, R4_SBC_VIDEO_IN) ──
 // A video link is real only when the source's signal format is one the sink
 // accepts. The project's record/downlink chain is analog CVBS:
 //   thermal cam (CVBS) -> DVR (CVBS-in) -> analog VTX -> analog VRX.
 // A USB/CSI/MIPI-only thermal cannot feed the CVBS-only DVR. The canonical
 // rule here is format equality; the executable sweep matches richer
 // multi-format capability strings (e.g. "CVBS / USB") by substring.
 enum def VideoFormat {
 CVBS;
 USB_UVC;
 MIPI_CSI;
 HDMI;
 DJI_DIGITAL;
 HDZERO;
 WALKSNAIL;
 }
 port def VideoSourcePort { attribute format : VideoFormat; out video : Flows::VideoSignal; }
 port def VideoSinkPort { attribute format : VideoFormat; in video : Flows::VideoSignal; }
 constraint def VideoFormatCompatible {
 in src : VideoFormat;
 in snk : VideoFormat;
 src == snk
 }
 interface def VideoLink {
 end source : VideoSourcePort;
 end sink : VideoSinkPort;
 constraint fmtOk : VideoFormatCompatible {
 in src = source.format;
 in snk = sink.format;
 }
 }

 // ── Interface R1-R2: Wireless RF links  (R4_GCS_IF) ──
 // R1 video downlink: VTX band must match the VRX band (all candidates are
 // analog 5.8 GHz -> compatible). R2 ELRS control+telemetry: the airborne RX
 // band must be one the ground TX supports (2.4 GHz, 900 MHz, or dual). The
 // canonical rule is band equality; dual-band TX membership is handled in the
 // executable sweep.
 enum def RfBand {
 GHZ_5_8;
 GHZ_2_4;
 MHZ_900;
 }
 port def RfSourcePort { attribute band : RfBand; out rf : Flows::RfSignal; }
 port def RfSinkPort { attribute band : RfBand; in rf : Flows::RfSignal; }
 constraint def RfBandCompatible {
 in src : RfBand;
 in snk : RfBand;
 src == snk
 }
 interface def RfLink {
 end source : RfSourcePort;
 end sink : RfSinkPort;
 constraint bandOk : RfBandCompatible {
 in src = source.band;
 in snk = sink.band;
 }
 }
 }

 // ════════════════════════════════════════════════════════════════════
 // Item-flow layer  (added 2026-07-13, MODEL_ISSUES.md §C32)
 // ════════════════════════════════════════════════════════════════════
 // Documents WHAT moves across the physical/logical connections declared
 // in Drone / GCS / AerialObservationSystem. Each transfer is a named
 // `flow` written inside the body of the connection it rides over, from a
 // source `out` feature to a sink `in` feature. Payloads are typed by the
 // item defs below; the directed item features live on the Compatibility
 // power/video/RF port defs and on the message sub-ports declared here.
 package Flows {

 // ── Physical carriers ──
 item def ElectricalPower;   // DC power over a wire, USB bus power, or charge lead
 item def RfSignal;          // modulated radio energy over an antenna / the air gap
 item def VideoSignal;       // video frames (signal format carried by the port's VideoFormat)

 // ── Logical messages / serial data ──
 item def MavlinkData;       // MAVLink 2 (FC <-> SBC UART, FC <-> GCS link, router <-> app)
 item def CrsfData;          // ELRS / CRSF control uplink + telemetry (RX <-> FC)
 item def GnssData;          // u-blox UBX / NMEA position fix (GPS -> FC)
 item def InferenceData;     // thermal frames + detection results (SBC detector seam)

 // ── Directed signal sub-ports for the data-bearing plugs ──
 // (the Compatibility power/video/RF port defs already carry their own
 //  in/out item features; these cover the UART / USB-data connectors.)
 port def PowerOut { out power : ElectricalPower; }
 port def PowerIn  { in  power : ElectricalPower; }
 port def MavlinkSerial { out txMav : MavlinkData; in rxMav : MavlinkData; }   // bidirectional UART
 port def CrsfSerial    { out txCrsf : CrsfData;  in rxCrsf : CrsfData; }      // bidirectional (control up / telem down)
 port def GnssSerial    { out fix : GnssData; }                               // GPS -> FC (one-way)
 port def InferClient   { out frames : InferenceData; in detections : InferenceData; }  // mission-app side of the seam
 port def InferServer   { in  frames : InferenceData; out detections : InferenceData; }  // runtime side of the seam
 }

 part def Battery {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute energy : EnergyValue;
 attribute chemistry : String;
 attribute cells_s : Integer;
 attribute capacity_mAh : Real;
 attribute nominalVoltage : ElectricPotentialDifferenceValue;
 attribute usableDoD : Real;
 attribute cellModel : String;
 attribute maxContinuousDischarge_A : Real;
 attribute connector : String;

 // Physical envelope (for the airframe battery-bay / strap fit check) [mm]
 attribute length_mm : ScalarValues::Real;
 attribute width_mm : ScalarValues::Real;
 attribute height_mm : ScalarValues::Real;

 port pwr_out : Compatibility::PowerSourcePort;   // XT60 discharge lead
 port charge_pwr_in : Flows::PowerIn;   // charge/balance lead from the bench charger (ground ops)

 satisfy R4_BAT_VOLT;
 satisfy R4_BAT_ENERGY;
 satisfy R4_BAT_ENERGY_STRETCH;
 satisfy R4_BAT_WT;
 satisfy R4_BAT_DISCHARGE;
 satisfy R4_BAT_COST;
 satisfy R4_BAT_IF;
 }

 part def AntiSparkFilter {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute connector : String;                  // inline connector family (XT60 / XT90)
 attribute currentRating_A : ScalarValues::Real;
 attribute maxCells_s : ScalarValues::Integer;
 attribute dimensions : String;
 attribute includedWithAirframe : Boolean;

 port pwr_in : Compatibility::PowerSinkPort;    // from battery.pwr_out
 port pwr_out : Compatibility::PowerSourcePort; // to platform.battery_pwr_in

 satisfy R4_BAT_IF;

 doc /* Inline anti-spark filter / soft-start fitted between the battery and the
 airframe power lead. It limits the inrush-current spike when the pack is plugged in,
 preventing connector arcing and extending ESC/PDB capacitor life — relevant for the
 high-capacity 6S Li-ion packs. Shares the battery connector family (XT60); composed
 into Drone in the power path. */
 }

 part def Charger {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute acPower_W : ScalarValues::Real;         // AC-input charge power
 attribute dcPower_W : ScalarValues::Real;         // DC-input charge power
 attribute channels : ScalarValues::Integer;       // simultaneous charge channels
 attribute maxCells_s : ScalarValues::Integer;     // max series cells (must be >= battery cells_s)
 attribute maxCurrent_A : ScalarValues::Real;      // per-channel charge current [A]
 attribute chemistrySupport : String;              // LiPo / Li-ion / LiFe / LiHV / NiMH ...
 attribute connector : String;                     // charge-lead connector (XT60)
 attribute acIntegrated : Boolean;                 // built-in AC PSU (no external supply needed)

 port ac_pwr_in;        // AC mains input
 port charge_pwr_out : Flows::PowerOut;   // DC charge lead to the battery pack

 doc /* Bench battery charger — ground-support (enabling) equipment. Must support the
 pack's chemistry (Li-ion AND LiPo), cell count (6S), and connector (XT60), with enough
 power for the 12 Ah packs. Reusable and not flown; composed into the top-level
 AerialObservationSystem as support equipment (excluded from the per-drone R4
 cost, like the existing laptop). Candidates: candidates.sysml `ChargerCandidates`. */
 }

 part def Ubec {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute maxCurrent_A : ScalarValues::Real;
 attribute inputCellsMin_s : ScalarValues::Integer;
 attribute inputCellsMax_s : ScalarValues::Integer;

 port pwr_in : Flows::PowerIn;    // taps raw VBAT from the FC breakout pad
 port pwr_out : Flows::PowerOut;  // regulated 12V to the SBC USB-C

 doc /* Dedicated 2-6S -> 12V UBEC that powers the SBC directly off the battery. The FC's
 5V BEC cannot feed the ~10 W SBC, and raw 6S peaks above the M5's 20 V USB-C input ceiling,
 so a dedicated regulator isolates the SBC and holds it inside its 6-20 V window. Composed
 into Drone in the power path; see SELECTED_COMPONENTS.md "SBC power delivery". */
 }

 part def Airframe {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute purchaseType : String;             // PNP, BNF Analog, BNF HD, frame kit, etc.
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;         // bare airframe weight
 attribute power : PowerValue;  // cruise propulsion power draw
 attribute propDiameter : LengthValue;
 attribute propSize_in : ScalarValues::Real;  // propeller diameter [inches] (catalog value)
 attribute wheelbase : LengthValue;
 attribute flightController : String;
 attribute esc : String;
 attribute fcFirmware : String;       // RESOLVED 2026-07-10: ArduPilot ArduCopter (see the fcSoftware register part below + analysis/software_by_component.md §2)
 attribute escFirmware : String;      // e.g. "BLHeli_32 32.9" / "AM32"
 attribute fcProtocols : String;      // e.g. "CRSF-in | UBX-in | DSHOT600-out | MAVLink2-out"
 attribute minCells_s : ScalarValues::Integer;  // min battery series cells the ESC/motors are rated for
 attribute maxCells_s : ScalarValues::Integer;  // max battery series cells the ESC/motors are rated for
 attribute batteryConnector : String;           // airframe battery-lead connector (XT60 / XT90) — must match the pack (R4_BAT_IF)
 attribute maxThrustPerMotor_g : ScalarValues::Real;  // published max static thrust per motor at the build's cell count [g] (B5)
 attribute motors : String;
 attribute propModel : String;
 attribute uartCount : ScalarValues::Integer;
 attribute receiverProtocols : String;        // protocols the FC supports
 attribute receiverIncluded : Boolean;
 attribute receiverProtocol : String;         // pre-installed RX protocol, if any
 attribute vtxIncluded : Boolean;
 attribute vtxModel : String;
 attribute fpvCameraIncluded : Boolean;
 attribute fpvCameraType : String;
 attribute fpvCameraModel : String;
 attribute gpsIncluded : Boolean;
 attribute gpsModel : String;
 attribute sourceConfidence : String;         // research confidence: High / Moderate / Low
 attribute manufacturerFlightTime : String;   // max flight time claim from manufacturer or third-party review [min]; source noted in sourceConfidence
 attribute manufacturerFlightTimeBattery : String;  // battery configuration used to achieve the claimed flight time

 // Physical-integration layer (does the SBC + payload actually fit?) — see
 // MODEL_ISSUES.md §C16. The usable flat top-deck area available for a mounted
 // payload (e.g. the SBC board), the max payload the frame can lift, and where
 // the main battery mounts (which decides whether it competes with the deck).
 attribute payloadDeckLength_mm : ScalarValues::Real;  // usable top-deck length [mm]
 attribute payloadDeckWidth_mm : ScalarValues::Real;   // usable top-deck width [mm]
 attribute payloadCapacity_g : ScalarValues::Real;     // max payload (battery + gear) the frame can lift [g]
 attribute batteryMount : String;                      // "top" / "bottom" / "both"

 // Each port below = ONE physical connector/pad on the FC (BLITZ F7 + E55 ESC).
 // Combined plugs carry power + video + data on one connector; the name lists what it carries.
 // Internal BEC rails: 5V 2.5A feeds the GPS+RX plugs; 9V 2A feeds the VTX+cam plugs.
 port battery_pwr_in : Compatibility::PowerSinkPort;  // XT60 from the anti-spark
 port vbat_pwr_out : Flows::PowerOut;   // raw VBAT breakout pad -> UBEC
 port gps_pwr_dta {      // 4-pin GPS plug: 5V + UART
  port pwr : Flows::PowerOut;         // 5V to the GPS
  port gnss : ~Flows::GnssSerial;     // position fix in from the GPS
 }
 port rx_pwr_dta {       // 6-pin RX plug: 5V + UART (control uplink + telemetry)
  port pwr : Flows::PowerOut;      // 5V to the RX
  port crsf : Flows::CrsfSerial;   // CRSF control down / telemetry up
 }
 port vtx_pwr_vid_dta {  // 5-pin VTX plug: 9V + video + smartaudio UART
  port pwr : Flows::PowerOut;                  // 9V to the VTX
  port vid : Compatibility::VideoSourcePort;   // FC OSD video out to the VTX
 }
 port cam_pwr_vid {      // FPV cam pads: 9V + analog video-in
  port pwr : Flows::PowerOut;                  // 9V to the FPV camera
  port vid : Compatibility::VideoSinkPort;     // FPV camera video in to the FC OSD
 }
 port sbc_dta : Flows::MavlinkSerial;   // spare UART pads: MAVLink to the SBC (data only)

 // FC firmware — implements ALL flight functions F1–F14 (software_by_component.md §2):
 // stabilization, EKF, AUTO waypoints @2.23 m/s, GUIDED external control, CRSF/ELRS,
 // telemetry, OSD, logging. The FS_*/BATT_* failsafe parameter VALUES (R6_FS_BATT,
 // R7_FS_LINK) realize R6_BHV_RTL_RESERVE / R7_BHV_LINKLOSS_RTL (config-as-requirement).
 part fcSoftware : Software::SoftwareItem {
  :>> productName = "ArduPilot ArduCopter";
  :>> version = ">= 4.5";
  :>> license = "GPLv3";
  :>> status = Software::SwStatus::EXISTS;
  port sbc_mav : Flows::MavlinkSerial;   // MAVLink to the SBC mavlink-router (rides the sbc_dta UART)
  port gcs_mav : Flows::MavlinkSerial;   // MAVLink telemetry to the GCS (rides the ELRS link)
  satisfy R6_BHV_RTL_RESERVE;
  satisfy R6_FS_BATT;
  satisfy R7_BHV_LINKLOSS_RTL;
  satisfy R7_FS_LINK;
 }

 // The FC firmware reaches the SBC over the physical UART, not a direct SW link:
 // its MAVLink port delegates to the sbc_dta pads (which wire to the SBC uart_dta).
 interface fcMavToUart connect fcSoftware.sbc_mav to sbc_dta;
 // FC telemetry to the GCS is tunneled MAVLink-over-CRSF to the ELRS RX (rx_pwr_dta),
 // then over the ELRS RF link — it is NOT a direct SW link to QGC. Delegates to the
 // same CRSF plug the telemToRx flow already rides.
 interface fcTelemToRx connect fcSoftware.gcs_mav to rx_pwr_dta.crsf;

 satisfy R4_AF_PAYLOAD;
 satisfy R4_AF_WT;
 satisfy R4_AF_PROP_CFG;
 satisfy R4_AF_PWR_DIST;
 satisfy R4_AF_ASSY;
 satisfy R4_AF_STIFF;
 satisfy R4_AF_LANDING;
 satisfy R4_AF_COST;
 }

 part def IRCamera {
 attribute name : String;
 attribute brand : String;
 attribute purchaseUrl : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute hfov : ScalarValues::Real;        // horizontal field of view [degrees]
 attribute netd : TemperatureValue;  // noise-equiv temp diff [mK]
 attribute resolutionH : ScalarValues::Integer;   // horizontal pixels
 attribute resolutionV : ScalarValues::Integer;   // vertical pixels
 attribute pixelPitch : LengthValue;     // detector pixel pitch [um]
 attribute detectorType : String;                 // e.g. Uncooled VOx, Thermopile
 attribute spectralRange : String;                // e.g. "8-14 um" LWIR
 attribute frameRate_Hz : ScalarValues::Real;
 attribute lensOptions : String;                  // available focal lengths [mm]
 attribute outputInterface : String;              // CVBS / USB / SPI / CSI / UART
 attribute outputProtocol : String;               // e.g. "USB UVC 1.1" / "CVBS analog"
 attribute radiometric : Boolean;
 attribute dimensions : String;                   // L x W x H [mm]
 attribute inputVoltageMin : ElectricPotentialDifferenceValue;
 attribute inputVoltageMax : ElectricPotentialDifferenceValue;
 attribute operatingTempMin_C : ScalarValues::Real;  // [degC] (Celsius offset unit)
 attribute operatingTempMax_C : ScalarValues::Real;  // [degC]
 attribute detectionRange : LengthValue;    // est. human/animal detection [m]
 attribute mountTilt_deg : ScalarValues::Real;    // as-built bracket depression off NADIR [deg]:
                                                  // 0 = straight down, 45 = the SELECTED down-look
                                                  // bracket (TASKS.md 2.8, 2026-08-07). Drives the
                                                  // off-nadir GSD degradation in Analysis.

 port usb_pwr_vid {   // USB-C to the SBC: bus power in + UVC video out (one cable)
  port pwr : Flows::PowerIn;                 // 5V bus power from the SBC
  port vid : Compatibility::VideoSourcePort;
 }

 satisfy R3_CAM_WT;
 satisfy R3_CAM_PWR;
 satisfy R3_CAM_FOV;
 satisfy R3_CAM_NETD;
 satisfy R3_CAM_RES;
 satisfy R3_CAM_COST;
 satisfy R3_CAM_IF;
 }

 part def SBCPayload {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute cost_USD : ScalarValues::Real;             // total solution cost
 attribute boardCost_USD : ScalarValues::Real;
 attribute additionalCost_USD : ScalarValues::Real;
 attribute mass : MassValue;                 // total solution mass
 attribute boardMass : MassValue;
 attribute additionalMass : MassValue;
 attribute power : PowerValue;          // max inference power
 attribute idlePower : PowerValue;
 attribute soc : String;
 attribute cpu : String;
 attribute npuTOPS : ScalarValues::Real;              // NPU throughput [TOPS]
 attribute ram : String;
 attribute storage : String;
 attribute powerInput : String;
 attribute usbPortCount : ScalarValues::Integer;
 attribute uartPortCount : ScalarValues::Integer;
 attribute wifiBt : String;
 attribute videoInput : String;
 attribute videoOutput : String;
 attribute gpio : String;
 attribute coolingType : String;
 attribute dimensions : String;                       // [mm]
 attribute osSupport : String;
 attribute osVersion : String;                        // e.g. "Ubuntu 22.04 LTS (FriendlyElec image)"
 attribute mlRuntime : String;                        // e.g. "RKNN Runtime 2.x + RKNN Toolkit2"
 attribute detectionModel : String;                   // e.g. "YOLOv8n-thermal → .rknn"
 attribute mavlinkLibrary : String;                   // e.g. "pymavlink 2.4.x" / "MAVSDK-Python"
 attribute videoProtocolIn : String;                  // "USB UVC 1.1 (← thermal cam)"
 attribute mavlinkProtocol : String;                  // "MAVLink 2 UART ↔ FC"
 attribute videoProtocolOut : String;                 // "RTSP H.264 → GCS (optional)"
 attribute recordingFormat : String;                  // "MP4/H.264 → NVMe or SD"

 port usbc_pwr_in : Flows::PowerIn;   // USB-C power in (from the 12V UBEC)
 port usba1_pwr_vid {  // USB-A #1: bus power out + UVC video in (thermal camera)
  port pwr : Flows::PowerOut;               // 5V bus power to the thermal camera
  port vid : Compatibility::VideoSinkPort;
 }
 port usba2_pwr_dta {  // USB-A #2: bus power out + data (OpenHD air module, Phase 4)
  port pwr : Flows::PowerOut;                  // 5V bus power to the air unit
  port vid : Compatibility::VideoSourcePort;   // encoded thermal video to the air unit
 }
 port uart_dta : Flows::MavlinkSerial;   // GPIO UART: MAVLink to the FC

 // ── SBC software stack (software_by_component.md §3) ──
 // The two TO_DEVELOP items below are the project's ENTIRE development scope.
 part rknnRuntime : Software::SoftwareItem {
  :>> productName = "RKNN-Toolkit2 runtime (librknnrt)";
  :>> version = "2.x";
  :>> license = "Rockchip (free redistribution)";
  :>> status = Software::SwStatus::EXISTS;
  port infer : Flows::InferServer;   // frames in / detections out (to missionApp); executes thermalModel
 }
 part mavlinkRouter : Software::SoftwareItem {
  :>> productName = "mavlink-router";
  :>> version = "current";
  :>> license = "Apache-2.0";
  :>> status = Software::SwStatus::EXISTS;
  port app : Flows::MavlinkSerial;   // MAVLink to the mission app (localhost)
  port fc : Flows::MavlinkSerial;    // MAVLink to the FC (rides the uart_dta UART)
  satisfy R4_SBC_DATA_AF;
 }
 part missionApp : Software::SoftwareItem {
  doc /* D-2: onboard mission application — the software realization of
       DroneSystemBehavior::SweepAndDetect / InvestigateAndClassify (UC-5):
       capture -> inference -> POI geotag -> operator alert -> AUTO<->GUIDED
       mode control -> classify retry/timeout. Uses pymavlink internally.
       Control-contract skeleton EXISTS AND IS TESTED (analysis/autonomy_sim,
       MODEL_ISSUES.md §C26); remaining scope in software_by_component.md D-2. */
  :>> productName = "Onboard mission application (D-2)";
  :>> version = "0.1 skeleton (analysis/autonomy_sim)";
  :>> license = "project-developed";
  :>> status = Software::SwStatus::TO_DEVELOP;
  port frameIn : Compatibility::VideoSinkPort;   // UVC thermal frames captured from the usba1 port
  port mav : Flows::MavlinkSerial;     // MAVLink to the router (commands out / telemetry in)
  port infer : Flows::InferClient;   // frames out / detections in (the Detector seam, to rknnRuntime)
 }
 part thermalModel : Software::SoftwareItem {
  doc /* D-1: LWIR wildlife detection/classification model (640x512; deer /
       turkey / other animal / human). Two operating points: presence >= 90%
       at 120 m (R3_1) and species >= 80% at 90 m (R3_2). No COTS/OSS product
       exists; training data largely self-collected — the schedule long pole.
       Deploys as a .rknn artifact executed by rknnRuntime. */
  :>> productName = "LWIR wildlife detect/classify model (D-1)";
  :>> version = "none yet";
  :>> license = "project-developed (AGPL training-stack caveat)";
  :>> status = Software::SwStatus::TO_DEVELOP;
  satisfy R3_1;
  satisfy R3_2;
 }

 // ── SBC-internal software interconnections (MODEL_ISSUES.md §C31/§C32) ──
 // Thermal frames arriving on the usba1 UVC port are delegated to the mission
 // app's capture input — the physical SOURCE of the Detector-seam frames below.
 // Port delegation — no own flow: the VideoSignal already flows onto usba1 (camToSbc)
 // and this connector hands that same input to the mission app.
 interface uvcToApp connect usba1_pwr_vid.vid to missionApp.frameIn;
 // The mavlink-router owns the SBC's physical UART — it does NOT interface with
 // the FC directly. Its FC-facing port delegates to uart_dta and the MAVLink
 // rides the uart_dta<->sbc_dta wire (sbcMavUart) to the FC (delegation, no flow).
 interface routerToUart connect mavlinkRouter.fc to uart_dta;
 // On-board IPC (localhost) — no physical wire; the mission app is the hub.
 connection appToRouter connect missionApp.mav to mavlinkRouter.app {   // MAVLink app <-> router
  flow appToRouterMav from missionApp.mav.txMav to mavlinkRouter.app.rxMav;
  flow routerToAppMav from mavlinkRouter.app.txMav to missionApp.mav.rxMav;
 }
 connection detectorSeam connect missionApp.infer to rknnRuntime.infer {   // frames out / detections in (Detector seam)
  flow frameFeed from missionApp.infer.frames to rknnRuntime.infer.frames;
  flow detectionFeed from rknnRuntime.infer.detections to missionApp.infer.detections;
 }
 allocate thermalModel to rknnRuntime;             // the .rknn is loaded + executed by the runtime

 satisfy R4_SBC_PWR;
 satisfy R4_SBC_WT;
 satisfy R4_SBC_COST;
 satisfy R4_SBC_VIDEO_IN;
 satisfy R4_SBC_VIDEO_PROC;
 satisfy R4_SBC_DATA_AF;
 satisfy R4_SBC_TEMP;
 }

 part def FpvCamera {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute includedWithAirframe : Boolean;
 attribute maxRange : LengthValue;           // video-link range when integrated cam+VTX (checked vs R7); N/A for separate-VTX cams
 attribute cameraType : String;                       // Analog CMOS / Digital MIPI / etc.
 attribute cameraModel : String;
 attribute sensorSize : String;                       // e.g. 1/3", 1/1.8"
 attribute resolutionTVL : ScalarValues::Real;        // analog resolution [TVL]
 attribute fovLens : String;                          // lens / field of view
 attribute minIllumination_lux : ScalarValues::Real;  // [lux]
 attribute inputVoltageMin : ElectricPotentialDifferenceValue;
 attribute inputVoltageMax : ElectricPotentialDifferenceValue;
 attribute outputType : String;                       // CVBS analog / MIPI / DJI digital
 attribute connectorType : String;
 attribute mountingPattern : String;
 attribute vtxTypeRequired : String;
 attribute goggleCompatibility : String;

 port pwr_vid {   // cam pads to FC: power in + analog video out
  port pwr : Flows::PowerIn;                 // 9V from the FC
  port vid : Compatibility::VideoSourcePort;
 }

 doc /* Non-IR FPV camera used for piloting. May be included with the airframe purchase (BNF/PNP bundles) or purchased separately. Distinct from the thermal IRCamera which is the mission payload. */
 }

 part def GpsModule {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute includedWithAirframe : Boolean;
 attribute chipset : String;
 attribute constellations : String;                   // GPS+GLO+GAL+BDS, etc.
 attribute coldStart : DurationValue;        // [s]
 attribute hotStart : DurationValue;         // [s]
 attribute updateRate_Hz : ScalarValues::Real;
 attribute accuracyCEP : LengthValue;        // circular error probable [m]
 attribute voltageMin : ElectricPotentialDifferenceValue;
 attribute voltageMax : ElectricPotentialDifferenceValue;
 attribute currentDraw : ElectricCurrentValue;  // [mA]
 attribute compass : String;                          // magnetometer model, or "No"
 attribute connector : String;
 attribute mounting : String;
 attribute dimensions : String;                       // [mm]
 attribute firmware : String;                         // e.g. "u-blox M10 HPG 1.32 (factory)"
 attribute outputProtocol : String;                   // "UBX binary" / "NMEA 0183"

 port pwr_dta {    // 4-pin plug to FC: 5V power in + UART
  port pwr : Flows::PowerIn;      // 5V from the FC
  port gnss : Flows::GnssSerial;  // position fix out to the FC
 }
 port gnss_rf_in : Compatibility::RfSinkPort;  // GNSS antenna (satellite RF in)

 doc /* GPS module providing position, velocity, and time data to the flight controller. Critical for return-to-home and autonomous waypoint navigation (Phase 1+). May be pre-installed with some airframe packages. */
 }

 part def RadioReceiver {
 attribute name : String;
 attribute manufacturer : String;
 attribute purchaseUrl : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute maxRange : LengthValue;          // LOS range [km]
 attribute protocol : String;                        // CRSF, etc.
 attribute elrsFirmware : String;                    // e.g. "ExpressLRS 3.5.2" — must match TX12 version
 attribute interfaceType : String;                   // CRSF / CRSF+UART
 attribute band : String;                            // 2.4 GHz / 900 MHz
 attribute size : String;                            // [mm]
 attribute antennaType : String;
 attribute telemetryPower : PowerValue; // [mW]
 attribute paLna : Boolean;                          // has PA/LNA front end
 attribute diversityType : String;
 attribute tcxo : Boolean;
 attribute currentDraw : ElectricCurrentValue; // [mA]
 attribute mcu : String;
 attribute rfChip : String;
 attribute includedWithAirframe : Boolean;
 attribute telemetryCapable : Boolean = true; // ELRS handles bidirectional RC + telemetry over one RF link

 port pwr_dta {   // plug to FC: 5V power in + UART (control out + telemetry in, one link)
  port pwr : Flows::PowerIn;       // 5V from the FC
  port crsf : Flows::CrsfSerial;   // CRSF control down / telemetry up
 }
 port rf_in_a : Compatibility::RfSinkPort;   // 2.4 GHz true-diversity antenna A
 port rf_in_b : Compatibility::RfSinkPort;   // 2.4 GHz true-diversity antenna B

 doc /* Bidirectional RF link using ELRS (ExpressLRS) protocol. Handles both RC control input (uplink) and telemetry return (downlink) over a single RF link, eliminating the need for a separate telemetry radio. Telemetry capability based on ELRS range analysis — see analysis/ELRS_telemetry_range_analysis.md. */
 }

 part def RcTx {
 attribute name : String;
 attribute brand : String;
 attribute purchaseUrl : String;
 attribute txType : String;                          // Integrated Controller / Standalone TX Module
 attribute formFactor : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute maxRange : LengthValue;          // est. ELRS range [km]
 attribute internalTxPower : PowerValue; // [mW]
 attribute frequencyBands : String;                  // 2.4 GHz / 900 MHz
 attribute elrsVersion : String;
 attribute hasExternalModuleBay : Boolean;
 attribute moduleBayType : String;                   // JR / Nano / Micro
 attribute firmware : String;                        // EdgeTX / OpenTX
 attribute mcu : String;
 attribute displayType : String;
 attribute dimensions : String;                      // [mm]
 attribute batteryConfig : String;
 attribute batteryIncluded : Boolean;
 attribute maxChannels : ScalarValues::Integer;
 attribute gimbalType : String;
 attribute usbCCharging : Boolean;
 attribute trainerPort : Boolean;
 attribute sdCardSlot : Boolean;
 attribute telemetryCapable : Boolean = true; // ELRS TX module receives telemetry and pipes to GCS via USB

 port user_controls;   // operator sticks/switches (human input)
 port telem_dta_out : Flows::MavlinkSerial;   // USB to the laptop: telemetry/joystick data
 port rf_out : Compatibility::RfSourcePort;   // 2.4 GHz antenna to the drone RX

 satisfy R4_GCS_CTRL;
 satisfy R4_GCS_TELEM;

 doc /* Ground-side RC transmitter with ELRS module. Transmits RC control uplink and receives telemetry downlink on the same RF link. Telemetry data is forwarded to the GCS laptop via USB/Bluetooth. */
 }

 part def Vtx {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute vtxType : String;                         // Analog VTX / Integrated Digital VTX+Cam
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute power : PowerValue;          // power draw at max output
 attribute maxRange : LengthValue;           // est. max range [km]
 attribute protocolControl : String;                 // SmartAudio / IRC Tramp / DJI
 attribute frequencyBand : String;                   // 5.8 GHz / 2.4 GHz
 attribute outputPowerLevels : String;               // selectable levels [mW]
 attribute maxOutputPower : PowerValue; // highest RF output level [mW]
 attribute inputVoltageMin : ElectricPotentialDifferenceValue;
 attribute inputVoltageMax : ElectricPotentialDifferenceValue;
 attribute antennaConnector : String;
 attribute mountingPattern : String;
 attribute audio : String;
 attribute channelCount : ScalarValues::Integer;
 attribute pitMode : Boolean;
 attribute includedWithAirframe : Boolean;

 port pwr_vid_dta {   // 5-pin plug to FC: 9V power in + video in + smartaudio UART
  port pwr : Flows::PowerIn;                // 9V from the FC
  port vid : Compatibility::VideoSinkPort;
 }
 port rf_out : Compatibility::RfSourcePort;   // 5.8 GHz antenna

 doc /* 5.8 GHz video transmitter for FPV piloting downlink. May be included with the airframe purchase (BNF/PNP) or purchased separately. */
 }

 part def Vrx {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute vrxType : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute inputFrequency : String;                // 5.8 GHz
 attribute outputToLaptop : String;                // USB via UVC capture, etc.
 attribute antenna : String;
 attribute range : LengthValue;           // [km] (VRX + antenna dependent)
 attribute diversity : String;                     // None / Optional / True
 attribute macOsCompatible : Boolean;
 attribute includedWithAirframe : Boolean;

 port rf_in : Compatibility::RfSinkPort;           // 5.8 GHz antenna
 port vid_out : Compatibility::VideoSourcePort;    // analog video to the capture card

 satisfy R4_GCS_VIDEO_DISP;

 doc /* Ground-side video receiver for live FPV downlink. Not typically bundled with airframe (sold separately or as part of GCS/goggles kit). Outputs analog composite video. */
 }

 part def UsbCap {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute captureType : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute inputType : String;                     // RCA composite / CVBS / HDMI
 attribute outputUsb : String;                     // USB-A / USB-C
 attribute protocol : String;                      // UVC 1.0, proprietary
 attribute maxResolution : String;
 attribute frameRate_fps : ScalarValues::Real;
 attribute macOsCompatible : Boolean;
 attribute driverlessUVC : Boolean;
 attribute busPowered : Boolean;

 port vid_in : Compatibility::VideoSinkPort;   // analog video from the VRX (CVBS)
 port usb_pwr_dta {   // USB to the laptop: bus power in + UVC video out
  port pwr : Flows::PowerIn;                 // USB bus power from the laptop
  port vid : Compatibility::VideoSourcePort;
 }

 doc /* Analog-to-USB video capture dongle. Converts analog CVBS/composite video from the VRX to USB Video Class (UVC) format readable by the laptop's OS. Used to pipe live FPV video into QGC / Mission Planner. Typical cost $10-25. */
 }

 part def TelemetryGroundLink {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute approach : String;                      // radio USB passthrough / standalone dongle / DIY
 attribute connectionToLaptop : String;            // USB-C virtual COM, USB-A serial, etc.
 attribute frequency : String;                     // 2.4 GHz / 900 MHz
 attribute rangeAt2_8kmOk : Boolean;               // maintains link at the 2.8 km requirement
 attribute macOsCompatible : Boolean;
 attribute cost_USD : ScalarValues::Real;
 attribute extraHardwareNeeded : String;

 port rf_out : Compatibility::RfSourcePort;  // 2.4 GHz antenna to the drone RX
 port usb_pwr_dta {    // USB to the laptop (bus power + data)
  port pwr : Flows::PowerIn;
  port mav : Flows::MavlinkSerial;
 }

 doc /* Ground-side ELRS USB dongle: plugs into the GCS laptop and provides the
 PRIMARY bidirectional control + telemetry link for Phase 1+ autonomous operation,
 in place of a handheld radio. (The RcTx is retained as a
 Phase-1 / backup manual-control path.) The candidates in analysis/ capture the
 standalone-dongle vs radio-passthrough vs DIY options. Composed into
 GCS as `laptopLink`. */
 }

 part def OhdWifiTx {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute chipset : String;
 attribute txPower_dBm : ScalarValues::Real;      // max transmit power [dBm]
 attribute usbStandard : String;                  // "USB 2.0" / "USB 3.0"
 attribute antennaConnector : String;             // connector on the adapter (IPEX/u.fl, RP-SMA)
 attribute antennaPortCount : ScalarValues::Integer;
 attribute dimensions : String;                   // [mm]
 attribute driverName : String;                   // DKMS driver package name
 attribute power : PowerValue;      // estimated power draw at max TX [W]

 port usb_pwr_dta {                               // USB from SBC USB-A #2 (bus power + data)
  port pwr : Flows::PowerIn;                 // 5V bus power from the SBC
  port vid : Compatibility::VideoSinkPort;   // encoded thermal video from the SBC
 }
 port rf_out_a : Compatibility::RfSourcePort;     // u.fl MIMO chain A -> air antenna A
 port rf_out_b : Compatibility::RfSourcePort;     // u.fl MIMO chain B -> air antenna B

 satisfy R4_GCS_VIDEO_DISP;
 satisfy R4_GCS_RANGE;

 doc /* Air-side WiFi adapter for OpenHD/WFB-ng digital video downlink (Phase 2+).
 Connects to the SBC via USB and operates in raw monitor-mode TX (packet injection)
 at 5825 MHz channel 165, transmitting the SBC-encoded H.264 thermal video stream
 to the ground station. Requires an ARM64 Linux DKMS driver. See
 analysis/openhd-air-wifi-adapter-trade-study.md. */
 }

 part def OhdGndRx {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute chipset : String;
 attribute rxSensitivity_dBm : ScalarValues::Real; // MCS1 receive sensitivity [dBm]
 attribute usbStandard : String;
 attribute antennaPortCount : ScalarValues::Integer;
 attribute antennaConnector : String;              // e.g. "RP-SMA female"
 attribute dimensions : String;
 attribute driverName : String;
 attribute vmCompatibility : String;               // "VMware Fusion xHCI / Parallels Desktop 20.3+"
 attribute power : PowerValue;

 port rf_in_a : Compatibility::RfSinkPort;         // ground antenna A
 port rf_in_b : Compatibility::RfSinkPort;         // ground antenna B
 port usb_pwr_dta {                                // USB to the laptop (bus power + video data)
  port pwr : Flows::PowerIn;                 // USB bus power from the laptop
  port vid : Compatibility::VideoSourcePort; // decoded thermal video to the laptop
 }

 satisfy R4_GCS_VIDEO_DISP;
 satisfy R4_GCS_RANGE;

 doc /* Ground-side WiFi adapter for OpenHD/WFB-ng digital thermal video reception.
 Plugs into the MacBook Air (USB-C) and is passed through to an ARM64 Ubuntu 22.04
 Linux VM (VMware Fusion, xHCI mode). WFB-ng runs inside the VM, decodes the stream,
 and forwards it to the host macOS as RTSP over loopback. Requires ARM64 DKMS driver
 inside the VM. See analysis/openhd-ground-wifi-adapter-trade-study.md. */
 }

 part def Antenna {
 attribute name : String;
 attribute purchaseUrl : String;
 attribute cost_USD : ScalarValues::Real;
 attribute mass : MassValue;
 attribute gain_dBi : ScalarValues::Real;          // antenna gain [dBi / dBic]
 attribute frequencyBand : String;                 // e.g. "5.8 GHz"
 attribute antennaType : String;                   // patch / panel / omni / dipole
 attribute polarization : String;                  // RHCP / LHCP / linear
 attribute beamwidth_deg : ScalarValues::Real;     // -3 dB beamwidth [deg] (0 = omni)
 attribute connector : String;                     // RP-SMA / SMA / MMCX
 attribute includedWithAirframe : Boolean;

 port rf_in : Compatibility::RfSinkPort;    // captures the over-air RF from the drone
 port rf_out : Compatibility::RfSourcePort; // coax feedline to the receiver

 satisfy R4_GCS_RANGE;

 doc /* A directional ground-station antenna (e.g. a 5.8 GHz patch) fitted to the
 Vrx to raise the video-link gain so the downlink closes the 2.8 km range
 requirement (R4_GCS_RANGE) with margin. Gain feeds the RF link budget — see
 analysis/rf_link_budget.md. */
 }

 part def GCS {
 attribute batteryEnergy : EnergyValue;

 // GCS external boundary: the human operator (display + controls). RF to the drone is via the antenna parts below.
 port operator_ui;

 // PRIMARY (Phase 1+): ELRS USB dongle to the laptop carries control + telemetry.
 part laptopLink : TelemetryGroundLink;  // PRIMARY control + telemetry via laptop USB
 // BACKUP / Phase 1: handheld ELRS radio for manual control if the laptop fails.
 part rcTx : RcTx;    // BACKUP / Phase-1 manual control
 part videoRx : Vrx;           // Analog 5.8 GHz VRX (live FPV piloting video to laptop)
 part capture : UsbCap;         // Bridges analog VRX to laptop USB
 part groundAntenna : Antenna;           // 5.8 GHz RHCP patch on the analog VRX (range margin)
 // Phase 2+: OpenHD digital thermal video downlink ground node
 part openHDRx : OhdGndRx;   // Alfa AWUS036ACH — WFB-ng RX via Linux VM on MacBook
 part openHDAntennaA : Antenna;          // Lumenier AXII Quadro #1 — diversity RX panel
 part openHDAntennaB : Antenna;          // Lumenier AXII Quadro #2 — diversity RX panel
 // The operator's laptop (existing equipment, excluded from cost) is the core of the GCS.
 part viewingComputer : Laptop;
 // Ground-support (bench) battery charger — reusable, not flown, excluded from cost.
 part charger : Charger;

 // Internal GCS wiring. openHDAntennaA/B are the GROUND antennas (Foxeer Echo) feeding the ground RX.
 interface gndVideoRf connect groundAntenna.rf_out to videoRx.rf_in {                     // patch antenna → analog VRX
  flow fpvVideoRf from groundAntenna.rf_out.rf to videoRx.rf_in.rf;
 }
 interface gndOhdRfA connect openHDAntennaA.rf_out to openHDRx.rf_in_a {                  // ground antenna A → OpenHD RX
  flow ohdVideoRxA from openHDAntennaA.rf_out.rf to openHDRx.rf_in_a.rf;
 }
 interface gndOhdRfB connect openHDAntennaB.rf_out to openHDRx.rf_in_b {                  // ground antenna B → OpenHD RX
  flow ohdVideoRxB from openHDAntennaB.rf_out.rf to openHDRx.rf_in_b.rf;
 }
 interface vrxToCapture : Compatibility::VideoLink connect videoRx.vid_out to capture.vid_in {  // analog VRX (CVBS) → USB capture
  flow analogVideo from videoRx.vid_out.video to capture.vid_in.video;
 }
 // Each laptop USB device on its own host port
 interface captureUsb connect capture.usb_pwr_dta to viewingComputer.usb_cap_pwr_dta {    // capture dongle → laptop (USB)
  flow captureBusPower from viewingComputer.usb_cap_pwr_dta.pwr.power to capture.usb_pwr_dta.pwr.power;
 }
 interface capToLaptop : Compatibility::VideoLink connect capture.usb_pwr_dta.vid to viewingComputer.usb_cap_pwr_dta.vid {  // UVC video → laptop
  flow uvcVideo from capture.usb_pwr_dta.vid.video to viewingComputer.usb_cap_pwr_dta.vid.video;
 }
 interface ohdGndUsb connect openHDRx.usb_pwr_dta to viewingComputer.usb_ohd_pwr_dta {   // OpenHD thermal video → laptop
  flow ohdRxBusPower from viewingComputer.usb_ohd_pwr_dta.pwr.power to openHDRx.usb_pwr_dta.pwr.power;
  flow ohdThermalToLaptop from openHDRx.usb_pwr_dta.vid.video to viewingComputer.usb_ohd_pwr_dta.vid.video;
 }
 interface elrsDongleUsb connect laptopLink.usb_pwr_dta to viewingComputer.usb_elrs_pwr_dta { // PRIMARY control + telemetry → laptop
  flow elrsDongleBusPower from viewingComputer.usb_elrs_pwr_dta.pwr.power to laptopLink.usb_pwr_dta.pwr.power;
  flow gcsToDongleMav from viewingComputer.usb_elrs_pwr_dta.mav.txMav to laptopLink.usb_pwr_dta.mav.rxMav;
  flow dongleToGcsMav from laptopLink.usb_pwr_dta.mav.txMav to viewingComputer.usb_elrs_pwr_dta.mav.rxMav;
 }
 interface radioUsb connect rcTx.telem_dta_out to viewingComputer.usb_radio_dta {       // BACKUP telemetry → laptop
  flow backupTelem from rcTx.telem_dta_out.txMav to viewingComputer.usb_radio_dta.rxMav;
 }

 // Derived total GCS component cost (all ground-side hardware; laptop itself excluded as existing equipment)
 attribute subTotalCost : ScalarValues::Real =
 laptopLink.cost_USD + rcTx.cost_USD + videoRx.cost_USD + capture.cost_USD + groundAntenna.cost_USD
 + openHDRx.cost_USD + openHDAntennaA.cost_USD + openHDAntennaB.cost_USD;

 satisfy R4_GCS_RANGE;
 satisfy R4_GCS_VIDEO_DISP;
 satisfy R4_GCS_TELEM;
 satisfy R4_GCS_CTRL;
 satisfy R4_GCS_BAT;
 satisfy R4_GCS_WT;
 satisfy R4_GCS_COST;
 satisfy R4_GCS_IF;

 doc /* Ground control station = the operator's laptop plus a minimal RF front-end.
 PRIMARY link (Phase 1+): an ELRS USB dongle (laptopLink) for bidirectional control
 + telemetry, plus an analog 5.8 GHz VRX + USB capture for live video — all through
 the laptop. A handheld ELRS radio (rcTx) is retained for Phase-1 manual flight and
 as a backup if the laptop link fails. The laptop itself (Laptop) is
 existing equipment, excluded from procurement cost. */

 // CATIA MSOSA diagram binding (DS_Views library; does not resolve in Syside).

 }

 part def Drone {

 part platform : Airframe;
 part battery : Battery;
 part antiSpark : AntiSparkFilter;  // inline between battery and platform power lead (shared XT60)
 part camera : IRCamera;
 part fpvCam : FpvCamera;
 part gps : GpsModule;
 part sbc : SBCPayload;
 part rx : RadioReceiver;  // ELRS — handles both RC control and telemetry
 part vtx : Vtx;
 part wifiTx : OhdWifiTx;  // Phase 2+: OpenHD digital thermal video downlink
 part ubec : Ubec;             // dedicated 12V SBC supply off the battery
 part vtxAntenna : Antenna;    // 5.8 GHz analog video dipole
 part rxAntennaA : Antenna;    // 2.4 GHz ELRS true-diversity antenna A
 part rxAntennaB : Antenna;    // 2.4 GHz ELRS true-diversity antenna B
 part wifiAntennaA : Antenna;  // OpenHD air antenna A (cloverleaf)
 part wifiAntennaB : Antenna;  // OpenHD air antenna B (cloverleaf)

 // --- Battery bus: battery -> anti-spark -> ESC/FC
 interface batteryToFilter connect battery.pwr_out to antiSpark.pwr_in {
  flow packDischarge from battery.pwr_out.power to antiSpark.pwr_in.power;   // pack discharge into the anti-spark
 }
 interface batteryPwr : Compatibility::BatteryPowerInterface connect antiSpark.pwr_out to platform.battery_pwr_in {
  flow packPower from antiSpark.pwr_out.power to platform.battery_pwr_in.power;   // 6S pack power to the ESC/FC
 }
 // UBEC taps raw VBAT from the FC breakout pad; SBC on its own 12V supply (NOT the FC BEC)
 interface ubecSupply connect platform.vbat_pwr_out to ubec.pwr_in {
  flow vbatToUbec from platform.vbat_pwr_out.power to ubec.pwr_in.power;   // raw VBAT tap to the UBEC
 }
 interface sbcSupply connect ubec.pwr_out to sbc.usbc_pwr_in {
  flow ubecToSbc from ubec.pwr_out.power to sbc.usbc_pwr_in.power;   // regulated 12 V to the SBC
 }
 // --- FC peripheral plugs: each connect = ONE physical connector (power+video+data as named)
 interface gpsLink connect platform.gps_pwr_dta to gps.pwr_dta {
  flow gpsPower from platform.gps_pwr_dta.pwr.power to gps.pwr_dta.pwr.power;   // 5V to the GPS
  flow gpsFix from gps.pwr_dta.gnss.fix to platform.gps_pwr_dta.gnss.fix;       // position fix to the FC
 }
 interface rxLink connect platform.rx_pwr_dta to rx.pwr_dta {
  flow rxPower from platform.rx_pwr_dta.pwr.power to rx.pwr_dta.pwr.power;         // 5V to the RX
  flow rcToFc from rx.pwr_dta.crsf.txCrsf to platform.rx_pwr_dta.crsf.rxCrsf;     // RC control uplink RX -> FC
  flow telemToRx from platform.rx_pwr_dta.crsf.txCrsf to rx.pwr_dta.crsf.rxCrsf;  // telemetry FC -> RX
 }
 interface vtxPlug connect platform.vtx_pwr_vid_dta to vtx.pwr_vid_dta {
  flow vtxPower from platform.vtx_pwr_vid_dta.pwr.power to vtx.pwr_vid_dta.pwr.power;   // 9V to the VTX
 }
 interface fpvCamPlug connect platform.cam_pwr_vid to fpvCam.pwr_vid {
  flow fpvCamPower from platform.cam_pwr_vid.pwr.power to fpvCam.pwr_vid.pwr.power;     // 9V to the FPV cam
 }
 interface sbcMavUart connect platform.sbc_dta to sbc.uart_dta {
  flow mavToSbc from platform.sbc_dta.txMav to sbc.uart_dta.rxMav;   // FC -> SBC (params, position, RC)
  flow mavToFc  from sbc.uart_dta.txMav to platform.sbc_dta.rxMav;   // SBC -> FC (GUIDED setpoints, STATUSTEXT)
 }
 // --- Video-format compatibility across the bundled connectors (nested vid sub-ports)
 interface fpvCamToFc : Compatibility::VideoLink connect fpvCam.pwr_vid.vid to platform.cam_pwr_vid.vid {   // FPV cam -> FC OSD
  flow fpvVideo from fpvCam.pwr_vid.vid.video to platform.cam_pwr_vid.vid.video;
 }
 interface fcToVtx : Compatibility::VideoLink connect platform.vtx_pwr_vid_dta.vid to vtx.pwr_vid_dta.vid {  // FC OSD -> VTX
  flow osdVideo from platform.vtx_pwr_vid_dta.vid.video to vtx.pwr_vid_dta.vid.video;
 }
 interface camToSbc : Compatibility::VideoLink connect camera.usb_pwr_vid.vid to sbc.usba1_pwr_vid.vid {   // thermal -> SBC (UVC)
  flow thermalVideo from camera.usb_pwr_vid.vid.video to sbc.usba1_pwr_vid.vid.video;
 }
 // --- Thermal on SBC USB-A #1 (one USB: bus power out + UVC video in)
 interface thermalUsb connect sbc.usba1_pwr_vid to camera.usb_pwr_vid {
  flow thermalBusPower from sbc.usba1_pwr_vid.pwr.power to camera.usb_pwr_vid.pwr.power;   // 5V bus power to the thermal cam
 }
 // --- OpenHD air module on SBC USB-A #2 (Phase 4)
 interface ohdAirUsb connect sbc.usba2_pwr_dta to wifiTx.usb_pwr_dta {
  flow ohdBusPower from sbc.usba2_pwr_dta.pwr.power to wifiTx.usb_pwr_dta.pwr.power;     // 5V bus power to the air unit
  flow ohdVideoToAir from sbc.usba2_pwr_dta.vid.video to wifiTx.usb_pwr_dta.vid.video;  // encoded thermal video to the air unit
 }
 // --- VTX analog video antenna
 interface vtxRf connect vtx.rf_out to vtxAntenna.rf_in {
  flow vtxVideoRf from vtx.rf_out.rf to vtxAntenna.rf_in.rf;   // 5.8 GHz analog FPV downlink onto the antenna
 }
 // --- ELRS RX true-diversity antennas (2x) feed the receiver
 interface rxRfA connect rxAntennaA.rf_out to rx.rf_in_a {
  flow ctrlTelemRfA from rxAntennaA.rf_out.rf to rx.rf_in_a.rf;   // 2.4 GHz ELRS control+telem, diversity A
 }
 interface rxRfB connect rxAntennaB.rf_out to rx.rf_in_b {
  flow ctrlTelemRfB from rxAntennaB.rf_out.rf to rx.rf_in_b.rf;   // 2.4 GHz ELRS control+telem, diversity B
 }
 // --- OpenHD air antennas (2x MIMO), mounted on the drone
 interface wifiRfA connect wifiTx.rf_out_a to wifiAntennaA.rf_in {
  flow ohdVideoRfA from wifiTx.rf_out_a.rf to wifiAntennaA.rf_in.rf;   // OpenHD digital video, MIMO chain A
 }
 interface wifiRfB connect wifiTx.rf_out_b to wifiAntennaB.rf_in {
  flow ohdVideoRfB from wifiTx.rf_out_b.rf to wifiAntennaB.rf_in.rf;   // OpenHD digital video, MIMO chain B
 }

 // --- MAVLink FC<->SBC flows through the PHYSICAL UART (sbcMavUart above), not a
 //     direct SW-to-SW link: mavlinkRouter.fc delegates to the SBC uart_dta and
 //     fcSoftware.sbc_mav delegates to the FC sbc_dta (see routerToUart /
 //     fcMavToUart in each part def). The MavlinkData flows live on sbcMavUart.

 // Derived total electrical load (SBC handles onboard recording, no separate DVR)
 attribute totalPower : PowerValue =
 platform.power + camera.power + fpvCam.power + gps.power + sbc.power + rx.power + vtx.power + wifiTx.power;

 // CATIA MSOSA diagram binding (DS_Views library; does not resolve in Syside).

 }

 // The human operator — external actor interacting with the ground control station.
 part def Operator;

 part def Laptop {
 // Existing equipment — MacBook Air, not procured
 attribute usb_port_count : ScalarValues::Integer;
 attribute os : String;                              // "macOS (Sequoia / latest)"
 attribute gcsSoftware : String;                     // "QGroundControl 4.x"
 attribute videoApp : String;                        // "QuickTime Player / OBS Studio"
 attribute radioConfigSoftware : String;             // "EdgeTX Companion + ExpressLRS Configurator"
 attribute protocolsReceived : String;               // "MAVLink 2 USB COM (← TX12 EdgeTX passthrough) | USB UVC (← VRX6)"

 // One USB host port per physically-attached device (via a hub in practice)
 port usb_cap_pwr_dta {  // analog video capture card (Phase 1): USB power + UVC video
  port pwr : Flows::PowerOut;                // USB bus power to the capture dongle
  port vid : Compatibility::VideoSinkPort;
 }
 port usb_elrs_pwr_dta {  // ELRS telemetry dongle (Phase 1)
  port pwr : Flows::PowerOut;
  port mav : Flows::MavlinkSerial;
 }
 port usb_ohd_pwr_dta {  // OpenHD ground RX (Phase 4)
  port pwr : Flows::PowerOut;
  port vid : Compatibility::VideoSinkPort;
 }
 port usb_radio_dta : Flows::MavlinkSerial;     // handheld radio telemetry/joystick

 // GCS application (software_by_component.md §1) — covers route planning, mission
 // upload, telemetry/map display, FPV video, FC parameters/calibration, detection
 // alerts (STATUSTEXT), and log review. macOS constraint (MacBook Air) rules out
 // Mission Planner; QGC is THE GCS application. Zero laptop development required.
 part gcsApp : Software::SoftwareItem {
  :>> productName = "QGroundControl";
  :>> version = "4.4+";
  :>> license = "Apache-2.0 / GPLv3";
  :>> status = Software::SwStatus::EXISTS;
  port mav : Flows::MavlinkSerial;   // MAVLink to the FC (rides the ELRS telemetry link)
  satisfy R4_GCS_TELEM;
 }
 // QGC receives telemetry from the ELRS USB dongle, not a direct SW link to the FC:
 // its MAVLink port delegates to the usb_elrs_pwr_dta.mav sub-port.
 interface gcsMavFromDongle connect gcsApp.mav to usb_elrs_pwr_dta.mav;
 }

 part def AerialObservationSystem {

 part drone : Drone;
 part gcs : GCS;   // includes the operator's laptop + bench charger (wired internally)

 // Wireless links between the drone and the ground station. Over-air RF terminates at the
 // ground antennas, which feed their receivers internally in GCS.
 // Video downlink: drone analog VTX antenna → 5.8 GHz ground patch → analog VRX
 connection videoDownlinkRf connect drone.vtxAntenna.rf_out to gcs.groundAntenna.rf_in {
  flow analogFpvDownlink from drone.vtxAntenna.rf_out.rf to gcs.groundAntenna.rf_in.rf;
 }
 // ELRS control + telemetry (2.4 GHz, over air): the diversity antennas hear the dongle and the handheld
 connection elrsTelemetry connect gcs.laptopLink.rf_out to drone.rxAntennaA.rf_in {
  flow elrsUplinkPrimary from gcs.laptopLink.rf_out.rf to drone.rxAntennaA.rf_in.rf;
 }
 connection ctrlUplinkBackupRf connect gcs.rcTx.rf_out to drone.rxAntennaB.rf_in {
  flow elrsUplinkBackup from gcs.rcTx.rf_out.rf to drone.rxAntennaB.rf_in.rf;
 }
 // Phase 2+: OpenHD digital thermal downlink: drone air antennas → ground antennas → OpenHD RX
 connection ohdDownlinkRfA connect drone.wifiAntennaA.rf_out to gcs.openHDAntennaA.rf_in {
  flow ohdDownlinkA from drone.wifiAntennaA.rf_out.rf to gcs.openHDAntennaA.rf_in.rf;
 }
 connection ohdDownlinkRfB connect drone.wifiAntennaB.rf_out to gcs.openHDAntennaB.rf_in {
  flow ohdDownlinkB from drone.wifiAntennaB.rf_out.rf to gcs.openHDAntennaB.rf_in.rf;
 }
 // Ground operations only: the bench charger charges the drone battery between flights.
 connection batteryCharge connect gcs.charger.charge_pwr_out to drone.battery.charge_pwr_in {
  flow chargeCurrent from gcs.charger.charge_pwr_out.power to drone.battery.charge_pwr_in.power;
 }

 // --- MAVLink FC<->GCS flows through the PHYSICAL ELRS chain, not a direct SW-to-SW
 //     link: fcSoftware.gcs_mav tunnels MAVLink-over-CRSF to the RX (fcTelemToRx),
 //     crosses the ELRS RF link (elrsTelemetry) to the ground dongle, and reaches
 //     QGC over the dongle USB (gcsMavFromDongle). Carries drone telemetry down +
 //     the SBC's STATUSTEXT detection alerts (via the FC). MODEL_ISSUES.md §C32.

 // Derived total acquisition cost (per-drone flight system).
 // The laptop (gcs.viewingComputer) and bench charger (gcs.charger) are support/enabling
 // equipment, excluded from gcs.subTotalCost and thus from this rollup — tracked in
 // SELECTED_COMPONENTS, not the R4 per-drone cost.
 attribute totalCost : ScalarValues::Real =
 drone.platform.cost_USD
 + drone.battery.cost_USD
 + drone.camera.cost_USD
 + drone.fpvCam.cost_USD
 + drone.gps.cost_USD
 + drone.sbc.cost_USD
 + drone.rx.cost_USD
 + drone.vtx.cost_USD
 + drone.wifiTx.cost_USD
 + drone.ubec.cost_USD
 + drone.vtxAntenna.cost_USD
 + drone.rxAntennaA.cost_USD
 + drone.rxAntennaB.cost_USD
 + drone.wifiAntennaA.cost_USD
 + drone.wifiAntennaB.cost_USD
 + gcs.subTotalCost;

 // CATIA MSOSA diagram binding (DS_Views library; does not resolve in Syside).

 }
 }

 package Behavior {
  doc /* Behavioral architecture (the FUNCTION pillar). Merged from the former
       standalone DroneSystemBehavior root into DroneSystemModel on 2026-07-11 so
       the model has ONE root with the standard four pillars: Requirements /
       Architecture / Behavior / Analysis (MODEL_ISSUES.md §C30). Derived from the
       2026-07-09 use-case brainstorm (UC-0..UC-13): action defs + the FlightMode
       state machine + a thin use-case veneer (package UseCases). The missionContext
       part binds the functions to the architecture (perform/exhibit/allocate) and
       is the receiver for the UC-5 seam-closure sends (§C25). */
  private import ScalarValues::*;
  private import Architecture::*;    // AerialObservationSystem, Operator, gcs/drone parts
  private import Phasing::*;         // @PhaseTag / Phase
  private import Requirements::**;   // so `satisfy R1_BHV_ALT_HOLD;` etc. resolve unqualified

 // ════════════════════════════════════════════════════════════════════
 // State-machine trigger signals (UC-9/10 failsafes + flight-mode events)
 // ════════════════════════════════════════════════════════════════════
 attribute def LinkLossDetected {
  doc /* Control link (ELRS) lost beyond the FC failsafe timeout, per the
       FS_THR_ENABLE/FS_THR_VALUE/FS_OPTIONS parameter set (UC-9; R7_FS_LINK,
       closing the former SSS §3.7 gap). Consumed by FlightMode's
       flyingToRtlOnLinkLoss transition. */
 }
 attribute def LowBatteryReached {
  doc /* Usable energy has reached the return reserve, per the BATT_LOW_MAH /
       BATT_FS_LOW_ACT parameter set (UC-10; R6_FS_BATT, closing the former
       SSS §3.7 gap). Consumed by FlightMode's flyingToRtlOnLowBattery
       transition. */
 }
 attribute def ArmCommand {
  doc /* Operator arms via the GCS (R4_GCS_CTRL). SSS §3.1 disarmed -> armed. */
 }
 attribute def LaunchCommand {
  doc /* Operator commands takeoff via the GCS (R4_GCS_CTRL). SSS §3.1
       armed -> takeoff. */
 }
 attribute def TargetDetected {
  doc /* UC-5: onboard inference crossed the R3_1 detection threshold. Formally
       EMITTED by SweepAndDetect's terminal `send`; consumed by FlightMode's
       cruiseToLoiter transition. In the real software: the SBC app switches
       the FC from AUTO to GUIDED via MAVLink. */
 }
 attribute def InvestigationComplete {
  doc /* UC-5: classification reported and the planned route rejoined. Formally
       EMITTED by InvestigateAndClassify's terminal `send`; consumed by
       FlightMode's loiterToCruise transition. In the real software: the SBC
       app switches the FC back from GUIDED to AUTO via MAVLink. */
 }
 attribute def OperatorOverride {
  doc /* UC-11 (analysis/operator_override_UC11.md, resolved 2026-08-06): the
       operator aborts an in-progress investigation by switching the FC off
       GUIDED via a QGC mode switch — no dedicated app input. External and
       unmodeled-sender like ArmCommand/LaunchCommand (it originates with the
       operator, not an onboard action def). Consumed by FlightMode's
       loiterToCruiseOnOverride transition. RTL/LAND are NOT this trigger —
       those already route through flyingToRtlOnLinkLoss/LowBattery-style
       failsafe stand-down; this covers the remaining non-GUIDED modes
       (including a direct switch back to AUTO). In the real software: the
       SBC app detects fc_mode != GUIDED while INVESTIGATE-ing, alerts, and
       resumes SWEEP once AUTO is confirmed. */
 }

 // ════════════════════════════════════════════════════════════════════
 // Leaf inference functions (typed so decision guards can read outputs)
 // ════════════════════════════════════════════════════════════════════
 action def InferFrame {
  doc /* One onboard NPU inference pass over the live thermal frame at survey
       altitude (120 m). Output drives the detection decision (R3_1). */
  @PhaseTag { phase = Phase::Phase3; }
  out detectionConfidence : Real;
 }

 action def ClassifyTarget {
  doc /* Classification pass while loitering at 90 m — Johnson recognition
       pixel density per Analysis::ThermalRecognitionCheck.
       Output drives the classification decision (R3_2). */
  @PhaseTag { phase = Phase::Phase3; }
  out classificationConfidence : Real;
  out speciesLabel : String;   // deer | turkey | other animal | human
 }

 // ════════════════════════════════════════════════════════════════════
 // UC-5 — Detect, investigate & classify (the mission-defining loop)
 // ════════════════════════════════════════════════════════════════════
 action def SweepAndDetect {
  doc /* UC-5 cruise half (R3_1, Phase 3): the live 120 m sweep loop — one NPU
       inference per frame; on a detection at >= 90% confidence, geotag a POI,
       alert the operator over ELRS telemetry (the committed no-downlink
       CONOPS, MODEL_ISSUES.md §C20), and EMIT TargetDetected — the formal
       trigger of FlightMode's cruiseToLoiter transition. This same definition
       is both the `do` of FlightMode.flying.cruise and a step of the
       DetectInvestigateClassify umbrella: one definition, two views (the
       §C22 seam, closed per §C25). */
  @PhaseTag { phase = Phase::Phase3; }

  attribute detectThreshold : Real = 0.90;      // R3_1: >= 90% detection confidence
  attribute targetDetectedEvt : TargetDetected; // event payload emitted by the send below

  first start;
  then merge sweep;
  then action inferFrame : InferFrame;
  then decide detected;
   if inferFrame.detectionConfidence >= detectThreshold then markPoi;
   else sweep;

  action markPoi {
   doc /* Geotag the detection as a GPS point of interest. */
  }
  then action alertOperator {
   doc /* Detection alert -> GCS map marker via MAVLink over the ELRS
        telemetry downlink (R4_GCS_TELEM path; no video downlink needed). */
  }
  then send targetDetectedEvt to missionContext;   // formal emitter for FlightMode.cruiseToLoiter (missionContext exhibits FlightMode)
  then done;
 }

 action def InvestigateAndClassify {
  doc /* UC-5 loiter half (R3_2, Phase 3): guided-mode reroute + descend to
       90 m, classify at >= 80% confidence with bounded retries, report the
       result, climb back and rejoin the planned route, then EMIT
       InvestigationComplete — the formal trigger of FlightMode's
       loiterToCruise transition. This same definition is both the `do` of
       FlightMode.flying.loiter and a step of the DetectInvestigateClassify
       umbrella. The send is deliberately LAST: exiting loiter terminates this
       do-activity, so the trigger must not fire before resumeRoute is done. */
  @PhaseTag { phase = Phase::Phase3; }

  attribute classifyThreshold : Real = 0.80;                // R3_2: >= 80% classification confidence
  attribute investigationCompleteEvt : InvestigationComplete; // event payload emitted by the send below

  first start;
  then action rerouteToTarget {
   doc /* Guided-mode reroute via MAVLink (R4_SBC_DATA_AF) + descend
        120 m -> 90 m over the target. */
  }
  then merge classifyLoop;
  then action classifyTarget : ClassifyTarget;
  then decide classified;
   if classifyTarget.classificationConfidence >= classifyThreshold then reportClassification;
   else adjustOrbit;

  action adjustOrbit {
   doc /* Adjust loiter orbit/aspect and retry classification; bounded by a
        30 s loiter time budget per investigation (task 0.4 / D2.9).
        On budget exhaustion: log POI as unclassified and resume route. */
  }
  then classifyLoop;

  action reportClassification {
   doc /* Classification alert (species + location) to the operator. */
  }
  then action resumeRoute {
   doc /* Climb back to 120 m and rejoin the planned route. */
  }
  then send investigationCompleteEvt to missionContext;   // formal emitter for FlightMode.loiterToCruise (missionContext exhibits FlightMode)
  then done;
 }

 action def DetectInvestigateClassify {
  doc /* UC-5 umbrella (R3, R3_1, R3_2 — all Phase 3): the endless
       detect-investigate cycle, composed from the two state-aligned halves
       above. Loops until the enclosing surveillance action ends (route
       complete / failsafe / operator override). */
  @PhaseTag { phase = Phase::Phase3; }

  first start;
  then merge cycle;
  then action sweepAndDetect : SweepAndDetect;
  then action investigateAndClassify : InvestigateAndClassify;
  then cycle;
 }

 // ════════════════════════════════════════════════════════════════════
 // UC-4 — Execute surveillance (route + live thermal chain)
 // ════════════════════════════════════════════════════════════════════
 action def ExecuteSurveillance {
  doc /* UC-4: fly the planned route at 2.23 m/s (R2), 90–120 m AGL (R1),
       covering >= 2800 m in sustained 4.5 m/s wind (R7), while the thermal
       camera streams live over USB-UVC to the SBC (R4_SBC_VIDEO_IN). The
       three subactions are deliberately unordered (concurrent); detectLoop
       ends when flyRoute completes. */
  @PhaseTag { phase = Phase::Phase3; } // fully implemented once the Phase 3 detect loop exists

  action flyRoute {
   doc /* Waypoint route execution by the FC (ArduPilot AUTO). */
   @PhaseTag { phase = Phase::Phase1; }
   satisfy R1_BHV_ALT_HOLD;
   satisfy R2_BHV_SPEED_HOLD;
  }
  action streamThermal {
   doc /* IRCamera -> SBC live USB-UVC stream (no recording, no downlink). */
   @PhaseTag { phase = Phase::Phase2; }
  }
  action detectLoop : DetectInvestigateClassify;
 }

 // ════════════════════════════════════════════════════════════════════
 // UC-0 — Conduct thermal surveillance sortie (umbrella thread)
 // ════════════════════════════════════════════════════════════════════
 action def ConductSortie {
  doc /* UC-0: the nominal sortie thread (UC-1..UC-7 in order) with the
       operator monitor running concurrently (members without successions
       are unordered). Link-loss/low-battery failsafe handling now lives in
       the FlightMode state machine (Layer 4, below) exhibited alongside this
       action on missionContext — see that state def's doc for why the
       earlier HandleLinkLoss/HandleLowBattery action defs were retired.
       UC-11 (operator override of autonomy) is now modeled as an exceptional
       flow (see FlightMode.loiterToCruiseOnOverride and UseCases::
       OperatorOverrideUC below, MODEL_ISSUES.md §B9). UC-8 (turnaround/
       charging) and UC-12 (GNSS degradation) remain intentionally not yet
       modeled. */
  @PhaseTag { phase = Phase::Phase3; } // the full function set lands with Phase 3 autonomy

  first start;
  then action prepareSystem {
   doc /* UC-1: assemble, install charged pack, power on, link checks
        (R5, R4_BAT_*, R4_GCS_BAT). */
   @PhaseTag { phase = Phase::Phase1; }
  }
  then action planRoute {
   doc /* UC-2: waypoint route at 90–120 m / 2.23 m/s within the energy budget
        (R1, R2, R6, R7); built and uploaded in QGroundControl via MAVLink.
        Survey grids additionally set the across-track line spacing that
        realizes gap-free coverage (R4_GCS_SWEEP_SPACING, supporting R9). */
   @PhaseTag { phase = Phase::Phase1; }
   satisfy R4_GCS_SWEEP_SPACING;
  }
  then action launch {
   doc /* UC-3: arm -> takeoff -> climb to survey altitude (SSS §3.1 states). */
   @PhaseTag { phase = Phase::Phase1; }
  }
  then action surveil : ExecuteSurveillance;
  then action returnAndRecover {
   doc /* UC-7: return (auto RTL or manual), land, disarm, post-flight checks. */
   @PhaseTag { phase = Phase::Phase1; }
  }
  then done;

  // Concurrent with the flight thread:
  action monitorMission {
   doc /* UC-6: operator watches telemetry (R4_GCS_TELEM), the FPV feed,
        link margins and battery state throughout the flight. */
   @PhaseTag { phase = Phase::Phase1; }
   satisfy R4_GCS_TELEM;
  }
 }

 // ════════════════════════════════════════════════════════════════════
 // Layer 4 — Flight-mode state machine (SSS §3.1)
 // ════════════════════════════════════════════════════════════════════
 state def FlightMode {
  doc /* Formalizes the SSS §3.1 flight states (disarmed/armed/takeoff/cruise/
       loiter/RTL/land) as a proper state machine. This SUPERSEDES the earlier
       Layer-1 HandleLinkLoss/HandleLowBattery action defs (removed above):
       link-loss and low-battery are now transitions out of the `flying`
       superstate, which gives them real preemptive semantics — exiting
       `flying` terminates whichever do-activity (cruise or loiter) is
       currently running — instead of the old unordered, never-completing
       concurrent actions.
       SEAM CLOSED (2026-07-10, MODEL_ISSUES.md §C25): UC-5 was split into two
       state-aligned halves so the two behavioral views share definitions —
       cruise's do IS SweepAndDetect and loiter's do IS InvestigateAndClassify
       (the same defs the DetectInvestigateClassify umbrella cycles: one
       definition, two views), and each half formally emits its transition
       trigger (send targetDetectedEvt / investigationCompleteEvt to
       missionContext, which exhibits this state machine). The cruise<->loiter
       transitions therefore have modeled senders. Still stand-ins by intent:
       the takeoff/RTL/land do actions (that behavior lives in ArduPilot, not
       custom software) and the LinkLossDetected/LowBatteryReached triggers
       (they originate in the FC/environment, outside the modeled software).
       UC-11 OPERATOR OVERRIDE ADDED (2026-08-12, MODEL_ISSUES.md §B9):
       loiterToCruiseOnOverride lets the operator abort an investigation via
       any non-GUIDED QGC mode switch during loiter, mirroring cruise/loiter
       sharing SweepAndDetect/InvestigateAndClassify — one more state-machine
       edge realized by software, not new hardware. */

  entry; then disarmed;

  state disarmed {
   doc /* Powered, unarmed, on the ground. */
  }

  state armed {
   doc /* Armed on the ground, awaiting the launch command. */
  }

  state flying {
   doc /* Superstate for the airborne substates, so the link-loss/low-battery
        transitions need to be declared only once — they apply from any of
        takeoff/cruise/loiter, not triplicated per substate. */
   entry; then takeoff;

   state takeoff {
    do action climbToAltitude {
     doc /* Corresponds to ConductSortie.launch (above). */
    }
   }
   state cruise {
    do action sweepAndDetect : SweepAndDetect {
     doc /* Same definition composed into DetectInvestigateClassify — one
          behavior, two views. Ends by emitting TargetDetected (waypoint
          route + thermal streaming continue via ExecuteSurveillance). */
    }
   }
   state loiter {
    do action investigateAndClassify : InvestigateAndClassify {
     doc /* Same definition composed into DetectInvestigateClassify. Ends by
          emitting InvestigationComplete after the route is rejoined. */
    }
   }

   transition takeoffToCruise
    first takeoff
    then cruise;

   transition cruiseToLoiter
    first cruise
    accept detected : TargetDetected
    then loiter;

   transition loiterToCruise
    first loiter
    accept investigated : InvestigationComplete
    then cruise;

   transition loiterToCruiseOnOverride
    first loiter
    accept overrideCmd : OperatorOverride
    then cruise;
  }

  state returnToLaunch {
   do action executeRtl {
    doc /* Autonomous climb-and-return to the launch point. Corresponds to
         the former HandleLinkLoss.failsafeRtl / HandleLowBattery.
         commandReturn, now superseded by this state. */
    satisfy R6_BHV_RTL_RESERVE;
    satisfy R7_BHV_LINKLOSS_RTL;
   }
  }

  state land {
   do action touchDownAndDisarm {
    doc /* Land, disarm. Corresponds to the landing portion of
         ConductSortie.returnAndRecover (above). */
   }
  }

  transition disarmedToArmed
   first disarmed
   accept armCmd : ArmCommand
   then armed;

  transition armedToFlying
   first armed
   accept launchCmd : LaunchCommand
   then flying;

  transition flyingToRtlOnLinkLoss
   first flying
   accept linkLoss : LinkLossDetected
   then returnToLaunch;

  transition flyingToRtlOnLowBattery
   first flying
   accept lowBattery : LowBatteryReached
   then returnToLaunch;

  transition rtlToLand
   first returnToLaunch
   then land;

  transition landToDisarmed
   first land
   then disarmed;
 }

 // ════════════════════════════════════════════════════════════════════
 // Layer 3 — Use-case veneer (thin operational wrapper over the functions)
 // ════════════════════════════════════════════════════════════════════
 // Gives the 2026-07-09 brainstorm use cases a formal SysML v2 home: each
 // use case names its SUBJECT (the system), its ACTOR (the single remote
 // operator, SSS §3.13 — also the explicit operational role for part def
 // Operator), an OBJECTIVE tracing to the mission requirements, and — in doc —
 // the Layer-1/Layer-4 element that actually realizes it. The behavior lives
 // in the actions + state machine; this layer is intentionally thin.
 // Secondary actors (the observed wildlife/humans; the GNSS constellation) are
 // named in doc only — the thin veneer adds no part def for them.
 // NOT modeled (no backing behavior yet): UC-8 turnaround, UC-12 GNSS
 // degradation, UC-13 Phase-4 thermal downlink.
 // Failsafes UC-9/UC-10, and now UC-11 operator override, are EXCEPTIONAL
 // flows (UML «extend»); SysML v2 use cases offer only `include` (always-
 // performed), so they are modeled as standalone use case defs realized by
 // FlightMode transitions, and deliberately NOT `include`d by ConductSortieUC.
 // UC-11 differs from UC-9/10 in having an actor (the operator originates
 // the override, unlike the system-internal failsafes).
 package UseCases {
  private import Architecture::*;

  use case def PrepareSystemUC {   // UC-1
   subject system : AerialObservationSystem;
   actor operator : Operator;
   objective {
    doc /* Ready the system for flight: assemble, install a charged pack, power
         on, run link checks (R5, R4_BAT_*, R4_GCS_BAT). Realized by the
         ConductSortie.prepareSystem action. */
   }
  }

  use case def PlanRouteUC {   // UC-2
   subject system : AerialObservationSystem;
   actor operator : Operator;
   objective {
    doc /* Build + upload the waypoint route at 90–120 m / 2.23 m/s within the
         energy budget (R1, R2, R6, R7). Realized by ConductSortie.planRoute. */
   }
  }

  use case def LaunchUC {   // UC-3
   subject system : AerialObservationSystem;
   actor operator : Operator;
   objective {
    doc /* Arm, take off, climb to survey altitude (R1; SSS §3.1). Realized by
         ConductSortie.launch + the FlightMode armed→flying/takeoff path. */
   }
  }

  use case def DetectInvestigateClassifyUC {   // UC-5
   subject system : AerialObservationSystem;
   objective {
    doc /* Detect a heat source at 120 m (R3_1), investigate + classify it at
         90 m (R3_2), alert the operator (R3). Realized by the
         DetectInvestigateClassify action + FlightMode cruise⇄loiter. */
   }
  }

  use case def ExecuteSurveillanceUC {   // UC-4
   subject system : AerialObservationSystem;
   objective {
    doc /* Fly the route (R1, R2, R7) with the live thermal chain running,
         detecting/classifying targets en route (R3). Realized by the
         ExecuteSurveillance action + FlightMode cruise. */
   }
   include use case detectClassify : DetectInvestigateClassifyUC;
  }

  use case def MonitorMissionUC {   // UC-6
   subject system : AerialObservationSystem;
   actor operator : Operator;
   objective {
    doc /* Operator watches telemetry, FPV, link margin, and battery state
         throughout (R4_GCS_TELEM, R4_GCS_CTRL). Realized by
         ConductSortie.monitorMission. */
   }
  }

  use case def ReturnAndRecoverUC {   // UC-7
   subject system : AerialObservationSystem;
   actor operator : Operator;
   objective {
    doc /* Return, land, disarm, post-flight (R4_AF_LANDING; SSS §3.1). Realized
         by ConductSortie.returnAndRecover + FlightMode returnToLaunch/land. */
   }
  }

  use case def HandleLinkLossUC {   // UC-9 (exceptional / «extend»)
   subject system : AerialObservationSystem;
   objective {
    doc /* On control-link loss, autonomously return to launch (failsafe;
         R7_FS_LINK). Realized by the FlightMode flyingToRtlOnLinkLoss
         transition. */
   }
  }

  use case def HandleLowBatteryUC {   // UC-10 (exceptional / «extend»)
   subject system : AerialObservationSystem;
   objective {
    doc /* At the return-energy reserve, alert the operator and return
         (R4_BAT_DISCHARGE, R6_FS_BATT). Realized by the FlightMode
         flyingToRtlOnLowBattery transition. */
   }
  }

  use case def OperatorOverrideUC {   // UC-11 (exceptional / «extend»)
   subject system : AerialObservationSystem;
   actor operator : Operator;
   objective {
    doc /* Operator aborts an in-progress investigation by switching the FC
         off GUIDED mode via QGC (no dedicated app input); the mission app
         logs the override and resumes SWEEP once AUTO is confirmed
         (analysis/operator_override_UC11.md). Realized by the FlightMode
         loiterToCruiseOnOverride transition. Unlike UC-9/UC-10 this is
         operator-initiated, not a system-internal failsafe. */
   }
  }

  use case def ConductSortieUC {   // UC-0 (umbrella)
   subject system : AerialObservationSystem;
   actor operator : Operator;
   objective {
    doc /* Conduct one thermal-surveillance sortie end to end (R1, R2, R3, R6,
         R7). Realized by the ConductSortie action + the exhibited FlightMode
         state machine on missionContext (whose subject is the same
         AerialObservationSystem type). */
   }
   include use case prepare : PrepareSystemUC;
   include use case plan : PlanRouteUC;
   include use case launch : LaunchUC;
   include use case surveil : ExecuteSurveillanceUC;
   include use case monitor : MonitorMissionUC;
   include use case recover : ReturnAndRecoverUC;
  }

  // Mission-level instance of the umbrella use case.
  use case conductSortie : ConductSortieUC;
 }

 // ════════════════════════════════════════════════════════════════════
 // Layer 2 — Mission context: functions allocated to components
 // ════════════════════════════════════════════════════════════════════
 part missionContext : AerialObservationSystem {
  doc /* Binds the functional architecture to the physical architecture.
       The operator part gives the (previously unused) Operator def its
       role (this block IS the behavioral context — it performs the sortie, exhibits
       the state machine, and is the receiver for the UC-5 seam-closure sends). */
  part operator : Operator;

  perform action sortie : ConductSortie;
  exhibit state flightMode : FlightMode;

  // Operator / GCS functions
  allocate sortie.prepareSystem to operator;
  allocate sortie.planRoute to gcs.viewingComputer;    // QGroundControl on the laptop
  allocate sortie.monitorMission to operator;

  // Flight functions -> flight controller (airframe)
  allocate sortie.launch to drone.platform;
  allocate sortie.surveil.flyRoute to drone.platform;
  allocate sortie.returnAndRecover to drone.platform;

  // Thermal mission chain
  allocate sortie.surveil.streamThermal to drone.camera;
  allocate sortie.surveil.detectLoop to drone.sbc;     // onboard inference (Phase 3)
 }
 }

 package Analysis {
 // ScalarQuantityValue is the generic result type of ISQ dimensional arithmetic
 // (e.g. energy / power); ToReal extracts a numeric magnitude for scoring.
 private import Quantities::ScalarQuantityValue;
 private import QuantityCalculations::ToReal;

 // ========================================================================
 // Parametric calculations (the executable analysis "tooling")
 // ========================================================================

 // Flight time = usable battery energy / total electrical power draw.
 // Dimensionally J / W = s. The ISQ '/' operator returns the generic
 // ScalarQuantityValue (it does not narrow to DurationValue), so the result
 // is typed as ScalarQuantityValue and compared dimensionally downstream.
 // Battery energy is expressed in joules [J] (Wh x 3600); power in watts [W].
 calc def FlightTimeCalc {
 in batteryEnergy : EnergyValue;
 in totalPower : PowerValue;
 return flightTime : ScalarQuantityValue = batteryEnergy / totalPower;
 }

 // Trade score = flight-time magnitude [s] / total cost [USD]. Higher is better
 // (more endurance per dollar). ToReal yields the flight-time magnitude in its
 // reduced unit (seconds, from J/W).
 calc def ScoreCalc {
 in flightTime : ScalarQuantityValue;
 in totalCost : ScalarValues::Real;
 return score : ScalarValues::Real = ToReal(flightTime) / totalCost;
 }

 // ========================================================================
 // Predicate constraints (boolean requirement checks)
 // ========================================================================

 // R4: total system cost <= $2,500.
 constraint def BudgetLimit {
 in attribute total_cost : ScalarValues::Real;
 in attribute limit : ScalarValues::Real;
 total_cost <= limit
 }

 // R6: minimum sustained flight time >= 30 min (1800 s).
 constraint def MinFlightTimeReq {
 in flightTime : ScalarQuantityValue;
 flightTime >= 1800 [s]
 }

 // R8: stretch-goal sustained flight time >= 60 min (3600 s).
 constraint def StretchFlightTimeReq {
 in flightTime : ScalarQuantityValue;
 flightTime >= 3600 [s]
 }

 // ========================================================================
 // Verification analysis case — checks a concrete system instance
 // ========================================================================

 // Computes flight time from the system's battery energy and total power,
 // then asserts the budget (R4) and minimum-flight-time (R6) requirements.
 // The stretch goal (R8) is reported as an informational attribute, not asserted.
 analysis def MinFlightTimeCheck {
 // An analysis def is a CaseDefinition; its subject must be the first input parameter.
 subject system : Architecture::AerialObservationSystem;

 calc ftc : FlightTimeCalc {
 in batteryEnergy = system.drone.battery.energy;
 in totalPower = system.drone.totalPower;
 }
 attribute computedFlightTime : ScalarQuantityValue = ftc.flightTime;

 assert constraint budgetCheck : BudgetLimit {
 in total_cost = system.totalCost;
 in limit = 2500.0; // R4: $2,500 max
 }
 assert constraint minFlightCheck : MinFlightTimeReq {
 in flightTime = computedFlightTime;
 }

 // R8 status — informational (stretch goal, not a hard requirement).
 attribute meetsStretchGoal : ScalarValues::Boolean =
 computedFlightTime >= 3600 [s];

 // Overall pass/fail verdict against the hard requirements (R4 + R6).
 return verdict : ScalarValues::Boolean =
 (system.totalCost <= 2500.0) and (computedFlightTime >= 1800 [s]);
 }

 // ========================================================================
 // Trade-space analysis case — scores a candidate for comparison
 // ========================================================================

 // Computes flight time and an endurance-per-dollar score for a candidate
 // configuration, and verifies the budget. Used to rank alternatives.
 analysis def TradeSpaceEvaluation {
 subject candidate : Architecture::AerialObservationSystem;

 calc ftc : FlightTimeCalc {
 in batteryEnergy = candidate.drone.battery.energy;
 in totalPower = candidate.drone.totalPower;
 }
 attribute flightTime : ScalarQuantityValue = ftc.flightTime;

 calc sc : ScoreCalc {
 in flightTime = flightTime;
 in totalCost = candidate.totalCost;
 }
 attribute tradeScore : ScalarValues::Real = sc.score;

 assert constraint budgetCheck : BudgetLimit {
 in total_cost = candidate.totalCost;
 in limit = 2500.0;
 }

 return score : ScalarValues::Real = tradeScore;
 }

 // ========================================================================
 // Thermal detection analysis  (B3 — Johnson-criteria pixels-on-target)
 // ========================================================================
 // Migrates the computed detection columns from
 // analysis/thermal_camera_analysis_expanded.csv into the model layer. Uses
 // Real magnitudes (suffix _m / _deg) to sidestep the dimensional '/'-narrowing
 // issue (see C10/A10). Syside validates the structure; a SysML v2 execution
 // engine is needed for numeric verdicts — the per-camera numbers stay in the
 // analysis CSV until such a tool is available.

 // Ground sample distance [m/px] at NADIR, small-angle approximation:
 //   GSD = altitude * (HFOV in radians) / horizontal pixels
 // This is the nadir BASE only. The as-built payload is tilted (IRCamera::
 // mountTilt_deg), so the checks below degrade this via OffNadirGsd before
 // applying the Johnson criteria — see the next calc def.
 calc def GroundSampleDistance {
  in altitude_m : ScalarValues::Real;
  in hfov_deg : ScalarValues::Real;
  in resolutionH : ScalarValues::Integer;
  return gsd_m : ScalarValues::Real = altitude_m * (hfov_deg * 0.0174532925) / resolutionH;
 }

 // Off-nadir GSD degradation (analysis/thermal_detection_offnadir_analysis.md §2).
 // A camera depressed `tilt` off nadir views an on-axis ground target at slant
 // range R = altitude / cos(tilt), stretching each pixel's ground footprint:
 //   cross-range GSD = GSD_nadir / cos(tilt)      -> x1.414 at 45 deg
 //   along-range GSD = GSD_nadir / cos(tilt)^2    -> x2.000 at 45 deg  <- BINDING
 // The along-range axis binds, so that is what the checks below use.
 // Trig is not evaluated in-model (same reason the nadir calc uses the
 // small-angle form, and why numeric verdicts still need an execution engine —
 // A10/C10), so the factor is supplied as a bound constant. It MUST be kept
 // consistent with IRCamera::mountTilt_deg: recompute 1/cos(tilt)^2 if the
 // bracket angle ever changes (45 deg -> 2.0; nadir -> 1.0).
 calc def OffNadirGsd {
  in gsdNadir_m : ScalarValues::Real;
  in degradationFactor : ScalarValues::Real;
  return gsd_m : ScalarValues::Real = gsdNadir_m * degradationFactor;
 }

 // Pixels spanning the target across one dimension.
 calc def PixelsAcrossTarget {
  in targetSize_m : ScalarValues::Real;
  in gsd_m : ScalarValues::Real;
  return px : ScalarValues::Real = targetSize_m / gsd_m;
 }

 // Johnson criteria (50% probability): detection ~1.5 px; recognition/
 // classification >= 4 px across the target (R3_CAM_RES uses 4 px on a 0.5 m
 // target at 90 m AGL).
 constraint def DetectionCriterion {
  in px : ScalarValues::Real;
  px >= 1.5
 }
 constraint def RecognitionCriterion {
  in px : ScalarValues::Real;
  px >= 4.0
 }

 // Recognition/classification check: does a 0.5 m target at 90 m AGL span
 // >= 4 px ALONG-RANGE at the as-built 45 deg tilt? (R3_CAM_RES, supporting
 // R3_2.) With T13 @ 18 mm this is the tightest margin in the whole thermal
 // chain — ~4.2 px against a 4 px floor (the off-nadir analysis computes 4.17
 // exactly), versus 8.3 px if the mount were nadir.
 analysis def ThermalRecognitionCheck {
  subject cam : Architecture::IRCamera;
  attribute altitude_m : ScalarValues::Real = 90.0;
  attribute targetSize_m : ScalarValues::Real = 0.5;
  // Along-range degradation at the as-built 45 deg mount: 1 / cos(45 deg)^2 = 2.0.
  attribute alongRangeFactor : ScalarValues::Real = 2.0;

  calc gsdNadir : GroundSampleDistance {
   in altitude_m = altitude_m;
   in hfov_deg = cam.hfov;
   in resolutionH = cam.resolutionH;
  }
  calc gsd : OffNadirGsd {
   in gsdNadir_m = gsdNadir.gsd_m;
   in degradationFactor = alongRangeFactor;
  }
  calc pot : PixelsAcrossTarget {
   in targetSize_m = targetSize_m;
   in gsd_m = gsd.gsd_m;
  }
  attribute pixelsOnTarget : ScalarValues::Real = pot.px;

  assert constraint recog : RecognitionCriterion {
   in px = pixelsOnTarget;
  }

  return verdict : ScalarValues::Boolean = pixelsOnTarget >= 4.0;
 }

 // Detection check at the 120 m detection altitude (R3_1), also along-range at
 // the as-built 45 deg tilt: ~3.2 px against a 1.5 px floor (off-nadir analysis
 // computes 3.13). Comfortable — detection during the sweep is unaffected by the
 // tilt; it is only RECOGNITION (above) that the tilt squeezes.
 analysis def ThermalDetectionCheck {
  subject cam : Architecture::IRCamera;
  attribute altitude_m : ScalarValues::Real = 120.0;
  attribute targetSize_m : ScalarValues::Real = 0.5;
  // Along-range degradation at the as-built 45 deg mount: 1 / cos(45 deg)^2 = 2.0.
  attribute alongRangeFactor : ScalarValues::Real = 2.0;

  calc gsdNadir : GroundSampleDistance {
   in altitude_m = altitude_m;
   in hfov_deg = cam.hfov;
   in resolutionH = cam.resolutionH;
  }
  calc gsd : OffNadirGsd {
   in gsdNadir_m = gsdNadir.gsd_m;
   in degradationFactor = alongRangeFactor;
  }
  calc pot : PixelsAcrossTarget {
   in targetSize_m = targetSize_m;
   in gsd_m = gsd.gsd_m;
  }
  attribute pixelsOnTarget : ScalarValues::Real = pot.px;

  assert constraint detect : DetectionCriterion {
   in px = pixelsOnTarget;
  }

  return verdict : ScalarValues::Boolean = pixelsOnTarget >= 1.5;
 }
 }

 // ════════════════════════════════════════════════════════════════════
 // Views — viewpoint-organized presentations of the model (added 2026-06-27)
 // ════════════════════════════════════════════════════════════════════
 // SysML v2 views: each `view` exposes a slice of the model for a stakeholder
 // concern. Syside validates the structure; actual diagram/table rendering needs
 // a SysML v2 viewer. (Views/viewpoints were not previously used in this model.)
 package Views {

  // ── 1. Operational mission view ──
  // Mission requirements + the system-of-interest in its operating context.
  view def OperationalMissionView;
  view operationalMission : OperationalMissionView {
   expose Requirements::**;
   expose Architecture::AerialObservationSystem;
   expose Architecture::Laptop;
  }

  // ── 2. Logical architecture view ──
  // Component decomposition: the system, drone, and GCS compositions (a tree
  // rendering shows their nested parts).
  view def LogicalArchitectureView;
  view logicalArchitecture : LogicalArchitectureView {
   expose Architecture::AerialObservationSystem;
   expose Architecture::Drone;
   expose Architecture::GCS;
  }

  // ── 3. Interface & behavior view ──
  // The compatibility interface layer (typed ports, enums, interface defs,
  // constraints) plus the connections wiring the airborne system together.
  view def InterfaceBehaviorView;
  view interfaceBehavior : InterfaceBehaviorView {
   expose Architecture::Compatibility::**;
   expose Architecture::Drone;
  }

  // ── 4. Verification view ──
  // The parametric/analysis layer that verifies the requirements (flight time
  // R6/R8, budget R4, thermal detection R3).
  view def VerificationView;
  view systemVerification : VerificationView {
   expose Analysis::**;
  }

  // ── 5. Drone interconnection view ──
  // The Drone's internal structure — its nested part usages plus the
  // `interface connect` links between their ports (the CATIA interconnection
  // diagram of the Drone). Exposed recursively (`Drone::**`) so SysON's
  // synchronized view materializes each part and connection as a node/edge;
  // open it in SysON and auto-layout (Flow or Compact).
  view def DroneInterconnectionView;
  view droneInterconnection : DroneInterconnectionView {
   expose Architecture::Drone;
   expose Architecture::Drone::**;
  }
 }
}