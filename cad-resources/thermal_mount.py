"""
Thermal-camera nose mount ("beak") for the Chimera9 ECO — v1, parametric.

Holds the PurpleRiver Mini 640 / T13 at the NOSE, aimed at NADIR (straight down),
cantilevered forward from the top-plate front edge.

SUPERSEDED 2026-08-07 (TASKS.md 2.8) by thermal_mount_45.py -- kept for reference
only, do not build this one. This docstring originally argued nadir was required
because tilt "breaks the R3_1/R3_2 Johnson pixel budget"; that turned out to be
wrong once computed properly (analysis/thermal_detection_offnadir_analysis.md) --
the 18 mm lens still recognizes at 45 deg, thin but passing (4.17 px along-range
@90 m; see model.sysml OffNadirGsd, 2026-08-12) -- which is why the 45 deg mount
was chosen instead. See mini640_t13_cad_spec.md for the camera's own dimensions
(unaffected by mount angle, still valid for either bracket).

Geometry: a flat horizontal plate.
  * FRONT region  -> 4x M2 CLEARANCE holes on the camera's 18.40 mm pattern + a central
    cutout for the rear DF40 connector/cable. The camera bolts to the UNDERSIDE via its
    rear-face M2 holes, so it hangs lens-DOWN (nadir).
  * REAR region   -> frame bolt pattern to the Chimera9 top-plate front (PARAMETRIC —
    exact positions get calipered off the real frame).

Coordinate system: plate is horizontal. Origin at the CAMERA center.
  +Y = forward (nose)   -Y = aft (toward frame)   +Z = up (sky); camera hangs -Z.
  Plate top face on Z=0, bottom on Z=-PLATE_T.

Run:  pip install build123d   then   python thermal_mount.py
"""

# ----------------------------------------------------------------------------
# PARAMETERS
# ---- Camera interface (EXACT, from the iRay drawing) ----
CAM_HOLE_PITCH = 18.40     # ✅ camera 18.40 x 18.40 M2 pattern
CAM_CLEAR_D    = 2.4       # ✅ M2 clearance (screw passes through plate into the camera's tapped hole)
CONN_CUT_L     = 16.0      # rear DF40 connector + cable clearance cutout (length, along X)
CONN_CUT_W     = 8.0       # ... width (along Y)

# ---- Frame interface (PARAMETRIC — caliper the Chimera9 top-plate front) ----
FRAME_BOLT_PITCH = 30.5    # ❌ assume the 30.5 stack pattern, 2 bolts side-by-side — CONFIRM
FRAME_CLEAR_D    = 3.2     # M3 clearance
BEAK_LEN         = 30.0    # ❌ camera-center -> frame-bolt-line distance (sets nose reach) — TUNE

# ---- Plate ----
PLATE_T   = 3.0            # plate thickness (PETG/ABS, 3-4 walls per cad-resources.md)
EDGE      = 6.0            # material margin around outermost holes

BUILD_WITH_CAMERA = True   # also emit an assembly STEP with the camera placed lens-down

# ----------------------------------------------------------------------------
def _install_font_loader_shim():
    """Skip a corrupt system font so build123d imports on Windows (see nanopi_m5.py)."""
    try:
        import glob, fontTools.ttLib as _tt
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

    def _safe(*a, **k):
        try:
            return _orig(*a, **k)
        except Exception:
            if good:
                return _orig(good)
            raise
    _tt.TTFont = _safe


_install_font_loader_shim()

try:
    from build123d import Box, Cylinder, Pos, Rot, Compound, export_step, export_stl
except ImportError:
    raise SystemExit("build123d not installed.  pip install build123d")

# Derived plate outline
_ch = CAM_HOLE_PITCH / 2.0        # 9.20  camera hole offset
_fh = FRAME_BOLT_PITCH / 2.0      # 15.25 frame bolt offset
Y_FRONT =  _ch + EDGE             # front edge (past camera holes)
Y_REAR  = -(BEAK_LEN + EDGE)      # rear edge (past frame holes)
PLATE_L = Y_FRONT - Y_REAR
PLATE_CY = (Y_FRONT + Y_REAR) / 2.0
PLATE_W = 2 * (_fh + EDGE)        # wide enough to span the frame bolts

CAM_HOLES   = [(_ch, _ch), (-_ch, _ch), (_ch, -_ch), (-_ch, -_ch)]
FRAME_HOLES = [(_fh, -BEAK_LEN), (-_fh, -BEAK_LEN)]


def build_mount():
    """The printable beak bracket (flat plate + holes + connector cutout)."""
    plate = Pos(0, PLATE_CY, -PLATE_T / 2) * Box(PLATE_W, PLATE_L, PLATE_T)
    thru = PLATE_T * 4
    # camera M2 clearance holes
    for x, y in CAM_HOLES:
        plate -= Pos(x, y, -PLATE_T / 2) * Cylinder(radius=CAM_CLEAR_D / 2, height=thru)
    # frame M3 clearance holes
    for x, y in FRAME_HOLES:
        plate -= Pos(x, y, -PLATE_T / 2) * Cylinder(radius=FRAME_CLEAR_D / 2, height=thru)
    # central connector / cable cutout (over the camera's rear-face DF40)
    plate -= Pos(0, 0, -PLATE_T / 2) * Box(CONN_CUT_L, CONN_CUT_W, thru)
    return plate


def main():
    mount = build_mount()
    export_step(mount, "thermal_mount.step")
    export_stl(mount, "thermal_mount.stl")
    print("wrote thermal_mount.step / .stl  (beak bracket)")
    print("  plate {:.0f} x {:.1f} x {:.0f} mm".format(PLATE_W, PLATE_L, PLATE_T))

    if BUILD_WITH_CAMERA:
        try:
            import mini640_t13 as cammod
            cam = cammod.build_camera()
            # camera is built rear-face@Z=0, lens +Z. Flip 180deg about X so the
            # lens points -Z (nadir) and the rear face seats against the plate underside.
            cam = Pos(0, 0, -PLATE_T) * Rot(180, 0, 0) * cam
            mount.label, cam.label = "beak_mount", "camera"
            try:
                from build123d import Color
                mount.color = Color(0.2, 0.5, 0.9)
                cam.color = Color(0.12, 0.12, 0.14)
            except Exception:
                pass
            asm = Compound(label="thermal_mount_assembly", children=[mount, cam])
            export_step(asm, "thermal_mount_with_camera.step")
            print("wrote thermal_mount_with_camera.step  (camera bolted lens-DOWN / nadir)")
        except Exception as e:
            print("  (skipped assembly view:", e, ")")

    print("\nAim = NADIR (analysis-driven). Camera bolts to plate underside via 4x M2 @ 18.40.")
    print("EXACT: camera interface.  PARAMETRIC (caliper frame): FRAME_BOLT_PITCH, BEAK_LEN.")


if __name__ == "__main__":
    main()
