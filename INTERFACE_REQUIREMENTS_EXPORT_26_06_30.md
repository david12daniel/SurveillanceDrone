# Interface Requirements Specification (IRS) — Thermal Surveillance Drone

*Content structured in alignment with **DI-IPSC-81434** (Interface Requirements Specification).*
*Generated export — 2026-06-30. Source of truth: [`model.sysml`](model.sysml) `DroneSystemModel::Architecture` (`Compatibility` sub-package + the `SurveillanceDrone` / `AerialThermalObservationSystem` connections).*

---

## 1. Scope

### 1.1 Identification
This IRS specifies the interfaces of the **Thermal Surveillance Drone System** — the
electrical-power, video, RF, and serial-data interfaces among the airborne components and
between the drone, the ground control station (GCS), and the operator's laptop.

### 1.2 System overview
See the companion **[SSS](REQUIREMENTS_EXPORT_26_06_30.md)** §1.2. The system's interfaces
are formalized in the model's `Compatibility` package as typed `port def`s, `enum def`s,
`constraint def`s, and `interface def`s, and instantiated as `interface`/`connection connect`
bindings in `SurveillanceDrone` and `AerialThermalObservationSystem`. Three compatibility
rules are machine-checked by the trade-study sweep:
- **BatteryVoltageCompatible (P1)** — `batteryCells ∈ [afMinCells, afMaxCells]`
- **VideoFormatCompatible (V)** — `source.format == sink.format`
- **RfBandCompatible (R)** — `source.band == sink.band`

### 1.3 Document overview
§3.1 identifies all interfaces; §3.2 specifies each (priority, type, data elements/assemblies,
communication method, protocol, physical & other characteristics, the governing compatibility
rule, the model binding, and traceability). §4 gives qualification; §5 traceability to the SSS.

---

## 2. Referenced documents

| Ref | Document |
|---|---|
| [`model.sysml`](model.sysml) | `Architecture::Compatibility` + system connections (authoritative) |
| [`REQUIREMENTS_EXPORT_26_06_30.md`](REQUIREMENTS_EXPORT_26_06_30.md) | System/Subsystem Specification (SSS) |
| [`SELECTED_COMPONENTS.md`](SELECTED_COMPONENTS.md) | Selected components (define the concrete endpoints) |
| [`analysis/flight_time_model.py`](analysis/flight_time_model.py) | Executes P1/V/R compatibility filtering across candidates |
| DI-IPSC-81434 | DID content template this export aligns to |

---

## 3. Interface requirements

### 3.1 Interface identification and diagrams

| ID | Interface | From → To | Model `interface`/`connect` | Type | Compat rule |
|---|---|---|---|---|---|
| **IF-PWR-01** | Battery → Airframe DC power | `battery.power_out` → `platform.power_battery` | `batteryPwr : BatteryPowerInterface` | Electrical power | P1 cell-count |
| **IF-PWR-02** | Airframe → payload regulated power | `platform.power_tp/power_sbc` → payload `power_in` | `interface connect` (×7) | Electrical power | — |
| **IF-VID-01** | Thermal camera → DVR (record) | `camera.video_out` → `recorder.video_in` | `camToRec : VideoLink` | Video | V format |
| **IF-VID-02** | Thermal camera → SBC (inference) | `camera.video_out` → `sbc.video_in` | `camToSbc : VideoLink` | Video | V format |
| **IF-VID-03** | FPV camera → VTX (pilot) | `fpvCam.video_out` → `vtx.video_in` | `fpvToVtx : VideoLink` | Video | V format |
| **IF-VID-04** | DVR → VTX (pass-through) | `recorder.video_out` → `vtx.video_in` | `recToVtx : VideoLink` | Video | V format |
| **IF-RF-01** | Drone VTX → GCS VRX (video downlink) | `drone.vtx.rf_out` → `gcs.videoRx.rf_in` | `connection connect` | Wireless RF | R band |
| **IF-RF-02** | GCS ELRS ↔ Drone RX (control + telemetry) | `gcs.laptopLink.rf_out` ↔ `drone.rx.rf_in` (backup `gcs.rcTx.rf_out`) | `connection connect` | Wireless RF (bidir) | R band |
| **IF-DAT-01** | GPS → Flight controller | `gps.data_out` → `platform.data_sbc` | `interface connect` | Serial data | — |
| **IF-DAT-02** | SBC ↔ Flight controller | `sbc.data_af` → `platform.data_sbc` | `interface connect` | Serial data | — |
| **IF-DAT-03** | RX ↔ Flight controller (control + telemetry) | `rx.control_signal_out`→`platform.control_input`; `rx.telemetry_data_in`→`platform.telemetry_data_out` | `interface connect` (×2) | Serial data | — |
| **IF-GND-01** | GCS VRX → capture → Laptop (video) | `videoRx.video_out`→`capture.video_in`→`displayComputer.video_in` | `connect` + `connection connect` | Video → USB | — |
| **IF-GND-02** | GCS ELRS dongle → Laptop (control + telemetry) | `gcs.laptopLink.usb_out` → `displayComputer.user_interface` | `connection connect` | USB serial | — |

```
                         AIRBORNE (SurveillanceDrone)                     GROUND
  Battery --IF-PWR-01(P1)--> Airframe/FC/ESC
     |                          |  --IF-PWR-02--> camera, SBC, GPS, RX, VTX, DVR, FPVcam
  Thermal cam --IF-VID-01--> DVR --IF-VID-04--> VTX --IF-RF-01(5.8GHz)--> VRX --IF-GND-01(USB)--> Laptop
     \--IF-VID-02--> SBC                          ^                                                  (GCS)
  FPV cam --IF-VID-03------------------------------|
  GPS --IF-DAT-01--> FC                          ELRS RX <--IF-RF-02(2.4GHz)--> ELRS dongle --IF-GND-02(USB)--> Laptop
  SBC <--IF-DAT-02--> FC                              ^------(backup)------ handheld radio
  ELRS RX <--IF-DAT-03--> FC
```

### 3.2 Interface specifications

Each interface below is specified per DI-IPSC-81434 §3.2: **priority · type · data elements ·
data assemblies · communication method · protocol · physical & other characteristics ·
compatibility rule · traceability**.

#### 3.2.1 Power interfaces

**IF-PWR-01 — Battery → Airframe DC power**
- **Priority:** Critical. **Type:** Unregulated DC electrical power.
- **Data elements / assemblies:** None (raw DC); parameters = pack nominal voltage, instantaneous current.
- **Communication method:** Direct wired DC; main discharge leads.
- **Protocol:** None.
- **Physical & other:** XT60/XT90 connector; series-cell count must lie within the airframe ESC/motor window (4S–8S class); battery must physically fit the mounting bay/strap (envelope `length/width/height_mm`). Continuous discharge per **R4_BAT_DISCHARGE** without ESC LVC.
- **Compatibility rule (P1):** `BatteryVoltageCompatible` — `battery.cells_s ∈ [airframe.minCells_s, airframe.maxCells_s]`. Ports: `PowerSourcePort{cells_s}` → `PowerSinkPort{minCells_s,maxCells_s}`.
- **Traceability:** R4_BAT_VOLT, R4_BAT_IF, R4_AF_PWR_DIST.

**IF-PWR-02 — Airframe → payload regulated power**
- **Priority:** Critical. **Type:** Regulated DC electrical power (rails).
- **Data elements/assemblies:** None; parameters = rail voltages (5 V BEC; 9/12 V as required), per-rail current budget.
- **Communication method:** Airframe power-distribution board (PDB) → component `power_in` leads.
- **Protocol:** None.
- **Physical & other:** Regulated rails to camera, SBC, GPS, RX, VTX, DVR; unfiltered battery voltage to ESCs. Pre-soldered/plug-in preferred (**R5/R4_AF_ASSY**).
- **Traceability:** R4_AF_PWR_DIST (and payload power budgets R3_CAM_PWR, R4_SBC_PWR).

#### 3.2.2 Video interfaces (rule V: `VideoFormatCompatible`, `VideoFormat ∈ {CVBS, USB_UVC, MIPI_CSI, HDMI, DJI_DIGITAL, HDZERO, WALKSNAIL}`)

**IF-VID-01 — Thermal camera → DVR (record)**
- **Priority:** High (Phase 3). **Type:** Real-time video stream.
- **Data elements:** Thermal video frames (LWIR 640×512 @ 25 Hz for the selected Mini 640).
- **Data assemblies:** Continuous composite/serial video signal.
- **Communication method:** Wired video out → DVR video in. **Protocol:** CVBS (analog) or USB-UVC (digital), per camera output.
- **Physical & other:** Coax/RCA (CVBS) or USB; recorded to microSD. **Compatibility rule:** source.format == sink.format.
- **Traceability:** R3_CAM_IF.

**IF-VID-02 — Thermal camera → SBC (inference)**
- **Priority:** High (Phase 4). **Type:** Real-time video stream.
- **Data elements:** Thermal frames (640×512 @ 25 Hz). **Data assemblies:** UVC/CSI frame stream.
- **Communication method:** Wired camera out → SBC video in. **Protocol:** USB-UVC (selected Mini 640 = USB) or MIPI-CSI.
- **Physical & other:** USB-C / CSI ribbon; ≥ ~25 fps to satisfy the live-processing chain. **Rule:** format match.
- **Traceability:** R4_SBC_VIDEO_IN, R4_SBC_VIDEO_PROC, R3_CAM_IF.

**IF-VID-03 — FPV camera → VTX (pilot)**
- **Priority:** High (Phase 2). **Type:** Real-time video stream.
- **Data elements:** Pilot FPV video frames. **Data assemblies:** Composite analog video.
- **Communication method:** Wired cam → VTX. **Protocol:** CVBS analog (or integrated digital cam+VTX).
- **Physical & other:** Coax pigtail; format must match the VTX input. **Rule:** format match.
- **Traceability:** R3_CAM_IF (piloting path).

**IF-VID-04 — DVR → VTX (pass-through)**
- **Priority:** Medium (Phase 3). **Type:** Real-time video stream (pass-through).
- **Data elements/assemblies:** Thermal video (post-DVR) to the downlink. **Protocol:** CVBS pass-through.
- **Communication method:** DVR video-out → VTX video-in. **Rule:** format match.
- **Traceability:** R3_CAM_IF.

#### 3.2.3 Wireless RF link interfaces (rule R: `RfBandCompatible`, `RfBand ∈ {GHZ_5_8, GHZ_2_4, MHZ_900}`)

**IF-RF-01 — Drone VTX → GCS VRX (video downlink)**
- **Priority:** Critical. **Type:** One-way wireless RF video downlink.
- **Data elements:** Live video (thermal/FPV). **Data assemblies:** Modulated RF video carrier.
- **Communication method:** Free-space RF; VTX antenna → VRX antenna (→ USB capture, see IF-GND-01).
- **Protocol:** Analog 5.8 GHz FM (selected baseline), or digital (DJI / Walksnail) per airframe VTX. The ground receiver is matched to the VTX video standard.
- **Physical & other:** 5.8 GHz band; MMCX/RP-SMA antennas; selectable 25–2500 mW; **reliable to ≥ 2800 m LOS**. **Compatibility rule:** VTX band == VRX band. Ports: `RfSourcePort{band}` → `RfSinkPort{band}`.
- **Traceability:** R4_GCS_VIDEO_DISP, R4_GCS_IF, R4_GCS_RANGE (⊆R7).

**IF-RF-02 — GCS ELRS ↔ Drone RX (control + telemetry)**
- **Priority:** Critical. **Type:** Bidirectional wireless RF (RC control uplink + telemetry downlink over one link).
- **Data elements:** RC channels (throttle, roll, pitch, yaw, arming, flight mode); telemetry (altitude, position, battery voltage, heading, speed, mode).
- **Data assemblies:** CRSF packets (channel frame uplink; telemetry frames downlink).
- **Communication method:** Free-space RF, single ELRS link (eliminates a separate telemetry radio). Primary = laptop ELRS dongle; backup = handheld ELRS radio.
- **Protocol:** ExpressLRS (LoRa-based) carrying CRSF; 2.4 GHz (900 MHz capable).
- **Physical & other:** 2.4 GHz band; **reliable to ≥ 2800 m LOS**; low latency for safe manual control. **Compatibility rule:** RX band == TX band.
- **Traceability:** R4_GCS_CTRL, R4_GCS_TELEM, R4_GCS_RANGE (⊆R7), R4_GCS_IF.

#### 3.2.4 Onboard serial-data interfaces

**IF-DAT-01 — GPS → Flight controller**
- **Priority:** High. **Type:** One-way serial data (sensor).
- **Data elements:** Latitude, longitude, altitude, ground velocity, heading, time, fix quality, satellite count.
- **Data assemblies:** NMEA-0183 sentences / u-blox UBX messages. **Protocol:** UART TTL (NMEA/UBX), typ. 9600–115200 baud.
- **Physical & other:** 3.3 V UART (+ optional I²C compass); JST-GH/solder. Enables nav at R1/R2.
- **Traceability:** R1, R2 (navigation); model: `gps.data_out → platform.data_sbc`.

**IF-DAT-02 — SBC ↔ Flight controller**
- **Priority:** High (Phase 4). **Type:** Bidirectional serial data.
- **Data elements:** Detection/classification results; route/mission commands; vehicle state/status.
- **Data assemblies:** MAVLink messages. **Protocol:** UART TTL (MAVLink), typ. 115200–921600 baud (FC TELEM port).
- **Physical & other:** 3.3 V UART; autonomous route modification at Phase 4.
- **Traceability:** R4_SBC_DATA_AF.

**IF-DAT-03 — RX ↔ Flight controller (control + telemetry)**
- **Priority:** Critical. **Type:** Bidirectional serial data (control + telemetry).
- **Data elements:** RC channels (to FC); telemetry (from FC). **Data assemblies:** CRSF frames.
- **Communication method:** Wired RX↔FC. **Protocol:** CRSF over UART (typ. 416 kbaud).
- **Physical & other:** 5 V power + UART; the airborne end of IF-RF-02.
- **Traceability:** R4_GCS_CTRL, R4_GCS_TELEM; model: `rx.control_signal_out → platform.control_input`, `rx.telemetry_data_in → platform.telemetry_data_out`.

#### 3.2.5 GCS-to-laptop interfaces

**IF-GND-01 — GCS VRX → USB capture → Laptop (video)**
- **Priority:** Critical. **Type:** Analog video → USB capture (storage-and-display).
- **Data elements:** Live video frames. **Data assemblies:** UVC video stream.
- **Communication method:** VRX analog out → USB capture dongle → laptop USB. **Protocol:** CVBS → USB-UVC 1.0.
- **Physical & other:** RCA/composite to USB-A/USB-C; macOS-compatible (QuickTime/UVC). For digital VTX frames the receiver is goggles with HDMI/USB out instead.
- **Traceability:** R4_GCS_VIDEO_DISP.

**IF-GND-02 — GCS ELRS dongle → Laptop (control + telemetry)**
- **Priority:** Critical. **Type:** USB serial (bidirectional control + telemetry).
- **Data elements:** RC channels (out); telemetry (in). **Data assemblies:** CRSF / MAVLink over USB CDC.
- **Communication method:** ELRS USB dongle ↔ laptop GCS software (virtual COM). **Protocol:** USB CDC serial carrying CRSF/MAVLink.
- **Physical & other:** USB-C/A virtual COM port; the laptop is the ground station. Backup path: handheld radio telemetry → laptop.
- **Traceability:** R4_GCS_TELEM, R4_GCS_CTRL.

---

## 4. Qualification provisions

| Method | Interfaces | How |
|---|---|---|
| **Analysis (A)** | IF-PWR-01, IF-VID-01/02/03/04, IF-RF-01/02 | The model's P1/V/R compatibility rules, executed across all candidates by [`flight_time_model.py`](analysis/flight_time_model.py) (incompatible pairings pruned); RF range margin checked vs the 2.8 km requirement. |
| **Inspection (I)** | IF-PWR-01/02, IF-DAT-01/02/03, IF-GND-01/02 | Connector/voltage/pinout and protocol/baud inspection of selected components vs this IRS; physical fit (battery bay, connectors). |
| **Test (T)** | IF-PWR-01/02, IF-DAT-02, IF-GND-01/02 | Bench bring-up: power rails under load, MAVLink SBC↔FC link, end-to-end video and telemetry to the laptop. |
| **Demonstration (D)** | IF-RF-01, IF-RF-02 | Field range walk-test of video and control+telemetry links to ≥ 2.8 km LOS. |

---

## 5. Requirements traceability (interface → SSS requirement)

| Interface | Governing requirement(s) |
|---|---|
| IF-PWR-01 | R4_BAT_VOLT, R4_BAT_IF, R4_AF_PWR_DIST |
| IF-PWR-02 | R4_AF_PWR_DIST, R3_CAM_PWR, R4_SBC_PWR |
| IF-VID-01 | R3_CAM_IF |
| IF-VID-02 | R4_SBC_VIDEO_IN, R4_SBC_VIDEO_PROC, R3_CAM_IF |
| IF-VID-03 | R3_CAM_IF |
| IF-VID-04 | R3_CAM_IF |
| IF-RF-01 | R4_GCS_VIDEO_DISP, R4_GCS_IF, R4_GCS_RANGE (⊆R7) |
| IF-RF-02 | R4_GCS_CTRL, R4_GCS_TELEM, R4_GCS_RANGE (⊆R7), R4_GCS_IF |
| IF-DAT-01 | R1, R2 (navigation) |
| IF-DAT-02 | R4_SBC_DATA_AF |
| IF-DAT-03 | R4_GCS_CTRL, R4_GCS_TELEM |
| IF-GND-01 | R4_GCS_VIDEO_DISP |
| IF-GND-02 | R4_GCS_TELEM, R4_GCS_CTRL |

---

## 6. Notes

- The three compatibility rules (P1/V/R) are declared in `model.sysml` `Architecture::Compatibility` and **executed** by the flight-time sweep — incompatible component pairings are pruned before ranking, so every analyzed configuration is interface-consistent.
- Concrete endpoint values (e.g. specific connectors, bands, baud) are realized by the selected components in [`SELECTED_COMPONENTS.md`](SELECTED_COMPONENTS.md); where a selection is still open, the protocol/band stated here is the baseline.
- **Acronyms:** see the [SSS](REQUIREMENTS_EXPORT_26_06_30.md) §6. Additional: BEC (battery-eliminator circuit / regulator), PDB (power-distribution board), UVC (USB Video Class), CDC (USB Communications Device Class), CRSF (Crossfire serial protocol), UBX (u-blox binary protocol).
- This export is a content-aligned rendering of DI-IPSC-81434; it is not a contractual CDRL deliverable.
