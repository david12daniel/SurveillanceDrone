# NanoPi M5 (SBC3) — CAD spec sheet

**Purpose:** structured, machine-usable dimensional spec for building a parametric CAD
model of the NanoPi M5 (for the Chimera9 integration mount, `MODEL_ISSUES.md` §C16).
This is the "prompt" that drives [`nanopi_m5.py`](nanopi_m5.py) (build123d → STEP/STL).

**Sources (ingested 2026-07-28):**
- `NanoPi M5 - FriendlyELEC WiKi.pdf` pp. 5–7 (Hardware Spec + labeled top/bottom Layout diagrams)
- `NanoPi_M5_schematic.pdf` (connector nets)
- Recorded dims in [`cad-resources.md`](cad-resources.md) §2B

**Confidence key:** ✅ exact (specced) · ⚠️ estimated (standard part dims, not specced) · ❌ must caliper the real board

---

## Board

| Attribute | Value | Conf. |
|---|---|---|
| PCB length (X) | **90.0 mm** | ✅ |
| PCB width (Y) | **62.0 mm** | ✅ |
| PCB thickness | **1.6 mm** (8-layer ENIG) | ✅ |
| Mounting holes | **4**, one near each corner | ✅ present |
| Hole diameter | **≈2.7 mm** (M2.5 clearance) | ⚠️ |
| Hole inset from edges | **≈3.5 mm** | ❌ caliper |

> The wiki shows a *labeled* layout diagram, **not** a dimensioned mechanical drawing.
> Board outline + thickness are stated exactly; **hole coordinates and connector offsets
> are NOT published** — they are estimated here and flagged for caliper confirmation.

## Connector layout (which edge each sits on)

Board viewed component-side up, **front port-wall = the +Y long edge**.

| Edge | Connectors (in order) | Notes |
|---|---|---|
| **Front long edge** (+Y, "port wall") | USB-C (PD/DC 6–20 V) · 2× RJ45 GbE · 2× USB 3.0 (stacked) · HDMI (full-size) · 3.5 mm audio | **tallest wall** — drives clearance |
| **Left short edge** (−X) | Power-On Mode jumper · 5V fan (ZH1.5-2A) | |
| **Right short edge** (+X) | Debug UART (3-pin) · MIC · M.2 E-key (WiFi) · RTC (2-pin 1.25 mm) · microSD (edge slot) | |
| **Rear long edge** (−Y) | 30-pin 2.54 mm GPIO header · LED1/2 · SYS LED · USER btn · POWER btn | |
| **Top center** | Rockchip RK3576 SoC | tallest active part → heatsink |
| **Bottom side** | M.2 M-key 2280 (NVMe PCIe 2.1 x1) · SPI-NOR · UFS · MIPI-CSI0/CSI1/DSI (0.5 mm FPC) · BOOT switch | NVMe module protrudes below |

## Keep-out envelope (for mount sizing)

| Zone | Height above/below PCB | Conf. |
|---|---|---|
| Top heatsink over RK3576 | **~15–25 mm** above (use 22 mm default) | ⚠️ |
| Front port-wall (RJ45/USB stack tallest) | **~16 mm** above | ⚠️ RJ45≈13.5, USB3 stack≈15–17 |
| Bottom NVMe module + solder | **~5 mm** below | ⚠️ |

## Parameters to confirm with calipers (turns ⚠️/❌ into ✅)

1. 4× mounting-hole **X/Y coordinates** (measure from a datum corner)
2. Mounting-hole **diameter** (confirm M2.5 vs M3)
3. **Heatsink height** of the actual passive sink you fit
4. NVMe module **protrusion** below the board (0 if you go eMMC/UFS instead)

Update the matching variables at the top of [`nanopi_m5.py`](nanopi_m5.py) and re-run.
