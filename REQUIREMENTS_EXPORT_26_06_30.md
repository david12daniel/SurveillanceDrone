# System/Subsystem Specification (SSS) — Thermal Surveillance Drone

*Content structured in alignment with **DI-IPSC-81431** (System/Subsystem Specification).*
*Generated export — 2026-06-30. Source of truth: [`model.sysml`](model.sysml) `DroneSystemModel::Requirements`.*

---

## 1. Scope

### 1.1 Identification
This specification establishes the requirements for the **Thermal Surveillance Drone
System** (the "system"), a small uncrewed aerial system for personal wildlife scouting.
Requirement identifiers (`R1`–`R8` and `R<n>_<SUBSYS>_<NAME>`) are the authoritative IDs
from the SysML v2 model and are used verbatim here.

### 1.2 System overview
The system is a battery-powered multirotor carrying a thermal (LWIR) camera, an FPV
piloting camera, GPS, an onboard single-board computer (SBC) for detection/classification,
and an RF data-link suite, operated from a laptop-based ground control station (GCS). Its
mission is to detect and classify deer, turkey, other animals, and humans by thermal
signature at 90–120 m above ground level (AGL). The system is delivered in four incremental
capability phases (see §3.1).

### 1.3 Document overview
This document records system and subsystem requirements (§3), their verification methods
(§4), and traceability (§5). **Interface requirements are specified in the companion
[Interface Requirements Specification (IRS)](INTERFACE_REQUIREMENTS_EXPORT_26_06_30.md)**
(DI-IPSC-81434 content); §3.3–3.4 here summarize and reference it.

---

## 2. Referenced documents

| Ref | Document |
|---|---|
| [`model.sysml`](model.sysml) | Authoritative SysML v2 system model (requirements, architecture, analysis) |
| [`INTERFACE_REQUIREMENTS_EXPORT_26_06_30.md`](INTERFACE_REQUIREMENTS_EXPORT_26_06_30.md) | Interface Requirements Specification (IRS) |
| [`SELECTED_COMPONENTS.md`](SELECTED_COMPONENTS.md) | Current locked/open component selections |
| [`systems_engineering_plan.md`](systems_engineering_plan.md) | Incremental build roadmap (phases) |
| [`analysis/flight_time_model.py`](analysis/flight_time_model.py) | Parametric endurance/trade-study analysis (verification by Analysis) |
| `MODEL_ISSUES.md` | Decisions log + open items |
| DI-IPSC-81431 / DI-IPSC-81434 | DID content templates this export aligns to |

---

## 3. Requirements

### 3.1 Required states and modes
The system is fielded in **three committed capability phases plus a deferred Phase 4** (future capability), each a superset of the prior (see `systems_engineering_plan.md`):
1. **Phase 1 — Flight + FPV + waypoints:** airframe + ELRS control link + battery + FPV/analog video downlink to the laptop + GPS pre-programmed waypoint routes.
2. **Phase 2 — Thermal + SBC (onboard):** adds the thermal camera (USB) + SBC. The thermal streams live to the SBC for real-time inference — **no recording and no downlink** in the committed build.
3. **Phase 3 — Onboard autonomy (software):** deploys the detection/classification model on the already-installed SBC + integrates MAVLink autonomous route modification, running **real-time inference on the live thermal feed**. *No hardware procurement in Phase 3.*
4. **Phase 4 — OpenHD downlink (deferred future capability):** adds a live digital video downlink of the thermal/AI feed to the ground station (`WLAN_AIR1` + air antennas, `WLAN_GND1` + Foxeer ground antennas, VMware VM). Not part of the committed Phase 1–3 system.

Flight states within any phase: **disarmed/idle, armed, takeoff, cruise (2.23 m/s surveillance), loiter, return-to-launch (failsafe), land.**

### 3.2 System capability requirements

#### 3.2.1 Flight performance
- **R1** — The system shall operate at a nominal cruising altitude relative to ground level between 90 meters and 120 meters.
- **R2** — The drone shall maintain a steady ground speed of 2.23 meters/second.
- **R6** — Minimum sustained flight time: 30 minutes in non-wind (0 m/s) conditions.
- **R7** — Minimum linear distance during surveillance: 2800 meters when performing surveillance at 2.2 m/s in sustained wind conditions of 4.5 m/s.
- **R8** *(stretch)* — Sustained flight time of 60 minutes in non-wind (0 m/s) conditions.

#### 3.2.2 Thermal detection & classification
- **R3** — At nominal cruising altitude (90 m to 120 m AGL), the thermal imaging system shall enable a remote operator to detect and classify heat signatures to distinguish deer, turkey, other animals, and humans under clear daytime conditions with a minimum target-to-background temperature differential of 5 °C.
- **R3_1** — *Detection:* a human operator viewing the live video feed shall be able to identify the presence of a deer-, turkey-, or human-sized heat source at 120 m AGL with a confidence level of at least 90%.
- **R3_2** — *Classification:* a human operator viewing the live video feed shall be able to correctly classify a detected heat source as deer, turkey, other animal, or human at 90 m AGL with a confidence level of at least 80%.
- **R3_CAM_FOV** *(⊆R3)* — The camera shall provide a horizontal field of view of at least 30 degrees.
- **R3_CAM_NETD** *(⊆R3)* — The thermal sensor NETD shall not exceed 50 mK.
- **R3_CAM_RES** *(⊆R3)* — The thermal sensor shall provide spatial resolution such that at 90 m AGL a 0.5 m × 0.5 m target occupies at least 4 contiguous pixels in each dimension (Johnson-criteria recognition).

#### 3.2.3 Onboard processing (SBC)
- **R4_SBC_VIDEO_IN** — The SBC shall accept a video input from the thermal camera that matches the camera's video output format.
- **R4_SBC_VIDEO_PROC** *(⊆R3)* — The SBC shall process the incoming video stream for live transmission to the GCS without introducing a processing delay that degrades the operator's ability to detect and classify targets per R3_1 and R3_2.
- **R4_SBC_DATA_AF** — The SBC shall exchange telemetry and status data with the flight controller (airframe) through the data_af interface.

#### 3.2.4 Ground control & display
- **R4_GCS_RANGE** *(⊆R7)* — The GCS control link and video receiver shall maintain a reliable connection with the drone at a slant range of at least 2800 meters under clear line-of-sight conditions.
- **R4_GCS_VIDEO_DISP** *(⊆R3)* — The GCS display shall render the thermal video feed at sufficient resolution, brightness, and size such that the operator can perform detection (R3_1) and classification (R3_2) tasks.
- **R4_GCS_TELEM** — The GCS display shall present real-time drone telemetry (altitude, position, battery voltage, heading, speed) to the operator.
- **R4_GCS_CTRL** — The GCS shall provide flight control inputs (throttle, roll, pitch, yaw, arming, flight-mode selection) with sufficient latency and resolution for safe manual operation at 2800 m range.

#### 3.2.5 Power & endurance (battery)
- **R4_BAT_ENERGY** *(⊆R6)* — The battery shall store sufficient usable energy such that, combined with the system total power draw (per FlightTimeCalc), the minimum sustained flight time of 1800 s (R6) is achieved.
- **R4_BAT_ENERGY_STRETCH** *(⊆R8)* — The battery shall store sufficient usable energy such that the stretch-goal sustained flight time of 3600 s (R8) is achievable.
- **R4_BAT_DISCHARGE** — The battery shall sustain continuous discharge at the system maximum current draw without triggering the ESC low-voltage cutoff or causing voltage sag that degrades flight performance.

#### 3.2.6 Lift & structure (airframe)
- **R4_AF_PAYLOAD** — The airframe shall have sufficient payload capacity to carry the combined mass of all onboard subsystems (battery, camera, SBC, cabling) while maintaining stable flight.
- **R4_AF_PROP_CFG** *(⊆R1, ⊆R2)* — The airframe shall accommodate propeller diameters and motor mounting patterns suitable for efficient cruise at 2.23 m/s and 90–120 m AGL.
- **R4_AF_STIFF** *(⊆R3)* — The airframe structure shall be sufficiently rigid to prevent vibration-induced degradation of thermal image quality during cruise.

### 3.3 System external interface requirements
External interfaces (drone ↔ GCS RF links; GCS ↔ operator laptop) are specified in the
**[IRS](INTERFACE_REQUIREMENTS_EXPORT_26_06_30.md) §3.2 (IF-RF-01, IF-RF-02, IF-GND-01, IF-GND-02)**. Governing requirements:
- **R4_GCS_IF** — The GCS receiver and transmitter shall be compatible with the drone's video transmitter and telemetry-radio operating frequencies and protocols.
- **R3_CAM_IF** — The camera shall output analog CVBS or digital video (HDMI/CSI/USB) compatible with the selected SBC or VTX video input port.
- (Range over these external RF links: **R4_GCS_RANGE**, both control and video links hard at 2.8 km.)

### 3.4 System internal interface requirements
Internal interfaces (battery↔airframe power, payload power rails, the camera→SBC/VTX
video chain, GPS/SBC↔flight-controller data) are specified in the **[IRS](INTERFACE_REQUIREMENTS_EXPORT_26_06_30.md) §3.2 (IF-PWR-\*, IF-VID-\*, IF-DAT-\*)**. Governing requirements:
- **R4_BAT_VOLT** — The battery nominal voltage shall be within the operating input voltage range of the airframe's flight controller, ESC, and payload voltage regulators.
- **R4_BAT_IF** — The battery connector and form factor shall be physically compatible with the airframe's power input leads and battery mounting bay.
- **R4_AF_PWR_DIST** — The airframe power distribution wiring and connectors shall supply regulated voltage to the payload subsystems (camera, SBC) and unfiltered battery voltage to the ESCs.
- **R4_SBC_VIDEO_IN**, **R4_SBC_DATA_AF** (see §3.2.3).

### 3.5 System internal data requirements
- **Telemetry data:** altitude, GPS position, battery voltage, heading, ground speed, flight mode (CRSF over the ELRS link; surfaced per R4_GCS_TELEM).
- **Video stream:** thermal LWIR 640×512 @ 25 Hz — streamed live over USB to the onboard SBC for real-time inference (not recorded; live ground downlink is the deferred Phase 4/OpenHD capability); FPV piloting video (analog CVBS) to the laptop.
- **GNSS data:** position/velocity/time to the flight controller (NMEA/UBX).
- **SBC↔FC data:** detection results / route commands (MAVLink, Phase 4).

### 3.6 Adaptation requirements
Field-configurable: flight modes and waypoint routes (GCS), VTX channel/power, ELRS
packet rate. No site-specific data tables beyond operator-defined routes.

### 3.7 Safety requirements
*Not yet formally captured as discrete model requirements; the following are derived/implicit and flagged for future formalization:*
- LVC: ESC low-voltage cutoff shall not be triggered in normal flight (derived from **R4_BAT_DISCHARGE**).
- Ground clearance: ≥ 30 mm below the lowest payload component (**R4_AF_LANDING**, see §3.12).
- Failsafe: loss of control link shall command a safe state (return-to-launch/land) — *to be specified.*
- Li-ion pack handling, charging, and transport safety — *to be specified.*

### 3.8 Security and privacy requirements
*Not formally specified (single-operator hobbyist system).* Considerations for future capture: control-link integrity (ELRS), protection of recorded footage on removable media, and applicable airspace/wildlife-observation regulations.

### 3.9 System environment requirements
- Operation under **clear daytime** conditions with a **≥ 5 °C** target-to-background differential (**R3**).
- Sustained **wind to 4.5 m/s** during surveillance (**R7**).
- **R4_SBC_TEMP** — The SBC shall operate within the full environmental temperature range of the drone system without active cooling.

### 3.10 Computer resource requirements
- **R4_SBC_PWR** — The SBC shall consume no more than 10 W average during continuous operation at cruise.
- **R4_SBC_WT** — The SBC (board + cabling + any enclosure) shall not exceed 100 g total mass.
- The SBC shall host the detection/classification inference workload (NPU-accelerated) — selected baseline: NanoPi M5 (RK3576, 6 TOPS), passively cooled (consistent with R4_SBC_TEMP).

### 3.11 System quality factors
- **Reliability:** control and video links reliable to ≥ 2.8 km LOS (**R4_GCS_RANGE**); the thermal mission does not depend on the RF link — inference runs onboard on the live USB feed, so detections/actions continue independent of downlink quality (the Phase 4 OpenHD downlink, when built, is for operator awareness only).
- **Maintainability / usability:** COTS modules, field-portable hand-held GCS (**R4_GCS_WT**), single-operator setup.

### 3.12 Design and construction constraints
- **R4** — The total cost for the entire integrated system shall be under $2,500.
- **R5** — The system shall minimize DIY soldering.
- **R3_CAM_WT** — The camera subsystem (sensor + lens + housing + cabling) shall not exceed 200 g total mass.
- **R3_CAM_PWR** — The camera subsystem shall consume no more than 4.5 W average during continuous operation.
- **R3_CAM_COST** *(⊆R4)* — The camera subsystem cost shall not exceed 600 USD.
- **R4_SBC_COST** *(⊆R4)* — The SBC cost shall not exceed 150 USD.
- **R4_BAT_WT** — The battery mass shall not exceed the payload capacity of the selected airframe when combined with all other onboard subsystems.
- **R4_BAT_COST** *(⊆R4)* — The battery cost, summed with all other subsystem costs, shall not cause the system total to exceed 2500 USD.
- **R4_GCS_COST** *(⊆R4)* — The GCS cost, summed with all other subsystem costs, shall not cause the system total to exceed 2500 USD.
- **R4_AF_COST** *(⊆R4)* — The complete airframe subsystem cost shall not cause the system total to exceed 2500 USD.
- **R4_AF_WT** — The bare airframe mass shall leave margin such that total takeoff mass ≤ 80% of the airframe's rated maximum takeoff mass.
- **R4_AF_ASSY** *(⊆R5)* — The airframe assembly shall minimize DIY soldering, preferring pre-soldered power-distribution boards, plug-in connectors, and screw-terminal motor connections.
- **R4_AF_LANDING** — The airframe shall provide landing gear or structural clearance of at least 30 mm below the lowest payload component.

### 3.13 Personnel-related requirements
Single remote operator (pilot + sensor operator combined). No crew beyond one.

### 3.14 Training-related requirements
Operation shall be achievable by a hobbyist FPV pilot; minimal training (manual-flight proficiency + GCS familiarization). No formal training program required.

### 3.15 Logistics-related requirements
Built from commercially-available (COTS) modules to minimize custom fabrication (**R5**); field-portable; operates on internal GCS battery without external AC power (**R4_GCS_BAT** — the GCS shall operate on internal battery power for a duration matching or exceeding the drone's maximum planned flight time).

### 3.16 Packaging requirements
- **R4_GCS_WT** — The GCS (transmitter, display, antennas, battery) shall be portable and hand-held for field operation.
- Other packaging: *not specified.*

### 3.17 Precedence and criticality of requirements
1. **Critical (mission-defining):** R3, R3_1, R3_2 (detection/classification); R4 (cost cap); R6 (endurance); R7 / R4_GCS_RANGE (range — hard for **both** control and video).
2. **High:** R1, R2 (flight regime); subsystem energy/power/mass constraints enabling R6 and R4.
3. **Goal:** R8 (60-min stretch endurance).

---

## 4. Qualification provisions

| Method | Applies to | How |
|---|---|---|
| **Analysis (A)** | R1, R2, R6, R7, R8, R3_CAM_RES, R3_CAM_FOV, R4_BAT_ENERGY(_STRETCH), R4_AF_PAYLOAD/WT, all cost (R4*) | The Analysis layer + [`flight_time_model.py`](analysis/flight_time_model.py): endurance (momentum/actuator-disk), Johnson pixels-on-target (GroundSampleDistance/PixelsAcrossTarget), cost roll-up, payload/thrust feasibility. |
| **Demonstration (D)** | R3_1, R3_2, R4_GCS_*, flight modes (§3.1) | Field flight tests per phase: operator detect/classify trials at 90/120 m; range walk-test of control+video to 2.8 km. |
| **Inspection (I)** | R3_CAM_WT/PWR/NETD, R4_SBC_*, R4_BAT_*, R4_AF_ASSY/LANDING, R5 | BOM/spec inspection of selected components vs limits; build inspection for solder-joint count and ground clearance. |
| **Test (T)** | R4_BAT_DISCHARGE, R4_SBC_PWR/TEMP, R4_GCS_BAT | Bench measurement: discharge under load, SBC power/thermal under inference, GCS endurance. |

> Note: Syside validates the model's parametric structure; numeric execution of the in-model `calc def`s requires a SysML v2 execution engine — the high-fidelity numbers come from `flight_time_model.py`.

---

## 5. Requirements traceability

### 5.1 Mission → subsystem refinement (`subsets`)
| Subsystem requirement | Refines (⊆) |
|---|---|
| R3_CAM_FOV, R3_CAM_NETD, R3_CAM_RES, R4_SBC_VIDEO_PROC, R4_GCS_VIDEO_DISP, R4_AF_STIFF | **R3** |
| R3_CAM_COST, R4_BAT_COST, R4_SBC_COST, R4_GCS_COST, R4_AF_COST | **R4** |
| R4_AF_ASSY | **R5** |
| R4_BAT_ENERGY | **R6** |
| R4_GCS_RANGE | **R7** |
| R4_BAT_ENERGY_STRETCH | **R8** |
| R4_AF_PROP_CFG | **R1, R2** |

### 5.2 Requirement → satisfying architecture element (`satisfy`)
| Architecture element (`part def`) | Satisfies |
|---|---|
| **Battery** | R4_BAT_VOLT, R4_BAT_ENERGY, R4_BAT_ENERGY_STRETCH, R4_BAT_WT, R4_BAT_DISCHARGE, R4_BAT_COST, R4_BAT_IF |
| **Airframe** | R4_AF_PAYLOAD, R4_AF_WT, R4_AF_PROP_CFG, R4_AF_PWR_DIST, R4_AF_ASSY, R4_AF_STIFF, R4_AF_LANDING, R4_AF_COST |
| **IRCamera** | R3_CAM_WT, R3_CAM_PWR, R3_CAM_FOV, R3_CAM_NETD, R3_CAM_RES, R3_CAM_COST, R3_CAM_IF |
| **SBCPayload** | R4_SBC_PWR, R4_SBC_WT, R4_SBC_COST, R4_SBC_VIDEO_IN, R4_SBC_VIDEO_PROC, R4_SBC_DATA_AF, R4_SBC_TEMP |
| **GCS** | R4_GCS_RANGE, R4_GCS_VIDEO_DISP, R4_GCS_TELEM, R4_GCS_CTRL, R4_GCS_BAT, R4_GCS_WT, R4_GCS_COST, R4_GCS_IF |
| **RcTx** | R4_GCS_CTRL, R4_GCS_TELEM |
| **Vrx** | R4_GCS_VIDEO_DISP |

> Mission requirements R1, R2, R6, R7, R8 are satisfied at the system level (emergent — verified by the endurance/flight analysis), and refined to the satisfying subsystems via the `subsets` links in §5.1.

---

## 6. Notes

- **Acronyms:** AGL (above ground level), LWIR (long-wave infrared), NETD (noise-equivalent temperature difference), SBC (single-board computer), GCS (ground control station), VTX/VRX (video transmitter/receiver), ELRS (ExpressLRS), CRSF (Crossfire serial protocol), CVBS (composite analog video), LOS (line of sight), COTS (commercial off-the-shelf), MTOM (max takeoff mass).
- Requirement text is reproduced verbatim from `model.sysml`; IDs use `_1`/`_2` (not `.1`/`.2`) because dots are invalid SysML identifiers.
- This export is a content-aligned rendering of DI-IPSC-81431; it is not a contractual CDRL deliverable.
