# Thermal Camera Market Analysis

**File:** `analysis/thermal_camera_candidates.csv` — 16 candidates, 23 columns

---

## Quick Summary

| Tier | Model | Resolution | Price | Weight | FPV Ready? |
|------|-------|------------|-------|--------|------------|
| **🟢 Budget** | Lepton 3.5 + DroneThermal v4 | 160×120 | ~$240 kit | ~4g | ✅ CVBS via carrier |
| **🟢 Budget** | Horus Dynamics Lepton Kit | 160×120 | ~$250 | ~15g | ✅ Plug-and-play |
| **🟢 Budget** | Generic 256×192 CVBS Module | **256×192** | **$100-200** | **≤21g** | **✅ Best value** |
| **🟡 Mid** | Generic 384×288 CVBS Module | 384×288 | $250-400 | ≤21g | ✅ |
| **🔴 Best** | Generic 640×512 CVBS Module | **640×512** | **$400-700** | **≤21g** | ✅ |
| **🔴 Best** | Axisflying 640 Thermal | 640×512 | $350-550 | ~23-30g | ✅ |

---

## Key Findings

### 1. Chinese Generic OEM Modules Are the Best Value by Far
The generic OEM modules sold on AliExpress/Alibaba (T8-T10) are the **real discovery** here. They offer:
- **Same 12µm VOx detector tech** as FLIR Boson at **1/3 to 1/5 the price**
- **CVBS analog output** — connects directly to any analog VTX for live FPV feed
- **USB output** — connects to SBC (Jetson, Pi) for recording/analysis
- **17×17×35mm form factor** — similar size to a standard FPV camera
- **21g weight and <0.75W power** — minimal impact on flight time
- **Radiometric output** — can measure actual temperatures

### 2. The FLIR Lepton Line Is Underwhelming for Surveillance
The Lepton 3.5 (T3) is the most popular DIY thermal camera, but:
- **Only 160×120 resolution** — 19,200 pixels
- **8.7 Hz frame rate** — choppy video
- **~$200** for the module alone + $40-50 for a breakout board = ~$250 total
- **Detection range only ~25m** — marginal for surveillance at 2.8km flight altitude
- **Best for:** hobbyist/experimental, not serious surveillance

### 3. 640×512 Chinese Modules Are the Sweet Spot
For $400-700 you get:
- **328,000 pixels** (17× the Lepton 3.5)
- **25-50 Hz frame rate** — smooth video
- **CVBS + USB dual output**
- **Detection ~150m, Recognition ~50m** (with 9mm lens)
- **21g weight** — same as a GoPro session
- **Under 0.75W power draw**

### 4. Axisflying 640 (T11) Is the Most "Drone-Ready"
- 60fps frame rate (smoothest of all options)
- CVBS direct to analog VTX
- Known compatibility with standard FPV stacks
- $350-550 — competitive pricing
- Branded product with better support than generic modules

### 5. The 256×192 Module (T8) Is the Best Budget Compromise
- $100-200
- 49,000 pixels (2.5× Lepton)
- 25-50 Hz
- CVBS + USB
- ~50m detection range
- **Best bang for buck if budget is tight**

### 6. What Won't Work for FPV (no CVBS)
- **Waveshare LWIR** (T6) — SPI/I2C only, for ground station use
- **Heimann HTPA** (T7) — SPI only, needs dev effort, thermopile (low sensitivity)
- **Arducam USB** (T14) — UVC plug-and-play, but no CVBS for live FPV

---

## Budget Impact Analysis

At the **$2,500 total system budget**, here's how these thermal options fit:

| Thermal Choice | Thermal Cost | Remaining Budget for Rest | Viability |
|----------------|-------------|--------------------------|-----------|
| Lepton 3.5 + carrier (T3+T4) | ~$240 | ~$2,260 | ✅ Easy fit, low res |
| Generic 256×192 (T8) | $100-200 | ~$2,300-2,400 | ✅ Best budget option |
| Generic 384×288 (T9) | $250-400 | ~$2,100-2,250 | ✅ Still comfortable |
| Axisflying 640 (T11) | $350-550 | ~$1,950-2,150 | ✅ Possible with careful choices |
| Generic 640×512 (T10) | $400-700 | ~$1,800-2,100 | ⚠️ Tight but possible |
| FLIR Boson 640 (T16) | $1,500-2,500 | $0-$1,000 | ❌ Over budget alone |

**Recommendation:** The **Generic 256×192** (T8) at $100-200 or **Generic 384×288** (T9) at $250-400 offer the best balance of cost, resolution, and capability for this project. If surveillance at range matters, jump to **T10 (640×512)** at $400-700.

---

## Comparison: Lepton vs Generic Chinese Modules

| Aspect | Lepton 3.5 | Generic 256×192 | Generic 384×288 | Generic 640×512 |
|--------|-----------|----------------|----------------|----------------|
| **Resolution** | 160×120 | 256×192 | 384×288 | 640×512 |
| **Pixels** | 19,200 | 49,152 | 110,592 | 327,680 |
| **Pixels vs Lepton** | 1× (baseline) | **2.6×** | **5.8×** | **17×** |
| **Frame Rate** | 8.7 Hz | 25-50 Hz | 25-50 Hz | 25-50 Hz |
| **Detection Range** | ~25m | ~50m | ~80m | ~160m |
| **Weight** | 0.9g (module) | ≤21g | ≤21g | ≤21g |
| **Power** | <0.15W | <0.7W | <0.7W | <0.75W |
| **CVBS for FPV?** | ❌ Needs carrier | ✅ Built-in | ✅ Built-in | ✅ Built-in |
| **USB for SBC?** | ❌ Needs breakout | ✅ Built-in | ✅ Built-in | ✅ Built-in |
| **Temp Range** | -10 to +80°C | -40 to +70°C | -40 to +70°C | -40 to +70°C |
| **Cost** | ~$200 + $50 carrier | **$100-200** | $250-400 | $400-700 |
| **Availability** | Distributors | AliExpress | AliExpress | AliExpress |

---

## Integration Notes

All **CVBS-output modules** (T8-T13) can connect to any analog VTX in the VTX CSV (V1-V11) for live FPV downlink. The same modules also have **USB output** for connecting to the SBC for onboard recording and analysis — which is the Phase 3 architecture we already decided on.

**Integration architecture:**
```
Thermal Camera (T8-T13)
  ├─ CVBS → Analog VTX (V1-V11) → Goggles (live FPV feed)
  └─ USB → SBC (Jetson/Zero) → microSD (onboard recording)
```

This dual-path approach gives the pilot live thermal vision while recording high-quality data for post-flight analysis — exactly what's needed for surveillance work.