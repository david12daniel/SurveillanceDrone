# SELECTED COMPONENTS — single source of truth

**This file is the authoritative, current list of selected components for the
surveillance-drone build.** If you are an AI or collaborator working on this
project, read this first to know what is DECIDED vs still OPEN. Component IDs
refer to the typed part usages in [`candidates.sysml`](candidates.sysml).

_Last updated: 2026-07-01._

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
| **Airframe** | **iFlight Chimera9 ECO (9"), PNP** | `AF3a` | 2026-06-30 | `FIXED_AIRFRAME_IDS = ["AF3a"]` | best endurance-per-dollar of the SBC-capable frames; SBC fits the deck (110×70 mm, 8 mm spare); PNP chosen to run ELRS. §C16–17. | **1** |
| **Receiver (RX)** | **iFlight True Diversity ELRS** (2.4 GHz, 5 km, dual-antenna) | `iFlightTD` | 2026-06-30 | recorded here † | true-diversity → reliable link at range; brand-matches the airframe. | **1** |
| **Handheld radio** | **RadioMaster TX12 Mark II ELRS** (0.25 W, ~6 km, hall gimbals, compact box) | `TX5` | 2026-07-01 | recorded here † | compact box form factor, full-size hall gimbals, EdgeTX; 0.25 W is ample (Hermes dongle is primary 2.8 km link; TX12 is backup/manual); saves $54 vs Boxer. | **1** |
| **Video receiver (VRX)** | **Skydroid 150CH 5.8 GHz true-diversity UVC** | `VRX6` | 2026-06-30 | sweep (matched VRX, CVBS) | laptop-direct UVC (QuickTime/OBS on macOS); receives the bundled analog VTX (pulled forward from Phase 2). | **1** |
| **Ground antenna** | **TrueRC X-AIR 5.8 MK II patch** (≈10 dBic, 120° beam, RHCP, RP-SMA) | `PATCH1` | 2026-06-30 | GCS cost basis | directional gain that closes the 2.8 km video link with margin — see [`analysis/rf_link_budget.md`](analysis/rf_link_budget.md). | **1** |
| **Anti-spark filter** | **iFlight Anti Spark Filter** (XT60, 6S, 150 A, inline) | `ASF1` | 2026-06-30 | recorded here | inline battery→airframe; limits the plug-in inrush spike, protecting ESC/PDB caps. | **1** |
| **Battery charger** | **HOTA D6 Pro** (AC 200 W / DC 650 W, dual, 6S Li-ion/LiPo, XT60) | `CHG1` | 2026-07-01 | support equipment | charges the 6S 12 Ah packs (Li-ion **and** LiPo); dual-channel AC; community standard, best value. | **1** |
| **Battery (flight)** | **Upgrade Energy GREEN V2 6S3P 12 Ah Amprius** — the default (BAT09 out of stock) | `BAT10` | 2026-07-01 | recorded here | 57.1 min hover, XT60, best in-stock 12 Ah Amprius pack; ~$275. | **1** |
| **Battery (dev, ×2)** | **GNB 6S3P 12 Ah 21700 Li-ion** — 2 packs | `BAT22` | 2026-07-01 | recorded here | cheap ($110), robust standard-cell packs for development/shakedown (~46 min); spares the Amprius on early flights. | **1** |
| **GPS** | **iFlight BLITZ M10 GPS V2 Mini** (u-blox M10, compass, bundled w/ AF3a) | `G4` | 2026-07-01 | bundled with `AF3a` (+$39 option) | selected by choosing the GPS pre-install option on the Chimera9 ECO; no separate procurement needed. | **1** |
| **GCS ELRS dongle** | **HGLRC Hermes ELRS SIM USB Dongle** (2.4 GHz, USB-A, standalone) | `TLM2` | 2026-07-01 | recorded here | stays plugged into the laptop for live in-flight MAVLink telemetry while the Boxer is with the pilot; $16 = cheapest no-solder standalone option (TLM1 Boxer USB passthrough is $0 but ground-only). | **1** |
| **Thermal camera** | **PurpleRiver Mini 640** (640×512, 12 µm, 13 mm lens, USB) | `T13` | earlier | `FIXED_THERMAL_ID = "T13"` | meets Johnson detect/recognize at 90–120 m; USB output. | **2** |
| **OpenHD air WiFi adapter** | **LB-LINK BL-M8812EU2** (RTL8812EU bare module, ~18 g, >29 dBm) | `WLAN_AIR1` | 2026-07-02 | recorded here | lightest + highest TX power of all WFB-ng–supported adapters; WFB-ng author's own test hardware; ARM64 DKMS driver. §OpenHD-Air. | **2** |
| **OpenHD ground WiFi adapter** | **Alfa AWUS036ACH** (RTL8812AU, USB-C, dual RP-SMA) | `WLAN_GND1` | 2026-07-02 | recorded here | dual standard RP-SMA ports for diversity directional panels; confirmed ARM64 VM via VMware Fusion xHCI on Apple Silicon. §OpenHD-Gnd. | **2** |
| **OpenHD ground antenna × 2** | **Foxeer Echo 2 Max 5.8 GHz** (13 dBi, 60°, Linear, RP-SMA) × 2 | `ANT_GND1` + `ANT_GND2` | 2026-07-02 | recorded here | 60° beam avoids need to track or re-aim during a survey; ±30° slack from aim point; +11.3 dB margin @2.8 km; reliable to 3.3 km. RP-SMA male mates directly to AWUS036ACH (no pigtail). Saves ~$13 vs AXII Quadro pair + pigtails. | **2** |
| **On-board computer (SBC)** | **NanoPi M5, 4 GB** (Rockchip RK3576, 6 TOPS) | `SBC3` | earlier | `FIXED_SBC_ID = "SBC3"` | mature RKNN toolchain + ≤10 W passive (meets power/cooling rules SBC2 fails). | **3** |


† The RX and handheld radio aren't `FIXED_*` sweep dimensions — the flight-time sweep holds the RX at a light representative (negligible endurance delta) and uses a cheapest-radio cost basis. These rows are the authoritative selection of record.

**Control ecosystem = ELRS (by choice, not requirement).** The RX (`iFlightTD`) + handheld (`TX5` TX12 MkII) + HGLRC Hermes laptop dongle (`TLM2`) are all ELRS 2.4 GHz, so the control stack is one ecosystem end-to-end. **Nothing in the model mandates ELRS** — the RF compatibility rule is band-match only — so non-ELRS remains valid; ELRS is a pragmatic preference (cheap, common laptop dongles for the GCS plan).

### Airframe variant — RESOLVED: PNP (`AF3a`) + GPS pre-installed
Chose the **PNP** variant + **GPS pre-install option** (+$39). All-up airframe mass = 729 g (~$386; no bundled receiver). External ELRS RX added separately. The airframe **bundles a BLITZ Whoop 5.8 GHz analog VTX + analog CMOS FPV camera + iFlight BLITZ M10 GPS V2 Mini** (so VTX, FPV-cam, and GPS selections are all decided by the airframe). Shared drivetrain: XING-E 2809 800KV · BLITZ F7 FC · BLITZ E55 55 A 4-in-1 ESC · HQ 9×4×3 props.

### Battery power interface — standardized on **XT60** (refined 2026-06-30)
The battery↔drone power interface is now modeled: `model.sysml` `BatteryPowerInterface` gained a **`ConnectorCompatible`** constraint, the power ports (`PowerSourcePort`/`PowerSinkPort`) carry a `connector` attribute, and `Airframe` gained `batteryConnector`. **The whole power chain is XT60:** battery → iFlight anti-spark (XT60) → Chimera9 ECO XT60 lead. Verified against the candidates — **BAT09 / BAT10 / BAT22 (the three contenders) are all XT60** ✓; only non-contenders differ (**BAT08 = XT90**, **BAT23 Tattu LiPo = EC5** → would need an adapter). Chargers (below) output XT60 or use an XT60 charge lead.

---

## 🔶 OPEN / in-progress

| Role | Status | ID(s) | Notes |
|---|---|---|---|
| **On-board DVR** | open (**Phase 2**) | `DVR9` (rep.) | **Phase 1–2 only** — at the SBC stage (**Phase 3**) the SBC records; the DVR is costed/compatibility-checked but not in the SBC-stage flight-time. |

---

## Phase 1 build (selected) — flight + FPV downlink + waypoints
| Item | Part | ~Cost |
|---|---|---|
| Airframe + GPS (bundled) | Chimera9 ECO PNP + BLITZ M10 GPS V2 Mini (`AF3a` + `G4`) | $386 |
| Extra props | HQ 9X4X3 — 4-pack | $17 |
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
| **Phase 1 subtotal** | | **~$1,355** |

*See [`BOM.md`](BOM.md) for the full phased bill of materials (all 3 phases, sorted, with per-phase subtotals). Flight-controller firmware (ArduPilot/PX4 vs Betaflight) is a configuration choice, not a procured component — TBD.*

## Support equipment (bench — reusable, not flown, not in system cost)
**Battery charger — ✅ SELECTED: HOTA D6 Pro (`CHG1`), Phase 1** (now in the LOCKED table above). Formalized in the model as a `Charger` part def + `ChargerCandidates`, composed into `AerialThermalObservationSystem` as ground-support equipment. Requirement: 6S **balance** + **Li-ion *and* LiPo** modes + XT60, with enough power for the 12 Ah packs (Li-ion ≈ 0.5C → 6 A/~133 W; LiPo 1C → 12 A/~266 W). Alternatives considered:

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
**Chimera9 ECO (AF3a PNP) + [battery TBD, leading BAT09] + T13 + SBC3** → ~58.6 min hover, ~$1,645 system (well under the $2,500 R4 cap), SBC fits the deck. See
[`analysis/flight_time_value_ranking.md`](analysis/flight_time_value_ranking.md) /
[`.csv`](analysis/flight_time_value_ranking.csv) for the full ranked loadouts.
