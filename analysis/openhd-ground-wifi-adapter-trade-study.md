# OpenHD Ground-Side WiFi Adapter — Market Analysis & Trade Study

**Role:** USB WiFi adapter plugged into the MacBook Air (Apple Silicon), passed through
via USB to an ARM64 Ubuntu 22.04 Linux VM (VMware Fusion, free personal use). Receives
the WFB-ng stream from the drone, decodes it inside the VM, and forwards the video to
the host macOS as an RTSP/UDP stream readable by VLC or QGroundControl.

**Evaluation date:** 2026-07-02  
**Sources:** WFB-ng wiki, OpenHD Gitbook, OpenIPC FPV wiki, Rokland, Amazon, Alfa community

---

## Requirements

| Requirement | Threshold |
|---|---|
| Chipset | RTL8812AU or RTL8812EU (WFB-ng officially supported) |
| Monitor mode + packet injection | Mandatory for WFB-ng RX path |
| ARM64 Ubuntu 22.04 in VM | Must work via USB passthrough through Parallels or VMware Fusion xHCI |
| External antenna connector | ≥1 standard RP-SMA female — for directional panel |
| Dual antenna ports | Preferred — enables diversity RX on two AXII Quadro panels |
| Weight | Not a constraint (stationary ground station) |
| Cost | Secondary — ground station is a one-time purchase |

### Critical VM Compatibility Note

USB WiFi monitor mode/packet injection **does work** via USB passthrough on Apple Silicon Macs,
provided:
1. The VM (VMware Fusion or Parallels Desktop) is configured for **USB 3.0 (xHCI)** controller
   mode — not USB 2.0 (EHCI). The difference: xHCI exposes the raw USB device with lower
   latency and full current delivery. EHCI causes intermittent drops at high TX/RX power.
2. The VM claims the USB device exclusively at startup (device is not shared with macOS host).
3. The DKMS driver (RTL8812AU or RTL8812EU) is installed inside the ARM64 Ubuntu guest.

**UTM (QEMU-based, free):** Not recommended for this application — USB passthrough in UTM
is less mature and has documented reliability issues with high-current WiFi adapters in
monitor mode. Use VMware Fusion (free personal) or Parallels Desktop (~$100/yr).

**macOS Realtek drivers:** Not applicable — Realtek macOS drivers are x86_64 only and do not
load on Apple Silicon. The Linux VM path is the only supported option.

---

## Candidate Table

| ID | Model | Chipset | External Connectors | USB | ARM64 VM | OpenHD/WFB-ng | Price |
|---|---|---|---|---|---|---|---|
| **W-G1** | **Alfa AWUS036ACH** | RTL8812AU | **2× RP-SMA female (standard)** | 3.0 (USB-C) | ✅ Confirmed (Parallels 20.3+, VMware Fusion, xHCI) | **Official** | **$65** |
| W-G2 | LB-LINK BL-M8812EU2 | RTL8812EU | 2× IPEX/u.fl (pigtails needed) | 2.0 | ✅ Same driver path | Official | ~$12 |
| W-G3 | ASUS USB-AC56 | RTL8812AU | 1× RP-SMA + 1× MS156 (proprietary) | 3.0 | ✅ Confirmed | Official (now discontinued) | ~$30 used |
| — | Alfa AWUS1900 | RTL8814AU | 4× RP-SMA female | 3.0 | ✅ | Listed in OpenHD docs | $65 |
| — | Alfa AWUS036ACHM | **MT7610U** | 1× RP-SMA | 2.0 | ✅ (mt76 in-kernel) | **Not supported** for WFB-ng | $40 |

### AWUS1900 disqualification note

The RTL8814AU (AWUS1900) is listed in older OpenHD docs but has documented failures in
current OpenHD builds: GitHub issue #280 "Restore support to AWUS1900" and multiple forum
threads report "no connection between RTL8814AU TX and RTL8812AU RX." Since the drone
air side uses RTL8812EU (W-A1), the ground side must be RTL8812AU or RTL8812EU for the
WFB-ng cross-chipset RX path. AWUS1900 is eliminated.

---

## Trade Study

### Scoring (1 = worst, 3 = best)

| ID | Model | Cost | Capability | Compatibility | Notes |
|---|---|---|---|---|---|
| **W-G1** | **Alfa AWUS036ACH** | 2 | **3** | **3** | Dual standard RP-SMA; canonical WFB-ng GS hardware |
| W-G2 | LB-LINK BL-M8812EU2 | **3** | 2 | **3** | Cheapest; but u.fl pigtails add wiring friction for ground station |
| W-G3 | ASUS USB-AC56 | 2 | 1 | 2 | Discontinued; MS156 proprietary port limits directional antenna attachment |

**Cost:** W-G2 is cheapest ($12); W-G1 and W-G3 at $30–65.  
**Capability:** W-G1 wins — two standard RP-SMA ports allow direct attachment of dual
directional panels for diversity receive with no adapter gymnastics.  
**Compatibility:** W-G1 and W-G2 both confirmed on ARM64 Ubuntu 22.04 via VMware Fusion
xHCI passthrough. W-G3 downgraded due to the proprietary MS156 second port.

---

## Selected: W-G1 — Alfa AWUS036ACH (~$65)

**Rationale:** The dual RP-SMA standard connectors are the deciding factor. Two Lumenier
AXII Quadro directional panels (see antenna trade study) plug directly into the two RP-SMA
ports, giving spatial diversity with no pigtail adapters. The AWUS036ACH is the most widely
documented adapter for WFB-ng ground station use, with confirmed working in Parallels
Desktop 20.3+ and VMware Fusion on Apple Silicon M-series Macs via xHCI USB 3.0 passthrough.

**VM setup:** VMware Fusion (free for personal use). Set VM USB controller to xHCI (USB 3.0).
Install `OpenHD/rtl8812au` DKMS driver in the ARM64 Ubuntu 22.04 guest. WFB-ng ground
station process outputs video as RTSP `rtsp://localhost:5600` — VLC on macOS receives it
over loopback. QGroundControl can also pull the RTSP stream from the VM.

**Candidate ID in model:** `WLAN_GND1` (Alfa AWUS036ACH, ground side)
