package DroneSystemModel {

 package Requirements {
 requirement R1 {
 doc /* The system shall operate at a nominal cruising altitude relative to ground level between 90 meters and 120 meters. */
 }

 requirement R2 {
 doc /* The drone shall maintain a steady ground speed of 2.23 meters/second. */
 }

 requirement R3 {
 doc /* At nominal cruising altitude (90m to 120m AGL), the thermal imaging system shall enable a remote operator to detect and classify heat signatures to distinguish deer, turkey, other animals, and humans under clear-night conditions with a minimum target-to-background temperature differential of 5°C. */
 }

 requirement R3.1 {
 doc /* Detection: A human operator viewing the live video feed shall be able to identify the presence of a deer-, turkey-, or human-sized heat source at 120m AGL with a confidence level of at least 90%. */
 }

 requirement R3.2 {
 doc /* Classification: A human operator viewing the live video feed shall be able to correctly classify a detected heat source as deer, turkey, other animal, or human at 90m AGL with a confidence level of at least 80%. */
 }

 requirement R4 {
 doc /* The total cost for the entire integrated system shall be under $2,500. */
 }

 requirement R5 {
 doc /* The system shall minimize DIY soldering. */
 }

 requirement R6 {
 doc /* Minimum sustained flight time: 30 minutes in non-wind (0 m/s) conditions. */
 }

 requirement R7 {
 doc /* Minimum linear distance during surveillance: 2800 meters when performing surveillance at 2.2 m/s in sustained wind conditions of 4.5 m/s. */
 }

 requirement R8 {
 doc /* Stretch Goal: sustained flight time of 60 minutes in non-wind (0 m/s) conditions. */
 }

 package CameraSubsystem {
 requirement R3_CAM_WT {
 doc /* The camera subsystem (sensor + lens + housing + cabling) shall not exceed 200g total mass. */
 }

 requirement R3_CAM_PWR {
 doc /* The camera subsystem shall consume no more than 4.5W average during continuous operation. */
 }

 requirement R3_CAM_FOV {
 doc /* The camera shall provide a horizontal field of view of at least 30 degrees. */
 refines R3;
 }

 requirement R3_CAM_NETD {
 doc /* The thermal sensor NETD (noise equivalent temperature difference) shall not exceed 50mK. */
 refines R3;
 }

 requirement R3_CAM_RES {
 doc /* The thermal sensor shall provide sufficient spatial resolution such that at 90m AGL a 0.5m x 0.5m target occupies at least 4 contiguous pixels in each dimension, enabling Johnson-criteria recognition. */
 refines R3;
 }

 requirement R3_CAM_COST {
 doc /* The camera subsystem cost shall not exceed 600 USD. */
 refines R4;
 }

 requirement R3_CAM_IF {
 doc /* The camera shall output analog CVBS or digital video (HDMI / CSI / USB) compatible with the selected SBC or VTX video input port. */
 }

 package BatterySubsystem {
 requirement R4_BAT_VOLT {
 doc /* The battery nominal voltage shall be within the operating input voltage range of the airframe's flight controller, ESC, and payload voltage regulators. */
 }

 requirement R4_BAT_ENERGY {
 doc /* The battery shall store sufficient usable energy such that, when combined with the system total power draw as computed by FlightTimeCalc, the minimum sustained flight time of 1800 seconds (R6) is achieved. */
 refines R6;
 }

 requirement R4_BAT_ENERGY_STRETCH {
 doc /* The battery shall store sufficient usable energy such that the stretch-goal sustained flight time of 3600 seconds (R8) is achievable. */
 refines R8;
 }

 requirement R4_BAT_WT {
 doc /* The battery mass shall not exceed the payload capacity of the selected airframe when combined with all other onboard subsystems. */
 }

 requirement R4_BAT_DISCHARGE {
 doc /* The battery shall sustain continuous discharge at the system maximum current draw without triggering the airframe ESC's low-voltage cutoff or causing voltage sag that degrades flight performance. */
 }

 requirement R4_BAT_COST {
 doc /* The battery cost, when summed with all other subsystem costs, shall not cause the system total cost to exceed 2500 USD (R4). */
 refines R4;
 }

 requirement R4_BAT_IF {
 doc /* The battery connector and form factor shall be physically compatible with the selected airframe's power input leads and battery mounting bay. */
 }
 }

 package SBCSubsystem {
 requirement R4_SBC_PWR {
 doc /* The SBC shall consume no more than 10W average during continuous operation at cruise. */
 }

 requirement R4_SBC_WT {
 doc /* The SBC (board + cabling + any enclosure) shall not exceed 100g total mass. */
 }

 requirement R4_SBC_COST {
 doc /* The SBC cost shall not exceed 150 USD. */
 refines R4;
 }

 requirement R4_SBC_VIDEO_IN {
 doc /* The SBC shall accept a video input from the thermal camera that matches the camera's video output format. */
 }

 requirement R4_SBC_VIDEO_PROC {
 doc /* The SBC shall process the incoming video stream for live transmission to the ground control station without introducing a processing delay that degrades the operator's ability to detect and classify targets per R3.1 and R3.2. */
 refines R3;
 }

 requirement R4_SBC_DATA_AF {
 doc /* The SBC shall exchange telemetry and status data with the flight controller (airframe) through the data_af interface. */
 }

 requirement R4_SBC_TEMP {
 doc /* The SBC shall operate within the full environmental temperature range of the drone system without active cooling. */
 }
 }

 package GCSSubsystem {
 requirement R4_GCS_RANGE {
 doc /* The GCS control link and video receiver shall maintain a reliable connection with the drone at a slant range of at least 2800 meters under clear line-of-sight conditions. */
 refines R7;
 }

 requirement R4_GCS_VIDEO_DISP {
 doc /* The GCS display shall render the thermal video feed at sufficient resolution, brightness, and size such that the operator can perform detection (R3.1) and classification (R3.2) tasks. */
 refines R3;
 }

 requirement R4_GCS_TELEM {
 doc /* The GCS display shall present real-time drone telemetry data (altitude, position, battery voltage, heading, speed) to the operator. */
 }

 requirement R4_GCS_CTRL {
 doc /* The GCS shall provide flight control inputs (throttle, roll, pitch, yaw, arming, flight mode selection) with sufficient latency and resolution for safe manual operation at 2800m range. */
 }

 requirement R4_GCS_BAT {
 doc /* The GCS shall operate on internal battery power for a duration matching or exceeding the drone's maximum planned flight time, without requiring external AC power during field operation. */
 }

 requirement R4_GCS_WT {
 doc /* The GCS system (transmitter, display, antennas, battery) shall be portable and hand-held for field operation. */
 }

 requirement R4_GCS_COST {
 doc /* The GCS cost, when summed with all other subsystem costs, shall not cause the system total cost to exceed 2500 USD (R4). */
 refines R4;
 }

 requirement R4_GCS_IF {
 doc /* The GCS receiver and transmitter shall be compatible with the drone's video transmitter and telemetry radio operating frequencies and protocols. */
 }
 }

 package AirframeSubsystem {
 requirement R4_AF_PAYLOAD {
 doc /* The airframe (frame + motors + ESCs + propellers + power distribution) shall have sufficient payload capacity to carry the combined mass of all onboard subsystems (battery, camera, SBC, cabling) while maintaining stable flight. */
 }

 requirement R4_AF_WT {
 doc /* The bare airframe mass (frame only, excluding motors, ESCs, and propellers) shall leave adequate margin such that the total takeoff mass does not exceed 80% of the airframe's rated maximum takeoff mass. */
 }

 requirement R4_AF_PROP_CFG {
 doc /* The airframe shall accommodate propeller diameters and motor mounting patterns suitable for efficient cruise at 2.23 m/s and 90-120m AGL. */
 refines R1;
 refines R2;
 }

 requirement R4_AF_PWR_DIST {
 doc /* The airframe's power distribution wiring and connectors shall supply regulated voltage to the payload subsystems (camera, SBC) and unfiltered battery voltage to the ESCs. */
 }

 requirement R4_AF_ASSY {
 doc /* The airframe assembly shall minimize DIY soldering, preferring pre-soldered power distribution boards, plug-in connectors, and screw-terminal motor connections. */
 refines R5;
 }

 requirement R4_AF_STIFF {
 doc /* The airframe structure shall be sufficiently rigid to prevent vibration-induced degradation of thermal image quality during cruise. */
 refines R3;
 }

 requirement R4_AF_LANDING {
 doc /* The airframe shall provide landing gear or structural clearance of at least 30mm below the lowest payload component to prevent ground contact during landing and takeoff. */
 }

 requirement R4_AF_COST {
 doc /* The complete airframe subsystem cost (frame + motors + ESCs + propellers + power distribution) shall not cause the system total cost to exceed 2500 USD (R4). */
 refines R4;
 }
 }

 package Architecture {

 part def Battery {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute energy : ISQThermodynamics::EnergyValue;

 // Derived specific energy
 attribute specificEnergy : ISQMechanics::SpecificEnergyValue =
 energy / mass;

 port power_out;

 satisfy R4_BAT_VOLT;
 satisfy R4_BAT_ENERGY;
 satisfy R4_BAT_ENERGY_STRETCH;
 satisfy R4_BAT_WT;
 satisfy R4_BAT_DISCHARGE;
 satisfy R4_BAT_COST;
 satisfy R4_BAT_IF;
 }

 part def Airframe {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;
 attribute maxTakeoffMass : ISQBase::MassValue;
 attribute propDiameter : ISQBase::LengthValue;

 port power_battery;
 port power_sbc;
 port power_tp;
 port data_sbc;
 port control_input;
 port telemetry_data_out;

 satisfy R4_AF_PAYLOAD;
 satisfy R4_AF_WT;
 satisfy R4_AF_PROP_CFG;
 satisfy R4_AF_PWR_DIST;
 satisfy R4_AF_ASSY;
 satisfy R4_AF_STIFF;
 satisfy R4_AF_LANDING;
 satisfy R4_AF_COST;
 }

 part def CameraSubsystem {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;
 attribute hfov : ScalarValues::Real;
 attribute netd : ISQThermodynamics::TemperatureValue;

 port video_out;
 port power;

 satisfy R3_CAM_WT;
 satisfy R3_CAM_PWR;
 satisfy R3_CAM_FOV;
 satisfy R3_CAM_NETD;
 satisfy R3_CAM_RES;
 satisfy R3_CAM_COST;
 satisfy R3_CAM_IF;
 }

 part def SingleBoardComputerPayload {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;

 port video_in;
 port data_af;
 port power;

 satisfy R4_SBC_PWR;
 satisfy R4_SBC_WT;
 satisfy R4_SBC_COST;
 satisfy R4_SBC_VIDEO_IN;
 satisfy R4_SBC_VIDEO_PROC;
 satisfy R4_SBC_DATA_AF;
 satisfy R4_SBC_TEMP;
 }

 part def FpvCamera {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;
 attribute includedWithAirframe : Boolean;
 attribute cameraType : string;
 attribute cameraModel : string;

 port video_out;
 port power;

 doc /* Non-IR FPV camera used for piloting. May be included with the airframe purchase (BNF/PNP bundles) or purchased separately. Distinct from the thermal CameraSubsystem which is the mission payload. */
 }

 part def GpsModule {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;
 attribute includedWithAirframe : Boolean;

 port data_out;  // to flight controller (UART)
 port power;
 port rf_in;     // GPS antenna

 doc /* GPS module providing position, velocity, and time data to the flight controller. Critical for return-to-home and autonomous waypoint navigation (Phase 2+). May be pre-installed with some airframe packages. */
 }

 part def RadioReceiver {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;
 attribute maxRange : ISQBase::LengthValue;
 attribute protocol : string;
 attribute includedWithAirframe : Boolean;
 attribute telemetryCapable : Boolean = true; // ELRS handles bidirectional RC + telemetry over one RF link

 port control_signal_out; // RC control to flight controller
 port telemetry_data_in;   // telemetry data from flight controller (CRSF)
 port power;
 port rf_in;               // combined RF: RC control in + telemetry out

 doc /* Bidirectional RF link using ELRS (ExpressLRS) protocol. Handles both RC control input (uplink) and telemetry return (downlink) over a single RF link, eliminating the need for a separate telemetry radio. Telemetry capability based on ELRS range analysis — see analysis/ELRS_telemetry_range_analysis.md. */
 }

 part def RadioControlTransmitter {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;
 attribute maxRange : ISQBase::LengthValue;
 attribute telemetryCapable : Boolean = true; // ELRS TX module receives telemetry and pipes to GCS via USB

 port user_controls;
 port telemetry_data_out;
 port rf_out;               // combined RF: RC control out + telemetry in

 satisfy R4_GCS_CTRL;
 satisfy R4_GCS_TELEM;

 doc /* Ground-side RC transmitter with ELRS module. Transmits RC control uplink and receives telemetry downlink on the same RF link. Telemetry data is forwarded to the GCS laptop via USB/Bluetooth. */
 }

 part def VideoTransmitter {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;
 attribute maxRange : ISQBase::LengthValue;
 attribute includedWithAirframe : Boolean;

 port video_in;
 port power;
 port rf_out;

 doc /* 5.8 GHz video transmitter for FPV piloting downlink. May be included with the airframe purchase (BNF/PNP) or purchased separately. */
 }

 part def ThermalVideoRecorder {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;
 attribute storageCapacity : ScalarValues::Real; // GB
 attribute recordingFormat : string; // e.g., "AVI", "MOV"

 port video_in;   // from CameraSubsystem
 port video_out;  // pass-through to VideoTransmitter
 port power;

 doc /* Inline DVR that records analog CVBS video to microSD card while passing video through to the VTX. Enables onboard storage of thermal footage without requiring the SBC (Phase 4). Survives RF signal loss — footage is on the card regardless of downlink quality. */
 }

 part def VideoReceiver {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;
 attribute includedWithAirframe : Boolean;

 port rf_in;
 port video_out;  // Analog CVBS/composite (RCA)

 satisfy R4_GCS_VIDEO_DISP;

 doc /* Ground-side video receiver for live FPV downlink. Not typically bundled with airframe (sold separately or as part of GCS/goggles kit). Outputs analog composite video. */
 }

 part def UsbVideoCapture {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;

 port video_in;   // from VideoReceiver (RCA/AV composite)
 port usb_out;    // to ViewingComputer (USB-C / UVC)

 doc /* Analog-to-USB video capture dongle. Converts analog CVBS/composite video from the VRX to USB Video Class (UVC) format readable by the laptop's OS. Used to pipe live FPV video into QGC / Mission Planner. Typical cost $10-25. */
 }

 part def GroundControlStation {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;
 attribute batteryEnergy : ISQThermodynamics::EnergyValue;
 attribute maxRange : ISQBase::LengthValue;

 port video_in;
 port user_interface;
 port status_and_control;

 part rcTx : RadioControlTransmitter;  // ELRS — handles both RC control and telemetry
 part videoRx : VideoReceiver;          // Analog 5.8 GHz VRX
 part capture : UsbVideoCapture;        // Bridges analog VRX to laptop USB

 // Internal GCS wiring: VRX analog output → USB capture dongle
 connect videoRx.video_out to capture.video_in;

 // Derived total GCS component cost
 attribute subTotalCost : ScalarValues::Real =
 rcTx.cost_USD + videoRx.cost_USD + capture.cost_USD;

 satisfy R4_GCS_RANGE;
 satisfy R4_GCS_VIDEO_DISP;
 satisfy R4_GCS_TELEM;
 satisfy R4_GCS_CTRL;
 satisfy R4_GCS_BAT;
 satisfy R4_GCS_WT;
 satisfy R4_GCS_COST;
 satisfy R4_GCS_IF;
 }

 part def SurveillanceDrone {

 part platform : Airframe;
 part battery : Battery;
 part camera : CameraSubsystem;
 part fpvCam : FpvCamera;
 part gps : GpsModule;
 part recorder : ThermalVideoRecorder;
 part sbc : SingleBoardComputerPayload;
 part rx : RadioReceiver;  // ELRS — handles both RC control and telemetry
 part vtx : VideoTransmitter;

 interface connect battery.power_out to platform.power_battery;
 interface connect platform.power_tp to camera.power;
 interface connect platform.power_sbc to fpvCam.power;
 interface connect platform.power_sbc to gps.power;
 interface connect platform.power_sbc to recorder.power;
 interface connect platform.power_sbc to sbc.power;
 interface connect platform.power_sbc to rx.power;
 interface connect platform.power_sbc to vtx.power;
 interface connect fpvCam.video_out to vtx.video_in;  // FPV camera feeds pilot VTX
 interface connect camera.video_out to recorder.video_in; // thermal camera feeds recorder
 interface connect recorder.video_out to vtx.video_in; // recorder also passes through to VTX (optional)
 interface connect camera.video_out to sbc.video_in;   // thermal camera also feeds SBC for inference (Phase 4)
 interface connect gps.data_out to platform.data_sbc;   // GPS data to flight controller
 interface connect sbc.data_af to platform.data_sbc;
 interface connect rx.control_signal_out to platform.control_input;
 interface connect rx.telemetry_data_in to platform.telemetry_data_out; // telemetry via same ELRS RX

 // Derived total electrical load
 attribute totalPower : ISQMechanics::PowerValue =
 platform.power + camera.power + fpvCam.power + gps.power + recorder.power + sbc.power + rx.power + vtx.power;
 }

 part def ViewingComputer {
 // Existing equipment — MacBook Air, not procured
 attribute usb_port_count : ScalarValues::Integer;

 port video_in;
 port user_interface;
 }

 part def AerialThermalObservationSystem {

 part drone : SurveillanceDrone;
 part gcs : GroundControlStation;
 part displayComputer : ViewingComputer;

 // Wireless RF links — ELRS handles RC control + telemetry on one link
 connection connect drone.vtx.rf_out to gcs.videoRx.rf_in;
 connection connect drone.rx.rf_in to gcs.rcTx.rf_out;

 // Video receiver path: VRX → USB capture dongle → laptop (USB-C)
 connection connect gcs.capture.usb_out to displayComputer.video_in;

 // Telemetry from ELRS TX module to GCS laptop (USB)
 // The radio controller forwards ELRS telemetry over USB as a virtual serial port
 connection connect gcs.rcTx.telemetry_data_out to displayComputer.user_interface;

 // Derived total acquisition cost
 // Note: displayComputer excluded — existing equipment, not procured
 attribute totalCost : ScalarValues::Real =
 drone.platform.cost_USD
 + drone.battery.cost_USD
 + drone.camera.cost_USD
 + drone.fpvCam.cost_USD
 + drone.gps.cost_USD
 + drone.recorder.cost_USD
 + drone.sbc.cost_USD
 + drone.rx.cost_USD
 + drone.vtx.cost_USD
 + gcs.subTotalCost;
 }
 }

 package Analysis {

 constraint def BudgetLimit {

 in attribute total_cost : ScalarValues::Real;
 in attribute limit : ScalarValues::Real;

 total_cost <= limit
 }

 constraint def FlightTimeCalc {

 in attribute batteryEnergy : ISQThermodynamics::EnergyValue;
 in attribute totalPower : ISQMechanics::PowerValue;

 out attribute flightTime : ISQBase::DurationValue =
 batteryEnergy / totalPower;
 }

 constraint def ScoreCalc {

 in attribute flightTime : ISQBase::DurationValue;
 in attribute totalCost : ScalarValues::Real;

 out attribute score : ScalarValues::Real =
 flightTime.num / totalCost;
 }

 part MinFlightTimeCheck {

 part system : Architecture::AerialThermalObservationSystem;

 attribute computed_flight_time : ISQBase::DurationValue;

 constraint budget_check : BudgetLimit {
 in total_cost = system.totalCost;
 in limit = 2500.0; // R4: $2,500 max
 }

 constraint ft_calc : FlightTimeCalc {
 in batteryEnergy = system.drone.battery.energy;
 in totalPower = system.drone.totalPower;
 out flightTime = computed_flight_time;
 }

 constraint flight_time_meets_req {
 computed_flight_time >= 1800.0; // R6: 30 min minimum
 }
 }

 analysis def TradeSpaceEvaluation {

 in part candidate : Architecture::AerialThermalObservationSystem;

 attribute flight_time : ISQBase::DurationValue;
 attribute score : ScalarValues::Real;

 constraint ft_calc : FlightTimeCalc {
 in batteryEnergy = candidate.drone.battery.energy;
 in totalPower = candidate.drone.totalPower;
 out flightTime = flight_time;
 }

 constraint score_calc : ScoreCalc {
 in flightTime = flight_time;
 in totalCost = candidate.totalCost;
 out score = score;
 }
 }
 }
}