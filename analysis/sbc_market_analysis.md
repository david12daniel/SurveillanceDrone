# SBC Market Analysis — Phase 1 Component Selection  
*Updated 2026-06-11 — filtered for inference capability, budgets relaxed*

**Purpose:** Identify commercially-available single-board computer modules capable of:
1. On-drone thermal image detection/classification at **≥25 Hz** (SEP Phase 4 requirement)
2. Accepting video input from the selected thermal camera (CVBS analog or USB UVC)
3. Justifying total system cost impact — budgets relaxed for the right solution

**NOTE from David:** Budets for SBC subsystem can be relaxed. Weight and power still matter for airframe payload capacity and flight time, but we want the *right* inference-capable SBC first and foremost.

---

## Requirement Summary

| Requirement | Phase 1–3 | Phase 4 (Inference) |
|---|---|---|
| **R4_SBC_VIDEO_IN** | N/A — DVR records from thermal camera directly | Must accept CVBS or USB UVC from thermal camera |
| **R4_SBC_VIDEO_PROC** | N/A | Process for live GCS downlink w/o excessive delay |
| **R4_SBC_DATA_AF** | N/A | UART-based MAVLink telemetry to flight controller |
| **Onboard inference** | N/A | ≥ 25 Hz detection/classification on thermal video |

**Soft constraints (relaxed for inference-capable options):**
- Mass: ≤ 100 g preferred, up to ~150 g workable with strong justification
- Power: ≤ 10 W preferred, up to ~15 W acceptable if flight time still meets R6
- Cost: ≤ $150 preferred, up to ~$300 workable if inference requirement cannot be met cheaper

---

## Thermal Camera Output Format

Leading candidates output **CVBS analog** (composite video) or **USB 2.0** (UVC-compatible). Most need a CVBS-to-USB video capture dongle (~$15, ~10 g) unless using USB UVC direct mode.

---

## Candidates That Support Inference (≥25 Hz)

### 1. Radxa Zero 2 Pro — $75 board / ~$113 total ✅

**NPU:** 5 TOPS @ INT8 (Amlogic A311D — TensorFlow, Caffe, ONNX)

| Item | Cost | Mass |
|---|---|---|
| Radxa Zero 2 Pro (4 GB) | $75 | 30 g |
| microSD (32 GB) | $8 | 1 g |
| USB-C to USB-A adapter cables (×2) | $8 | 8 g |
| CVBS-to-USB capture dongle | $15 | 10 g |
| Heatsink (included) | $0 | 5 g |
| Cabling, connectors | $7 | 5 g |
| **Total** | **$113** | **~59 g** |

| Metric | Value | Check |
|---|---|---|
| **Mass** | **~59 g** | ✅ Under 100 g soft limit |
| **Power (video + NPU)** | **~8.5–10.5 W** | ✅ Under 10 W preferred limit |
| **Cost** | **$113** | ✅ Under $150 preferred limit |
| **Inference** | **5 TOPS NPU** | ✅ MobileNet SSD at 30–60+ FPS |
| **RAM** | 4 GB LPDDR4 | ✅ |
| **WiFi** | WiFi 5 + BT 5.0 | ✅ Built-in |

**Pros:** All budget constraints met with margin. 5 TOPS NPU is sufficient. Tiny footprint (65×36 mm). Passive heatsink only.
**Cons:** Both USB ports are Type-C (needs adapters). Smaller community than Pi or Jetson. NPU SDK less mature than NVIDIA's.

**Verdict: ✅ Easiest fit. The only candidate that satisfies all relaxed budgets without compromise.**

---

### 2. Orange Pi 5 — $80–110 board / ~$120–150 total ✅

**NPU:** 6 TOPS @ INT8 (Rockchip RK3588S — TensorFlow, ONNX, PyTorch via RKNN)

| Item | Cost | Mass |
|---|---|---|
| Orange Pi 5 (8 GB RAM) | $100 | ~50 g (estimate for 8-layer PCB + heatsink) |
| microSD (32 GB) | $8 | 1 g |
| CVBS-to-USB capture dongle | $15 | 10 g |
| Heatsink + 5V fan (recommended) | $10 | 12 g |
| Cabling, connectors | $7 | 5 g |
| **Total** | **~$140** | **~78 g** |

| Metric | Value | Check |
|---|---|---|
| **Mass** | **~78 g** | ✅ Under 100 g soft limit |
| **Power (idle)** | **~3–5 W** | ✅ |
| **Power (load + NPU)** | **~8–12 W** | ⚠️ Can exceed 10 W under heavy load |
| **Cost** | **~$140** | ✅ Under $150 preferred |
| **Inference** | **6 TOPS NPU (RK3588S)** | ✅ More powerful than Radxa Zero 2 Pro |
| **RAM** | 8 GB LPDDR4X | ✅ |
| **USB** | 2× USB 3.0 + 2× USB 2.0 | ✅ Plenty of ports, no adapters needed |
| **WiFi** | Built-in (dual-band) | ✅ |

**Pros:** RK3588S is the most powerful SoC in this price range. 6 TOPS NPU handles heavier thermal models. 8 GB RAM is generous. Full-sized USB ports (no adapters). Excellent community — RK3588 has deep documentation.
**Cons:** ~78 g total is heavier than Radxa. Higher power draw (~12 W max with NPU + full CPU). Larger form factor (90×62 mm vs Radxa 65×36 mm). May need passive heatsink + small fan.

**Verdict: ✅ Strongest inference performance. More USB ports, more RAM, more NPU headroom. Heavier and higher power but still within relaxed limits.**

---

### 3. Orange Pi 5 Plus — $120–170 board / ~$165–215 total ⚠️

**NPU:** Same RK3588 (not S variant) — up to 6 TOPS @ INT8, more I/O

| Item | Cost | Mass |
|---|---|---|
| Orange Pi 5 Plus (8 GB) | $150 | ~55 g (larger board) |
| microSD (32 GB) | $8 | 1 g |
| CVBS-to-USB capture dongle | $15 | 10 g |
| Heatsink + fan | $12 | 15 g |
| Cabling, connectors | $7 | 5 g |
| **Total** | **~$192** | **~86 g** |

| Metric | Value | Check |
|---|---|---|
| **Mass** | **~86 g** | ✅ Under 100 g |
| **Power** | **~10–15 W** | ⚠️ High |
| **Cost** | **~$192** | ⚠️ Above $150 preferred, but within relaxed budget |
| **Inference** | **6 TOPS NPU** | ✅ |

**Pros:** Same RK3588 NPU as Orange Pi 5 but with PCIe 3.0, dual HDMI, more connectivity. Can add Coral TPU via M.2 slot for even more inference.
**Cons:** Larger and more expensive than Orange Pi 5 with no inference benefit. The Orange Pi 5 (non-Plus) gives the same NPU for ~$50 less.

**Verdict: ⚠️ Overkill. Same NPU as Orange Pi 5 at higher cost and size. Not worth the premium.**

---

### 4. FriendlyELEC NanoPi M5 — $65–87 board / ~$105–130 total ✅

**NPU:** 6 TOPS @ INT8 (Rockchip RK3576 — quad A72 + quad A53)

| Item | Cost | Mass |
|---|---|---|
| NanoPi M5 (4 GB) | $87 | 58 g (board only) |
| microSD (32 GB) | $8 | 1 g |
| CVBS-to-USB capture dongle | $15 | 10 g |
| Cabling, connectors | $5 | 5 g |
| **Total (if M.2 WiFi added)** | **~$116 + $9 (WiFi module)** | **~80 g** |
| **Total (bare board, no WiFi dongle)** | **~$115** | **~74 g** |

| Metric | Value | Check |
|---|---|---|
| **Mass** | **~74–80 g** | ✅ Under 100 g |
| **Power** | **~6–10 W** (estimate, RK3576 is 8 nm) | ✅ Lower than RK3588 |
| **Cost** | **~$115–125** | ✅ Under $150 |
| **Inference** | **6 TOPS NPU (RK3576)** | ✅ 8 nm process, very efficient |
| **RAM** | 4 GB LPDDR4X | ✅ |
| **USB** | 2× USB 3.2 Gen 1 | ✅ Full-size ports |
| **WiFi** | ❌ Optional M.2 SDIO module (+$9) | ⚠️ |

**Pros:** RK3576 is an 8 nm chip — very power-efficient. 6 TOPS NPU is identical in performance to RK3588S in AI workloads. 2× full-size USB 3.0. Only 58 g board. Two Ethernet ports (useful for ground testing).
**Cons:** No built-in WiFi (+$9 module). Smaller community than Orange Pi. Newer SoC (2024) — less software maturity for the NPU SDK.

**Verdict: ✅ Best efficiency option for RK3588-class NPU. Lower power draw than Orange Pi 5 at the same 6 TOPS. Needs WiFi module.**

---

### 5. FriendlyELEC NanoPi M6V2 — $172 board / ~$210 total ⚠️

**NPU:** 6 TOPS @ INT8 (Rockchip RK3588S)

| Item | Cost | Mass |
|---|---|---|
| NanoPi M6V2 (8 GB) | $172 | ~60 g (estimate) |
| WiFi module (+$6.90) | $7 | 3 g |
| microSD (32 GB) | $8 | 1 g |
| CVBS-to-USB capture dongle | $15 | 10 g |
| Cabling, connectors | $7 | 5 g |
| **Total** | **~$210** | **~79 g** |

| Metric | Value | Check |
|---|---|---|
| **Mass** | **~79 g** | ✅ Under 100 g |
| **Power** | **~8–12 W** | ⚠️ Same as Orange Pi 5 |
| **Cost** | **~$210** | ❌ Above relaxed budgets |
| **Inference** | **6 TOPS NPU (RK3588S)** | ✅ Same as Orange Pi 5 |

**Verdict: ❌ More expensive than Orange Pi 5 for the same NPU. Pass.**

---

### 6. NVIDIA Jetson Nano (B01 Module) — ~$300–360 total ❌ with $150 budget, ⚠️ with relaxed budget

**GPU:** 128 CUDA cores (Maxwell), 4 GB RAM, no dedicated NPU

| Item | Cost | Mass |
|---|---|---|
| Jetson Nano B01 module | $196 | 25 g |
| Third-party mini carrier | $50–100 | 40–60 g |
| M.2 WiFi card + antenna | $30 | 8 g |
| Heatsink + fan (required) | $12 | 15 g |
| CVBS-to-USB capture dongle | $15 | 10 g |
| Cabling, connectors | $10 | 10 g |
| **Total** | **~$313–363** | **~108–128 g** |

| Metric | Value | Check (relaxed) |
|---|---|---|
| **Mass** | **~108–128 g** | ❌ Over relaxed 150 g if carrier is heavy. Barely possible with ultra-mini carrier |
| **Power** | **~10–15 W** | ⚠️ Over 10 W preferred, at edge of 15 W relaxed |
| **Cost** | **~$313+** | ⚠️ Well over $150, but within relaxed. Still painful |
| **Inference** | **128 CUDA cores** | ✅ TensorRT is mature and well-supported |
| **RAM** | 4 GB LPDDR4 | ✅ |
| **WiFi** | ❌ M.2 Key E (needs card) | ⚠️ |

**Pros:** NVIDIA TensorRT is the gold standard for edge AI inference. CUDA ecosystem is mature and well-documented. Many thermal detection models already exist for Jetson.
**Cons:** Module alone costs $196. Mandatory carrier board adds cost and weight. Active cooling fan required (failure risk). Still over budget even with relaxed limits. The oldest Jetson platform — Orin is the current gen.

**Verdict: ⚠️ Only if you specifically need CUDA/TensorRT toolchain and have the weight/power margin. The Orange Pi 5 or NanoPi M5 give similar inference performance at half the cost with no active cooling.**

---

### 7. Pi 4 + Coral USB Accelerator — $105 board + $60 Coral = ~$170 total ⚠️

| Item | Cost | Mass |
|---|---|---|
| Raspberry Pi 4 (2 GB) | $45 | 46 g |
| Coral USB Accelerator (Edge TPU) | $60 | 27 g |
| microSD (32 GB) | $8 | 1 g |
| CVBS-to-USB capture dongle | $15 | 10 g |
| Heatsink (passive) | $5 | 8 g |
| Cabling, connectors | $7 | 5 g |
| **Total** | **~$140** | **~97 g** |

| Metric | Value | Check |
|---|---|---|
| **Mass** | **~97 g** | ✅ Under 100 g |
| **Power** | **~10–11 W** (Pi ~8.5W + Coral ~2.5W) | ⚠️ At edge |
| **Cost** | **~$140** | ✅ Under $150 |
| **Inference** | **4 TOPS Edge TPU** | ✅ MobileNet SSD at 30+ FPS |
| **RAM** | 2 GB | ⚠️ Tight for video pipeline + inference |
| **USB** | 4× USB | ✅ Coral + dongle + room to spare |

**Pros:** Leverages the massive Pi ecosystem. Coral Edge TPU is well-documented with TFLite. The entire drone community knows Pi.
**Cons:** 97 g is barely under 100 g. 11 W at load is over 10 W. Coral USB Accelerator is another USB dongle to cable. 2 GB RAM with Coral TFLite + OpenCV video pipeline is tight. Coral is an aging product (Google has de-emphasized it in favor of their own NPU IP).

**Verdict: ⚠️ Works on paper, tight on all margins. Viable backup if you already have a Pi 4 and Coral in-hand. Otherwise the Radxa Zero 2 Pro or Orange Pi 5 are better.**

---

## Quick Comparison

| Candidate | Total Cost | Total Mass | Load Power | NPU | Video | Notes |
|---|---|---|---|---|---|---|
| **Radxa Zero 2 Pro** | **$113** ✅ | **59 g** ✅ | **~10 W** ✅ | **5 TOPS** | USB-C (needs adapter) | Best all-around fit |
| **Orange Pi 5 (8 GB)** | **~$140** ✅ | **~78 g** ✅ | **~10–12 W** ⚠️ | **6 TOPS** | USB-A (no adapter) | Best inference |
| **NanoPi M5 (4 GB)** | **~$125** ✅ | **~80 g** ✅ | **~6–10 W** ✅ | **6 TOPS** | USB-A | Most efficient |
| **Orange Pi 5 Plus** | **~$192** ⚠️ | **~86 g** ✅ | **~10–15 W** ⚠️ | **6 TOPS** | USB-A | Same NPU, costs more |
| **NanoPi M6V2** | **~$210** ❌ | **~79 g** ✅ | **~8–12 W** ⚠️ | **6 TOPS** | USB-A | Same as OP5, pricier |
| **Pi 4 + Coral USB** | **~$140** ✅ | **~97 g** ⚠️ | **~11 W** ⚠️ | **4 TOPS** | USB-A | Tight margins, aging |
| **Jetson Nano** | **~$313+** ❌ | **~108–128 g** ❌ | **10–15 W** ⚠️ | **128 CUDA** | USB-A | CUDA ecosystem, but old/heavy/pricey |

---

## Assessment for Budget Impact

### Winner: 3-Way Tie for Inference-Capable SBC

**🥇 Orange Pi 5 (8 GB) — ~$140 total** — *Best all-around*

The RK3588S NPU (6 TOPS) is the most capable in the field, 8 GB RAM is generous, and the full-size USB ports mean no adapter hassle. Weight at ~78 g is fine. Power at ~12 W under heavy load is acceptable with relaxed budgets. Largest community of the RK3588 boards.

**🥇 Radxa Zero 2 Pro — ~$113 total** — *Best fit for tight budgets*

Smallest, lightest (59 g), lowest power (~10 W), and cheapest ($113). The 5 TOPS NPU is sufficient for MobileNet SSD at 30–60 FPS — well over the 25 Hz requirement. Fits the original $150/100g/10W budgets without needing to relax them.

**🥇 NanoPi M5 — ~$125 total** — *Best efficiency*

RK3576 at 8 nm gives the same 6 TOPS NPU as RK3588 but at lower power (~6–10 W). 58 g board weight. Two Ethernet ports for ground testing. Needs a $9 WiFi module. Newer/less mature NPU SDK.

### Excluded

| Candidate | Reason |
|---|---|
| **Orange Pi 5 Plus** | Same NPU as Orange Pi 5 for $50+ more. No inference benefit. |
| **NanoPi M6V2** | $210+ for same RK3588S NPU as Orange Pi 5 at $100. Not worth it. |
| **Pi 4 + Coral USB** | Works but tight on every margin. Only if you already have a Pi. |
| **Jetson Nano** | ~$313 total, ~120 g, ~15 W. Only if you *must* have CUDA/TensorRT and have the budget/weight/power to spare. |

---

## Next Steps

1. **Narrow to one candidate** — Which matters most: smallest/lightest (Radxa Zero 2 Pro), most powerful/accessible (Orange Pi 5), or most efficient (NanoPi M5)?
2. **Verify NPU software compatibility** — Confirm the thermal detection model can be converted to NPU format (RKNN for Rockchip, TFLite for Amlogic)
3. **Test video pipeline latency** — CVBS → USB UVC → NPU → MAVLink round-trip timing
4. **Benchmark models** — Run MobileNet SSD and a lightweight thermal classifier on the chosen board to confirm ≥25 Hz
