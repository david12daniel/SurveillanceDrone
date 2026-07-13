// MINIFIED CATIA/MSOSA export — // comments stripped; Analysis/Views/UseCases omitted; component data attributes (cost/mass/power/specs) and cost/power rollups stripped (they carry no values here — the :>> bindings live in candidates.sysml — and are pure element cost). Kept: parts, ports, connects, interfaces, satisfy, requirements (system-level R1–R8/R3_1/R3_2 carry their doc text; subsystem-requirement docs stripped for budget), behavior, software register + interconnections. Authoritative source is model.sysml (all pillars, full docs); regenerate from it — do not hand-edit. MODEL_ISSUES.md §C30/§C31.
package DroneSystemModel_Community {
 private import ScalarValues::*;
 private import SI::*;
 private import ISQBase::*;
 private import ISQMechanics::*;
 private import ISQThermodynamics::*;
 private import ISQElectromagnetism::*;
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
 requirement R3_1 {
 doc /* Detection: A human operator viewing the live video feed shall be able to identify the presence of a deer-, turkey-, or human-sized heat source at 120m AGL with a confidence level of at least 90%. */
 }
 requirement R3_2 {
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
 package Software {
 enum def SwStatus { EXISTS; TO_DEVELOP; }
 part def SoftwareItem {
 attribute productName : String;
 attribute version : String;
 attribute license : String;
 attribute status : SwStatus;
 }
 }
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
 port pwr_out;
 port charge_pwr_in;
 satisfy R4_BAT_VOLT;
 satisfy R4_BAT_ENERGY;
 satisfy R4_BAT_ENERGY_STRETCH;
 satisfy R4_BAT_WT;
 satisfy R4_BAT_DISCHARGE;
 satisfy R4_BAT_COST;
 satisfy R4_BAT_IF;
 }
 part def AntiSparkFilter {
 port pwr_in;
 port pwr_out;
 satisfy R4_BAT_IF;
 }
 part def Charger {
 port ac_pwr_in;
 port charge_pwr_out;
 }
 part def Ubec {
 port pwr_in;
 port pwr_out;
 }
 part def Airframe {
 port battery_pwr_in;
 port vbat_pwr_out;
 port gps_pwr_dta;
 port rx_pwr_dta;
 port vtx_pwr_vid_dta {
  port vid : Compatibility::VideoSourcePort;
 }
 port cam_pwr_vid {
  port vid : Compatibility::VideoSinkPort;
 }
 port sbc_dta;
 part fcSoftware : Software::SoftwareItem {
  :>> productName = "ArduPilot ArduCopter";
  :>> version = ">= 4.5";
  :>> license = "GPLv3";
  :>> status = Software::SwStatus::EXISTS;
  port sbc_mav;
  port gcs_mav;
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
 port usb_pwr_vid {
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
 port usbc_pwr_in;
 port usba1_pwr_vid {
  port vid : Compatibility::VideoSinkPort;
 }
 port usba2_pwr_dta;
 port uart_dta;
 part rknnRuntime : Software::SoftwareItem {
  :>> productName = "RKNN-Toolkit2 runtime (librknnrt)";
  :>> version = "2.x";
  :>> license = "Rockchip (free redistribution)";
  :>> status = Software::SwStatus::EXISTS;
  port infer;
 }
 part mavlinkRouter : Software::SoftwareItem {
  :>> productName = "mavlink-router";
  :>> version = "current";
  :>> license = "Apache-2.0";
  :>> status = Software::SwStatus::EXISTS;
  port app;
  port fc;
 }
 part missionApp : Software::SoftwareItem {
  :>> productName = "Onboard mission application (D-2)";
  :>> version = "0.1 skeleton (analysis/autonomy_sim)";
  :>> license = "project-developed";
  :>> status = Software::SwStatus::TO_DEVELOP;
  port mav;
  port infer;
 }
 part thermalModel : Software::SoftwareItem {
  :>> productName = "LWIR wildlife detect/classify model (D-1)";
  :>> version = "none yet";
  :>> license = "project-developed (AGPL training-stack caveat)";
  :>> status = Software::SwStatus::TO_DEVELOP;
  satisfy R3_1;
  satisfy R3_2;
 }
 connect missionApp.mav to mavlinkRouter.app;
 connect missionApp.infer to rknnRuntime.infer;
 allocate thermalModel to rknnRuntime;
 satisfy R4_SBC_PWR;
 satisfy R4_SBC_WT;
 satisfy R4_SBC_COST;
 satisfy R4_SBC_VIDEO_IN;
 satisfy R4_SBC_VIDEO_PROC;
 satisfy R4_SBC_DATA_AF;
 satisfy R4_SBC_TEMP;
 }
 part def FpvCamera {
 port pwr_vid {
  port vid : Compatibility::VideoSourcePort;
 }
 }
 part def GpsModule {
 port pwr_dta;
 port gnss_rf_in;
 }
 part def RadioReceiver {
 port pwr_dta;
 port rf_in_a;
 port rf_in_b;
 }
 part def RcTx {
 port user_controls;
 port telem_dta_out;
 port rf_out;
 satisfy R4_GCS_CTRL;
 satisfy R4_GCS_TELEM;
 }
 part def Vtx {
 port pwr_vid_dta {
  port vid : Compatibility::VideoSinkPort;
 }
 port rf_out;
 }
 part def Vrx {
 port rf_in;
 port vid_out : Compatibility::VideoSourcePort;
 satisfy R4_GCS_VIDEO_DISP;
 }
 part def UsbCap {
 port vid_in : Compatibility::VideoSinkPort;
 port usb_pwr_dta {
  port vid : Compatibility::VideoSourcePort;
 }
 }
 part def TelemetryGroundLink {
 port rf_out;
 port usb_pwr_dta;
 }
 part def OhdWifiTx {
 port usb_pwr_dta;
 port rf_out_a;
 port rf_out_b;
 satisfy R4_GCS_VIDEO_DISP;
 satisfy R4_GCS_RANGE;
 }
 part def OhdGndRx {
 port rf_in_a;
 port rf_in_b;
 port usb_pwr_dta;
 satisfy R4_GCS_VIDEO_DISP;
 satisfy R4_GCS_RANGE;
 }
 part def Antenna {
 port rf_in;
 port rf_out;
 satisfy R4_GCS_RANGE;
 }
 part def GCS {
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
 connect groundAntenna.rf_out to videoRx.rf_in;
 connect openHDAntennaA.rf_out to openHDRx.rf_in_a;
 connect openHDAntennaB.rf_out to openHDRx.rf_in_b;
 interface vrxToCapture : Compatibility::VideoLink connect videoRx.vid_out to capture.vid_in;
 connect capture.usb_pwr_dta to viewingComputer.usb_cap_pwr_dta;
 interface capToLaptop : Compatibility::VideoLink connect capture.usb_pwr_dta.vid to viewingComputer.usb_cap_pwr_dta.vid;
 connect openHDRx.usb_pwr_dta to viewingComputer.usb_ohd_pwr_dta;
 connect laptopLink.usb_pwr_dta to viewingComputer.usb_elrs_pwr_dta;
 connect rcTx.telem_dta_out to viewingComputer.usb_radio_dta;
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
 part vtxAntenna : Antenna;
 part rxAntennaA : Antenna;
 part rxAntennaB : Antenna;
 part wifiAntennaA : Antenna;
 part wifiAntennaB : Antenna;
 interface connect battery.pwr_out to antiSpark.pwr_in;
 interface batteryPwr connect antiSpark.pwr_out to platform.battery_pwr_in;
 interface connect platform.vbat_pwr_out to ubec.pwr_in;
 interface connect ubec.pwr_out to sbc.usbc_pwr_in;
 interface connect platform.gps_pwr_dta to gps.pwr_dta;
 interface connect platform.rx_pwr_dta to rx.pwr_dta;
 interface connect platform.vtx_pwr_vid_dta to vtx.pwr_vid_dta;
 interface connect platform.cam_pwr_vid to fpvCam.pwr_vid;
 interface sbcMavUart connect platform.sbc_dta to sbc.uart_dta;
 interface connect sbc.usba1_pwr_vid to camera.usb_pwr_vid;
 interface fpvCamToFc : Compatibility::VideoLink connect fpvCam.pwr_vid.vid to platform.cam_pwr_vid.vid;
 interface fcToVtx : Compatibility::VideoLink connect platform.vtx_pwr_vid_dta.vid to vtx.pwr_vid_dta.vid;
 interface camToSbc : Compatibility::VideoLink connect camera.usb_pwr_vid.vid to sbc.usba1_pwr_vid.vid;
 interface connect sbc.usba2_pwr_dta to wifiTx.usb_pwr_dta;
 interface connect vtx.rf_out to vtxAntenna.rf_in;
 interface connect rxAntennaA.rf_out to rx.rf_in_a;
 interface connect rxAntennaB.rf_out to rx.rf_in_b;
 interface connect wifiTx.rf_out_a to wifiAntennaA.rf_in;
 interface connect wifiTx.rf_out_b to wifiAntennaB.rf_in;
 view Drone : DS_Views::SymbolicViews::iv;
 }
 part def Operator;
 part def Laptop {
 port usb_cap_pwr_dta {
  port vid : Compatibility::VideoSinkPort;
 }
 port usb_elrs_pwr_dta;
 port usb_ohd_pwr_dta;
 port usb_radio_dta;
 part gcsApp : Software::SoftwareItem {
  :>> productName = "QGroundControl";
  :>> version = "4.4+";
  :>> license = "Apache-2.0 / GPLv3";
  :>> status = Software::SwStatus::EXISTS;
  port mav;
 }
 }
 part def AerialObservationSystem {
 part drone : Drone;
 part gcs : GCS;
 connection connect drone.vtxAntenna.rf_out to gcs.groundAntenna.rf_in;
 connection elrsTelemetry connect gcs.laptopLink.rf_out to drone.rxAntennaA.rf_in;
 connection connect gcs.rcTx.rf_out to drone.rxAntennaB.rf_in;
 connection connect drone.wifiAntennaA.rf_out to gcs.openHDAntennaA.rf_in;
 connection connect drone.wifiAntennaB.rf_out to gcs.openHDAntennaB.rf_in;
 connection connect gcs.charger.charge_pwr_out to drone.battery.charge_pwr_in;
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
