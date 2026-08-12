// MINIFIED CATIA/MSOSA export — // comments stripped; Analysis/Views/UseCases omitted; component data attributes (cost/mass/power/specs) and cost/power rollups stripped (they carry no values here — the :>> bindings live in candidates.sysml — and are pure element cost); deferred Phase-4/OpenHD hardware omitted; software-register attributes stripped (§C32 element-budget trims). Kept: parts, ports, connects, interfaces, behavior, software register (names only) + interconnections. Requirements/satisfy omitted (not needed for the CATIA structural view; full traceability lives in model.sysml). Authoritative source is model.sysml (all pillars, full docs); regenerate from it — do not hand-edit. MODEL_ISSUES.md §C30/§C31/§C32.
package DroneSystemModel_Community {
 private import ScalarValues::*;
 private import SI::*;
 private import ISQBase::*;
 private import ISQMechanics::*;
 private import ISQThermodynamics::*;
 private import ISQElectromagnetism::*;
 package Architecture {
 package Software {
 // Attributes (productName/version/license/status) + SwStatus stripped for the
 // element budget — they live in model.sysml. Usage names carry the identity.
 part def SoftwareItem { }
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
 }
 part def AntiSparkFilter {
 port pwr_in;
 port pwr_out;
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
  port sbc_mav;
  port gcs_mav;
 }
 interface fcMavToUart connect fcSoftware.sbc_mav to sbc_dta;
 interface fcTelemToRx connect fcSoftware.gcs_mav to rx_pwr_dta;
 }
 part def IRCamera {
 port usb_pwr_vid {
  port vid : Compatibility::VideoSourcePort;
 }
 }
 part def SBCPayload {
 port usbc_pwr_in;
 port usba1_pwr_vid {
  port vid : Compatibility::VideoSinkPort;
 }
 port uart_dta;
 part rknnRuntime : Software::SoftwareItem {
  port infer;
 }
 part mavlinkRouter : Software::SoftwareItem {
  port app;
  port fc;
 }
 part missionApp : Software::SoftwareItem {
  port frameIn : Compatibility::VideoSinkPort;
  port mav;
  port infer;
 }
 part thermalModel : Software::SoftwareItem;
 connect usba1_pwr_vid.vid to missionApp.frameIn;
 interface routerToUart connect mavlinkRouter.fc to uart_dta;
 connect missionApp.mav to mavlinkRouter.app;
 connect missionApp.infer to rknnRuntime.infer;
 allocate thermalModel to rknnRuntime;
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
 // Phase-4 OpenHD hardware (OhdWifiTx / OhdGndRx) omitted from this export — a
 // deferred, non-committed capability; full defs are in model.sysml. §C32.
 part def Antenna {
 port rf_in;
 port rf_out;
 }
 part def GCS {
 port operator_ui;
 part laptopLink : TelemetryGroundLink;
 part rcTx : RcTx;
 part videoRx : Vrx;
 part capture : UsbCap;
 part groundAntenna : Antenna;
 part viewingComputer : Laptop;
 part charger : Charger;
 connect groundAntenna.rf_out to videoRx.rf_in;
 interface vrxToCapture : Compatibility::VideoLink connect videoRx.vid_out to capture.vid_in;
 connect capture.usb_pwr_dta to viewingComputer.usb_cap_pwr_dta;
 interface capToLaptop : Compatibility::VideoLink connect capture.usb_pwr_dta.vid to viewingComputer.usb_cap_pwr_dta.vid;
 connect laptopLink.usb_pwr_dta to viewingComputer.usb_elrs_pwr_dta;
 connect rcTx.telem_dta_out to viewingComputer.usb_radio_dta;
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
 part vtxAntenna : Antenna;
 part rxAntennaA : Antenna;
 part rxAntennaB : Antenna;
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
 interface connect vtx.rf_out to vtxAntenna.rf_in;
 interface connect rxAntennaA.rf_out to rx.rf_in_a;
 interface connect rxAntennaB.rf_out to rx.rf_in_b;
 view Drone : DS_Views::SymbolicViews::iv;
 }
 part def Operator;
 part def Laptop {
 port usb_cap_pwr_dta {
  port vid : Compatibility::VideoSinkPort;
 }
 port usb_elrs_pwr_dta;
 port usb_radio_dta;
 part gcsApp : Software::SoftwareItem {
  port mav;
 }
 interface gcsMavFromDongle connect gcsApp.mav to usb_elrs_pwr_dta;
 }
 part def AerialObservationSystem {
 part drone : Drone;
 part gcs : GCS;
 connection connect drone.vtxAntenna.rf_out to gcs.groundAntenna.rf_in;
 connection elrsTelemetry connect gcs.laptopLink.rf_out to drone.rxAntennaA.rf_in;
 connection connect gcs.rcTx.rf_out to drone.rxAntennaB.rf_in;
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
 attribute def OperatorOverride {
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
   transition first loiter accept overrideCmd : OperatorOverride then cruise;
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
