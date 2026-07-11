package DroneSystemModel_Community {   // renamed 2026-07-11 to de-conflict the Syside fork (model.sysml is the sole DroneSystemModel); MODEL_ISSUES.md §C30
 private import ScalarValues::*;
 private import SI::*;
 private import ISQBase::*;
 private import ISQMechanics::*;
 private import ISQThermodynamics::*;
 private import ISQElectromagnetism::*;
 package Requirements {
 requirement R1 {
 }
 requirement R2 {
 }
 requirement R3 {
 }
 requirement R3_1 {
 }
 requirement R3_2 {
 }
 requirement R4 {
 }
 requirement R5 {
 }
 requirement R6 {
 }
 requirement R7 {
 }
 requirement R8 {
 }
 package CameraRequirements {
 requirement R3_CAM_WT {
 }
 requirement R3_CAM_PWR {
 }
 requirement R3_CAM_FOV {
 subsets R3;
 }
 requirement R3_CAM_NETD {
 subsets R3;
 }
 requirement R3_CAM_RES {
 subsets R3;
 }
 requirement R3_CAM_COST {
 subsets R4;
 }
 requirement R3_CAM_IF {
 }
 }
 package BatterySubsystem {
 requirement R4_BAT_VOLT {
 }
 requirement R4_BAT_ENERGY {
 subsets R6;
 }
 requirement R4_BAT_ENERGY_STRETCH {
 subsets R8;
 }
 requirement R4_BAT_WT {
 }
 requirement R4_BAT_DISCHARGE {
 }
 requirement R4_BAT_COST {
 subsets R4;
 }
 requirement R4_BAT_IF {
 }
 }
 package SBCSubsystem {
 requirement R4_SBC_PWR {
 }
 requirement R4_SBC_WT {
 }
 requirement R4_SBC_COST {
 subsets R4;
 }
 requirement R4_SBC_VIDEO_IN {
 }
 requirement R4_SBC_VIDEO_PROC {
 subsets R3;
 }
 requirement R4_SBC_DATA_AF {
 }
 requirement R4_SBC_TEMP {
 }
 }
 package GCSSubsystem {
 requirement R4_GCS_RANGE {
 subsets R7;
 }
 requirement R4_GCS_VIDEO_DISP {
 subsets R3;
 }
 requirement R4_GCS_TELEM {
 }
 requirement R4_GCS_CTRL {
 }
 requirement R4_GCS_BAT {
 }
 requirement R4_GCS_WT {
 }
 requirement R4_GCS_COST {
 subsets R4;
 }
 requirement R4_GCS_IF {
 }
 }
 package AirframeSubsystem {
 requirement R4_AF_PAYLOAD {
 }
 requirement R4_AF_WT {
 }
 requirement R4_AF_PROP_CFG {
 subsets R1;
 subsets R2;
 }
 requirement R4_AF_PWR_DIST {
 }
 requirement R4_AF_ASSY {
 subsets R5;
 }
 requirement R4_AF_STIFF {
 subsets R3;
 }
 requirement R4_AF_LANDING {
 }
 requirement R4_AF_COST {
 subsets R4;
 }
 }
 }
 package Architecture {
 private import Requirements::**;
 // Software allocation layer (2026-07-10): existing products + to-be-developed
 // items composed into the executing component (Laptop / Airframe / SBCPayload).
 // TO_DEVELOP = D-register (D-1 thermal model, D-2 mission app) per
 // analysis/software_by_component.md; MODEL_ISSUES.md §C28.
 package Software {
 enum def SwStatus { EXISTS; TO_DEVELOP; }
 part def SoftwareItem {
 attribute productName : String;
 attribute version : String;
 attribute license : String;
 attribute status : SwStatus;
 }
 }
 // Video-format compatibility layer. The combined connector ports carry a nested
 // typed video sub-port (vid); VideoLink asserts source.format == sink.format.
 package Compatibility {
 enum def VideoFormat { CVBS; USB_UVC; MIPI_CSI; HDMI; DJI_DIGITAL; HDZERO; WALKSNAIL; }
 port def VideoSourcePort { attribute format : VideoFormat; }
 port def VideoSinkPort { attribute format : VideoFormat; }
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
 }
 part def Battery {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute energy : EnergyValue;
 attribute cells_s : Integer;
 attribute capacity_mAh : Real;
 attribute nominalVoltage : ElectricPotentialDifferenceValue;
 attribute maxContinuousDischarge_A : Real;
 attribute connector : String;
 port pwr_out;       // XT60 discharge lead (power)
 port charge_pwr_in; // charge/balance lead (power)
 satisfy R4_BAT_VOLT;
 satisfy R4_BAT_ENERGY;
 satisfy R4_BAT_ENERGY_STRETCH;
 satisfy R4_BAT_WT;
 satisfy R4_BAT_DISCHARGE;
 satisfy R4_BAT_COST;
 satisfy R4_BAT_IF;
 }
 part def AntiSparkFilter {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute connector : String;
 attribute maxCells_s : Integer;
 port pwr_in;
 port pwr_out;
 satisfy R4_BAT_IF;
 }
 part def Charger {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute maxCells_s : Integer;
 attribute connector : String;
 port ac_pwr_in;
 port charge_pwr_out;
 }
 // Dedicated 2-6S->12V UBEC that powers the SBC directly off the battery
 // (the FC's 5V BEC cannot feed the ~10 W SBC, and raw 6S exceeds the M5's input window).
 part def Ubec {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute maxCurrent_A : Real;
 port pwr_in;
 port pwr_out;
 }
 part def Airframe {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute minCells_s : Integer;
 attribute maxCells_s : Integer;
 attribute batteryConnector : String;
 // Each port below = ONE physical connector/pad on the FC (BLITZ F7 + E55 ESC).
 // Combined plugs carry power + video + data on a single connector; the name lists what it carries.
 // Internal BEC rails: 5V 2.5A feeds the GPS+RX plugs; 9V 2A feeds the VTX+cam plugs.
 port battery_pwr_in;    // XT60 from the anti-spark (battery power in to the ESC)
 port vbat_pwr_out;      // raw VBAT breakout pad -> UBEC
 port gps_pwr_dta;       // 4-pin GPS plug: 5V + UART
 port rx_pwr_dta;        // 6-pin RX plug: 5V + UART (control uplink + telemetry)
 port vtx_pwr_vid_dta {  // 5-pin VTX plug: 9V + video + smartaudio UART
  port vid : Compatibility::VideoSourcePort;   // FC OSD video out to the VTX
 }
 port cam_pwr_vid {      // FPV cam pads: 9V + analog video-in
  port vid : Compatibility::VideoSinkPort;     // FPV camera video in to the FC OSD
 }
 port sbc_dta;           // spare UART pads: MAVLink to the SBC (data only)
 // FC firmware — all flight functions; FS_*/BATT_* param values realize the §3.7 failsafe reqs
 part fcSoftware : Software::SoftwareItem {
  :>> productName = "ArduPilot ArduCopter";
  :>> version = ">= 4.5";
  :>> license = "GPLv3";
  :>> status = Software::SwStatus::EXISTS;
 }
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
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute hfov : Real;
 attribute netd : TemperatureValue;
 attribute resolutionH : Integer;
 attribute resolutionV : Integer;
 attribute pixelPitch : LengthValue;
 attribute detectionRange : LengthValue;
 port usb_pwr_vid { // USB-C to the SBC: bus power in + UVC video out (one cable)
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
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 port usbc_pwr_in;    // USB-C power in (from the 12V UBEC)
 port usba1_pwr_vid {  // USB-A #1: bus power out + UVC video in (thermal camera)
  port vid : Compatibility::VideoSinkPort;
 }
 port usba2_pwr_dta;  // USB-A #2: bus power out + data (OpenHD air module, Phase 4)
 port uart_dta;       // GPIO UART: MAVLink to the FC
 // SBC software stack — the two TO_DEVELOP items are the project's entire development scope
 part rknnRuntime : Software::SoftwareItem {
  :>> productName = "RKNN-Toolkit2 runtime (librknnrt)";
  :>> version = "2.x";
  :>> license = "Rockchip (free redistribution)";
  :>> status = Software::SwStatus::EXISTS;
 }
 part mavlinkRouter : Software::SoftwareItem {
  :>> productName = "mavlink-router";
  :>> version = "current";
  :>> license = "Apache-2.0";
  :>> status = Software::SwStatus::EXISTS;
 }
 part missionApp : Software::SoftwareItem {
  // D-2: SweepAndDetect/InvestigateAndClassify realization; skeleton tested (analysis/autonomy_sim)
  :>> productName = "Onboard mission application (D-2)";
  :>> version = "0.1 skeleton (analysis/autonomy_sim)";
  :>> license = "project-developed";
  :>> status = Software::SwStatus::TO_DEVELOP;
 }
 part thermalModel : Software::SoftwareItem {
  // D-1: LWIR deer/turkey/other/human model; >=90% @120 m (R3_1), >=80% @90 m (R3_2)
  :>> productName = "LWIR wildlife detect/classify model (D-1)";
  :>> version = "none yet";
  :>> license = "project-developed (AGPL training-stack caveat)";
  :>> status = Software::SwStatus::TO_DEVELOP;
  satisfy R3_1;
  satisfy R3_2;
 }
 satisfy R4_SBC_PWR;
 satisfy R4_SBC_WT;
 satisfy R4_SBC_COST;
 satisfy R4_SBC_VIDEO_IN;
 satisfy R4_SBC_VIDEO_PROC;
 satisfy R4_SBC_DATA_AF;
 satisfy R4_SBC_TEMP;
 }
 part def FpvCamera {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute maxRange : LengthValue;
 port pwr_vid { // cam pads to FC: power in + analog video out
  port vid : Compatibility::VideoSourcePort;
 }
 }
 part def GpsModule {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute connector : String;
 port pwr_dta;     // 4-pin plug to FC: 5V power in + UART
 port gnss_rf_in;  // GNSS antenna (satellite RF in)
 }
 part def RadioReceiver {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute maxRange : LengthValue;
 port pwr_dta;   // plug to FC: 5V power in + UART (control out + telemetry in, one link)
 port rf_in_a;   // 2.4 GHz true-diversity antenna A
 port rf_in_b;   // 2.4 GHz true-diversity antenna B
 }
 part def RcTx {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute maxRange : LengthValue;
 port user_controls;   // operator sticks/switches (human input)
 port telem_dta_out;   // USB to the laptop: telemetry/joystick data
 port rf_out;          // 2.4 GHz antenna to the drone RX
 satisfy R4_GCS_CTRL;
 satisfy R4_GCS_TELEM;
 }
 part def Vtx {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 attribute maxRange : LengthValue;
 port pwr_vid_dta { // 5-pin plug to FC: 9V power in + video in + smartaudio UART
  port vid : Compatibility::VideoSinkPort;
 }
 port rf_out;      // 5.8 GHz antenna
 }
 part def Vrx {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 port rf_in;    // 5.8 GHz antenna
 port vid_out : Compatibility::VideoSourcePort;  // analog video to the capture card
 satisfy R4_GCS_VIDEO_DISP;
 }
 part def UsbCap {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 port vid_in : Compatibility::VideoSinkPort;  // analog video from the VRX (CVBS)
 port usb_pwr_dta {  // USB to the laptop: bus power in + UVC video out
  port vid : Compatibility::VideoSourcePort;
 }
 }
 part def TelemetryGroundLink {
 attribute cost_USD : Real;
 port rf_out;       // 2.4 GHz antenna to the drone RX
 port usb_pwr_dta;  // USB to the laptop (bus power + data)
 }
 part def OhdWifiTx {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 port usb_pwr_dta; // USB from SBC USB-A #2 (bus power + data)
 port rf_out_a;    // u.fl MIMO chain A -> air antenna A
 port rf_out_b;    // u.fl MIMO chain B -> air antenna B
 satisfy R4_GCS_VIDEO_DISP;
 satisfy R4_GCS_RANGE;
 }
 part def OhdGndRx {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute power : PowerValue;
 port rf_in_a;      // ground antenna A
 port rf_in_b;      // ground antenna B
 port usb_pwr_dta;  // USB to the laptop (bus power + video data)
 satisfy R4_GCS_VIDEO_DISP;
 satisfy R4_GCS_RANGE;
 }
 part def Antenna {
 attribute cost_USD : Real;
 attribute mass : MassValue;
 attribute connector : String;
 port rf_in;
 port rf_out;
 satisfy R4_GCS_RANGE;
 }
 part def GCS {
 // GCS external boundary: the human operator (display + controls). RF to the drone is via the antenna parts below.
 port operator_ui;
 part laptopLink : TelemetryGroundLink;
 part rcTx : RcTx;
 part videoRx : Vrx;
 part capture : UsbCap;
 part groundAntenna : Antenna;
 part openHDRx : OhdGndRx;
 part openHDAntennaA : Antenna;
 part openHDAntennaB : Antenna;
 part viewingComputer : Laptop;
 part charger : Charger;
 // openHDAntennaA/B here are the GROUND antennas (Foxeer Echo) feeding the ground RX
 connect groundAntenna.rf_out to videoRx.rf_in;
 connect openHDAntennaA.rf_out to openHDRx.rf_in_a;
 connect openHDAntennaB.rf_out to openHDRx.rf_in_b;
 interface vrxToCapture : Compatibility::VideoLink connect videoRx.vid_out to capture.vid_in;
 // Each laptop USB device on its own host port (the capture dongle presents UVC video to the laptop)
 connect capture.usb_pwr_dta to viewingComputer.usb_cap_pwr_dta;
 interface capToLaptop : Compatibility::VideoLink connect capture.usb_pwr_dta.vid to viewingComputer.usb_cap_pwr_dta.vid;
 connect openHDRx.usb_pwr_dta to viewingComputer.usb_ohd_pwr_dta;
 connect laptopLink.usb_pwr_dta to viewingComputer.usb_elrs_pwr_dta;
 connect rcTx.telem_dta_out to viewingComputer.usb_radio_dta;
 attribute subTotalCost : Real =
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
 view GCS : DS_Views::SymbolicViews::iv;
 }
 part def Drone {
 part platform : Airframe;
 part battery : Battery;
 part antiSpark : AntiSparkFilter;
 part ubec : Ubec;
 part camera : IRCamera;
 part fpvCam : FpvCamera;
 part gps : GpsModule;
 part sbc : SBCPayload;
 part rx : RadioReceiver;
 part vtx : Vtx;
 part wifiTx : OhdWifiTx;
 part vtxAntenna : Antenna;    // 5.8 GHz analog video dipole
 part rxAntennaA : Antenna;    // 2.4 GHz ELRS true-diversity antenna A
 part rxAntennaB : Antenna;    // 2.4 GHz ELRS true-diversity antenna B
 part wifiAntennaA : Antenna;  // OpenHD air antenna A (cloverleaf)
 part wifiAntennaB : Antenna;  // OpenHD air antenna B (cloverleaf)
 // --- Battery bus: battery -> anti-spark -> ESC/FC
 interface connect battery.pwr_out to antiSpark.pwr_in;
 interface batteryPwr connect antiSpark.pwr_out to platform.battery_pwr_in;
 // UBEC taps raw VBAT from the FC breakout pad; SBC on its own 12V supply (NOT the FC BEC)
 interface connect platform.vbat_pwr_out to ubec.pwr_in;
 interface connect ubec.pwr_out to sbc.usbc_pwr_in;
 // --- FC peripheral plugs: each connect = ONE physical connector (power+video+data as named)
 interface connect platform.gps_pwr_dta to gps.pwr_dta;
 interface connect platform.rx_pwr_dta to rx.pwr_dta;
 interface connect platform.vtx_pwr_vid_dta to vtx.pwr_vid_dta;
 interface connect platform.cam_pwr_vid to fpvCam.pwr_vid;   // FPV cam video routes cam -> FC OSD -> VTX
 interface connect platform.sbc_dta to sbc.uart_dta;
 // --- Thermal on SBC USB-A #1 (one USB: bus power out + UVC video in)
 interface connect sbc.usba1_pwr_vid to camera.usb_pwr_vid;
 // --- Video-format compatibility across the bundled connectors (nested vid sub-ports)
 interface fpvCamToFc : Compatibility::VideoLink connect fpvCam.pwr_vid.vid to platform.cam_pwr_vid.vid;
 interface fcToVtx : Compatibility::VideoLink connect platform.vtx_pwr_vid_dta.vid to vtx.pwr_vid_dta.vid;
 interface camToSbc : Compatibility::VideoLink connect camera.usb_pwr_vid.vid to sbc.usba1_pwr_vid.vid;
 // --- OpenHD air module on SBC USB-A #2 (Phase 4)
 interface connect sbc.usba2_pwr_dta to wifiTx.usb_pwr_dta;
 // --- VTX analog video antenna
 interface connect vtx.rf_out to vtxAntenna.rf_in;
 // --- ELRS RX true-diversity antennas (2x) feed the receiver
 interface connect rxAntennaA.rf_out to rx.rf_in_a;
 interface connect rxAntennaB.rf_out to rx.rf_in_b;
 // --- OpenHD air antennas (2x MIMO), mounted on the drone
 interface connect wifiTx.rf_out_a to wifiAntennaA.rf_in;
 interface connect wifiTx.rf_out_b to wifiAntennaB.rf_in;
 attribute totalPower : PowerValue =
 platform.power + camera.power + fpvCam.power + gps.power + sbc.power + rx.power + vtx.power + wifiTx.power;
 view Drone : DS_Views::SymbolicViews::iv;
 }
 part def Operator;
 part def Laptop {
 // One USB host port per physically-attached device (via a hub in practice)
 port usb_cap_pwr_dta {  // analog video capture card (Phase 1): USB power + UVC video
  port vid : Compatibility::VideoSinkPort;
 }
 port usb_elrs_pwr_dta;  // ELRS telemetry dongle (Phase 1)
 port usb_ohd_pwr_dta;   // OpenHD ground RX (Phase 4)
 port usb_radio_dta;     // handheld radio telemetry/joystick
 // GCS application — planning/upload/telemetry/video/params/alerts/logs (macOS -> QGC)
 part gcsApp : Software::SoftwareItem {
  :>> productName = "QGroundControl";
  :>> version = "4.4+";
  :>> license = "Apache-2.0 / GPLv3";
  :>> status = Software::SwStatus::EXISTS;
 }
 }
 part def AerialObservationSystem {
 part drone : Drone;
 part gcs : GCS;
 // Analog video downlink (drone VTX antenna -> ground patch, over air)
 connection connect drone.vtxAntenna.rf_out to gcs.groundAntenna.rf_in;
 // ELRS control + telemetry (2.4 GHz, over air) — the diversity antennas hear the dongle and the handheld
 connection connect gcs.laptopLink.rf_out to drone.rxAntennaA.rf_in;
 connection connect gcs.rcTx.rf_out to drone.rxAntennaB.rf_in;
 // OpenHD digital downlink: drone air antennas -> ground antennas (over air, Phase 4)
 connection connect drone.wifiAntennaA.rf_out to gcs.openHDAntennaA.rf_in;
 connection connect drone.wifiAntennaB.rf_out to gcs.openHDAntennaB.rf_in;
 // Charging (bench)
 connection connect gcs.charger.charge_pwr_out to drone.battery.charge_pwr_in;
 attribute totalCost : Real =
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
 view AerialObservationSystem : DS_Views::SymbolicViews::iv;
 }
 }
 package Behavior {
 private import ScalarValues::*;
 private import Architecture::*;
 attribute def LinkLossDetected {
 }
 attribute def LowBatteryReached {
 }
 attribute def ArmCommand {
 }
 attribute def LaunchCommand {
 }
 attribute def TargetDetected {
 }
 attribute def InvestigationComplete {
 }
 action def InferFrame {
  out detectionConfidence : Real;
 }
 action def ClassifyTarget {
  out classificationConfidence : Real;
  out speciesLabel : String;
 }
 action def SweepAndDetect {
  attribute detectThreshold : Real = 0.90;
  attribute targetDetectedEvt : TargetDetected;
  first start;
  then merge sweep;
  then action inferFrame : InferFrame;
  then decide detected;
   if inferFrame.detectionConfidence >= detectThreshold then markPoi;
   else sweep;
  action markPoi {
  }
  then action alertOperator {
  }
  then send targetDetectedEvt to missionContext;
  then done;
 }
 action def InvestigateAndClassify {
  attribute classifyThreshold : Real = 0.80;
  attribute investigationCompleteEvt : InvestigationComplete;
  first start;
  then action rerouteToTarget {
  }
  then merge classifyLoop;
  then action classifyTarget : ClassifyTarget;
  then decide classified;
   if classifyTarget.classificationConfidence >= classifyThreshold then reportClassification;
   else adjustOrbit;
  action adjustOrbit {
  }
  then classifyLoop;
  action reportClassification {
  }
  then action resumeRoute {
  }
  then send investigationCompleteEvt to missionContext;
  then done;
 }
 action def DetectInvestigateClassify {
  first start;
  then merge cycle;
  then action sweepAndDetect : SweepAndDetect;
  then action investigateAndClassify : InvestigateAndClassify;
  then cycle;
 }
 action def ExecuteSurveillance {
  action flyRoute {
  }
  action streamThermal {
  }
  action detectLoop : DetectInvestigateClassify;
 }
 action def ConductSortie {
  first start;
  then action prepareSystem {
  }
  then action planRoute {
  }
  then action launch {
  }
  then action surveil : ExecuteSurveillance;
  then action returnAndRecover {
  }
  then done;
  action monitorMission {
  }
 }
 state def FlightMode {
  entry; then disarmed;
  state disarmed {
  }
  state armed {
  }
  state flying {
   entry; then takeoff;
   state takeoff {
    do action climbToAltitude;
   }
   state cruise {
    do action sweepAndDetect : SweepAndDetect;
   }
   state loiter {
    do action investigateAndClassify : InvestigateAndClassify;
   }
   transition takeoff then cruise;
   transition first cruise accept detected : TargetDetected then loiter;
   transition first loiter accept investigated : InvestigationComplete then cruise;
  }
  state returnToLaunch {
   do action executeRtl;
  }
  state land {
   do action touchDownAndDisarm;
  }
  transition first disarmed accept armCmd : ArmCommand then armed;
  transition first armed accept launchCmd : LaunchCommand then flying;
  transition first flying accept linkLoss : LinkLossDetected then returnToLaunch;
  transition first flying accept lowBattery : LowBatteryReached then returnToLaunch;
  transition returnToLaunch then land;
  transition land then disarmed;
 }
 // (use-case veneer package UseCases kept in model.sysml only — trimmed from this lean CATIA export for the element/char cap; MODEL_ISSUES.md §C30)
 part missionContext : AerialObservationSystem {
  part operator : Operator;
  perform action sortie : ConductSortie;
  exhibit state flightMode : FlightMode;
  allocate sortie.prepareSystem to operator;
  allocate sortie.planRoute to gcs.viewingComputer;
  allocate sortie.monitorMission to operator;
  allocate sortie.launch to drone.platform;
  allocate sortie.surveil.flyRoute to drone.platform;
  allocate sortie.returnAndRecover to drone.platform;
  allocate sortie.surveil.streamThermal to drone.camera;
  allocate sortie.surveil.detectLoop to drone.sbc;
 }
 }
}
