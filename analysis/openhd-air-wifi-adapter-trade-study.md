# OpenHD Air-Side WiFi Adapter — Market Analysis & Trade Study

**Role:** USB WiFi adapter mounted on the NanoPi M5 SBC (drone airframe). Transmits the
encoded thermal video stream to the ground station via WFB-ng (monitor-mode raw packet
injection at 5825 MHz / channel 165, ~7 Mbit/s at MCS1).

**Evaluation date:** 2026-07-02  
**Sources:** WFB-ng wiki, OpenHD Gitbook, OpenIPC FPV wiki, PX4 docs, AliExpress, Rokland

---

## Requirements

| Requirement | Threshold |
|---|---|
| Chipset | RTL8812AU or RTL8812EU (WFB-ng author officially tests both) |
| Monitor mode + packet injection | Mandatory (WFB-ng TX path) |
| ARM64 Ubuntu 22.04 driver | DKMS or in-kernel (NanoPi M5 runs Ubuntu 22.04 ARM) |
| USB standard | USB 2.0 minimum (WFB-ng bandwidth ≪ USB 2.0 ceiling) |
| TX power | ≥ 27 dBm (500 mW) at 5.8 GHz for 3–5 km link |
| Mass | Minimize — every gram on the drone costs flight time |
| Cost | Minimize — already using budget on T13 ($650) and SBC3 ($126) |

---

## Candidate Table

| ID | Model | Chipset | TX Power | Mass | USB | ARM64 Driver | OpenHD/WFB-ng | Connector | Price |
|---|---|---|---|---|---|---|---|---|---|
| **W-A1** | **LB-LINK BL-M8812EU2** | RTL8812EU | >29 dBm (800 mW+) | **~18 g** | 2.0 | DKMS `OpenHD/rtl88x2eu` | **Official** — WFB-ng author's own test hardware | 2× IPEX/u.fl | **~$12** |
| W-A2 | Taobao bare RTL8812AU card | RTL8812AU | 27 dBm (500 mW) | ~15–25 g | 2.0 | DKMS `OpenHD/rtl8812au` | Official | 2× u.fl | ~$15 |
| W-A3 | Generic RTL8812AU high-power module | RTL8812AU | 32 dBm (1.5–1.8 W) with PA | ~20 g | 3.0 | DKMS `OpenHD/rtl8812au` | Community | 2× u.fl | ~$25 |
| W-A4 | ASUS USB-AC56 | RTL8812AU | 27 dBm | ~50 g | 3.0 | DKMS `OpenHD/rtl8812au` | **Top OpenHD recommendation** (legacy, now discontinued) | 1× RP-SMA + 1× MS156 | ~$30 used |
| W-A5 | Alfa AWUS036ACH | RTL8812AU | 27 dBm | ~90–100 g (w/ antennas) | 3.0 (USB-C) | DKMS `OpenHD/rtl8812au` | Official | 2× RP-SMA | $65 |
| — | Alfa AWUS036ACHM | **MT7610U** | ~20 dBm | ~30 g | 2.0 | in-kernel mt76 | **Not supported** — wrong chipset | 1× RP-SMA | $40 |
| — | RTL8812BU adapters (TP-Link T4U v2, etc.) | RTL8812BU | ~23 dBm | varies | 3.0 | DKMS (exists) | **Eliminated** — packet injection unreliable; WFB-ng author marks "at your own risk" | varies | $25–40 |
| — | MT7612U adapters | MT7612U | ~20 dBm | ~30 g | 3.0 | patched `morrownr/7612u` | **Eliminated** — not on WFB-ng supported list; mixed results | RP-SMA (some) | $18–25 |

---

## Trade Study

### Scoring (1 = worst, 3 = best)

| ID | Model | Cost | Capability | Compatibility | Notes |
|---|---|---|---|---|---|
| **W-A1** | **LB-LINK BL-M8812EU2** | **3** | **3** | **3** | Highest TX power, lightest, cheapest, official support |
| W-A2 | Taobao bare RTL8812AU | **3** | 2 | **3** | Requires Taobao agent; soldered wiring; quality variable |
| W-A3 | Generic high-power RTL8812AU | 2 | **3** | 2 | PA gives range boost; less community-documented on ARM64 |
| W-A4 | ASUS USB-AC56 | 2 | 1 | **3** | Discontinued; 50 g; MS156 proprietary secondary port |
| W-A5 | Alfa AWUS036ACH | 1 | 1 | **3** | 90–100 g with antennas — prohibitively heavy for air side |

**Cost:** W-A1/W-A2 at $12–15 score highest; W-A5 at $65 lowest.  
**Capability:** Dominated by TX power and mass. W-A1 wins both (>29 dBm, 18 g). W-A5 loses on mass despite solid TX power.  
**Compatibility:** W-A1 and W-A2 both use officially supported chipsets with confirmed ARM64 DKMS paths.

### Key compatibility flags

- **RTL8812EU ARM64 driver note (W-A1) — VERIFIED 2026-07-06:** aarch64 is a first-class
  build target. The `OpenHD/rtl88x2eu` Makefile carries explicit `CONFIG_PLATFORM_ARM64`
  / `CONFIG_PLATFORM_ARM64_RPI` flags (default off; set `CONFIG_PLATFORM_I386_PC = n` +
  `CONFIG_PLATFORM_ARM64_RPI = y`, then `make`/DKMS) — the same path used on aarch64
  Raspberry Pi 4/5. **The previously-cited "issue #9" does not exist** (the repo has 0 open
  issues / only closed PRs; upstream `svpcom/rtl8812eu` #9 is 404) — that citation was
  spurious and is retracted. Only real variable: DKMS build against the running Ubuntu 22.04
  kernel headers (5.15/6.x — in range). Not a procurement blocker.
- **USB current draw — VERIFIED 2026-07-06:** the NanoPi M5's USB-A ports are USB 3.2 Gen 1
  with **1.5 A per-port over-current protection**; the BL-M8812EU2 draws ~1 A at max TX,
  comfortably under that. Powered by the board's 12 V/3 A UBEC (36 W ≫ ~16 W total load).
  No separate adapter regulator needed. **Note: both M5 USB-A ports are then consumed**
  (this adapter + the T13 thermal cam) — zero spare USB.
- **TX power cap:** Set `driver_txpower_override` to 40–50 in WFB-ng config; >50
  causes PA clipping (not more range, just harmonic distortion).

---

## Selected: W-A1 — LB-LINK BL-M8812EU2

**Rationale:** Best combined score on all three drivers. An order-of-magnitude lighter than
any consumer USB adapter (18 g vs 50–100 g), highest TX power (>29 dBm), cheapest (~$12),
and is the WFB-ng author's own validated hardware. The bare-PCB form factor requires a
USB-A cable stub and two u.fl→RP-SMA pigtails (~$5–8 total) plus a small heatsink — a
five-minute assembly, not a solder job.

**Integration note:** Mounts directly to the SBC (NanoPi M5) via a USB-A port.
Air-side antennas: two u.fl→RP-SMA pigtails terminated in 2.4/5.8 GHz cloverleaf omnidirec­tional
antennas pointing down through the airframe arms (away from carbon-fibre shielding).

**Candidate ID in model:** `WLAN_AIR1` (LB-LINK BL-M8812EU2, air side)
