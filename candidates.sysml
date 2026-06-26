package DroneCandidates {
 doc /*
  * Candidate option library for the Surveillance Drone.
  *
  * Single source of truth for the component market/trade-study data that used to
  * live in analysis/*.csv. Each candidate is a SysML v2 part usage typed by the
  * matching definition in DroneSystemModel::Architecture, with attribute values
  * bound via redefinition (:>>). This keeps the option data co-located with the
  * model schema it conforms to.
  *
  * Conventions:
  *  - Usage name carries the CSV row ID (airframes prefixed "AF" since SysML
  *    names cannot start with a digit). Original model name is in `name`.
  *  - Cost ranges are bound to a single representative value; the range is noted
  *    in a trailing comment.
  *  - Sub-units absent from the SI library (mW, mA, mK, um) are bound in base SI
  *    units with the original value in a comment: 100 mW -> 0.1 [W],
  *    120 mA -> 0.12 [A], 50 mK -> 0.05 [K], 12 um -> 0.012 [mm].
  *  - Attributes with only "Unknown"/"N/A"/estimate-only CSV data are omitted and
  *    recorded in MODEL_ISSUES.md.
  *  - Derived analysis columns (Johnson criteria, GSD, NPU load margin, pass/fail)
  *    are NOT component attributes and are intentionally excluded — they belong to
  *    the Analysis layer.
  */

 private import ScalarValues::*;
 private import SI::*;
 private import DroneSystemModel::Architecture::*;  // the component part definitions

 // =========================================================================
 // AIRFRAME CANDIDATES  (source: analysis/airframe-candidates.csv)
 // =========================================================================
 package AirframeCandidates {

  part AF1 : Airframe {
   :>> name = "GEPRC MARK4 LR7";
   :>> purchaseType = "PNP";
   :>> cost_USD = 285.0;            // range 240-330
   :>> mass = 455.0 [g];
   :>> propSize_in = 7.0;
   :>> wheelbase = 295.0 [mm];
   :>> flightController = "GEPRC TAKER F405 V2";
   :>> esc = "SPAN 50A BLHeli_S 4-in-1";
   :>> motors = "GEPRC E2806.5 1350KV";
   :>> propModel = "Gemfan 7037-3";
   :>> uartCount = 6;
   :>> receiverProtocols = "SBUS, PPM, CRSF, DSMX, iBus";
   :>> receiverIncluded = false;
   :>> vtxIncluded = true;
   :>> vtxModel = "GEPRC RAD 5.8G 1.6W";
   :>> fpvCameraIncluded = true;
   :>> fpvCameraType = "Analog CMOS 1/3in 1200TVL";
   :>> fpvCameraModel = "Caddx H1";
   :>> gpsIncluded = false;
   :>> gpsModel = "aftermarket (G3 Matek M10Q-5883 recommended)";
   :>> sourceConfidence = "High";
  }

  part AF2a : Airframe {
   :>> name = "Axisflying KOLAS7";
   :>> purchaseType = "PNP";
   :>> cost_USD = 175.0;            // est. range 150-200
   :>> mass = 257.0 [g];
   :>> propSize_in = 7.0;
   :>> wheelbase = 298.0 [mm];
   :>> flightController = "iStack F722 / Argus F722";
   :>> esc = "iStack 50A / Argus 65A";
   :>> motors = "Axisflying C287 1350KV";
   :>> propModel = "HQ 7035 / GF 7042";
   :>> uartCount = 6;
   :>> receiverProtocols = "SBUS, PPM, CRSF, DSMX, iBus (F7)";
   :>> receiverIncluded = false;
   :>> vtxIncluded = false;
   :>> fpvCameraIncluded = false;
   :>> gpsIncluded = false;
   :>> gpsModel = "aftermarket (G3 Matek M10Q-5883 recommended)";
   :>> sourceConfidence = "Moderate";
  }

  part AF2b : Airframe {
   :>> name = "Axisflying KOLAS7";
   :>> purchaseType = "BNF Analog";
   :>> cost_USD = 419.90;
   :>> mass = 257.0 [g];
   :>> propSize_in = 7.0;
   :>> wheelbase = 298.0 [mm];
   :>> flightController = "iStack F722 / Argus F722";
   :>> esc = "iStack 50A / Argus 65A";
   :>> motors = "Axisflying C287 1350KV";
   :>> propModel = "HQ 7035 / GF 7042";
   :>> uartCount = 6;
   :>> receiverProtocols = "TBS Nano RX (100mW PA)";
   :>> receiverIncluded = true;
   :>> receiverProtocol = "TBS Crossfire (CRSF)";
   :>> vtxIncluded = true;
   :>> vtxModel = "Unknown (not named on product page)";
   :>> fpvCameraIncluded = false;          // CSV: Unclear
   :>> gpsIncluded = true;
   :>> gpsModel = "Axisflying unbranded (likely M8N-class)";
   :>> sourceConfidence = "Low-Moderate";
  }

  part AF2c : Airframe {
   :>> name = "Axisflying KOLAS7";
   :>> purchaseType = "BNF HD";
   :>> cost_USD = 713.0;            // range 649-777
   :>> mass = 257.0 [g];
   :>> propSize_in = 7.0;
   :>> wheelbase = 298.0 [mm];
   :>> flightController = "iStack F722 / Argus F722";
   :>> esc = "iStack 50A / Argus 65A";
   :>> motors = "Axisflying C287 1350KV";
   :>> propModel = "HQ 7035 / GF 7042";
   :>> uartCount = 6;
   :>> receiverProtocols = "TBS Nano RX (100mW PA, O3 variant)";
   :>> receiverIncluded = true;
   :>> receiverProtocol = "TBS Crossfire (CRSF)";
   :>> vtxIncluded = true;
   :>> vtxModel = "DJI O3 Air Unit or Walksnail Avatar Pro";
   :>> fpvCameraIncluded = true;
   :>> fpvCameraType = "Digital HD (integrated with VTX)";
   :>> fpvCameraModel = "DJI O3 (1/1.7in) or Walksnail Avatar Pro";
   :>> gpsIncluded = true;
   :>> gpsModel = "Axisflying unbranded";
   :>> sourceConfidence = "High";
  }

  part AF3a : Airframe {
   :>> name = "iFlight Chimera9 ECO";
   :>> purchaseType = "PNP";
   :>> cost_USD = 346.99;
   :>> mass = 721.0 [g];
   :>> propSize_in = 9.0;
   :>> wheelbase = 405.0 [mm];
   :>> flightController = "BLITZ F7 (updated Jun 2026)";
   :>> esc = "BLITZ E55 4-in-1 55A";
   :>> motors = "XING-E 2809 800KV";
   :>> propModel = "HQ 9X4X3";
   :>> uartCount = 6;
   :>> receiverProtocols = "SBUS, PPM, CRSF, DSMX, iBus";
   :>> receiverIncluded = false;
   :>> vtxIncluded = true;
   :>> vtxModel = "BLITZ Whoop 5.8G 1.6W or 2.5W";
   :>> fpvCameraIncluded = true;
   :>> fpvCameraType = "Analog CMOS (model not named)";
   :>> gpsIncluded = false;          // optional +$39
   :>> gpsModel = "iFlight BLITZ M10 GPS V2 (G4, +$39 option)";
   :>> sourceConfidence = "High";
  }

  part AF3b : Airframe {
   :>> name = "iFlight Chimera9 ECO";
   :>> purchaseType = "BNF";
   :>> cost_USD = 372.0;            // ~372
   :>> mass = 721.0 [g];
   :>> propSize_in = 9.0;
   :>> wheelbase = 405.0 [mm];
   :>> flightController = "BLITZ F7 (updated Jun 2026)";
   :>> esc = "BLITZ E55 4-in-1 55A";
   :>> motors = "XING-E 2809 800KV";
   :>> propModel = "HQ 9X4X3";
   :>> uartCount = 6;
   :>> receiverProtocols = "TBS Crossfire Nano (100mW PA)";
   :>> receiverIncluded = true;
   :>> receiverProtocol = "TBS Crossfire (CRSF)";
   :>> vtxIncluded = true;
   :>> vtxModel = "BLITZ Whoop 5.8G 1.6W or 2.5W";
   :>> fpvCameraIncluded = true;
   :>> fpvCameraType = "Analog CMOS (model not named)";
   :>> gpsIncluded = false;          // optional +$39
   :>> gpsModel = "iFlight BLITZ M10 GPS V2 (G4, +$39 option)";
   :>> sourceConfidence = "High";
  }

  part AF4a : Airframe {
   :>> name = "DarwinFPV X9";
   :>> purchaseType = "PNP";
   :>> cost_USD = 340.0;            // range 280-400
   :>> propSize_in = 9.0;
   :>> wheelbase = 363.0 [mm];
   :>> flightController = "F411 MPU6500";
   :>> esc = "100A BLHeli_32 4-in-1";
   :>> motors = "2812 1100KV";
   :>> propModel = "Gemfan 9045-3";
   :>> uartCount = 2;               // 2 HW + 2 softserial
   :>> receiverProtocols = "SBUS, PPM, CRSF (UART2), DSMX/iBus via softserial";
   :>> receiverIncluded = false;
   :>> vtxIncluded = false;          // CSV: Unlikely
   :>> fpvCameraIncluded = false;    // CSV: Unlikely
   :>> gpsIncluded = false;          // not confirmed
   :>> sourceConfidence = "Low-Moderate";
  }

  part AF5 : Airframe {
   :>> name = "EMAX Hawk 7";
   :>> purchaseType = "BNF";
   :>> cost_USD = 398.86;
   :>> propSize_in = 7.0;
   :>> flightController = "F4 (model TBD)";
   :>> esc = "60A";
   :>> motors = "ECOII2807";
   :>> uartCount = 6;
   :>> receiverProtocols = "ELRS (CRSF protocol)";
   :>> receiverIncluded = true;
   :>> receiverProtocol = "ELRS (CRSF)";
   :>> vtxIncluded = true;
   :>> vtxModel = "EMAX 2.5W VTX (likely V4)";
   :>> fpvCameraIncluded = true;
   :>> fpvCameraType = "Analog CMOS (unknown model)";
   :>> fpvCameraModel = "Caddx or generic analog";
   :>> gpsIncluded = false;
   :>> sourceConfidence = "High";
  }

  part AF6a : Airframe {
   :>> name = "DeepSpace ROC7 O4 PRO";
   :>> purchaseType = "PNP+GPS";
   :>> cost_USD = 369.0;
   :>> propSize_in = 7.0;
   :>> flightController = "Argus F722 (STM32F722)";
   :>> esc = "60A BLHeli_32";
   :>> motors = "Redline 2807 1350KV";
   :>> uartCount = 6;
   :>> receiverProtocols = "SBUS, PPM, CRSF, DSMX, iBus (F7)";
   :>> receiverIncluded = false;
   :>> vtxIncluded = true;
   :>> vtxModel = "DJI O4 Pro Air Unit (digital HD)";
   :>> fpvCameraIncluded = true;
   :>> fpvCameraType = "Digital HD (integrated with VTX)";
   :>> fpvCameraModel = "DJI O4 Pro (1/1.3in, 4K/120fps)";
   :>> gpsIncluded = true;
   :>> gpsModel = "DeepSpace unbranded (~M8N/M10 class)";
   :>> sourceConfidence = "High";
  }

  part AF6b : Airframe {
   :>> name = "DeepSpace ROC7 O4 PRO";
   :>> purchaseType = "BNF";
   :>> cost_USD = 394.0;            // ~394
   :>> propSize_in = 7.0;
   :>> flightController = "Argus F722 (STM32F722)";
   :>> esc = "60A BLHeli_32";
   :>> motors = "Redline 2807 1350KV";
   :>> uartCount = 6;
   :>> receiverProtocols = "TBS Nano RX (100mW PA)";
   :>> receiverIncluded = true;
   :>> receiverProtocol = "TBS Crossfire (CRSF)";
   :>> vtxIncluded = true;
   :>> vtxModel = "DJI O4 Pro Air Unit (digital HD)";
   :>> fpvCameraIncluded = true;
   :>> fpvCameraType = "Digital HD (integrated with VTX)";
   :>> fpvCameraModel = "DJI O4 Pro (1/1.3in, 4K/120fps)";
   :>> gpsIncluded = true;
   :>> gpsModel = "DeepSpace unbranded";
   :>> sourceConfidence = "High";
  }

  part AF7 : Airframe {
   :>> name = "GEPRC Crocodile75 V3";
   :>> purchaseType = "PNP";
   :>> cost_USD = 510.0;            // range 470-550
   :>> propSize_in = 7.5;
   :>> wheelbase = 342.0 [mm];
   :>> flightController = "SPAN F722-BT-HD V2";
   :>> esc = "SPAN G50A / TAKER 32-bit 60A";
   :>> motors = "SPEEDX2 2806.5 1350KV";
   :>> propModel = "HQ 7.5x3.7x3";
   :>> uartCount = 5;
   :>> receiverProtocols = "SBUS, PPM, CRSF, DSMX, iBus, DUMD";
   :>> receiverIncluded = false;
   :>> vtxIncluded = true;
   :>> vtxModel = "GEPRC RAD 5.8G 1.6W (likely)";
   :>> fpvCameraIncluded = true;     // CSV: Likely Yes
   :>> fpvCameraType = "Analog CMOS";
   :>> gpsIncluded = false;
   :>> sourceConfidence = "Moderate";
  }

  part AF8a : Airframe {
   :>> name = "iFlight Chimera7 Pro V2";
   :>> purchaseType = "PNP";
   :>> cost_USD = 499.99;
   :>> mass = 725.0 [g];
   :>> propSize_in = 7.5;
   :>> wheelbase = 327.0 [mm];
   :>> flightController = "BLITZ F722";
   :>> esc = "BLITZ E55 4-in-1 55A";
   :>> motors = "XING2 2809 1250KV";
   :>> propModel = "HQ 7.5x3.7x3";
   :>> uartCount = 6;
   :>> receiverProtocols = "SBUS, PPM, CRSF, DSMX, iBus";
   :>> receiverIncluded = false;
   :>> vtxIncluded = true;
   :>> vtxModel = "BLITZ 5.8G 1.6W or 2.5W";
   :>> fpvCameraIncluded = true;
   :>> fpvCameraType = "Analog CMOS";
   :>> gpsIncluded = true;
   :>> gpsModel = "iFlight BLITZ M10 GPS V2 Mini (G4, pre-installed)";
   :>> sourceConfidence = "High";
  }

  part AF8b : Airframe {
   :>> name = "iFlight Chimera7 Pro V2";
   :>> purchaseType = "BNF";
   :>> cost_USD = 525.0;            // ~525
   :>> mass = 725.0 [g];
   :>> propSize_in = 7.5;
   :>> wheelbase = 327.0 [mm];
   :>> flightController = "BLITZ F722";
   :>> esc = "BLITZ E55 4-in-1 55A";
   :>> motors = "XING2 2809 1250KV";
   :>> propModel = "HQ 7.5x3.7x3";
   :>> uartCount = 6;
   :>> receiverProtocols = "TBS Crossfire Nano (100mW PA)";
   :>> receiverIncluded = true;
   :>> receiverProtocol = "TBS Crossfire (CRSF)";
   :>> vtxIncluded = true;
   :>> vtxModel = "BLITZ 5.8G 1.6W or 2.5W";
   :>> fpvCameraIncluded = true;
   :>> fpvCameraType = "Analog CMOS";
   :>> gpsIncluded = true;
   :>> gpsModel = "iFlight BLITZ M10 GPS V2 Mini (G4)";
   :>> sourceConfidence = "High";
  }

  part AF9a : Airframe {
   :>> name = "DarwinFPV 129 7in";
   :>> purchaseType = "PNP";
   :>> cost_USD = 222.0;            // range 180-264
   :>> propSize_in = 7.0;
   :>> flightController = "F4 (STM32F405, MATEKF405 firmware)";
   :>> esc = "50A";
   :>> motors = "2507";
   :>> propModel = "7040";
   :>> uartCount = 6;
   :>> receiverProtocols = "SBUS, PPM, CRSF, DSMX, iBus";
   :>> receiverIncluded = false;
   :>> vtxIncluded = false;          // CSV: Unlikely
   :>> fpvCameraIncluded = false;    // CSV: Unlikely
   :>> gpsIncluded = true;
   :>> gpsModel = "Darwin unbranded (likely BN-220/BN-880 class)";
   :>> sourceConfidence = "Moderate";
  }

  part AF10 : Airframe {
   :>> name = "NewBeeDrone ROC7 O4PRO";
   :>> purchaseType = "BNF only";
   :>> cost_USD = 699.0;
   :>> propSize_in = 7.0;
   :>> flightController = "Argus F722 (STM32F722)";
   :>> esc = "60A";
   :>> motors = "Redline 2807 1350KV";
   :>> uartCount = 6;
   :>> receiverProtocols = "Pre-configured BNF (receiver included)";
   :>> receiverIncluded = true;
   :>> vtxIncluded = true;
   :>> vtxModel = "DJI O4 Pro Air Unit";
   :>> fpvCameraIncluded = true;
   :>> fpvCameraType = "Digital HD (integrated with VTX)";
   :>> fpvCameraModel = "DJI O4 Pro (1/1.3in, 4K/120fps)";
   :>> gpsIncluded = true;
   :>> gpsModel = "DeepSpace unbranded (same unit)";
   :>> sourceConfidence = "Moderate";
  }
 }

 // =========================================================================
 // THERMAL CAMERA CANDIDATES  (source: analysis/thermal_camera_candidates.csv)
 // Base modules only; lens-variant analysis lives in the Analysis layer.
 // =========================================================================
 package ThermalCameraCandidates {

  part T1 : CameraSubsystem {
   :>> name = "Lepton 2.5";
   :>> brand = "FLIR / Teledyne";
   :>> cost_USD = 75.0;             // 65-85
   :>> mass = 0.9 [g];
   :>> power = 0.15 [W];
   :>> resolutionH = 80;
   :>> resolutionV = 60;
   :>> pixelPitch = 0.017 [mm];     // 17 um
   :>> detectorType = "Uncooled VOx";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 8.7;
   :>> netd = 0.05 [K];             // <50 mK
   :>> hfov = 57.0;
   :>> lensOptions = "2.1 / 4.7 / 9.4";
   :>> outputInterface = "SPI / CSI / USB via breakout";
   :>> radiometric = false;
   :>> dimensions = "11.5x11.5x7.5 core";
   :>> operatingTempMin_C = -10.0;
   :>> operatingTempMax_C = 80.0;
   :>> detectionRange = 15.0 [m];
  }

  part T2 : CameraSubsystem {
   :>> name = "Lepton 3.0";
   :>> brand = "FLIR / Teledyne";
   :>> cost_USD = 140.0;            // 130-150
   :>> mass = 0.9 [g];
   :>> power = 0.15 [W];
   :>> resolutionH = 160;
   :>> resolutionV = 120;
   :>> pixelPitch = 0.012 [mm];
   :>> detectorType = "Uncooled VOx";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 8.7;
   :>> netd = 0.05 [K];
   :>> hfov = 57.0;
   :>> lensOptions = "2.1 / 4.7 / 9.4";
   :>> outputInterface = "SPI / CSI / USB via breakout";
   :>> radiometric = false;
   :>> dimensions = "11.5x11.5x7.5 core";
   :>> operatingTempMin_C = -10.0;
   :>> operatingTempMax_C = 80.0;
   :>> detectionRange = 25.0 [m];
  }

  part T3 : CameraSubsystem {
   :>> name = "Lepton 3.5";
   :>> brand = "FLIR / Teledyne";
   :>> cost_USD = 186.0;            // 172-200
   :>> mass = 0.9 [g];
   :>> power = 0.15 [W];
   :>> resolutionH = 160;
   :>> resolutionV = 120;
   :>> pixelPitch = 0.012 [mm];
   :>> detectorType = "Uncooled VOx";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 8.7;
   :>> netd = 0.05 [K];
   :>> hfov = 57.0;
   :>> lensOptions = "2.1 / 4.7 / 9.4";
   :>> outputInterface = "SPI / CSI / USB via breakout";
   :>> radiometric = true;          // radiometric to +400C
   :>> dimensions = "11.5x11.5x7.5 core";
   :>> operatingTempMin_C = -10.0;
   :>> operatingTempMax_C = 80.0;
   :>> detectionRange = 25.0 [m];
  }

  part T4 : CameraSubsystem {
   :>> name = "DroneThermal v4 (Lepton Carrier)";
   :>> brand = "GroupGets / Horus Dynamics";
   :>> cost_USD = 240.0;            // 40-50 board / 240 kit w/ Lepton 3.5
   :>> mass = 2.3 [g];              // board only, no Lepton
   :>> power = 0.45 [W];
   :>> detectorType = "Lepton carrier (uses T1-T3 core)";
   :>> outputInterface = "Analog CVBS output";
   :>> radiometric = true;          // depends on Lepton core
   :>> dimensions = "20x20x10";
  }

  part T5 : CameraSubsystem {
   :>> name = "Horus Dynamics Lepton Drone Kit";
   :>> brand = "Horus Dynamics";
   :>> cost_USD = 245.0;            // 220-270
   :>> mass = 15.0 [g];
   :>> power = 0.8 [W];
   :>> resolutionH = 160;
   :>> resolutionV = 120;
   :>> pixelPitch = 0.012 [mm];
   :>> detectorType = "Uncooled VOx (Lepton 3.5)";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 8.7;
   :>> netd = 0.05 [K];
   :>> hfov = 57.0;
   :>> lensOptions = "2.1";
   :>> outputInterface = "Built-in CVBS analog";
   :>> radiometric = true;
   :>> dimensions = "~30x30x15";
   :>> operatingTempMin_C = -10.0;
   :>> operatingTempMax_C = 80.0;
  }

  part T6 : CameraSubsystem {
   :>> name = "Waveshare LWIR 80x62";
   :>> brand = "Waveshare";
   :>> cost_USD = 85.0;             // 70-100
   :>> mass = 15.0 [g];
   :>> power = 0.3 [W];
   :>> resolutionH = 80;
   :>> resolutionV = 62;
   :>> pixelPitch = 0.012 [mm];     // hybrid
   :>> detectorType = "Hybrid microbolometer + thermopile";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 8.7;
   :>> netd = 0.06 [K];             // <60 mK
   :>> hfov = 90.0;                 // 45 or 90 variant
   :>> lensOptions = "Fixed (two FOV variants)";
   :>> outputInterface = "SPI / I2C (HAT) or USB-C";
   :>> radiometric = false;
   :>> dimensions = "~40x30x15";
   :>> operatingTempMin_C = -20.0;
   :>> operatingTempMax_C = 85.0;
   :>> detectionRange = 10.0 [m];
  }

  part T7 : CameraSubsystem {
   :>> name = "Heimann HTPA80x64d";
   :>> brand = "Heimann Sensor";
   :>> cost_USD = 65.0;             // 50-80
   :>> mass = 0.6 [g];              // TO-8 only
   :>> power = 0.3 [W];
   :>> resolutionH = 80;
   :>> resolutionV = 64;
   :>> pixelPitch = 0.0125 [mm];    // ~12.5 um
   :>> detectorType = "Thermopile array";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 20.0;
   :>> netd = 0.1 [K];              // <100 mK
   :>> hfov = 33.0;                 // 33 to 120 depending on lens
   :>> lensOptions = "TO-8 lens options";
   :>> outputInterface = "SPI digital";
   :>> radiometric = true;
   :>> dimensions = "TO-8 ~9x9 mm";
   :>> operatingTempMin_C = -20.0;
   :>> operatingTempMax_C = 85.0;
   :>> detectionRange = 8.0 [m];
  }

  part T8 : CameraSubsystem {
   :>> name = "Generic 256x192 CVBS Module";
   :>> brand = "Generic OEM (Chinese)";
   :>> cost_USD = 150.0;            // 100-200
   :>> mass = 21.0 [g];
   :>> power = 0.7 [W];
   :>> resolutionH = 256;
   :>> resolutionV = 192;
   :>> pixelPitch = 0.012 [mm];
   :>> detectorType = "Uncooled VOx";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 25.0;
   :>> netd = 0.05 [K];             // <=50 mK (typical <40)
   :>> hfov = 30.0;                 // ~30x22 (9mm lens)
   :>> lensOptions = "4 / 7 / 9.1 / 10";
   :>> outputInterface = "CVBS / USB / UART";
   :>> radiometric = true;
   :>> dimensions = "~17x17x35";
   :>> inputVoltageMin = 4.5 [V];
   :>> inputVoltageMax = 20.0 [V];
   :>> operatingTempMin_C = -40.0;
   :>> operatingTempMax_C = 70.0;
   :>> detectionRange = 50.0 [m];
  }

  part T9 : CameraSubsystem {
   :>> name = "Generic 384x288 CVBS Module";
   :>> brand = "Generic OEM (Chinese)";
   :>> cost_USD = 320.0;            // 250-400
   :>> mass = 21.0 [g];
   :>> power = 0.7 [W];
   :>> resolutionH = 384;
   :>> resolutionV = 288;
   :>> pixelPitch = 0.012 [mm];
   :>> detectorType = "Uncooled VOx";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 25.0;
   :>> netd = 0.04 [K];             // <=40 mK typical
   :>> hfov = 24.0;                 // ~24x18 (9mm lens)
   :>> lensOptions = "4 / 9.1 / 13 / 15 / 19";
   :>> outputInterface = "CVBS / USB / UART";
   :>> radiometric = true;
   :>> dimensions = "~17x17x35";
   :>> inputVoltageMin = 4.5 [V];
   :>> inputVoltageMax = 20.0 [V];
   :>> operatingTempMin_C = -40.0;
   :>> operatingTempMax_C = 70.0;
   :>> detectionRange = 80.0 [m];
  }

  part T10 : CameraSubsystem {
   :>> name = "Generic 640x512 CVBS Module";
   :>> brand = "Generic OEM (Chinese)";
   :>> cost_USD = 550.0;            // 400-700
   :>> mass = 21.0 [g];
   :>> power = 0.75 [W];
   :>> resolutionH = 640;
   :>> resolutionV = 512;
   :>> pixelPitch = 0.012 [mm];
   :>> detectorType = "Uncooled VOx";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 25.0;
   :>> netd = 0.04 [K];
   :>> hfov = 46.0;                 // ~46x37 (9.1mm lens)
   :>> lensOptions = "9.1 / 13 / 15 / 19";
   :>> outputInterface = "CVBS / USB / UART";
   :>> radiometric = true;
   :>> dimensions = "~17x17x35";
   :>> inputVoltageMin = 4.5 [V];
   :>> inputVoltageMax = 20.0 [V];
   :>> operatingTempMin_C = -40.0;
   :>> operatingTempMax_C = 70.0;
   :>> detectionRange = 160.0 [m];
  }

  part T11 : CameraSubsystem {
   :>> name = "Axisflying 640 Thermal";
   :>> brand = "Axisflying";
   :>> cost_USD = 450.0;            // 350-550
   :>> mass = 25.0 [g];
   :>> power = 1.0 [W];
   :>> resolutionH = 640;
   :>> resolutionV = 512;
   :>> pixelPitch = 0.012 [mm];
   :>> detectorType = "Uncooled VOx";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 60.0;
   :>> netd = 0.04 [K];
   :>> hfov = 46.0;
   :>> lensOptions = "9mm fixed typically";
   :>> outputInterface = "CVBS analog";
   :>> radiometric = true;
   :>> dimensions = "~17x17x38";
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 24.0 [V];
   :>> operatingTempMin_C = -20.0;
   :>> operatingTempMax_C = 65.0;
   :>> detectionRange = 160.0 [m];
  }

  part T12 : CameraSubsystem {
   :>> name = "iVcan Mini-640-CVBS";
   :>> brand = "iVcan";
   :>> cost_USD = 575.0;            // 450-700
   :>> mass = 21.0 [g];
   :>> power = 0.75 [W];
   :>> resolutionH = 640;
   :>> resolutionV = 512;
   :>> pixelPitch = 0.012 [mm];
   :>> detectorType = "Uncooled VOx";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 50.0;
   :>> netd = 0.04 [K];
   :>> hfov = 46.0;
   :>> lensOptions = "9.1 / 13";
   :>> outputInterface = "CVBS / USB 2.0 / UART";
   :>> radiometric = true;
   :>> dimensions = "17.3x17.3x35.6";
   :>> inputVoltageMin = 4.5 [V];
   :>> inputVoltageMax = 20.0 [V];
   :>> operatingTempMin_C = -40.0;
   :>> operatingTempMax_C = 70.0;
   :>> detectionRange = 160.0 [m];
  }

  part T13 : CameraSubsystem {
   :>> name = "PurpleRiver Mini 640";
   :>> brand = "PurpleRiver";
   :>> cost_USD = 450.0;            // 350-550
   :>> mass = 21.0 [g];
   :>> power = 0.8 [W];
   :>> resolutionH = 640;
   :>> resolutionV = 512;
   :>> pixelPitch = 0.012 [mm];
   :>> detectorType = "Uncooled VOx";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 25.0;
   :>> netd = 0.05 [K];
   :>> hfov = 46.0;
   :>> lensOptions = "9.1 / 13";
   :>> outputInterface = "CVBS / USB";
   :>> radiometric = true;
   :>> dimensions = "~17x17x35";
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 24.0 [V];
   :>> operatingTempMin_C = -40.0;
   :>> operatingTempMax_C = 65.0;
   :>> detectionRange = 160.0 [m];
  }

  part T14 : CameraSubsystem {
   :>> name = "Arducam 640x512 USB Thermal";
   :>> brand = "Arducam";
   :>> cost_USD = 650.0;            // 500-800
   :>> mass = 40.0 [g];
   :>> power = 1.5 [W];
   :>> resolutionH = 640;
   :>> resolutionV = 512;
   :>> pixelPitch = 0.012 [mm];
   :>> detectorType = "Uncooled VOx";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 50.0;
   :>> netd = 0.04 [K];
   :>> hfov = 46.0;
   :>> lensOptions = "9.1";
   :>> outputInterface = "USB UVC (plug-and-play)";
   :>> radiometric = true;
   :>> dimensions = "~45x45x60 enclosed";
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 5.0 [V];   // USB bus
   :>> operatingTempMin_C = -20.0;
   :>> operatingTempMax_C = 55.0;
   :>> detectionRange = 160.0 [m];
  }

  part T15 : CameraSubsystem {
   :>> name = "Seek Thermal Mosaic Core 320";
   :>> brand = "Seek Thermal";
   :>> cost_USD = 400.0;            // 350-500
   :>> mass = 25.0 [g];
   :>> power = 1.0 [W];
   :>> resolutionH = 320;
   :>> resolutionV = 240;
   :>> pixelPitch = 0.012 [mm];
   :>> detectorType = "Thermal CMOS";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 9.0;          // <=9 slow / <=32 fast
   :>> netd = 0.07 [K];             // <70 mK
   :>> hfov = 56.0;                 // 24 or 56 HFOV
   :>> lensOptions = "Fixed";
   :>> outputInterface = "UART / USB";
   :>> radiometric = true;
   :>> dimensions = "~27x25x18";
   :>> inputVoltageMin = 3.3 [V];
   :>> inputVoltageMax = 5.0 [V];
   :>> operatingTempMin_C = -10.0;
   :>> operatingTempMax_C = 50.0;
   :>> detectionRange = 60.0 [m];
  }

  part T16 : CameraSubsystem {
   :>> name = "FLIR Boson 640";
   :>> brand = "FLIR / Teledyne";
   :>> cost_USD = 2000.0;           // 1500-2500 (benchmark, over budget)
   :>> mass = 13.0 [g];             // module only
   :>> power = 0.5 [W];
   :>> resolutionH = 640;
   :>> resolutionV = 512;
   :>> pixelPitch = 0.012 [mm];
   :>> detectorType = "Uncooled VOx";
   :>> spectralRange = "8-14 um (LWIR)";
   :>> frameRate_Hz = 60.0;
   :>> netd = 0.03 [K];             // <=30 mK (best in class)
   :>> lensOptions = "7.5 / 9 / 13 / 19 / 25+";
   :>> outputInterface = "CMOS / LVCMOS / UART";
   :>> radiometric = true;
   :>> dimensions = "~21x21x12";
   :>> inputVoltageMin = 3.3 [V];
   :>> inputVoltageMax = 5.0 [V];
   :>> operatingTempMin_C = -40.0;
   :>> operatingTempMax_C = 85.0;
   :>> detectionRange = 400.0 [m];
  }
 }

 // =========================================================================
 // FPV (NON-IR) CAMERA CANDIDATES  (source: analysis/nonIR_camera_candidates.csv)
 // =========================================================================
 package FpvCameraCandidates {

  part A1 : FpvCamera {
   :>> name = "Caddx H1";
   :>> cameraModel = "Caddx H1";
   :>> cameraType = "Analog CMOS";
   :>> cost_USD = 20.0;             // 15-25
   :>> mass = 7.4 [g];
   :>> power = 0.8 [W];
   :>> includedWithAirframe = true; // bundled in MARK4 LR7 (#1)
   :>> sensorSize = "1/3in";
   :>> resolutionTVL = 1200.0;
   :>> fovLens = "2.1mm (~100 deg FOV)";
   :>> minIllumination_lux = 0.00001;
   :>> inputVoltageMin = 4.5 [V];
   :>> inputVoltageMax = 25.0 [V];
   :>> outputType = "CVBS analog";
   :>> connectorType = "Molex picoblade 1.25mm";
   :>> mountingPattern = "14x14mm";
   :>> vtxTypeRequired = "Separate analog VTX";
   :>> goggleCompatibility = "Any analog goggles/receiver";
  }

  part A2 : FpvCamera {
   :>> name = "Caddx Ratel 2";
   :>> cameraModel = "Caddx Ratel 2";
   :>> cameraType = "Analog CMOS (Starlight)";
   :>> cost_USD = 30.0;
   :>> mass = 8.0 [g];
   :>> power = 0.9 [W];
   :>> includedWithAirframe = false;
   :>> sensorSize = "1/1.8in";
   :>> resolutionTVL = 1200.0;
   :>> fovLens = "2.1 or 2.5mm (~100-120 deg)";
   :>> minIllumination_lux = 0.0001;
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 40.0 [V];
   :>> outputType = "CVBS analog";
   :>> mountingPattern = "14x14mm";
   :>> vtxTypeRequired = "Separate analog VTX";
   :>> goggleCompatibility = "Any analog goggles/receiver";
  }

  part A3 : FpvCamera {
   :>> name = "Foxeer Predator Mini V4";
   :>> cameraModel = "Foxeer Predator Mini V4";
   :>> cameraType = "Analog CMOS";
   :>> cost_USD = 25.0;
   :>> mass = 6.0 [g];
   :>> power = 0.7 [W];
   :>> includedWithAirframe = false;
   :>> sensorSize = "1/3in";
   :>> resolutionTVL = 1200.0;
   :>> fovLens = "2.1mm (~100 deg)";
   :>> minIllumination_lux = 0.001;
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 40.0 [V];
   :>> outputType = "CVBS analog";
   :>> mountingPattern = "14x14mm";
   :>> vtxTypeRequired = "Separate analog VTX";
   :>> goggleCompatibility = "Any analog goggles/receiver";
  }

  part A4 : FpvCamera {
   :>> name = "Runcam Phoenix 2";
   :>> cameraModel = "Runcam Phoenix 2";
   :>> cameraType = "Analog CMOS (StarLight)";
   :>> cost_USD = 35.0;
   :>> mass = 8.0 [g];
   :>> power = 0.9 [W];
   :>> includedWithAirframe = false;
   :>> sensorSize = "1/2.8in";
   :>> resolutionTVL = 1200.0;
   :>> fovLens = "2.1mm (~100 deg WDR)";
   :>> minIllumination_lux = 0.0001;
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 36.0 [V];
   :>> outputType = "CVBS analog";
   :>> mountingPattern = "14x14mm";
   :>> vtxTypeRequired = "Separate analog VTX";
   :>> goggleCompatibility = "Any analog goggles/receiver";
  }

  part A5 : FpvCamera {
   :>> name = "iFlight Generic Analog";
   :>> cameraModel = "iFlight Generic Analog (unnamed)";
   :>> cameraType = "Analog CMOS";
   :>> cost_USD = 12.0;             // ~10-15
   :>> mass = 7.0 [g];
   :>> power = 0.7 [W];
   :>> includedWithAirframe = true; // Chimera9 ECO (#3), Chimera7 Pro V2 (#8)
   :>> sensorSize = "1/3in (est)";
   :>> resolutionTVL = 1200.0;
   :>> fovLens = "Standard FPV (~90-100 deg)";
   :>> outputType = "CVBS analog";
   :>> mountingPattern = "14x14mm";
   :>> vtxTypeRequired = "Separate analog VTX";
   :>> goggleCompatibility = "Any analog goggles/receiver";
  }

  part A6 : FpvCamera {
   :>> name = "EMAX Generic Analog";
   :>> cameraModel = "EMAX Generic Analog (unnamed)";
   :>> cameraType = "Analog CMOS";
   :>> cost_USD = 15.0;
   :>> mass = 7.0 [g];
   :>> power = 0.7 [W];
   :>> includedWithAirframe = true; // EMAX Hawk 7 (#5)
   :>> fovLens = "Standard FPV";
   :>> outputType = "CVBS analog";
   :>> mountingPattern = "14x14mm";
   :>> vtxTypeRequired = "Separate analog VTX";
   :>> goggleCompatibility = "Any analog goggles/receiver";
  }

  part A7 : FpvCamera {
   :>> name = "Caddx Ant";
   :>> cameraModel = "Caddx Ant";
   :>> cameraType = "Analog CMOS (Nano)";
   :>> cost_USD = 17.0;
   :>> mass = 2.0 [g];
   :>> power = 0.3 [W];
   :>> includedWithAirframe = false;
   :>> sensorSize = "1/3in";
   :>> resolutionTVL = 1200.0;
   :>> fovLens = "1.8mm (~165 deg FOV)";
   :>> minIllumination_lux = 0.01;
   :>> inputVoltageMin = 3.7 [V];
   :>> inputVoltageMax = 18.0 [V];
   :>> outputType = "CVBS analog";
   :>> connectorType = "Standard analog plug (1.0mm pitch)";
   :>> mountingPattern = "14x14mm nano";
   :>> vtxTypeRequired = "Separate analog VTX";
   :>> goggleCompatibility = "Any analog goggles/receiver";
  }

  part A8 : FpvCamera {
   :>> name = "Foxeer T-Rex Micro";
   :>> cameraModel = "Foxeer T-Rex Micro";
   :>> cameraType = "Analog CMOS";
   :>> cost_USD = 25.0;
   :>> mass = 7.0 [g];
   :>> power = 0.5 [W];
   :>> includedWithAirframe = false;
   :>> sensorSize = "1/3in (2MP)";
   :>> resolutionTVL = 1500.0;
   :>> fovLens = "2.1mm (~120 deg FOV)";
   :>> minIllumination_lux = 0.001;
   :>> inputVoltageMin = 4.5 [V];
   :>> inputVoltageMax = 25.0 [V];
   :>> outputType = "CVBS analog";
   :>> mountingPattern = "14x14mm";
   :>> vtxTypeRequired = "Separate analog VTX";
   :>> goggleCompatibility = "Any analog goggles/receiver";
  }

  part D1 : FpvCamera {
   :>> name = "DJI O4 Pro Air Unit";
   :>> cameraModel = "DJI O4 Pro Air Unit";
   :>> cameraType = "Integrated Digital (DJI)";
   :>> cost_USD = 229.0;
   :>> mass = 32.0 [g];             // all-in-one
   :>> power = 10.0 [W];            // 8-10 W
   :>> includedWithAirframe = true; // DeepSpace ROC7 (#6), NewBeeDrone ROC7 (#10)
   :>> sensorSize = "1/1.3in CMOS";
   :>> fovLens = "~110 deg FOV";
   :>> inputVoltageMin = 7.4 [V];
   :>> inputVoltageMax = 26.4 [V];
   :>> outputType = "Digital HD (DJI O4 protocol)";
   :>> connectorType = "IPEX/U.FL (dual antenna)";
   :>> vtxTypeRequired = "Integrated (camera+VTX combo)";
   :>> goggleCompatibility = "DJI Goggles 3 / N3 / Integra";
  }

  part D2 : FpvCamera {
   :>> name = "DJI O3 Air Unit";
   :>> cameraModel = "DJI O3 Air Unit";
   :>> cameraType = "Integrated Digital (DJI)";
   :>> cost_USD = 174.0;            // 149-199
   :>> mass = 36.0 [g];
   :>> power = 8.0 [W];             // 5-8 W
   :>> includedWithAirframe = true; // KOLAS7 BNF HD (#2c)
   :>> sensorSize = "1/1.7in CMOS";
   :>> fovLens = "~110 deg FOV";
   :>> inputVoltageMin = 7.4 [V];
   :>> inputVoltageMax = 26.4 [V];
   :>> outputType = "Digital HD (DJI O3 protocol)";
   :>> connectorType = "IPEX (single antenna)";
   :>> vtxTypeRequired = "Integrated (camera+VTX combo)";
   :>> goggleCompatibility = "DJI Goggles 2 / Integra / V2";
  }

  part D3 : FpvCamera {
   :>> name = "Walksnail Avatar Pro";
   :>> cameraModel = "Walksnail Avatar Pro";
   :>> cameraType = "Integrated Digital (Walksnail)";
   :>> cost_USD = 275.0;            // 250-300
   :>> mass = 30.0 [g];
   :>> power = 8.0 [W];             // 5-8 W
   :>> includedWithAirframe = true; // KOLAS7 BNF HD (#2c)
   :>> sensorSize = "1/1.8in CMOS";
   :>> fovLens = "~110 deg FOV";
   :>> inputVoltageMin = 7.4 [V];
   :>> inputVoltageMax = 26.4 [V];
   :>> outputType = "Digital HD (Walksnail protocol)";
   :>> connectorType = "IPEX (single antenna)";
   :>> vtxTypeRequired = "Integrated (camera+VTX combo)";
   :>> goggleCompatibility = "Walksnail Avatar goggles / VRX";
  }

  part D4 : FpvCamera {
   :>> name = "RunCam Racer 4 (Analog+MIPI)";
   :>> cameraModel = "RunCam Racer 4";
   :>> cameraType = "Hybrid Analog / Digital MIPI";
   :>> cost_USD = 40.0;             // 35-45
   :>> mass = 6.0 [g];
   :>> power = 1.15 [W];            // 0.55 analog / 1.15 digital
   :>> includedWithAirframe = false;
   :>> sensorSize = "1/2.7in Super WDR CMOS";
   :>> fovLens = "1.8mm (~160 deg FOV)";
   :>> minIllumination_lux = 0.001;
   :>> inputVoltageMin = 3.3 [V];   // 3.3 digital / 5-36 analog
   :>> inputVoltageMax = 36.0 [V];
   :>> outputType = "CVBS analog + MIPI digital (switchable)";
   :>> connectorType = "Analog JST + MIPI ribbon";
   :>> mountingPattern = "20x19x19mm board";
   :>> vtxTypeRequired = "Analog VTX or DJI/HDZero air unit";
   :>> goggleCompatibility = "Any analog or DJI goggles";
  }

  part D5 : FpvCamera {
   :>> name = "Foxeer Apollo Digital (DJI)";
   :>> cameraModel = "Foxeer Apollo Digital";
   :>> cameraType = "Digital MIPI (DJI)";
   :>> cost_USD = 50.0;             // 45-55
   :>> mass = 8.0 [g];
   :>> power = 0.7 [W];
   :>> includedWithAirframe = false;
   :>> sensorSize = "1/2in Sony CMOS";
   :>> fovLens = "~160 deg FOV";
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 36.0 [V];
   :>> outputType = "MIPI digital (DJI/HDZero compatible)";
   :>> connectorType = "MIPI ribbon cable";
   :>> mountingPattern = "19x19mm (est)";
   :>> vtxTypeRequired = "Separate DJI air unit or HDZero VTX";
   :>> goggleCompatibility = "DJI Goggles, HDZero Goggles";
  }

  part D6 : FpvCamera {
   :>> name = "HDZero Nano V3 (Camera only)";
   :>> cameraModel = "HDZero Nano V3";
   :>> cameraType = "Digital MIPI (HDZero)";
   :>> cost_USD = 30.0;             // 25-35
   :>> mass = 5.0 [g];
   :>> power = 0.5 [W];
   :>> includedWithAirframe = false;
   :>> sensorSize = "1/3in (est)";
   :>> fovLens = "~150 deg FOV (est)";
   :>> inputVoltageMin = 3.3 [V];   // from VTX
   :>> inputVoltageMax = 3.3 [V];
   :>> outputType = "MIPI digital";
   :>> connectorType = "MIPI ribbon cable";
   :>> mountingPattern = "14x14mm nano";
   :>> vtxTypeRequired = "Separate HDZero VTX";
   :>> goggleCompatibility = "HDZero Goggles (any)";
  }

  part D7 : FpvCamera {
   :>> name = "Foxeer Digisight 3 (HDZero)";
   :>> cameraModel = "Foxeer Digisight 3";
   :>> cameraType = "Digital MIPI (HDZero)";
   :>> cost_USD = 40.0;             // 35-45
   :>> mass = 8.0 [g];
   :>> power = 0.7 [W];
   :>> includedWithAirframe = false;
   :>> sensorSize = "1/2.7in CMOS";
   :>> fovLens = "~160 deg FOV";
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 36.0 [V];
   :>> outputType = "MIPI digital";
   :>> connectorType = "MIPI ribbon cable";
   :>> mountingPattern = "19x19mm mount";
   :>> vtxTypeRequired = "Separate HDZero VTX";
   :>> goggleCompatibility = "HDZero Goggles (any)";
  }

  part D8 : FpvCamera {
   :>> name = "Walksnail Avatar Nano Kit V3";
   :>> cameraModel = "Walksnail Avatar Nano Kit V3";
   :>> cameraType = "Digital VTX+Camera Kit (Walksnail)";
   :>> cost_USD = 135.0;            // 120-150
   :>> mass = 17.0 [g];            // ~14 VTX + ~3 cam
   :>> power = 5.0 [W];            // ~4-6 W
   :>> includedWithAirframe = false;
   :>> sensorSize = "1/3.2in CMOS";
   :>> fovLens = "2.1mm (~160 deg FOV)";
   :>> inputVoltageMin = 7.4 [V];
   :>> inputVoltageMax = 26.4 [V];
   :>> outputType = "Digital HD (Walksnail protocol)";
   :>> connectorType = "IPEX (U.FL)";
   :>> mountingPattern = "VTX 20x20mm M2, Cam 14x14mm";
   :>> vtxTypeRequired = "Separate Walksnail VTX (included in kit)";
   :>> goggleCompatibility = "Walksnail Avatar goggles (any)";
  }
 }

 // =========================================================================
 // GPS MODULE CANDIDATES  (source: analysis/gps_candidates.csv)
 // =========================================================================
 package GpsCandidates {

  part G1 : GpsModule {
   :>> name = "Beitian BN-220";
   :>> chipset = "M10050 (M8N-class)";
   :>> cost_USD = 18.0;             // 15-20
   :>> mass = 5.0 [g];
   :>> power = 0.25 [W];
   :>> includedWithAirframe = false;
   :>> constellations = "GPS+BDS+GALILEO+SBAS+QZSS";
   :>> coldStart = 38.0 [s];        // 30-45
   :>> hotStart = 3.0 [s];          // 2-5
   :>> updateRate_Hz = 10.0;
   :>> accuracyCEP = 2.5 [m];
   :>> currentDraw = 0.05 [A];      // 50 mA @5V
   :>> voltageMin = 3.6 [V];
   :>> voltageMax = 5.5 [V];
   :>> compass = "No";
   :>> connector = "4-pin JST-SH (UART)";
   :>> mounting = "22x20mm";
   :>> dimensions = "22x20x6mm";
  }

  part G2 : GpsModule {
   :>> name = "Beitian BN-880";
   :>> chipset = "M8N clone (u-blox)";
   :>> cost_USD = 12.0;             // 10-14
   :>> mass = 8.0 [g];
   :>> power = 0.25 [W];
   :>> includedWithAirframe = false;
   :>> constellations = "GPS+GLONASS+Galileo+BeiDou+SBAS+QZSS";
   :>> coldStart = 38.0 [s];
   :>> hotStart = 3.0 [s];
   :>> updateRate_Hz = 10.0;
   :>> accuracyCEP = 2.5 [m];
   :>> currentDraw = 0.05 [A];
   :>> voltageMin = 2.8 [V];
   :>> voltageMax = 6.0 [V];
   :>> compass = "HMC5883L";
   :>> connector = "6-pin JST-SH (UART + I2C)";
   :>> mounting = "28x28mm";
   :>> dimensions = "28x28x10mm";
  }

  part G3 : GpsModule {
   :>> name = "Matek M10Q-5883";
   :>> chipset = "u-blox SAM-M10Q";
   :>> cost_USD = 25.0;             // 22-28
   :>> mass = 5.0 [g];
   :>> power = 0.23 [W];
   :>> includedWithAirframe = false;
   :>> constellations = "GPS+GLO+GAL+BDS";
   :>> coldStart = 18.0 [s];        // 15-20
   :>> hotStart = 1.5 [s];          // 1-2
   :>> updateRate_Hz = 14.0;        // 10-18
   :>> accuracyCEP = 1.5 [m];
   :>> currentDraw = 0.045 [A];     // ~45 mA
   :>> voltageMin = 5.0 [V];
   :>> voltageMax = 5.0 [V];        // 5V BEC
   :>> compass = "QMC5883L (included)";
   :>> connector = "6-pin JST-GH (UART+I2C)";
   :>> mounting = "15x15mm (antenna)";
   :>> dimensions = "~20x20mm board";
  }

  part G4 : GpsModule {
   :>> name = "iFlight BLITZ M10 GPS V2 (Mini)";
   :>> chipset = "u-blox M10";
   :>> cost_USD = 41.99;
   :>> mass = 8.0 [g];
   :>> power = 0.25 [W];
   :>> includedWithAirframe = false;
   :>> constellations = "GPS+SBAS+Galileo+QZSS+Glonass";
   :>> coldStart = 27.0 [s];
   :>> hotStart = 1.0 [s];
   :>> updateRate_Hz = 10.0;
   :>> accuracyCEP = 1.5 [m];
   :>> currentDraw = 0.05 [A];
   :>> voltageMin = 3.3 [V];
   :>> voltageMax = 5.5 [V];
   :>> compass = "QMC5883L";
   :>> connector = "JST-SH (UART+I2C)";
   :>> mounting = "20x21mm";
   :>> dimensions = "20x21x8mm";
  }

  part G5 : GpsModule {
   :>> name = "iFlight BLITZ M10 GPS V2 (Standard)";
   :>> chipset = "u-blox M10";
   :>> cost_USD = 41.99;
   :>> mass = 16.0 [g];
   :>> power = 0.25 [W];
   :>> includedWithAirframe = false;
   :>> constellations = "GPS+SBAS+Galileo+QZSS+Glonass";
   :>> coldStart = 27.0 [s];
   :>> hotStart = 1.0 [s];
   :>> updateRate_Hz = 10.0;
   :>> accuracyCEP = 1.5 [m];
   :>> currentDraw = 0.05 [A];
   :>> voltageMin = 3.3 [V];
   :>> voltageMax = 5.5 [V];
   :>> compass = "QMC5883L";
   :>> connector = "JST-SH (UART+I2C)";
   :>> mounting = "25x25mm";
   :>> dimensions = "25x25x11mm";
  }

  part G6 : GpsModule {
   :>> name = "TBS M10 GPS";
   :>> chipset = "u-blox M10";
   :>> cost_USD = 32.0;             // 30-35
   :>> mass = 4.0 [g];
   :>> power = 0.2 [W];
   :>> includedWithAirframe = false;
   :>> constellations = "GPS+GLO+GAL+BDS";
   :>> coldStart = 15.0 [s];        // 12-18
   :>> hotStart = 1.0 [s];
   :>> updateRate_Hz = 18.0;
   :>> accuracyCEP = 1.5 [m];
   :>> currentDraw = 0.04 [A];      // ~40 mA
   :>> voltageMin = 5.0 [V];
   :>> voltageMax = 5.0 [V];
   :>> compass = "No";
   :>> connector = "u.FL (active antenna) + JST-SH (UART)";
   :>> mounting = "Integrated";
   :>> dimensions = "~15x12mm";
  }
 }

 // =========================================================================
 // SBC (SINGLE-BOARD COMPUTER) CANDIDATES  (source: analysis/sbc_comparison.csv)
 // =========================================================================
 package SbcCandidates {

  part SBC1 : SingleBoardComputerPayload {
   :>> name = "Radxa ZERO 2 Pro";
   :>> cost_USD = 113.0;            // total solution
   :>> boardCost_USD = 75.0;
   :>> additionalCost_USD = 38.0;
   :>> mass = 59.0 [g];            // total solution
   :>> boardMass = 30.0 [g];
   :>> additionalMass = 29.0 [g];
   :>> power = 10.0 [W];           // max inference
   :>> idlePower = 3.0 [W];
   :>> soc = "Amlogic A311D";
   :>> cpu = "4x A73 @2.2GHz + 2x A53 @1.8GHz";
   :>> npuTOPS = 5.0;
   :>> ram = "4 GB LPDDR4";
   :>> storage = "16-64 GB eMMC + microSD";
   :>> powerInput = "USB-C 5V (PD)";
   :>> usbPortCount = 2;
   :>> uartPortCount = 3;
   :>> wifiBt = "WiFi 5 + BT 5.0";
   :>> videoInput = "MIPI CSI (31-pin)";
   :>> videoOutput = "Micro HDMI 4K@60";
   :>> gpio = "40-pin header";
   :>> coolingType = "Passive (heatsink included)";
   :>> dimensions = "65 x 36 mm";
   :>> osSupport = "Ubuntu / Armbian / Android";
  }

  part SBC2 : SingleBoardComputerPayload {
   :>> name = "Orange Pi 5 (8 GB)";
   :>> cost_USD = 150.0;
   :>> boardCost_USD = 110.0;
   :>> additionalCost_USD = 40.0;
   :>> mass = 78.0 [g];
   :>> boardMass = 55.0 [g];
   :>> additionalMass = 23.0 [g];
   :>> power = 12.0 [W];
   :>> idlePower = 4.0 [W];
   :>> soc = "Rockchip RK3588S";
   :>> cpu = "4x A76 @2.4GHz + 4x A55 @1.8GHz";
   :>> npuTOPS = 6.0;
   :>> ram = "8 GB LPDDR4X";
   :>> storage = "microSD (optional eMMC module)";
   :>> powerInput = "USB-C 5V/4A PD";
   :>> usbPortCount = 4;
   :>> uartPortCount = 3;
   :>> wifiBt = "WiFi 6 + BT 5.0";
   :>> videoInput = "MIPI CSI";
   :>> videoOutput = "2x HDMI 2.0 (4K@60)";
   :>> gpio = "40-pin header";
   :>> coolingType = "Passive + optional fan (recommended under load)";
   :>> dimensions = "90 x 62 mm";
   :>> osSupport = "Ubuntu / Armbian / Debian / Android / Orange Pi OS";
  }

  part SBC3 : SingleBoardComputerPayload {
   :>> name = "NanoPi M5 (4 GB)";
   :>> cost_USD = 126.0;
   :>> boardCost_USD = 87.0;
   :>> additionalCost_USD = 39.0;
   :>> mass = 80.0 [g];
   :>> boardMass = 58.0 [g];
   :>> additionalMass = 22.0 [g];
   :>> power = 10.0 [W];
   :>> idlePower = 4.0 [W];
   :>> soc = "Rockchip RK3576";
   :>> cpu = "4x A72 @2.2GHz + 4x A53 @2.0GHz";
   :>> npuTOPS = 6.0;
   :>> ram = "4 GB LPDDR4X";
   :>> storage = "16 MB SPI NOR + microSD + UFS (optional)";
   :>> powerInput = "USB-C 6-20V PD";
   :>> usbPortCount = 2;
   :>> uartPortCount = 4;
   :>> wifiBt = "M.2 SDIO module required (+$9)";
   :>> videoInput = "2x MIPI CSI (4-lane)";
   :>> videoOutput = "HDMI 2.0 (4K@60)";
   :>> gpio = "30-pin header";
   :>> coolingType = "Passive (fan header available)";
   :>> dimensions = "90 x 62 mm";
   :>> osSupport = "Ubuntu / Debian / Armbian / Android";
  }
 }

 // =========================================================================
 // RADIO RECEIVER (ELRS / onboard) CANDIDATES  (source: analysis/ELRS_receivers.csv)
 // =========================================================================
 package RadioReceiverCandidates {

  part RP3V2 : RadioReceiver {
   :>> name = "RadioMaster RP3 V2";
   :>> manufacturer = "RadioMaster";
   :>> cost_USD = 27.0;            // 24.99-29.99
   :>> mass = 4.6 [g];
   :>> maxRange = 3.5 [km];
   :>> protocol = "ELRS";
   :>> interfaceType = "CRSF";
   :>> band = "2.4 GHz";
   :>> size = "22x13x4 mm";
   :>> antennaType = "2x External UFL T (65mm)";
   :>> telemetryPower = 0.1 [W];   // 100 mW
   :>> paLna = true;
   :>> diversityType = "Antenna Diversity (switched)";
   :>> tcxo = true;
   :>> currentDraw = 0.15 [A];     // ~120-180 mA
   :>> mcu = "ESP8285";
   :>> rfChip = "SX1281";
   :>> includedWithAirframe = false;
  }

  part RP4TD : RadioReceiver {
   :>> name = "RadioMaster RP4TD";
   :>> manufacturer = "RadioMaster";
   :>> cost_USD = 42.0;            // 39.99-44.99
   :>> mass = 3.0 [g];
   :>> maxRange = 5.0 [km];
   :>> protocol = "ELRS";
   :>> interfaceType = "CRSF + UART";
   :>> band = "2.4 GHz";
   :>> size = "23.7x16.3x4 mm";
   :>> antennaType = "2x External UFL T (65mm)";
   :>> telemetryPower = 0.1 [W];   // 2x 100 mW
   :>> paLna = true;
   :>> diversityType = "True Diversity (dual RX chains)";
   :>> tcxo = true;
   :>> currentDraw = 0.2 [A];      // ~150-250 mA
   :>> mcu = "ESP32";
   :>> rfChip = "2x SX1281";
   :>> includedWithAirframe = false;
  }

  part RP4TD_M : RadioReceiver {
   :>> name = "RadioMaster RP4TD-M";
   :>> manufacturer = "RadioMaster";
   :>> cost_USD = 34.99;
   :>> mass = 1.0 [g];
   :>> maxRange = 4.0 [km];
   :>> protocol = "ELRS";
   :>> interfaceType = "CRSF";
   :>> band = "2.4 GHz";
   :>> size = "mini";
   :>> antennaType = "2x External UFL";
   :>> telemetryPower = 0.1 [W];
   :>> paLna = true;
   :>> diversityType = "True Diversity";
   :>> tcxo = true;
   :>> currentDraw = 0.15 [A];
   :>> mcu = "ESP32";
   :>> rfChip = "2x SX1281";
   :>> includedWithAirframe = false;
  }

  part EP1 : RadioReceiver {
   :>> name = "Happymodel EP1 Dual TCXO";
   :>> manufacturer = "Happymodel";
   :>> cost_USD = 16.0;            // 14.39-18.99
   :>> mass = 1.5 [g];
   :>> maxRange = 4.0 [km];
   :>> protocol = "ELRS";
   :>> interfaceType = "CRSF";
   :>> band = "2.4 GHz";
   :>> size = "19x14 mm";
   :>> antennaType = "2x External UFL";
   :>> telemetryPower = 0.08 [W];  // ~80 mW (>19 dBm)
   :>> paLna = true;
   :>> diversityType = "True Diversity";
   :>> tcxo = true;
   :>> currentDraw = 0.125 [A];
   :>> mcu = "ESP32 PICO D4";
   :>> rfChip = "2x SX1280/SX1281";
   :>> includedWithAirframe = false;
  }

  part SuperD : RadioReceiver {
   :>> name = "BetaFPV SuperD";
   :>> manufacturer = "BetaFPV";
   :>> cost_USD = 24.99;
   :>> mass = 1.1 [g];
   :>> maxRange = 4.0 [km];
   :>> protocol = "ELRS";
   :>> interfaceType = "CRSF";
   :>> band = "2.4 GHz";
   :>> size = "22x14 mm";
   :>> antennaType = "2x External";
   :>> telemetryPower = 0.1 [W];
   :>> paLna = true;
   :>> diversityType = "True Diversity";
   :>> tcxo = true;
   :>> currentDraw = 0.125 [A];
   :>> includedWithAirframe = false;
  }

  part iFlightTD : RadioReceiver {
   :>> name = "iFlight True Diversity";
   :>> manufacturer = "iFlight";
   :>> cost_USD = 29.99;
   :>> mass = 3.3 [g];
   :>> maxRange = 5.0 [km];
   :>> protocol = "ELRS";
   :>> interfaceType = "CRSF";
   :>> band = "2.4 GHz";
   :>> size = "24.5x18.6 mm";
   :>> antennaType = "2x External";
   :>> telemetryPower = 0.25 [W];  // 250 mW
   :>> paLna = true;
   :>> diversityType = "True Diversity";
   :>> tcxo = true;
   :>> currentDraw = 0.2 [A];
   :>> includedWithAirframe = false;
  }

  part TBSNano : RadioReceiver {
   :>> name = "TBS Nano RX";
   :>> manufacturer = "Team BlackSheep (TBS)";
   :>> cost_USD = 24.99;
   :>> mass = 1.7 [g];
   :>> maxRange = 5.0 [km];
   :>> protocol = "TBS Crossfire (CRSF)";
   :>> interfaceType = "CRSF";
   :>> band = "900 MHz";
   :>> size = "25x14 mm";
   :>> antennaType = "1x External U.FL (900 MHz)";
   :>> telemetryPower = 0.1 [W];
   :>> paLna = true;
   :>> diversityType = "None (single)";
   :>> tcxo = false;               // N/A (not ELRS)
   :>> currentDraw = 0.125 [A];
   :>> mcu = "STM32";
   :>> rfChip = "SX1276";
   :>> includedWithAirframe = true; // KOLAS7 BNF (#2b/#2c), DeepSpace ROC7 BNF (#6b)
  }

  part TBSCrossfireNano : RadioReceiver {
   :>> name = "TBS Crossfire Nano";
   :>> manufacturer = "Team BlackSheep (TBS)";
   :>> cost_USD = 24.99;
   :>> mass = 1.7 [g];
   :>> maxRange = 5.0 [km];
   :>> protocol = "TBS Crossfire (CRSF)";
   :>> interfaceType = "CRSF";
   :>> band = "900 MHz";
   :>> size = "25x14 mm";
   :>> antennaType = "1x External U.FL (900 MHz)";
   :>> telemetryPower = 0.1 [W];
   :>> paLna = true;
   :>> diversityType = "None (single)";
   :>> tcxo = false;
   :>> currentDraw = 0.125 [A];
   :>> mcu = "STM32";
   :>> rfChip = "SX1276";
   :>> includedWithAirframe = true; // Chimera9 ECO BNF (#3b), Chimera7 Pro V2 BNF (#8b)
  }

  part GEPRC2G4Dual : RadioReceiver {
   :>> name = "GEPRC ELRS 2.4G Dual";
   :>> manufacturer = "GEPRC";
   :>> cost_USD = 19.99;
   :>> mass = 1.2 [g];
   :>> maxRange = 4.0 [km];
   :>> protocol = "ELRS";
   :>> interfaceType = "CRSF";
   :>> band = "2.4 GHz";
   :>> size = "20x14 mm";
   :>> antennaType = "2x External";
   :>> telemetryPower = 0.1 [W];
   :>> paLna = true;
   :>> diversityType = "True Diversity";
   :>> tcxo = true;
   :>> currentDraw = 0.125 [A];
   :>> mcu = "ESP8285";
   :>> rfChip = "SX1281";
   :>> includedWithAirframe = false;
  }

  part GEPRCNanoPA100 : RadioReceiver {
   :>> name = "GEPRC ELRS Nano 2.4G PA100";
   :>> manufacturer = "GEPRC";
   :>> cost_USD = 14.99;
   :>> mass = 0.7 [g];
   :>> maxRange = 3.5 [km];
   :>> protocol = "ELRS";
   :>> interfaceType = "CRSF";
   :>> band = "2.4 GHz";
   :>> size = "17x11 mm (Nano)";
   :>> antennaType = "1x External";
   :>> telemetryPower = 0.1 [W];
   :>> paLna = true;
   :>> diversityType = "None";
   :>> tcxo = true;
   :>> currentDraw = 0.11 [A];
   :>> mcu = "ESP8285";
   :>> rfChip = "SX1281";
   :>> includedWithAirframe = false;
  }

  part MatekR24D : RadioReceiver {
   :>> name = "MATEK ELRS-R24-D";
   :>> manufacturer = "MATEK";
   :>> cost_USD = 24.99;
   :>> maxRange = 4.0 [km];
   :>> protocol = "ELRS";
   :>> interfaceType = "CRSF";
   :>> band = "2.4 GHz";
   :>> antennaType = "2x External";
   :>> telemetryPower = 0.1 [W];   // est.
   :>> paLna = true;
   :>> diversityType = "True Diversity";
   :>> tcxo = true;
   :>> currentDraw = 0.125 [A];
   :>> mcu = "ESP8285";
   :>> rfChip = "SX1281";
   :>> includedWithAirframe = false;
  }
 }

 // =========================================================================
 // RADIO CONTROL TRANSMITTER CANDIDATES  (source: analysis/radio_controller_tx_market.csv)
 // =========================================================================
 package RadioControlTransmitterCandidates {

  part TX1 : RadioControlTransmitter {
   :>> name = "RadioMaster Boxer (M2) ELRS";
   :>> brand = "RadioMaster";
   :>> txType = "Integrated Controller";
   :>> formFactor = "Gamepad (full-size)";
   :>> cost_USD = 172.0;
   :>> mass = 532.5 [g];
   :>> maxRange = 10.0 [km];
   :>> internalTxPower = 1.0 [W];  // 1000 mW
   :>> frequencyBands = "2.4 GHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = true;
   :>> moduleBayType = "JR (full-size)";
   :>> firmware = "EdgeTX";
   :>> mcu = "STM32F407VGT6 (F4)";
   :>> displayType = "128x64 monochrome LCD";
   :>> dimensions = "235x178x77 mm";
   :>> batteryConfig = "2S LiPo / 2x18650 (not incl)";
   :>> batteryIncluded = false;
   :>> maxChannels = 16;
   :>> gimbalType = "V4.0 Hall effect (full-size)";
   :>> usbCCharging = true;
   :>> trainerPort = true;
   :>> sdCardSlot = true;
  }

  part TX2 : RadioControlTransmitter {
   :>> name = "RadioMaster TX16S Mark II ELRS";
   :>> brand = "RadioMaster";
   :>> txType = "Integrated Controller";
   :>> formFactor = "Full-size tray";
   :>> cost_USD = 250.0;
   :>> mass = 750.0 [g];
   :>> maxRange = 6.0 [km];        // 5-7+
   :>> internalTxPower = 0.25 [W]; // 250 mW
   :>> frequencyBands = "2.4 GHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = true;
   :>> moduleBayType = "JR (full-size)";
   :>> firmware = "EdgeTX";
   :>> mcu = "STM32F407VGT6 (F4)";
   :>> displayType = "128x64 monochrome LCD";
   :>> dimensions = "287x129x184 mm";
   :>> batteryConfig = "2S LiPo / 2x18650 (not incl)";
   :>> batteryIncluded = false;
   :>> maxChannels = 16;
   :>> gimbalType = "V4.0 Hall effect (full-size)";
   :>> usbCCharging = true;
   :>> trainerPort = true;
   :>> sdCardSlot = true;
  }

  part TX3 : RadioControlTransmitter {
   :>> name = "RadioMaster TX16S MK3 ELRS";
   :>> brand = "RadioMaster";
   :>> txType = "Integrated Controller";
   :>> formFactor = "Full-size tray";
   :>> cost_USD = 350.0;
   :>> mass = 790.0 [g];
   :>> maxRange = 10.0 [km];
   :>> internalTxPower = 1.0 [W];
   :>> frequencyBands = "2.4 GHz + 900 MHz (Gemini)";
   :>> elrsVersion = "ELRS 3.x (Gemini)";
   :>> hasExternalModuleBay = true;
   :>> moduleBayType = "JR (full-size)";
   :>> firmware = "EdgeTX";
   :>> mcu = "STM32H750 (H7)";
   :>> displayType = "128x64 OLED";
   :>> dimensions = "287x129x184 mm";
   :>> batteryConfig = "2S LiPo / 2x18650 (not incl)";
   :>> batteryIncluded = false;
   :>> maxChannels = 16;
   :>> gimbalType = "AG01 CNC Hall (full-size)";
   :>> usbCCharging = true;
   :>> trainerPort = true;
   :>> sdCardSlot = true;
  }

  part TX4 : RadioControlTransmitter {
   :>> name = "RadioMaster TX15 ELRS";
   :>> brand = "RadioMaster";
   :>> txType = "Integrated Controller";
   :>> formFactor = "Gamepad (compact)";
   :>> cost_USD = 260.0;
   :>> mass = 540.0 [g];
   :>> maxRange = 10.0 [km];
   :>> internalTxPower = 1.0 [W];
   :>> frequencyBands = "2.4 GHz + 900 MHz (LR1121)";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = true;
   :>> moduleBayType = "Nano";
   :>> firmware = "EdgeTX";
   :>> mcu = "STM32H750 (H7)";
   :>> displayType = "3.5in IPS touchscreen";
   :>> dimensions = "200x140x90 mm (est)";
   :>> batteryConfig = "2x21700 (not incl)";
   :>> batteryIncluded = false;
   :>> maxChannels = 16;
   :>> gimbalType = "AG02 CNC Hall (full-size)";
   :>> usbCCharging = true;
   :>> trainerPort = true;
   :>> sdCardSlot = true;
  }

  part TX5 : RadioControlTransmitter {
   :>> name = "RadioMaster TX12 Mark II ELRS";
   :>> brand = "RadioMaster";
   :>> txType = "Integrated Controller";
   :>> formFactor = "Compact box";
   :>> cost_USD = 130.0;
   :>> mass = 363.0 [g];
   :>> maxRange = 6.0 [km];
   :>> internalTxPower = 0.25 [W];
   :>> frequencyBands = "2.4 GHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = true;
   :>> moduleBayType = "JR (full-size)";
   :>> firmware = "EdgeTX";
   :>> mcu = "STM32F407VGT6 (F4)";
   :>> displayType = "128x64 monochrome LCD";
   :>> dimensions = "170x159x108 mm";
   :>> batteryConfig = "2S LiPo / 2x18650 (not incl)";
   :>> batteryIncluded = false;
   :>> maxChannels = 16;
   :>> gimbalType = "Hall effect (full-size)";
   :>> usbCCharging = true;
   :>> trainerPort = true;
   :>> sdCardSlot = true;
  }

  part TX6 : RadioControlTransmitter {
   :>> name = "RadioMaster Zorro ELRS";
   :>> brand = "RadioMaster";
   :>> txType = "Integrated Controller";
   :>> formFactor = "Gamepad (compact)";
   :>> cost_USD = 130.0;
   :>> mass = 350.0 [g];
   :>> maxRange = 6.0 [km];
   :>> internalTxPower = 0.25 [W];
   :>> frequencyBands = "2.4 GHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = true;
   :>> moduleBayType = "Nano";
   :>> firmware = "EdgeTX";
   :>> mcu = "STM32F407VGT6 (F4)";
   :>> displayType = "128x64 OLED";
   :>> dimensions = "170x100x70 mm (est)";
   :>> batteryConfig = "2x18650 (not incl)";
   :>> batteryIncluded = false;
   :>> maxChannels = 16;
   :>> gimbalType = "Hall effect (V3/V4)";
   :>> usbCCharging = true;
   :>> trainerPort = true;
   :>> sdCardSlot = true;
  }

  part TX7 : RadioControlTransmitter {
   :>> name = "RadioMaster Pocket ELRS";
   :>> brand = "RadioMaster";
   :>> txType = "Integrated Controller";
   :>> formFactor = "Ultra-compact gamepad";
   :>> cost_USD = 65.0;
   :>> mass = 288.0 [g];
   :>> maxRange = 3.0 [km];        // 2-4
   :>> internalTxPower = 0.1 [W];
   :>> frequencyBands = "2.4 GHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = false;
   :>> firmware = "EdgeTX";
   :>> mcu = "STM32F407VGT6 (F4)";
   :>> displayType = "128x64 monochrome LCD";
   :>> dimensions = "157x73x155 mm";
   :>> batteryConfig = "Built-in Li-ion (18650 not user-replaceable)";
   :>> batteryIncluded = true;
   :>> maxChannels = 16;
   :>> gimbalType = "Hall effect (mini)";
   :>> usbCCharging = true;
   :>> trainerPort = false;
   :>> sdCardSlot = true;
  }

  part TX8 : RadioControlTransmitter {
   :>> name = "Jumper T20 V2 ELRS";
   :>> brand = "Jumper";
   :>> txType = "Integrated Controller";
   :>> formFactor = "Compact (gamepad-ish)";
   :>> cost_USD = 150.0;
   :>> mass = 450.0 [g];
   :>> maxRange = 10.0 [km];
   :>> internalTxPower = 1.0 [W];
   :>> frequencyBands = "2.4 GHz / 915 MHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = true;
   :>> moduleBayType = "Nano";
   :>> firmware = "EdgeTX";
   :>> mcu = "STM32F407ZGT6";
   :>> displayType = "1.3in 128x64 OLED";
   :>> dimensions = "185x140x75 mm (est)";
   :>> batteryConfig = "2x21700 (not incl)";
   :>> batteryIncluded = false;
   :>> maxChannels = 16;
   :>> gimbalType = "Hall sensor";
   :>> usbCCharging = true;
   :>> trainerPort = true;
   :>> sdCardSlot = true;
  }

  part TX9 : RadioControlTransmitter {
   :>> name = "Jumper T-Pro V2 ELRS";
   :>> brand = "Jumper";
   :>> txType = "Integrated Controller";
   :>> formFactor = "Gamepad (pocket)";
   :>> cost_USD = 110.0;
   :>> mass = 488.0 [g];
   :>> maxRange = 10.0 [km];
   :>> internalTxPower = 1.0 [W];
   :>> frequencyBands = "2.4 GHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = true;
   :>> moduleBayType = "Nano";
   :>> firmware = "EdgeTX / OpenTX";
   :>> mcu = "STM32F407VGT6 (F4)";
   :>> displayType = "1.3in 128x64 OLED";
   :>> dimensions = "160x128x68 mm";
   :>> batteryConfig = "2x18650 (not incl)";
   :>> batteryIncluded = false;
   :>> maxChannels = 16;
   :>> gimbalType = "Hall sensor";
   :>> usbCCharging = true;
   :>> trainerPort = true;
   :>> sdCardSlot = true;
  }

  part TX10 : RadioControlTransmitter {
   :>> name = "BetaFPV LiteRadio 3 Pro ELRS";
   :>> brand = "BetaFPV";
   :>> txType = "Integrated Controller";
   :>> formFactor = "Gamepad (ultra-compact)";
   :>> cost_USD = 90.0;
   :>> mass = 250.0 [g];
   :>> maxRange = 6.0 [km];
   :>> internalTxPower = 0.25 [W];
   :>> frequencyBands = "2.4 GHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = true;
   :>> moduleBayType = "Nano";
   :>> firmware = "EdgeTX";
   :>> mcu = "ESP32";
   :>> displayType = "128x64 OLED";
   :>> dimensions = "145x105x60 mm (est)";
   :>> batteryConfig = "Built-in Li-ion";
   :>> batteryIncluded = true;
   :>> maxChannels = 16;
   :>> gimbalType = "Hall sensor";
   :>> usbCCharging = true;
   :>> trainerPort = false;
   :>> sdCardSlot = true;
  }

  part TXM1 : RadioControlTransmitter {
   :>> name = "RadioMaster Ranger ELRS 2.4GHz Module";
   :>> brand = "RadioMaster";
   :>> txType = "Standalone TX Module";
   :>> formFactor = "External module";
   :>> cost_USD = 70.0;
   :>> mass = 30.0 [g];
   :>> maxRange = 10.0 [km];
   :>> internalTxPower = 1.0 [W];
   :>> frequencyBands = "2.4 GHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = false;  // it IS the module
   :>> moduleBayType = "JR + Nano (adapters incl)";
   :>> dimensions = "65x45x20 mm (est)";
   :>> batteryIncluded = false;       // powered by radio
   :>> maxChannels = 16;
  }

  part TXM2 : RadioControlTransmitter {
   :>> name = "RadioMaster Ranger Micro ELRS 2.4GHz Module";
   :>> brand = "RadioMaster";
   :>> txType = "Standalone TX Module";
   :>> formFactor = "External module";
   :>> cost_USD = 50.0;
   :>> mass = 15.0 [g];
   :>> maxRange = 10.0 [km];
   :>> internalTxPower = 1.0 [W];
   :>> frequencyBands = "2.4 GHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = false;
   :>> moduleBayType = "Micro";
   :>> dimensions = "40x30x15 mm (est)";
   :>> batteryIncluded = false;
   :>> maxChannels = 16;
  }

  part TXM3 : RadioControlTransmitter {
   :>> name = "Happymodel ES24TX Pro ELRS Module";
   :>> brand = "Happymodel";
   :>> txType = "Standalone TX Module";
   :>> formFactor = "External module";
   :>> cost_USD = 45.0;
   :>> mass = 22.0 [g];
   :>> maxRange = 10.0 [km];
   :>> internalTxPower = 1.0 [W];
   :>> frequencyBands = "2.4 GHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = false;
   :>> moduleBayType = "Micro JR";
   :>> dimensions = "44x30x15 mm (est)";
   :>> batteryIncluded = false;
   :>> maxChannels = 16;
  }

  part TXM4 : RadioControlTransmitter {
   :>> name = "Happymodel ES24TX Slim Pro ELRS Module";
   :>> brand = "Happymodel";
   :>> txType = "Standalone TX Module";
   :>> formFactor = "External module";
   :>> cost_USD = 35.0;
   :>> mass = 15.0 [g];
   :>> maxRange = 6.0 [km];
   :>> internalTxPower = 0.25 [W];
   :>> frequencyBands = "2.4 GHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = false;
   :>> moduleBayType = "Slim (FrSky X-lite etc.)";
   :>> dimensions = "60x20x12 mm (est)";
   :>> batteryIncluded = false;
   :>> maxChannels = 16;
  }

  part TXM5 : RadioControlTransmitter {
   :>> name = "BetaFPV ELRS Nano TX Module";
   :>> brand = "BetaFPV";
   :>> txType = "Standalone TX Module";
   :>> formFactor = "External module";
   :>> cost_USD = 25.0;
   :>> mass = 6.0 [g];
   :>> maxRange = 6.0 [km];
   :>> internalTxPower = 0.25 [W];
   :>> frequencyBands = "2.4 GHz";
   :>> elrsVersion = "ELRS 3.x";
   :>> hasExternalModuleBay = false;
   :>> moduleBayType = "Nano";
   :>> dimensions = "25x18x10 mm (est)";
   :>> batteryIncluded = false;
   :>> maxChannels = 16;
  }
 }

 // =========================================================================
 // VIDEO TRANSMITTER (VTX) CANDIDATES  (source: analysis/vtx_candidates.csv)
 // Analog VTX only. The digital units (DJI O4/O3, Walksnail) are integrated
 // camera+VTX and are modeled in FpvCameraCandidates (D1-D3).
 // =========================================================================
 package VideoTransmitterCandidates {

  part V1 : VideoTransmitter {
   :>> name = "BLITZ Whoop 1.6W";
   :>> vtxType = "Analog VTX";
   :>> cost_USD = 30.0;
   :>> mass = 18.9 [g];
   :>> power = 4.5 [W];            // at 1.6W output
   :>> maxRange = 4.0 [km];        // 3-5
   :>> protocolControl = "IRC Tramp";
   :>> frequencyBand = "5.8 GHz";
   :>> outputPowerLevels = "25 / 400 / 800 / 1600 mW";
   :>> maxOutputPower = 1.6 [W];
   :>> inputVoltageMin = 7.0 [V];
   :>> inputVoltageMax = 34.0 [V];
   :>> antennaConnector = "MMCX";
   :>> mountingPattern = "30.5x30.5mm";
   :>> audio = "Built-in mic";
   :>> channelCount = 48;
   :>> pitMode = true;
   :>> includedWithAirframe = true; // Chimera9 ECO (#3), Chimera7 Pro V2 (#8)
  }

  part V2 : VideoTransmitter {
   :>> name = "BLITZ Whoop 2.5W";
   :>> vtxType = "Analog VTX";
   :>> cost_USD = 40.0;
   :>> mass = 20.0 [g];
   :>> power = 7.0 [W];
   :>> maxRange = 6.5 [km];        // 5-8
   :>> protocolControl = "IRC Tramp";
   :>> frequencyBand = "5.8 GHz";
   :>> outputPowerLevels = "25 / 400 / 800 / 1600 / 2500 mW";
   :>> maxOutputPower = 2.5 [W];
   :>> inputVoltageMin = 7.0 [V];
   :>> inputVoltageMax = 34.0 [V];
   :>> antennaConnector = "MMCX";
   :>> mountingPattern = "30.5x30.5mm";
   :>> audio = "Built-in mic";
   :>> channelCount = 48;
   :>> pitMode = true;
   :>> includedWithAirframe = true;
  }

  part V3 : VideoTransmitter {
   :>> name = "GEPRC RAD 1.6W";
   :>> vtxType = "Analog VTX";
   :>> cost_USD = 25.0;
   :>> mass = 16.0 [g];
   :>> power = 4.5 [W];
   :>> maxRange = 4.0 [km];
   :>> protocolControl = "IRC Tramp";
   :>> frequencyBand = "5.8 GHz";
   :>> outputPowerLevels = "25 / 400 / 800 / 1600 mW";
   :>> maxOutputPower = 1.6 [W];
   :>> inputVoltageMin = 7.0 [V];
   :>> inputVoltageMax = 26.0 [V];
   :>> antennaConnector = "MMCX";
   :>> mountingPattern = "30.5x30.5mm";
   :>> channelCount = 48;
   :>> pitMode = true;
   :>> includedWithAirframe = true; // MARK4 LR7 (#1), Crocodile75 V3 (#7)
  }

  part V4 : VideoTransmitter {
   :>> name = "EMAX 2.5W VTX";
   :>> vtxType = "Analog VTX";
   :>> cost_USD = 25.0;
   :>> mass = 20.0 [g];
   :>> power = 7.0 [W];
   :>> maxRange = 6.5 [km];
   :>> protocolControl = "IRC Tramp (likely)";
   :>> frequencyBand = "5.8 GHz";
   :>> outputPowerLevels = "25 / 400 / 800 / 1600 / 2500 mW (est)";
   :>> maxOutputPower = 2.5 [W];
   :>> inputVoltageMin = 7.0 [V];
   :>> inputVoltageMax = 26.0 [V];
   :>> antennaConnector = "MMCX";
   :>> mountingPattern = "30.5x30.5mm (est)";
   :>> channelCount = 48;
   :>> pitMode = true;
   :>> includedWithAirframe = true; // EMAX Hawk 7 (#5)
  }

  part V5 : VideoTransmitter {
   :>> name = "RushFPV Tank SOLO 1W";
   :>> vtxType = "Analog VTX";
   :>> cost_USD = 30.0;
   :>> mass = 12.0 [g];
   :>> power = 3.5 [W];
   :>> maxRange = 4.0 [km];
   :>> protocolControl = "SmartAudio";
   :>> frequencyBand = "5.8 GHz";
   :>> outputPowerLevels = "25 / 400 / 600 / 800 / 1000 mW";
   :>> maxOutputPower = 1.0 [W];
   :>> inputVoltageMin = 7.0 [V];
   :>> inputVoltageMax = 36.0 [V];
   :>> antennaConnector = "MMCX";
   :>> mountingPattern = "37x24mm (no standard stack holes)";
   :>> audio = "Built-in AGC mic";
   :>> channelCount = 48;
   :>> pitMode = true;
   :>> includedWithAirframe = false;
  }

  part V6 : VideoTransmitter {
   :>> name = "RushFPV Tank MAX SOLO 2.5W";
   :>> vtxType = "Analog VTX";
   :>> cost_USD = 67.0;            // 50-85
   :>> mass = 15.0 [g];
   :>> power = 7.0 [W];
   :>> maxRange = 8.0 [km];        // 6-10
   :>> protocolControl = "SmartAudio";
   :>> frequencyBand = "5.8 GHz";
   :>> outputPowerLevels = "25 / 500 / 1000 / 2500 mW";
   :>> maxOutputPower = 2.5 [W];
   :>> inputVoltageMin = 7.0 [V];
   :>> inputVoltageMax = 36.0 [V];
   :>> antennaConnector = "MMCX";
   :>> mountingPattern = "40x24x10.5mm";
   :>> audio = "Built-in AGC mic";
   :>> channelCount = 48;
   :>> pitMode = true;
   :>> includedWithAirframe = false;
  }

  part V7 : VideoTransmitter {
   :>> name = "HGLRC Zeus 1.6W VTX PRO";
   :>> vtxType = "Analog VTX";
   :>> cost_USD = 48.0;            // 42-55
   :>> mass = 13.0 [g];
   :>> power = 4.0 [W];
   :>> maxRange = 5.0 [km];        // 4-6
   :>> protocolControl = "IRC Tramp";
   :>> frequencyBand = "5.8 GHz";
   :>> outputPowerLevels = "25 / 400 / 800 / 1600 mW";
   :>> maxOutputPower = 1.6 [W];
   :>> inputVoltageMin = 7.0 [V];
   :>> inputVoltageMax = 36.0 [V];
   :>> antennaConnector = "MMCX";
   :>> mountingPattern = "20x20mm M2";
   :>> audio = "Built-in mic";
   :>> channelCount = 48;
   :>> pitMode = true;
   :>> includedWithAirframe = false;
  }

  part V8 : VideoTransmitter {
   :>> name = "AKK X2-Ultimate 1W";
   :>> vtxType = "Analog VTX";
   :>> cost_USD = 35.0;            // 30-40
   :>> mass = 6.8 [g];
   :>> power = 3.5 [W];
   :>> maxRange = 4.0 [km];
   :>> protocolControl = "SmartAudio";
   :>> frequencyBand = "5.8 GHz";
   :>> outputPowerLevels = "25 / 200 / 600 / 1000 mW";
   :>> maxOutputPower = 1.0 [W];
   :>> inputVoltageMin = 7.0 [V];
   :>> inputVoltageMax = 26.0 [V];
   :>> antennaConnector = "MMCX";
   :>> mountingPattern = "32x22mm";
   :>> audio = "No mic";
   :>> channelCount = 37;          // US
   :>> pitMode = true;
   :>> includedWithAirframe = false;
  }

  part V10 : VideoTransmitter {
   :>> name = "AKK A1918 1W";
   :>> vtxType = "Analog VTX";
   :>> cost_USD = 27.0;            // 25-30
   :>> mass = 9.6 [g];
   :>> power = 4.0 [W];
   :>> maxRange = 4.0 [km];
   :>> protocolControl = "SmartAudio";
   :>> frequencyBand = "5.8 GHz";
   :>> outputPowerLevels = "200 / 400 / 800 / 1000 mW";
   :>> maxOutputPower = 1.0 [W];
   :>> inputVoltageMin = 7.0 [V];
   :>> inputVoltageMax = 28.0 [V];
   :>> antennaConnector = "MMCX";
   :>> mountingPattern = "36x36mm / 30.5x30.5mm holes";
   :>> audio = "Built-in mic";
   :>> channelCount = 40;          // US
   :>> pitMode = true;
   :>> includedWithAirframe = false;
  }

  part V11 : VideoTransmitter {
   :>> name = "SoloGood TS582000 2W";
   :>> vtxType = "Analog VTX";
   :>> cost_USD = 30.0;            // 25-35
   :>> mass = 30.0 [g];
   :>> power = 9.6 [W];            // 12V testing
   :>> maxRange = 7.0 [km];        // 5-10+
   :>> protocolControl = "None (button only)";
   :>> frequencyBand = "5.8 GHz";
   :>> outputPowerLevels = "2000 mW (fixed/8-channel)";
   :>> maxOutputPower = 2.0 [W];
   :>> inputVoltageMin = 8.0 [V];
   :>> inputVoltageMax = 25.0 [V];
   :>> antennaConnector = "SMA (female)";
   :>> mountingPattern = "Standalone board ~50x30mm";
   :>> audio = "Audio in (AV sync)";
   :>> channelCount = 8;
   :>> pitMode = false;
   :>> includedWithAirframe = false;
  }
 }

 // =========================================================================
 // VIDEO RECEIVER (VRX, ground) CANDIDATES  (source: analysis/vtx_receive_candidates.csv)
 // =========================================================================
 package VideoReceiverCandidates {

  part VRX1 : VideoReceiver {
   :>> name = "Standard Analog VRX + USB Capture Dongle";
   :>> vrxType = "Separate stack (VRX + capture)";
   :>> cost_USD = 40.0;            // 15-60
   :>> inputFrequency = "5.8 GHz";
   :>> outputToLaptop = "USB via UVC capture";
   :>> antenna = "RPSMA";
   :>> range = 2.8 [km];           // with proper VRX + patch antenna
   :>> diversity = "Optional";
   :>> includedWithAirframe = false;
  }

  part VRX3 : VideoReceiver {
   :>> name = "Flying Tech USB-C Analog FPV Capture Adapter";
   :>> vrxType = "Capture dongle only";
   :>> cost_USD = 17.0;            // 15-20
   :>> inputFrequency = "N/A (AV input)";
   :>> outputToLaptop = "USB-C (UVC)";
   :>> diversity = "N/A";
   :>> macOsCompatible = true;
   :>> includedWithAirframe = false;
  }

  part VRX4 : VideoReceiver {
   :>> name = "Generic AV-to-USB Capture Card (ATCCPYDM)";
   :>> vrxType = "Capture dongle only";
   :>> cost_USD = 13.0;            // 10-16
   :>> inputFrequency = "N/A (AV input)";
   :>> outputToLaptop = "USB-A (UVC)";
   :>> diversity = "N/A";
   :>> macOsCompatible = true;
   :>> includedWithAirframe = false;
  }

  part VRX5 : VideoReceiver {
   :>> name = "CVBS/AV to USB Module Board (bare PCB)";
   :>> vrxType = "Capture dongle only";
   :>> cost_USD = 11.0;            // 7-15
   :>> inputFrequency = "N/A (AV input)";
   :>> outputToLaptop = "USB-A (UVC)";
   :>> diversity = "N/A";
   :>> macOsCompatible = true;
   :>> includedWithAirframe = false;
  }
 }

 // =========================================================================
 // USB VIDEO CAPTURE CANDIDATES  (source: analysis/usb_video_capture_candidates.csv)
 // =========================================================================
 package UsbVideoCaptureCandidates {

  part VC1 : UsbVideoCapture {
   :>> name = "Flying Tech USB-C Analog FPV Capture Adapter";
   :>> captureType = "USB Capture Adapter";
   :>> cost_USD = 17.0;            // 15-20
   :>> inputType = "RCA composite (CVBS)";
   :>> outputUsb = "USB-C";
   :>> protocol = "UVC 1.0";
   :>> maxResolution = "1080p (MJPEG)";
   :>> frameRate_fps = 30.0;
   :>> macOsCompatible = true;
   :>> driverlessUVC = true;
   :>> busPowered = true;
  }

  part VC2 : UsbVideoCapture {
   :>> name = "CVBS/AV to USB Module Board";
   :>> captureType = "USB Capture Module (bare PCB)";
   :>> cost_USD = 11.0;            // 7-15
   :>> inputType = "CVBS (pin header)";
   :>> outputUsb = "USB-A";
   :>> protocol = "UVC 1.0";
   :>> maxResolution = "1080p (MJPEG)";
   :>> frameRate_fps = 30.0;
   :>> macOsCompatible = true;
   :>> driverlessUVC = true;
   :>> busPowered = true;
  }

  part VC3 : UsbVideoCapture {
   :>> name = "ATCCPYDM / Generic AV-to-USB Capture Card";
   :>> captureType = "USB Capture Card";
   :>> cost_USD = 13.0;            // 10-16
   :>> inputType = "RCA composite (female jack)";
   :>> outputUsb = "USB-A";
   :>> protocol = "UVC 1.0";
   :>> maxResolution = "1080p (MJPEG)";
   :>> frameRate_fps = 30.0;
   :>> macOsCompatible = true;
   :>> driverlessUVC = true;
   :>> busPowered = true;
  }

  part VC4 : UsbVideoCapture {
   :>> name = "EasyCAP USB 2.0";
   :>> captureType = "USB Capture Adapter";
   :>> cost_USD = 13.0;            // 11-15
   :>> inputType = "RCA / S-Video";
   :>> outputUsb = "USB-A";
   :>> protocol = "Proprietary (not UVC)";
   :>> maxResolution = "480p";
   :>> frameRate_fps = 30.0;
   :>> macOsCompatible = false;    // partial / driver issues on modern macOS
   :>> driverlessUVC = false;
   :>> busPowered = true;
  }

  part VC5 : UsbVideoCapture {
   :>> name = "Magewell USB Capture HDMI";
   :>> captureType = "USB Capture Dongle";
   :>> cost_USD = 225.0;           // 150-300
   :>> inputType = "HDMI";
   :>> outputUsb = "USB-C";
   :>> protocol = "UVC 1.0";
   :>> maxResolution = "1080p";
   :>> frameRate_fps = 60.0;
   :>> macOsCompatible = true;
   :>> driverlessUVC = true;
   :>> busPowered = true;
  }
 }

 // =========================================================================
 // THERMAL VIDEO RECORDER (inline DVR) CANDIDATES  (source: analysis/thermal_dvr_candidates.csv)
 // =========================================================================
 package ThermalVideoRecorderCandidates {

  part DVR1 : ThermalVideoRecorder {
   :>> name = "RunCam Mini FPV DVR (RUNCAM-DVR-S)";
   :>> cost_USD = 17.99;           // 29.99 at Amazon
   :>> mass = 3.5 [g];
   :>> power = 1.3 [W];
   :>> storageCapacity = 32.0;
   :>> recordingFormat = "MJPEG / AVI";
   :>> dimensions = "25x25x6 mm (est)";
   :>> mountPattern = "20x20mm M2";
   :>> inputVoltageMin = 3.3 [V];
   :>> inputVoltageMax = 5.5 [V];
   :>> currentMax = 0.25 [A];      // 250 mA
   :>> videoInput = "CVBS analog";
   :>> inputPortType = "Solder pads (1.0mm pitch)";
   :>> videoPassThrough = true;
   :>> passThroughMethod = "Direct solder: Camera V_OUT -> DVR V_IN / DVR V_OUT -> VTX V_IN";
   :>> maxResolution = "720x480 (D1)";
   :>> frameRate_fps = 30.0;
   :>> storageType = "microSD";
   :>> audioRecording = true;
   :>> startStopControl = "Via flight controller GPIO (SpeedyBee App)";
  }

  part DVR2 : ThermalVideoRecorder {
   :>> name = "Eachine EV100 Micro AV Recorder";
   :>> cost_USD = 16.14;
   :>> mass = 9.0 [g];
   :>> power = 1.2 [W];
   :>> storageCapacity = 32.0;
   :>> recordingFormat = "AVI (MJPEG)";
   :>> dimensions = "38.5x30.8x12.5 mm";
   :>> mountPattern = "N/A (double-sided tape)";
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 7.4 [V];  // 2S
   :>> currentMax = 0.24 [A];      // 240 mA
   :>> videoInput = "CVBS analog";
   :>> inputPortType = "3.5mm TRRS AV jack + JST-SH 1.0mm";
   :>> videoPassThrough = true;
   :>> passThroughMethod = "Included A/V cable splits to RCA; internal pass-through circuit";
   :>> maxResolution = "1280x480 (HD)";
   :>> frameRate_fps = 30.0;
   :>> storageType = "TF/microSD";
   :>> audioRecording = true;
   :>> startStopControl = "Push-button (on module)";
  }

  part DVR3 : ThermalVideoRecorder {
   :>> name = "Eachine ProDVR";
   :>> cost_USD = 16.46;
   :>> mass = 9.9 [g];
   :>> power = 1.0 [W];
   :>> storageCapacity = 32.0;
   :>> recordingFormat = "AVI (MJPEG)";
   :>> dimensions = "41x32.9x9 mm";
   :>> mountPattern = "N/A (adhesive included)";
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 5.0 [V];
   :>> currentMax = 0.2 [A];       // ~200 mA
   :>> videoInput = "CVBS analog";
   :>> inputPortType = "JST-SH 1.0mm 5-pin + solder pad backup";
   :>> videoPassThrough = true;
   :>> passThroughMethod = "Breakout cable: Video In/Out/Audio/Power; internal pass-through";
   :>> maxResolution = "1280x480 (HD)";
   :>> frameRate_fps = 30.0;
   :>> storageType = "TF/microSD";
   :>> audioRecording = true;
   :>> startStopControl = "Push-button (on module)";
  }

  part DVR4 : ThermalVideoRecorder {
   :>> name = "Generic Mini FPV DVR (Aluminum Case)";
   :>> cost_USD = 14.99;
   :>> mass = 12.0 [g];
   :>> power = 1.3 [W];
   :>> storageCapacity = 32.0;
   :>> recordingFormat = "MJPEG / AVI";
   :>> dimensions = "40x30x15 mm (est)";
   :>> mountPattern = "N/A (adhesive)";
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 8.4 [V];
   :>> currentMax = 0.25 [A];
   :>> videoInput = "CVBS analog";
   :>> inputPortType = "Pigtail leads (pre-wired)";
   :>> videoPassThrough = true;
   :>> passThroughMethod = "Pre-wired pigtails: Camera V_OUT -> V_IN lead; V_OUT lead -> VTX";
   :>> maxResolution = "1280x480 (HD)";
   :>> frameRate_fps = 30.0;
   :>> storageType = "TF/microSD";
   :>> audioRecording = true;
   :>> startStopControl = "Push-button";
  }

  part DVR5 : ThermalVideoRecorder {
   :>> name = "Generic Mini FPV DVR (eBay)";
   :>> cost_USD = 11.99;
   :>> mass = 9.0 [g];
   :>> power = 1.2 [W];
   :>> storageCapacity = 32.0;     // includes 32GB TF card
   :>> recordingFormat = "MJPEG";
   :>> dimensions = "38x30x12 mm (est)";
   :>> mountPattern = "N/A (adhesive)";
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 5.0 [V];
   :>> currentMax = 0.24 [A];
   :>> videoInput = "CVBS analog";
   :>> inputPortType = "Pigtail leads (pre-wired)";
   :>> videoPassThrough = true;
   :>> passThroughMethod = "Pre-wired pigtails: Camera V_OUT -> V_IN; V_OUT -> VTX";
   :>> maxResolution = "1280x480 (HD)";
   :>> frameRate_fps = 30.0;
   :>> storageType = "TF/microSD";
   :>> audioRecording = true;
   :>> startStopControl = "Remote button included";
  }

  part DVR6 : ThermalVideoRecorder {
   :>> name = "Generic Mini FPV DVR (no card)";
   :>> cost_USD = 8.99;
   :>> mass = 8.0 [g];
   :>> power = 1.1 [W];
   :>> storageCapacity = 32.0;     // max supported (no card included)
   :>> recordingFormat = "MJPEG";
   :>> dimensions = "38x30x12 mm (est)";
   :>> mountPattern = "N/A (adhesive)";
   :>> inputVoltageMin = 5.0 [V];
   :>> inputVoltageMax = 5.0 [V];
   :>> currentMax = 0.22 [A];
   :>> videoInput = "CVBS analog";
   :>> inputPortType = "Pigtail leads (pre-wired)";
   :>> videoPassThrough = true;
   :>> passThroughMethod = "Pre-wired pigtails: Camera V_OUT -> V_IN; V_OUT -> VTX";
   :>> maxResolution = "1280x480 (HD)";
   :>> frameRate_fps = 30.0;
   :>> storageType = "TF/microSD";
   :>> audioRecording = true;
   :>> startStopControl = "Push-button";
  }
 }

 // =========================================================================
 // GROUND TELEMETRY LINK CANDIDATES  (source: analysis/telemetry_rx_candidates.csv)
 // =========================================================================
 package TelemetryGroundLinkCandidates {

  part TLM1 : TelemetryGroundLink {
   :>> name = "EdgeTX Radio USB Passthrough";
   :>> approach = "Radio USB serial";
   :>> connectionToLaptop = "USB-C (virtual COM port)";
   :>> frequency = "2.4 GHz / 900 MHz";
   :>> rangeAt2_8kmOk = true;
   :>> macOsCompatible = true;
   :>> cost_USD = 0.0;             // uses the RC radio itself
   :>> extraHardwareNeeded = "None";
  }

  part TLM2 : TelemetryGroundLink {
   :>> name = "HGLRC Hermes ELRS SIM USB Dongle";
   :>> approach = "Standalone ELRS RX USB dongle";
   :>> connectionToLaptop = "USB-A (serial)";
   :>> frequency = "2.4 GHz";
   :>> rangeAt2_8kmOk = true;
   :>> macOsCompatible = true;
   :>> cost_USD = 16.0;            // 14-18
   :>> extraHardwareNeeded = "None";
  }

  part TLM3 : TelemetryGroundLink {
   :>> name = "CubeFPV USB ELRS Dongle";
   :>> approach = "Standalone ELRS RX USB dongle";
   :>> connectionToLaptop = "USB (serial)";
   :>> frequency = "2.4 GHz";
   :>> rangeAt2_8kmOk = true;
   :>> macOsCompatible = true;
   :>> cost_USD = 17.0;            // 15-20
   :>> extraHardwareNeeded = "None";
  }

  part TLM4 : TelemetryGroundLink {
   :>> name = "DIY ESP32 Dev Board + ELRS RX";
   :>> approach = "DIY ESP32 + RX module";
   :>> connectionToLaptop = "USB (serial)";
   :>> frequency = "2.4 GHz";
   :>> rangeAt2_8kmOk = true;
   :>> macOsCompatible = true;
   :>> cost_USD = 12.0;            // 10-15 (violates R5: DIY soldering)
   :>> extraHardwareNeeded = "ELRS RX module (~$5-10)";
  }

  part TLM5 : TelemetryGroundLink {
   :>> name = "RadioMaster Ranger Module + AirPort";
   :>> approach = "External TX module direct USB (AirPort firmware)";
   :>> connectionToLaptop = "USB (serial / AirPort firmware)";
   :>> frequency = "2.4 GHz";
   :>> rangeAt2_8kmOk = true;
   :>> macOsCompatible = true;
   :>> cost_USD = 70.0;
   :>> extraHardwareNeeded = "2nd ELRS RX on drone (~$15-25); different band for RC";
  }
 }
}
// End of the DroneCandidates library. See MODEL_ISSUES.md for data gaps.
