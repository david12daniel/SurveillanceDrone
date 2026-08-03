"""
NanoPi M5 (SBC3) — parametric CAD model for the Chimera9 integration mount.

Generates:
  * nanopi_m5.step               — the PCB solid (90x62x1.6) with 4 mounting holes
  * nanopi_m5_with_keepout.step  — PCB + top/bottom keep-out boxes (clearance check)
  * nanopi_m5.stl                — PCB only, for quick viewing / slicing

Data source: cad-resources/nanopi_m5_cad_spec.md (ingested from the FriendlyELEC
wiki PDF pp.5-7 + schematic, 2026-07-28).

Coordinate system: origin at the bottom-left PCB corner (component side up).
  X in [0, 90]  (board length)      Y in [0, 62]  (board width)
  Z = 0 is the PCB BOTTOM face; +Z is up out of the component side.
This datum makes the mounting-hole values below read like caliper measurements
"from the corner", so confirming them against the real board is trivial.

Run:  pip install build123d   then   python nanopi_m5.py
"""

# ----------------------------------------------------------------------------
# PARAMETERS  —  ✅ exact (specced) · ⚠️ estimated · ❌ caliper the real board
# ----------------------------------------------------------------------------
PCB_L = 90.0          # ✅ board length  (X)   wiki: 90 x 62 x 1.6
PCB_W = 62.0          # ✅ board width   (Y)
PCB_T = 1.6           # ✅ PCB thickness (8-layer ENIG)

# Mounting holes — 4, one near each corner. Coordinates NOT published by the
# wiki (labeled diagram only, no dimensions). Values below are the standard
# estimate; replace with caliper readings from the corner datum above.
HOLE_D    = 2.7       # ⚠️ Ø for M2.5 clearance (confirm M2.5 vs M3)
HOLE_INSET = 3.5      # ❌ hole-center inset from each edge  — CALIPER

# Keep-out envelope (for mount clearance sizing) — heights above/below the PCB.
TOP_KEEPOUT    = 22.0  # ⚠️ heatsink over RK3576 (~15-25) — also clears the
                       #    front RJ45/USB port-wall (~16). Conservative full-footprint box.
BOTTOM_KEEPOUT = 5.0   # ⚠️ M.2 2280 NVMe module + solder below the board
                       #    (set to ~1.5 if you populate eMMC/UFS instead of NVMe)

BUILD_KEEPOUT = True   # set False to skip the keep-out export

# ----------------------------------------------------------------------------
def _install_font_loader_shim():
    """build123d scans every system font at import time and aborts if a single
    font file is corrupt (fontTools 'bad sfntVersion' — common on Windows).
    Patch fontTools.TTFont BEFORE importing build123d so unreadable fonts fall
    back to a good one instead of crashing the import. No-op if not needed."""
    try:
        import glob
        import fontTools.ttLib as _tt
    except Exception:
        return
    _orig = _tt.TTFont
    good = None
    for pat in ("arial*.ttf", "segoeui*.ttf", "tahoma*.ttf", "verdana*.ttf"):
        for cand in glob.glob("C:/Windows/Fonts/" + pat):
            try:
                _orig(cand)
                good = cand
                break
            except Exception:
                continue
        if good:
            break

    def _safe_ttfont(*args, **kwargs):
        try:
            return _orig(*args, **kwargs)
        except Exception:
            if good:
                return _orig(good)  # stand-in for the corrupt file
            raise
    _tt.TTFont = _safe_ttfont


_install_font_loader_shim()

try:
    from build123d import (
        Box, Cylinder, Pos, Compound,
        export_step, export_stl,
    )
except ImportError:
    raise SystemExit(
        "build123d is not installed.\n"
        "  pip install build123d\n"
        "Then re-run:  python nanopi_m5.py\n"
        "(build123d is free/open-source and exports STEP for FreeCAD + STL for slicing.)"
    )

# Hole centers, referenced from the bottom-left corner datum.
HOLE_LOCS = [
    (HOLE_INSET,          HOLE_INSET),           # bottom-left
    (PCB_L - HOLE_INSET,  HOLE_INSET),           # bottom-right
    (HOLE_INSET,          PCB_W - HOLE_INSET),   # top-left
    (PCB_L - HOLE_INSET,  PCB_W - HOLE_INSET),   # top-right
]


def build_pcb():
    """PCB slab (bottom face on Z=0) with the 4 through mounting holes."""
    pcb = Pos(PCB_L / 2, PCB_W / 2, PCB_T / 2) * Box(PCB_L, PCB_W, PCB_T)
    for hx, hy in HOLE_LOCS:
        # generous height so the cylinder fully pierces the slab
        pcb -= Pos(hx, hy, PCB_T / 2) * Cylinder(radius=HOLE_D / 2, height=PCB_T * 4)
    return pcb


def build_keepout():
    """Top + bottom clearance boxes, full board footprint (conservative)."""
    top = Pos(PCB_L / 2, PCB_W / 2, PCB_T + TOP_KEEPOUT / 2) * \
        Box(PCB_L, PCB_W, TOP_KEEPOUT)
    bot = Pos(PCB_L / 2, PCB_W / 2, -BOTTOM_KEEPOUT / 2) * \
        Box(PCB_L, PCB_W, BOTTOM_KEEPOUT)
    return top, bot


def main():
    pcb = build_pcb()
    export_step(pcb, "nanopi_m5.step")
    export_stl(pcb, "nanopi_m5.stl")
    print("wrote nanopi_m5.step  (PCB + 4 holes)")
    print("wrote nanopi_m5.stl   (PCB, for quick view)")

    if BUILD_KEEPOUT:
        top, bot = build_keepout()
        # label the solids so they're identifiable in FreeCAD's tree
        pcb.label, top.label, bot.label = "PCB", "keepout_top", "keepout_bottom"
        try:  # colors are cosmetic; don't fail the export if the API shifts
            from build123d import Color
            pcb.color = Color(0.05, 0.45, 0.15)
            top.color = Color(0.9, 0.3, 0.1, alpha=0.35)
            bot.color = Color(0.9, 0.3, 0.1, alpha=0.35)
        except Exception:
            pass
        asm = Compound(label="NanoPi_M5_with_keepout", children=[pcb, top, bot])
        export_step(asm, "nanopi_m5_with_keepout.step")
        print("wrote nanopi_m5_with_keepout.step  (PCB + top/bottom keep-out)")

    print("\nDatum = bottom-left PCB corner.  Board {}x{}x{} mm."
          .format(PCB_L, PCB_W, PCB_T))
    print("Confirm HOLE_INSET / HOLE_D / keep-out heights with calipers, then re-run.")


if __name__ == "__main__":
    main()
