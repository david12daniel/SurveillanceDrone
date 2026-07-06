# Bill of Materials (BOM) — Thermal Surveillance Drone

Full procurement list, **sorted by build phase** with a subtotal per phase. Derived from
[`SELECTED_COMPONENTS.md`](SELECTED_COMPONENTS.md) (selections) and
[`candidates.sysml`](candidates.sysml) (names, IDs, links, costs). **Part #** = the model
candidate ID (the project's internal part number). Three phases.

> **Flight battery = `BAT10`** (Upgrade Energy 6S 12 Ah Amprius) — `BAT09` is out of stock.
> **2× `BAT22`** (GNB) are procured as development/shakedown packs (spare the Amprius on early flights).

---

## Phase 1 — Basic flight + FPV downlink + waypoints

| Product | Part # | Link | Cost |
|---|---|---|---|
| iFlight Chimera9 ECO 6S (9", PNP) + **GPS pre-installed** | `AF3a` | [shop.iflight.com](https://shop.iflight.com/Chimera9-ECO-6S-Pro2068) | $457.99 |
| HQ 9X4X3 props — 4-pack (extra set) | — | shop.iflight.com / HQ | $17.00 |
| iFlight True Diversity ELRS receiver | `iFlightTD` | [shop.iflight.com](https://shop.iflight.com/) | $31.99 |
| RadioMaster TX12 Mark II ELRS radio | `TX5` | [radiomasterrc.com](https://www.radiomasterrc.com/products/tx12) | $117.93 |
| HGLRC Hermes ELRS SIM USB Dongle — primary laptop control + telemetry | `TLM2` | [amazon.com](https://www.amazon.com/s?k=HGLRC+Hermes+ELRS+USB+dongle) | $16.00 |
| Battery **(flight)** — Upgrade Energy GREEN V2 6S3P 12 Ah Amprius | `BAT10` | [upgrade-energy.com](https://www.upgrade-energy.com/) | $275.00 |
| Battery **(development, ×2)** — GNB 6S3P 12 Ah 21700 Li-ion | `BAT22` | [gaoneng.shop](https://www.gaoneng.shop/products/gaoneng-gnb-6s-22.2v-12000mah-10c-xt60-li-ion-battery-made-with-li-ion-lithium-ion-21700) | $220.00 |
| Skydroid 5.8 GHz 150CH UVC receiver (**dual antenna**) | `VRX6` | [alibaba.com](https://www.alibaba.com/product-detail/SKYDROID-5-8GHz-FPV-Receiver-UVC_1601393061166.html) *(select dual-antenna variant; confirm price at checkout)* | ~$44.45 |
| TrueRC X-AIR 5.8 MK II RHCP patch antenna | `PATCH1` | [truerc.com](https://truerc.com/63425-x-air-58-mk-ii-rp-sma) | $36.85 |
| iFlight Anti Spark Filter (XT60, 150 A) | `ASF1` | [shop.iflight.com](https://shop.iflight.com/index.php?route=product/product&product_id=3474) | $14.99 |
| HOTA D6 Pro battery charger | `CHG1` | [hotarc.com](https://www.amazon.com/gp/product/B0FLXL4SZW/ref=ox_sc_act_image_1?smid=A10OEFIP1P2D8&th=1) | $111.55 |
| USB-A→USB-C adapter (MacBook Air) | — | generic | $11.00 |
| FPV camera + 5.8 GHz analog VTX | *(bundled w/ `AF3a`)* | — | $0.00 |
| GCS laptop (existing MacBook Air) | — | — | $0.00 |
| **Phase 1 subtotal** | | | **$1,354.75** |

## Phase 2 — EO/IR thermal camera + SBC + OpenHD digital downlink

| Product | Part # | Link | Cost |
|---|---|---|---|
| PurpleRiver Mini 640 thermal camera (640×512, 12 µm, 13 mm) | `T13` | [thermal-image.com](https://www.thermal-image.com/product/mini-640-uncooled-lwir-thermal-camera-module/) | $650.00 |
| NanoPi M5, 4 GB SBC (Rockchip RK3576) — onboard recording + AI inference | `SBC3` | [friendlyelec.com](https://www.friendlyelec.com/index.php?route=product/product&path=69&product_id=309) | $126.00 |
| SBC mount + cooling (3D-printed deck + 30 mm fan + heat-set hardware) | — | fabricated ([reference/cad-resources.md](reference/cad-resources.md)) | ~$15.00 |
| LB-LINK BL-M8812EU2 RTL8812EU bare WiFi module (air side) + USB-A stub + 2× u.fl→RP-SMA pigtails | `WLAN_AIR1` | [aliexpress.com](https://www.aliexpress.com/item/1005007098141054.html) | ~$20.00 |
| Alfa AWUS036ACH RTL8812AU USB-C WiFi adapter (ground side) | `WLAN_GND1` | [rokland.com](https://store.rokland.com/products/alfa-awus036ach-usb-c-802-11ac-ac1200-dual-band-high-power-wifi-usb-adapter) | $65.00 |
| Foxeer Echo 2 Max 5.8 GHz linear patch antenna × 2 (ground diversity, 60° beam, RP-SMA male) | `ANT_GND1` + `ANT_GND2` | [foxeer.com](https://www.foxeer.com/foxeer-echo-2-max-high-gain-antenna-g-434) | $60.00 |
| VMware Fusion (ground station VM — free personal use) | — | vmware.com | $0.00 |
| **Phase 2 subtotal** | | | **~$936.00** |

## Phase 3 — AI detection + autonomous route modification (software)

| Product | Part # | Link | Cost |
|---|---|---|---|
| All hardware on-board since Phase 2. Phase 3 is software-only: deploy INT8-quantized model via RKNN toolchain, integrate MAVLink autonomous route modification. | — | — | $0.00 |
| **Phase 3 subtotal** | | | **$0.00** |

---

## Totals

| Phase | Subtotal |
|---|---|
| Phase 1 — flight + FPV + waypoints | $1,354.75 |
| Phase 2 — thermal + SBC + OpenHD digital downlink | ~$936.00 |
| Phase 3 — AI deployment (software only) | $0.00 |
| **Grand total (all procurement)** | **~$2,290.75** |

**R4 integrated-system cost ≈ $1,960** (≤ $2,500 ✓) — the grand total minus **reusable/support
items not part of the per-drone flight system**: the 2× `BAT22` development packs ($220) and
the `CHG1` charger ($100). Both totals are under the $2,500 R4 cap.

## Next steps
- **Phase 2 pricing** — T13 updated to $650.00 ($590 base + $60 shipping, confirmed 2026-07-05).
  DVR9 removed from architecture — SBC handles onboard recording (moved from Phase 3).
  Remaining items: confirm actual purchase prices for WLAN_AIR1, WLAN_GND1, and Foxeer Echo 2 Max
  antennas; update candidates.sysml cost_USD and BOM subtotal accordingly.
- **Phase 3 pricing** — all hardware procured in Phase 2; Phase 3 is software-only (RKNN model
  deployment, MAVLink integration), $0 hardware.
- Recompute grand total and R4 system cost once remaining Phase 2 prices are confirmed.

## Notes
- **Part # = model candidate ID** (the internal part number in [`candidates.sysml`](candidates.sysml));
  "—" = no catalog part yet (generic/fabricated/TBD).
- **Battery:** `BAT10` is the flight default (`BAT09` out of stock); the **2× `BAT22`** are
  development/shakedown packs (cheap, robust — fly these first, spare the Amprius).
- **Bundled at $0:** the FPV camera + analog VTX ship with the Chimera9 ECO PNP. **GPS is now
  pre-installed** (iFlight BLITZ M10 GPS V2 Mini, `G4`; cost folded into the airframe line at
  $457.99 incl. shipping). **Existing at $0:** the MacBook Air GCS.
- **DVR removed:** the standalone Monster UVC Recorder (`DVR9`) was dropped from the architecture
  (2026-07-05). The SBC (`SBC3`) handles all onboard recording via USB-UVC from the T13 thermal
  camera, eliminating the need for a separate DVR.
- **TBD lines:** the flight-controller firmware (ArduPilot/PX4 vs Betaflight — a configuration
  choice, no cost).
- The flight-time sweep reports ~$1,690 for the drone + GCS using *cost-representative* RX/radio;
  this BOM uses the **actual selected** parts (iFlight TD RX + TX12 MkII radio) plus GPS, dongle,
  charger, adapter, dev batteries, and the SBC mount — hence the higher, complete figure.