# Bill of Materials (BOM) — Thermal Surveillance Drone

Full procurement list, **sorted by build phase** with a subtotal per phase. Derived from
[`SELECTED_COMPONENTS.md`](SELECTED_COMPONENTS.md) (selections) and
[`candidates.sysml`](candidates.sysml) (names, IDs, links, costs). **Part #** = the model
candidate ID (the project's internal part number). Four build phases — **Phase 4 (OpenHD video downlink) is a future capability** held separate from the committed Phase 1–3 system.

> **Flight battery = `BAT10`** (Upgrade Energy 6S 12 Ah Amprius) — `BAT09` is out of stock.
> **2× `BAT22`** (GNB) are procured as development/shakedown packs (spare the Amprius on early flights).

---

## Phase 1 — Basic flight + FPV downlink + waypoints

| Product | Part # | Link | Cost |
|---|---|---|---|
| iFlight Chimera9 ECO 6S (9", PNP) — incl. **GPS + analog VTX + FPV cam + 4 extra props**, w/ shipping | `AF3a` | [shop.iflight.com](https://shop.iflight.com/Chimera9-ECO-6S-Pro2068) | $490.99 |
| HQ 9X4X3 props — 4-pack (extra set) | — | *(included w/ `AF3a`)* | $0.00 |
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
| **Phase 1 subtotal** | | | **$1,370.75** |

## Phase 2 — EO/IR thermal camera + SBC (onboard, live-inference feed)

| Product | Part # | Link | Cost |
|---|---|---|---|
| PurpleRiver Mini 640 thermal camera (640×512, 12 µm, 13 mm) | `T13` | [thermal-image.com](https://www.thermal-image.com/product/mini-640-uncooled-lwir-thermal-camera-module/) | $650.00 |
| NanoPi M5, 4 GB SBC (Rockchip RK3576) — real-time onboard AI inference (thermal via USB-UVC) | `SBC3` | [friendlyelec.com](https://www.friendlyelec.com/index.php?route=product/product&path=69&product_id=309) | $126.00 |
| SBC mount + cooling (3D-printed deck + 30 mm fan + heat-set hardware) | — | fabricated ([reference/cad-resources.md](reference/cad-resources.md)) | ~$15.00 |
| SBC power — 2-6S→12V 3A UBEC (2-pack) | — | [amazon.com](https://www.amazon.com/2pcs-2S-6S-DC-DC-Converter-Module/dp/B0CTZHJR5L) | $9.99 |
| SBC power — USB-C power-only cable (bare wire→USB-C male, 20AWG 5A) | — | [amazon.com](https://www.amazon.com/USB-C-Power-Copper-Connector-Device/dp/B0GBGLNR52) | $7.99 |
| **Phase 2 subtotal** | | | **~$808.98** |

## Phase 3 — AI detection + autonomous route modification (software)

| Product | Part # | Link | Cost |
|---|---|---|---|
| All hardware on-board since Phase 2. Phase 3 is software-only: deploy INT8-quantized model via RKNN toolchain, integrate MAVLink autonomous route modification. | — | — | $0.00 |
| **Phase 3 subtotal** | | | **$0.00** |

## Phase 4 — Future capability: OpenHD digital video downlink to ground station

> **Deferred / future capability (moved here 2026-07-07).** Phases 1–3 are the committed build.
> Phase 4 adds a live digital downlink of the thermal (and/or AI-annotated) video to the ground
> station via OpenHD/WFB-ng. Held separate so its cost is **not** part of the committed system.

| Product | Part # | Link | Cost |
|---|---|---|---|
| LB-LINK BL-M8812EU2 RTL8812EU bare WiFi module (air side) + USB-A stub + 2× u.fl→RP-SMA pigtails | `WLAN_AIR1` | [aliexpress.com](https://www.aliexpress.com/item/1005007098141054.html) | ~$20.00 |
| Air-side antennas — 5.8 GHz RHCP cloverleaf, RP-SMA male × 2 (pair) | — | [amazon.com](https://www.amazon.com/5-8GHz-Cloverleaf-Antenna-Receiver-Transmitter/dp/B0CDZ8FXFW) | $13.99 |
| Alfa AWUS036ACH RTL8812AU USB-C WiFi adapter (ground side) | `WLAN_GND1` | [rokland.com](https://store.rokland.com/products/alfa-awus036ach-usb-c-802-11ac-ac1200-dual-band-high-power-wifi-usb-adapter) | $65.00 |
| Foxeer Echo 2 Max 5.8 GHz linear patch antenna × 2 (ground diversity, 60° beam, RP-SMA male) | `ANT_GND1` + `ANT_GND2` | [foxeer.com](https://www.foxeer.com/foxeer-echo-2-max-high-gain-antenna-g-434) | $60.00 |
| Air-module 5 V power — spare 2nd unit of the Phase 2 UBEC 2-pack (set to 5 V) | — | *(already procured in Phase 2)* | $0.00 |
| VMware Fusion (ground station VM — free personal use) | — | vmware.com | $0.00 |
| **Phase 4 subtotal** | | | **~$158.99** |

---

## Totals

| Phase | Subtotal |
|---|---|
| Phase 1 — flight + FPV + waypoints | $1,370.75 |
| Phase 2 — thermal + SBC (onboard) | ~$808.98 |
| Phase 3 — AI deployment (software only) | $0.00 |
| **Committed system subtotal (Phases 1–3)** | **~$2,179.73** |
| Phase 4 — OpenHD downlink (*future capability*) | ~$158.99 |
| **Grand total (all four phases)** | **~$2,338.72** |

**R4 integrated-system cost** (phase grand total minus **reusable/support items** — the 2× `BAT22`
development packs ($220) and the `CHG1` charger ($112)):
- **Committed (Phases 1–3): ≈ $1,848** (≤ $2,500 ✓)
- **With Phase 4 (all four phases): ≈ $2,007** (≤ $2,500 ✓)

Both are under the $2,500 R4 cap.

## Next steps
- **OpenHD → Phase 4 (2026-07-07):** the OpenHD digital video-downlink capability (`WLAN_AIR1`,
  air/ground antennas, `WLAN_GND1`, VMware VM) was moved to a **future Phase 4**. The committed
  build (Phases 1–3) is analog FPV for piloting + thermal→SBC **live onboard inference**, with **no
  thermal downlink and no onboard recording**. Phase 4 prices (WLAN_AIR1, WLAN_GND1, Foxeer) remain
  estimates — confirm before building Phase 4.
- **Phase 2** — T13 confirmed $650.00 ($590 base + $60 shipping) as the **USB** variant (thermal →
  SBC over USB-UVC for live inference; MIPI and CVBS were evaluated and rejected — see
  [`MODEL_ISSUES.md`](MODEL_ISSUES.md)).
- **Phase 3** — software-only (RKNN model deployment + MAVLink autonomous route modification), $0
  hardware; runs live inference on the Phase 2 thermal feed.
- **SBC power — RESOLVED (2026-07-06):** the NanoPi M5 USB-C port accepts wide-input DC 6–20 V
  *without PD negotiation* (onboard buck), so no PD-trigger module is needed. **Selected + priced:**
  2-6S→12V 3A UBEC 2-pack ($9.99) + USB-C power-only cable ($7.99) — $17.98 total. The 2-pack's
  spare unit (set to 5 V) powers the Phase 4 air WiFi module. Build check: UBEC jumper on 12 V (not
  5 V) before connecting the SBC. The T13 thermal cam needs no power part — USB-bus-powered (<1 W).

## Notes
- **Part # = model candidate ID** (the internal part number in [`candidates.sysml`](candidates.sysml));
  "—" = no catalog part yet (generic/fabricated/TBD).
- **Battery:** `BAT10` is the flight default (`BAT09` out of stock); the **2× `BAT22`** are
  development/shakedown packs (cheap, robust — fly these first, spare the Amprius).
- **Bundled at $0:** the FPV camera + analog VTX + GPS + 4 extra props all ship with the Chimera9
  ECO — their cost is folded into the single airframe line at **$490.99** (incl. shipping; GPS =
  iFlight BLITZ M10 GPS V2 Mini, `G4`). The separate props line is therefore $0. **Existing at $0:**
  the MacBook Air GCS.
- **No recording / no DVR:** the thermal feed is **not recorded** — it streams live from the T13
  (USB-UVC) to the SBC (`SBC3`) for **real-time inference** that drives autonomous actions (Phase 3).
  The standalone DVR (`DVR9`) was dropped 2026-07-05; with live-inference-only there is no recording
  device in the architecture at all.
- **TBD lines:** the flight-controller firmware (ArduPilot/PX4 vs Betaflight — a configuration
  choice, no cost).
- The flight-time sweep reports ~$1,690 for the drone + GCS using *cost-representative* RX/radio;
  this BOM uses the **actual selected** parts (iFlight TD RX + TX12 MkII radio) plus GPS, dongle,
  charger, adapter, dev batteries, and the SBC mount — hence the higher, complete figure.