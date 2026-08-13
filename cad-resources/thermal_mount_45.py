"""
Thermal-camera nose mount — 45° DOWNLOOK variant (v1, parametric).

Aims the Mini 640 / T13 forward-and-down at 45° off-nadir (valid with the 18 mm lens,
which recognizes at 45°; see analysis/thermal_detection_offnadir_analysis.md). Same
top-plate-front "beak" attachment as the nadir mount; the difference is a 45° camera
face + a support gusset instead of a flat plate.

Construction: start from the nadir camera-face plate (camera bolts to its underside,
lens -Z) and rotate the face + camera +TILT_DEG about X so the lens points
(0, sin, -cos) = forward-and-down. A horizontal base tab carries the frame bolts; a
gusset bridges base->face.

Coords: origin near the frame-bolt line. +Y forward (nose), +Z up. TILT_DEG measured
from nadir (0 = straight down = the other mount; 45 = this one).

Run: python thermal_mount_45.py   (needs build123d in the venv)
"""
# ---------------- parameters ----------------
TILT_DEG = 45.0

CAM_HOLE_PITCH = 18.40     # camera 8-M2 pattern (rear face)
CAM_CLEAR_D    = 2.4       # M2 clearance
CONN_CUT_L, CONN_CUT_W = 16.0, 8.0   # rear DF40 connector/cable cutout

FRAME_BOLT_PITCH = 30.5    # ❌ assume 30.5 stack pattern — caliper the real top-plate front
FRAME_CLEAR_D    = 3.2     # M3 clearance

T        = 3.0             # plate thickness
FACE_W   = 32.0            # camera-face plate width (X) and length
FACE_L   = 32.0
BASE_W   = 42.0            # base width (spans the frame bolts)
BASE_L   = 30.0            # base length (Y)

BUILD_WITH_CAMERA = True

# ---------------- font shim + imports ----------------
def _shim():
    try:
        import glob, fontTools.ttLib as _tt
    except Exception:
        return
    _o = _tt.TTFont; g = None
    for pat in ("arial*.ttf", "segoeui*.ttf", "tahoma*.ttf"):
        for c in glob.glob("C:/Windows/Fonts/" + pat):
            try: _o(c); g = c; break
            except Exception: continue
        if g: break
    def _s(*a, **k):
        try: return _o(*a, **k)
        except Exception:
            if g: return _o(g)
            raise
    _tt.TTFont = _s
_shim()

def _stub_brep_from_stl():
    # build123d/__init__.py unconditionally imports build123d.brep_from_stl
    # (STL -> primitive detection, unused here), which pulls in sklearn ->
    # pandas; an ABI-mismatched pandas/numpy pair crashes that import and
    # takes `import build123d` down with it. Stub the submodule out first.
    import sys, types
    if "build123d.brep_from_stl" in sys.modules:
        return
    stub = types.ModuleType("build123d.brep_from_stl")
    def _np(*a, **k):
        raise NotImplementedError("brep_from_stl stubbed out (numpy/pandas ABI mismatch); unused here")
    stub.detect_primitives = _np
    sys.modules["build123d.brep_from_stl"] = stub
_stub_brep_from_stl()

try:
    from build123d import Box, Cylinder, Pos, Rot, Compound, export_step, export_stl
except ImportError:
    raise SystemExit("build123d not installed. pip install build123d")

import math
_c, _s = math.cos(math.radians(TILT_DEG)), math.sin(math.radians(TILT_DEG))
_h = CAM_HOLE_PITCH / 2.0
_fh = FRAME_BOLT_PITCH / 2.0
CAM_HOLES = [(_h, _h), (-_h, _h), (_h, -_h), (-_h, -_h)]

# Face placement: rotate +TILT about X, then translate so the face's rear-lower edge
# meets the base front-top and the camera hangs forward-down.
FACE_TY = 13.3
FACE_TZ = 10.3
_face_xform = lambda o: Pos(0, FACE_TY, FACE_TZ) * Rot(TILT_DEG, 0, 0) * o


def build_face():
    """Tilted camera-mount plate (local horizontal, then transformed)."""
    p = Box(FACE_W, FACE_L, T)                     # centered, normal Z
    thru = T * 4
    for x, y in CAM_HOLES:
        p -= Pos(x, y, 0) * Cylinder(radius=CAM_CLEAR_D / 2, height=thru)
    p -= Box(CONN_CUT_L, CONN_CUT_W, thru)         # central connector cutout
    return _face_xform(p)


def build_base():
    base = Pos(0, -BASE_L / 2 + 2, -T / 2) * Box(BASE_W, BASE_L, T)   # top at Z=0, front at Y=2
    thru = T * 4
    for x in (_fh, -_fh):
        base -= Pos(x, -BASE_L / 2 + 2, -T / 2) * Cylinder(radius=FRAME_CLEAR_D / 2, height=thru)
    return base


def build_gusset():
    """Chunky bridge from the base front down to the tilted face (support + connection)."""
    # a wedge box, then trim later if needed; kept simple + overlapping for a clean fuse
    g = Pos(0, 8, -7) * Box(BASE_W * 0.55, 20, 16)
    return g


def build_mount():
    return build_base() + build_gusset() + build_face()


def place_camera(cammod):
    cam = cammod.build_camera()               # rear@Z=0, lens +Z
    # nadir seating (lens -Z, rear on plate underside), then same face transform
    cam = Pos(0, 0, -T) * Rot(180, 0, 0) * cam
    return _face_xform(cam)


def main():
    mount = build_mount()
    export_step(mount, "thermal_mount_45.step")
    export_stl(mount, "thermal_mount_45.stl")
    print("wrote thermal_mount_45.step / .stl  (tilt %.0f deg)" % TILT_DEG)
    if BUILD_WITH_CAMERA:
        try:
            import mini640_t13 as cammod
            cam = place_camera(cammod)
            mount.label, cam.label = "mount_45", "camera"
            try:
                from build123d import Color
                mount.color = Color(0.2, 0.5, 0.9); cam.color = Color(0.12, 0.12, 0.14)
            except Exception:
                pass
            export_step(Compound(label="thermal_mount_45_assembly", children=[mount, cam]),
                        "thermal_mount_45_with_camera.step")
            print("wrote thermal_mount_45_with_camera.step")
        except Exception as e:
            print("  (assembly skipped:", e, ")")


if __name__ == "__main__":
    main()
