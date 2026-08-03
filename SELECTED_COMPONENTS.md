# SELECTED COMPONENTS — single source of truth

**This file is the authoritative, current list of selected components for the
surveillance-drone build.** If you are an AI or collaborator working on this
project, read this first to know what is DECIDED vs still OPEN. Component IDs
refer to the typed part usages in [`candidates.sysml`](candidates.sysml).

_Last updated: 2026-07-10._

> How selections are enforced (so they can't silently drift):
> - **Design data** lives in [`candidates.sysml`](candidates.sysml) (every candidate, by ID).
> - **Locks** are enforced in the analysis by `FIXED_*` constants in
>   [`analysis/flight_time_model.py`](analysis/flight_time_model.py) — the flight-time
>   sweep only builds configs using the locked parts. Setting a constant to `None`
>   re-opens that dimension.
> - **Rationale** for each decision is logged in [`MODEL_ISSUES.md`](MODEL_ISSUES.md)
>   (chronological) and the `analysis/*.md` trade studies.
> - **CAD / 3D-model resources + the free-CAD modeling pathway** (for building the
>   physical-integration mount) live in [`reference/cad-resources.md`](reference/cad-resources.md).
> - **Formal requirements & interfaces** are exported as the SSS
>   [`REQUIREMENTS_EXPORT_26_06_30.md`](REQUIREMENTS_EXPORT_26_06_30.md) and the IRS
>   [`INTERFACE_REQUIREMENTS_EXPORT_26_06_30.md`](INTERFACE_REQUIREMENTS_EXPORT_26_06_30.md).
> - **Phased bill of materials** (product / part # / link / cost, per-phase subtotals): [`BOM.md`](BOM.md).

---

## ✅ LOCKED selections

| Role | Selected component | ID | Locked | Enforced by | Rationale | Phase |
|---|---|---|---|---|---|:--:|
| **Airframe** | **iFlight Chimera9 ECO (9"), PNP** | [`AF3a`](https://shop.iflight.com/Chimera9-ECO-6S-Pro2068) | 2026-06-30 | `FIXED_AIRFRAME_IDS = ["AF3a"]` | best endurance-per-dollar of the SBC-capable frames; SBC fits the deck (110×70 mm, 8 mm spare); PNP chosen to run ELRS. §C16–17. | **1** |
| **Receiver (RX)** | **iFlight True Diversity ELRS** (2.4 GHz, 5 km, dual-antenna) | [`iFlightTD`](https://shop.iflight.com/) | 2026-06-30 | recorded here † | true-diversity → reliable link at range; brand-matches the airframe. | **1** |
| **Handheld radio** | **RadioMaster TX12 Mark II ELRS** (0.25 W, ~6 km, hall gimbals, compact box) | [`TX5`](https://www.radiomasterrc.com/products/tx12) | 2026-07-01 | recorded here † | compact box form factor, full-size hall gimbals, EdgeTX; 0.25 W is ample (Hermes dongle is primary 2.8 km link; TX12 is backup/manual); saves $54 vs Boxer. | **1** |
| **Video receiver (VRX)** | **Skydroid 150CH 5.8 GHz true-diversity UVC** | [`VRX6`](https://www.alibaba.com/product-detail/SKYDROID-5-8GHz-FPV-Receiver-UVC_1601393061166.html) | 2026-06-30 | sweep (matched VRX, CVBS) | laptop-direct UVC (QuickTime/OBS on macOS); receives the bundled analog VTX (pulled forward from Phase 2). | **1** |
| **Ground antenna** | **TrueRC X-AIR 5.8 MK II patch** (≈10 dBic, 120° beam, RHCP, RP-SMA) | [`PATCH1`](https://truerc.com/63425-x-air-58-mk-ii-rp-sma) | 2026-06-30 | GCS cost basis | directional gain that closes the 2.8 km video link with margin — see [`analysis/rf_link_budget.md`](analysis/rf_link_budget.md). | **1** |
| **Anti-spark filter** | **iFlight Anti Spark Filter** (XT60, 6S, 150 A, inline) | [`ASF1`](https://shop.iflight.com/index.php?route=product/product&product_id=3474) | 2026-06-30 | recorded here | inline battery→airframe; limits the plug-in inrush spike, protecting ESC/PDB caps. | **1** |
| **Battery charger** | **HOTA D6 Pro** (AC 200 W / DC 650 W, dual, 6S Li-ion/LiPo, XT60) | [`CHG1`](https://www.hotarc.com/) | 2026-07-01 | support equipment | charges the 6S 12 Ah packs (Li-ion **and** LiPo); dual-channel AC; community standard, best value. | **1** |
| **Battery (flight)** | **Upgrade Energy GREEN V2 6S3P 12 Ah Amprius** — the default (BAT09 out of stock) | [`BAT10`](https://www.upgradeenergytech.com/products/green-v2-6s3p-12ah-ampruis-sa10) | 2026-07-01 | recorded here | 57.1 min hover, XT60, best in-stock 12 Ah Amprius pack; ~$275. | **1** |
| **Battery (dev, ×2)** | **GNB 6S3P 12 Ah 21700 Li-ion** — 2 packs | [`BAT22`](https://www.gaoneng.shop/products/gaoneng-gnb-6s-22.2v-12000mah-10c-xt60-li-ion-battery-made-with-li-ion-lithium-ion-21700) | 2026-07-01 | recorded here | cheap ($110), robust standard-cell packs for development/shakedown (~46 min); spares the Amprius on early flights. | **1** |
| **GPS** | **iFlight BLITZ M10 GPS V2 Mini** (u-blox M10, compass, bundled w/ AF3a) | [`G4`](https://shop.iflight.com/) | 2026-07-01 | bundled with `AF3a` (+$39 option) | selected by choosing the GPS pre-install option on the Chimera9 ECO; no separate procurement needed. | **1** |
| **GCS ELRS dongle** | **HGLRC Hermes ELRS SIM USB Dongle** (2.4 GHz, USB-A, standalone) | [`TLM2`](https://www.amazon.com/s?k=HGLRC+Hermes+ELRS+USB+dongle) | 2026-07-01 | recorded here | stays plugged into the laptop for live in-flight MAVLink telemetry while the Boxer is with the pilot; $16 = cheapest no-solder standalone option (TLM1 Boxer USB passthrough is $0 but ground-only). | **1** |
| **Thermal camera** | **PurpleRiver Mini 640** (640×512, 12 µm, **18 mm lens**, USB) | [`T13`](https://www.thermal-image.com/product/mini-640-uncooled-lwir-thermal-camera-module/) | 18mm updated 2026-07-29 | `FIXED_THERMAL_ID = "T13"` | 18 mm (was 13 mm): 8.3 px on 0.5 m @90 m (Johnson recognize, better margin) + still detects @120 m, and is the shortest lens that **recognizes at a 45° oblique tilt**. HFOV **24.1°** is *below* R3_CAM_FOV (≥30°) — an accepted trade: IR is **surveillance-only, not used to fly** (the FPV cam does), so FOV is a coverage goal not a hard limit; costs ~28% area/sweep. See [`analysis/thermal_detection_offnadir_analysis.md`](analysis/thermal_detection_offnadir_analysis.md). **R3_CAM_FOV re-tag pending David's model.sysml approval** (MODEL_ISSUES.md). | **2** |
| **OpenHD air WiFi adapter** | **LB-LINK BL-M8812EU2** (RTL8812EU bare module, ~18 g, >29 dBm) | [`WLAN_AIR1`](https://www.aliexpress.com/item/1005007098141054.html) | 2026-07-02 | recorded here | lightest + highest TX power of all WFB-ng–supported adapters; WFB-ng author's own test hardware; ARM64 build verified (Makefile `CONFIG_PLATFORM_ARM64_RPI`). §OpenHD-Air. | **4** |
| **OpenHD air antenna × 2** | **5.8 GHz RHCP cloverleaf, RP-SMA male** ([amazon](https://www.amazon.com/5-8GHz-Cloverleaf-Antenna-Receiver-Transmitter/dp/B0CDZ8FXFW), ~9 g ea) | — | 2026-07-06 | BOM-only ($13.99/pair) | circular omni on the moving drone avoids the deep nulls a linear dipole hits when banking (accepts ~3 dB polarization mismatch vs the linear ground panels — small vs the +11.3 dB @2.8 km margin). RP-SMA male mates the u.fl→RP-SMA pigtails. | **4** |
| **OpenHD ground WiFi adapter** | **Alfa AWUS036ACH** (RTL8812AU, USB-C, dual RP-SMA) | [`WLAN_GND1`](https://store.rokland.com/products/alfa-awus036ach-usb-c-802-11ac-ac1200-dual-band-high-power-wifi-usb-adapter) | 2026-07-02 | recorded here | dual standard RP-SMA ports for diversity directional panels; confirmed ARM64 VM via VMware Fusion xHCI on Apple Silicon. §OpenHD-Gnd. | **4** |
| **OpenHD ground antenna × 2** | **Foxeer Echo 2 Max 5.8 GHz** (13 dBi, 60°, Linear, RP-SMA) × 2 | [`ANT_GND1`](https://www.foxeer.com/foxeer-echo-2-max-high-gain-antenna-g-434) + [`ANT_GND2`](https://www.foxeer.com/foxeer-echo-2-max-high-gain-antenna-g-434) | 2026-07-02 | recorded here | 60° beam avoids need to track or re-aim during a survey; ±30° slack from aim point; +11.3 dB margin @2.8 km; reliable to 3.3 km. RP-SMA male mates directly to AWUS036ACH (no pigtail). Saves ~$13 vs AXII Quadro pair + pigtails. | **4** |
| **On-board computer (SBC)** | **NanoPi M5, 4 GB** (Rockchip RK3576, 6 TOPS) | [`SBC3`](https://www.friendlyelec.com/index.php?route=product/product&path=69&product_id=309) | earlier | `FIXED_SBC_ID = "SBC3"` | mature RKNN toolchain + ≤10 W passive (meets power/cooling rules SBC2 fails). | **2** |
| **FC firmware** | **ArduPilot ArduCopter ≥ 4.5** (GPLv3, $0) | `Architecture::Software` register (`Airframe.fcSoftware`) | 2026-07-10 | model register + `candidates.sysml` `AF3a.fcFirmware` | resolves the ArduPilot-vs-PX4 TBD: the autonomy contract + mission app are built and tested on ArduCopter AUTO/GUIDED (`analysis/autonomy_sim/`, §C26); its FS_*/BATT_* params realize the §3.7 failsafe reqs. §C28. | **1** |
| **GCS application** | **QGroundControl 4.4+** (Apache-2.0/GPLv3, $0) | `Architecture::Software` register (`Laptop.gcsApp`) | 2026-07-10 | model register | covers ALL laptop functions (plan/upload/telemetry/video/params/alerts/logs — [`analysis/software_by_component.md`](analysis/software_by_component.md) §1); macOS (MacBook Air) rules out Mission Planner. | **1** |


**Phase 4 = deferred future capability.** The four **OpenHD** rows above (`WLAN_AIR1`, air antennas, `WLAN_GND1`, `ANT_GND1`/`ANT_GND2`) are *selected but deferred* — together they build the live thermal-video downlink to the ground, which is **not part of the committed Phase 1–3 system** (moved to Phase 4 on 2026-07-07). The committed build streams the thermal to the onboard SBC for **real-time inference only** — no thermal downlink, no recording. See [`BOM.md`](BOM.md) Phase 4 and [`systems_engineering_plan.md`](systems_engineering_plan.md) Phase 4.

† The RX and handheld radio aren't `FIXED_*` sweep dimensions — the flight-time sweep holds the RX at a light representative (negligible endurance delta) and uses a cheapest-radio cost basis. These rows are the authoritative selection of record.

**Control ecosystem = ELRS (by choice, not requirement).** The RX (`iFlightTD`) + handheld (`TX5` TX12 MkII) + HGLRC Hermes laptop dongle (`TLM2`) are all ELRS 2.4 GHz, so the control stack is one ecosystem end-to-end. **Nothing in the model mandates ELRS** — the RF compatibility rule is band-match only — so non-ELRS remains valid; ELRS is a pragmatic preference (cheap, common laptop dongles for the GCS plan).

### Airframe variant — RESOLVED: PNP (`AF3a`) + GPS pre-installed
Chose the **PNP** variant + **GPS pre-install option** (+$39). All-up airframe mass = 729 g; **as-purchased $490.99 all-in** (airframe + GPS + analog VTX + FPV cam + 4 extra props + shipping; no bundled receiver — the ELRS RX is added separately). The airframe **bundles a BLITZ Whoop 5.8 GHz analog VTX + analog CMOS FPV camera + iFlight BLITZ M10 GPS V2 Mini** (so VTX, FPV-cam, and GPS selections are all decided by the airframe). Shared drivetrain: XING-E 2809 800KV · BLITZ F7 FC · BLITZ E55 55 A 4-in-1 ESC · HQ 9×4×3 props.

### SBC power delivery — dedicated 12 V UBEC (added 2026-07-06, parts locked 2026-07-06)
The NanoPi M5 (`SBC3`) is powered by its own **2-6S→12V 3A UBEC** off the battery, feeding the M5's USB-C port via a plain **USB-C power-only cable (bare wire→USB-C male)**. The M5's USB-C input accepts **wide-input DC 6–20 V without PD negotiation** (onboard buck) — verified against FriendlyElec's spec — so **no USB-C PD-trigger module is needed**. A dedicated UBEC (not the airframe's small 5 V FC BEC) isolates the SBC and keeps it inside the M5's 6–20 V window (raw 6S peaks at 25.2 V, above the 20 V ceiling). **Committed (Phase 2) load on the 12 V unit ≈ 12 W** (SBC ~10 W + the `T13` thermal drawing <1 W over USB). The **2nd UBEC unit (set to 5 V) is held for Phase 4** to power the `WLAN_AIR1` OpenHD air module (~10 W); it is unused in the committed build. **Selected parts (no matching `model.sysml` part def exists, so these are BOM-only line items like the USB adapter/SBC mount, not `candidates.sysml` entries):**

| Part | Link | Cost |
|---|---|---|
| 2-6S→12V 3A UBEC (2-pack) | [amazon.com](https://www.amazon.com/2pcs-2S-6S-DC-DC-Converter-Module/dp/B0CTZHJR5L) | $9.99 |
| USB-C power-only cable (20AWG, 5A) | [amazon.com](https://www.amazon.com/USB-C-Power-Copper-Connector-Device/dp/B0GBGLNR52) | $7.99 |

**The `T13` thermal camera needs no power part** — it is a USB-C UVC device, bus-powered (<1 W) from the SBC's USB port. Build-time check: confirm the UBEC's jumper/preset is on 12V (not 5V) and solder its 12V+/GND leads to the pigtail's bare-wire end before connecting to the SBC. See `BOM.md` Phase 2.

### SBC port inventory — everything fits, USB is full (verified 2026-07-06)
The NanoPi M5 has **2× USB-A (USB 3.2 Gen 1, 1.5 A OCP each)**, USB-C (power), 4× UART on the GPIO header, and a microSD slot. Allocation:

| Connection | M5 interface | Phase |
|---|---|---|
| T13 thermal camera (UVC) | USB-A #1 | ✅ committed (2) |
| 12 V UBEC power | USB-C | ✅ committed (2) |
| MAVLink ↔ flight controller | GPIO UART (1 of 4) | ✅ committed (2) |
| BL-M8812EU2 WiFi (WFB-ng TX) | USB-A #2 | ⏳ Phase 4 (future) |

**In the committed build only USB-A #1 is used** (the thermal); USB-A #2 is free and **reserved for the Phase 4 OpenHD air module.** There is **no recording** — the thermal streams live to the SBC for real-time inference. Onboard Wi-Fi/BT (the +$9 M.2 SDIO module) is intentionally omitted (Phase 4 WFB-ng runs on the external `WLAN_AIR1`).

### Battery power interface — standardized on **XT60** (refined 2026-06-30)
The battery↔drone power interface is now modeled: `model.sysml` `BatteryPowerInterface` gained a **`ConnectorCompatible`** constraint, the power ports (`PowerSourcePort`/`PowerSinkPort`) carry a `connector` attribute, and `Airframe` gained `batteryConnector`. **The whole power chain is XT60:** battery → iFlight anti-spark (XT60) → Chimera9 ECO XT60 lead. Verified against the candidates — **BAT09 / BAT10 / BAT22 (the three contenders) are all XT60** ✓; only non-contenders differ (**BAT08 = XT90**, **BAT23 Tattu LiPo = EC5** → would need an adapter). Chargers (below) output XT60 or use an XT60 charge lead.

---

## 🔶 OPEN / in-progress

| Role | Status | ID(s) | Notes |
|---|---|---|---|
| **On-board recording** | **RESOLVED — no recording.** The architecture does not record thermal; the T13 streams live (USB-UVC) to the SBC for **real-time inference** driving autonomous actions (Phase 3). DVR9 removed 2026-07-05; live-inference-only means no recording device at all. | `—` | eliminated the DVR ($129) + mass; SBC is inference-only. |

---

## Phase 1 build (selected) — flight + FPV downlink + waypoints
| Item | Part | ~Cost |
|---|---|---|
| Airframe + GPS + VTX + 4 props (bundled, incl. shipping) | Chimera9 ECO PNP + BLITZ M10 GPS V2 Mini (`AF3a` + `G4`) | $491 |
| Extra props | HQ 9X4X3 — 4-pack *(included w/ airframe)* | $0 |
| Receiver | iFlight True Diversity ELRS (`iFlightTD`) | $30 |
| Handheld radio | RadioMaster TX12 Mark II ELRS (`TX5`) | $118 |
| ELRS USB dongle (primary laptop link) | HGLRC Hermes (`TLM2`) | $16 |
| Battery (flight) | Upgrade Energy 6S3P 12 Ah Amprius (`BAT10`) | $275 |
| Battery (dev ×2) | GNB 6S3P 12 Ah (`BAT22`) × 2 | $220 |
| Video receiver | Skydroid 150CH 5.8 GHz UVC dual-antenna (`VRX6`) | $44 |
| Ground antenna | TrueRC X-AIR 5.8 patch (`PATCH1`) | $37 |
| Anti-spark filter | iFlight Anti Spark, XT60 (`ASF1`) | $15 |
| Battery charger | HOTA D6 Pro (`CHG1`) | $112 |
| USB-A→USB-C adapter | for the MacBook Air (USB-C only) | ~$11 |
| FPV cam + VTX (air video) | bundled with the Chimera9 PNP | $0 |
| GCS laptop | existing MacBook Air | $0 |
| **Phase 1 subtotal** | | **~$1,371** |

*See [`BOM.md`](BOM.md) for the full phased bill of materials (all four phases — Phase 4 = deferred future capability — sorted, with per-phase subtotals). Flight-controller firmware — **RESOLVED 2026-07-10: ArduPilot ArduCopter ≥ 4.5** (see the LOCKED table + [`analysis/software_by_component.md`](analysis/software_by_component.md)); still a configuration choice, not a procured component ($0).*

## Support equipment (bench — reusable, not flown, not in system cost)
**Battery charger — ✅ SELECTED: HOTA D6 Pro (`CHG1`), Phase 1** (now in the LOCKED table above). Formalized in the model as a `Charger` part def + `ChargerCandidates`, composed into `AerialObservationSystem` as ground-support equipment. Requirement: 6S **balance** + **Li-ion *and* LiPo** modes + XT60, with enough power for the 12 Ah packs (Li-ion ≈ 0.5C → 6 A/~133 W; LiPo 1C → 12 A/~266 W). Alternatives considered:

| Charger | ID | AC / DC power | Ch. | Notes | ~$ |
|---|---|---|---|---|---|
| **HOTA D6 Pro** ✅ **SELECTED** | `CHG1` | AC 200 W / DC 650 W · 15 A×2 | dual | community standard; Li-ion/LiPo/LiFe/LiHV, 1.6 A balance; best value | ~$112 |
| ISDT 608AC | `CHG2` | AC/DC 200 W · 8 A | single | simplest; XT60 built-in; AC-integrated; great for a single pack | ~$75 |
| ToolkitRC M6DAC | `CHG3` | AC 200 W / DC 700 W | dual | premium dual; full 700 W on DC | ~$120 |
| HOTA S6 | `CHG4` | AC 400 W / DC 325 W×2 · 15 A×2 | dual | highest AC power → fastest 12 Ah charging | ~$140 |

All do 6S **Li-ion + LiPo** with balance and XT60 (lead). **Recommended: HOTA D6 Pro** (value + dual channel + AC convenience); step to the **HOTA S6** if you want ≥1C charging of the 12 Ah packs. *(Charging Li-ion: charge to 4.1–4.2 V/cell at ≤0.5C for long cell life; always balance-charge.)*

## Not procured / external
- **Viewing computer** — existing MacBook Air (external actor; excluded from cost).

## Current reference build (full mission system)
**Chimera9 ECO (AF3a PNP) + BAT10 (Upgrade Energy 6S 12 Ah) + T13 + SBC3** → ~58.6 min hover, ~$1,645 system (well under the $2,500 R4 cap), SBC fits the deck. See
[`analysis/flight_time_value_ranking.md`](analysis/flight_time_value_ranking.md) /
[`.csv`](analysis/flight_time_value_ranking.csv) for the full ranked loadouts.
