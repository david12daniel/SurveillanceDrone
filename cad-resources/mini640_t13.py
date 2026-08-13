"""
PurpleRiver Mini 640 / T13 thermal camera — parametric CAD model for the
Chimera9 nose bracket. OEM core = Raytron/iRay WN640 (18 mm lens variant, SELECTED).

Generates:
  * mini640_t13.step               — camera solid: 21x21 body + 8xM2 holes + 18mm lens barrel
  * mini640_t13_with_keepout.step  — camera + rear connector keep-out + lens sweep clearance
  * mini640_t13.stl                — body+lens, for quick viewing

Data source: cad-resources/mini640_t13_cad_spec.md, extracted from the LEGIBLE iRay
OEM manual drawing (iRay_MINI_384-640_Module_Manual_V1.10.pdf §6, 1183x810 px).

Coordinate system: origin at the CENTER of the REAR mounting face.
  X,Y centered on the body      (body spans -10.5..+10.5 in each)
  Z = 0 is the REAR face; +Z points OUT THE FRONT (camera's view direction).
  Body occupies Z 0..CORE_D; the lens barrel extends beyond the front face.
The bracket bolts to the REAR face's 4 x M2 holes; the lens looks +Z.

Run:  pip install build123d   then   python mini640_t13.py
"""

# ----------------------------------------------------------------------------
# PARAMETERS  —  ✅ read clearly off the legible iRay drawing · ⚠️ conflict · ❌ estimate, caliper
# ----------------------------------------------------------------------------
BODY = 21.0            # ✅ square body 21.00 x 21.00 (±0.10)
CORE_D = 10.3          # ⚠️ core depth (no lens): rebrand=10.3, iRay text=8.0 — CALIPER.
                       #    Using the larger value (conservative for clearance).

HOLE_PITCH = 18.40     # ✅ 8-M2 pattern is 18.40 x 18.40 (±0.10), centered
HOLE_D    = 2.0        # ✅ M2 nominal (callout "8-M2▽1.5")
HOLE_DEPTH = 1.5       # ✅ tapped 1.5 mm deep, blind
#   -> 8 holes total: 4 tapped into the REAR face, 4 into the FRONT face.

LENS_BOSS_D = 21.0     # ✅ Ø21.00 (±0.10) circular lens-mount boss on the front face

# T13 = 18 mm lens (SELECTED 2026-07-29; was 13 mm). The 18 mm barrel is NOT dimensioned
# in any source (the drawing only details the 9.1 mm example), so these are flagged
# estimates — caliper the real lens. (Mounting interface below is lens-independent.)
LENS_OD  = 20.0        # ❌ barrel outer Ø (f/1.0 => ~Ø18-24) — CALIPER
LENS_LEN = 24.0        # ❌ barrel protrusion beyond the front face for the 18 mm lens — CALIPER

# Rear board-to-board connector (Hirose DF40C-50DP-0.4V, 50-pin) keep-out estimate.
CONN_L, CONN_W, CONN_H = 14.0, 4.0, 2.5   # ❌ estimate — CALIPER

BUILD_KEEPOUT = True

# ----------------------------------------------------------------------------
def _install_font_loader_shim():
    """build123d scans system fonts at import and aborts on a corrupt font
    (fontTools 'bad sfntVersion', common on Windows). Patch fontTools.TTFont
    BEFORE importing build123d so unreadable fonts fall back to a good one."""
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
                _orig(cand); good = cand; break
            except Exception:
                continue
        if good:
            break

    def _safe_ttfont(*a, **k):
        try:
            return _orig(*a, **k)
        except Exception:
            if good:
                return _orig(good)
            raise
    _tt.TTFont = _safe_ttfont


_install_font_loader_shim()


def _install_brep_from_stl_stub():
    """build123d/__init__.py unconditionally imports build123d.brep_from_stl
    (STL -> primitive-shape detection), which pulls in sklearn -> pandas. If
    the installed pandas predates the installed numpy's ABI, that import
    raises ("numpy.dtype size changed... binary incompatibility") and takes
    down the whole `import build123d` with it. This script never calls
    detect_primitives, so stub the submodule out before importing build123d
    rather than require a pandas/numpy version fix — a real future call to
    it fails loudly instead of pretending to work."""
    import sys
    import types

    if "build123d.brep_from_stl" in sys.modules:
        return
    stub = types.ModuleType("build123d.brep_from_stl")

    def _detect_primitives_stub(*args, **kwargs):
        raise NotImplementedError(
            "build123d.brep_from_stl.detect_primitives is stubbed out in this "
            "environment (numpy/pandas ABI mismatch); not used by this script."
        )

    stub.detect_primitives = _detect_primitives_stub
    sys.modules["build123d.brep_from_stl"] = stub


_install_brep_from_stl_stub()

try:
    from build123d import Box, Cylinder, Pos, Compound, export_step, export_stl
except ImportError:
    raise SystemExit(
        "build123d is not installed.\n  pip install build123d\n"
        "Then re-run:  python mini640_t13.py"
    )

# 4 hole centers on the 18.40 pattern (shared by both faces)
h = HOLE_PITCH / 2.0
HOLE_XY = [(h, h), (-h, h), (h, -h), (-h, -h)]


def build_camera():
    """21x21xCORE_D body + Ø21 front boss + 18mm lens barrel, with 8 blind M2 holes."""
    # body: rear face on Z=0, front face on Z=CORE_D
    cam = Pos(0, 0, CORE_D / 2) * Box(BODY, BODY, CORE_D)
    # lens barrel out the front (+Z)
    cam += Pos(0, 0, CORE_D + LENS_LEN / 2) * Cylinder(radius=LENS_OD / 2, height=LENS_LEN)
    # 4 blind M2 holes tapped into the REAR face (opening at Z=0, 1.5 deep into +Z)
    for x, y in HOLE_XY:
        cam -= Pos(x, y, HOLE_DEPTH / 2) * Cylinder(radius=HOLE_D / 2, height=HOLE_DEPTH)
    # 4 blind M2 holes tapped into the FRONT face (opening at Z=CORE_D, 1.5 deep into -Z)
    for x, y in HOLE_XY:
        cam -= Pos(x, y, CORE_D - HOLE_DEPTH / 2) * Cylinder(radius=HOLE_D / 2, height=HOLE_DEPTH)
    return cam


def build_keepout():
    """Rear connector box (behind Z=0) + swept lens clearance cylinder."""
    conn = Pos(0, 0, -CONN_H / 2) * Box(CONN_L, CONN_W, CONN_H)
    lens_clear = Pos(0, 0, CORE_D + LENS_LEN / 2) * Cylinder(radius=LENS_OD / 2 + 1.0, height=LENS_LEN)
    return conn, lens_clear


def main():
    cam = build_camera()
    export_step(cam, "mini640_t13.step")
    export_stl(cam, "mini640_t13.stl")
    print("wrote mini640_t13.step  (body + lens + 8x M2 holes)")
    print("wrote mini640_t13.stl")

    if BUILD_KEEPOUT:
        conn, lens_clear = build_keepout()
        cam.label, conn.label, lens_clear.label = "camera", "rear_connector", "lens_clearance"
        try:
            from build123d import Color
            cam.color = Color(0.1, 0.1, 0.12)
            conn.color = Color(0.9, 0.3, 0.1, alpha=0.4)
            lens_clear.color = Color(0.2, 0.5, 0.9, alpha=0.25)
        except Exception:
            pass
        asm = Compound(label="Mini640_T13_with_keepout", children=[cam, conn, lens_clear])
        export_step(asm, "mini640_t13_with_keepout.step")
        print("wrote mini640_t13_with_keepout.step  (+ rear connector + lens clearance)")

    print("\nDatum = center of REAR mounting face. Body {0}x{0}x{1} mm; lens +{2} mm."
          .format(BODY, CORE_D, LENS_LEN))
    print("EXACT: body 21x21, 8xM2 @ 18.40 pattern.  ESTIMATE (caliper): CORE_D, LENS_OD, LENS_LEN.")


if __name__ == "__main__":
    main()
