"""
Simulate what a deer and a person look like through the PurpleRiver Mini 640
(640x512, 12 um) at a 45-degree DOWNLOOK, for 13 / 15 / 18 mm lenses at 90 m and
120 m AGL. Educational illustration of pixels-on-target (Johnson-style).

Method: build a high-res thermal silhouette (hot body vs cool ground), then resample
it to the number of sensor pixels the target actually spans at each geometry, add
NETD-like noise, and upscale (nearest) so the true sensor blockiness is visible.

Geometry (45 deg off-nadir, target on the optical axis):
  R = H/cos45 ; GSD_cross = R*IFOV ; GSD_along = R*IFOV/cos45  (along-range is foreshortened)
  horizontal target size -> GSD_cross ; vertical size -> GSD_along (conservative, ground-plane).

Run: python generate_thermal_sim.py  (numpy, scipy, matplotlib, Pillow)
"""
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

PITCH = 12e-6                      # sensor pixel pitch [m]
THETA = np.deg2rad(45.0)
LENSES = [13, 15, 18]             # mm
HEIGHTS = [90, 120]               # m AGL
CMAP = "inferno"                  # ironbow-like white->hot
PPM = 240                         # silhouette render resolution [px per metre]

def ifov(f_mm): return PITCH / (f_mm * 1e-3)
def gsd(f_mm, H):                 # (cross, along) ground sample distance [m/px] at 45 deg
    R = H / np.cos(THETA)
    return R * ifov(f_mm), R * ifov(f_mm) / np.cos(THETA)

# ---------- silhouette builders (return hot-body mask, real size W x H metres) ----------
def _grid(W, H):
    nx, ny = int(W * PPM), int(H * PPM)
    xs = (np.arange(nx) + 0.5) / PPM
    ys = (np.arange(ny) + 0.5) / PPM
    X, Y = np.meshgrid(xs, ys)
    return X, Y, np.zeros((ny, nx))

def _ellipse(m, X, Y, cx, cy, rx, ry, v=1.0):
    m[((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2 <= 1] = v

def _capsule(m, X, Y, ax, ay, bx, by, r, v=1.0):
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = np.clip(((X - ax) * dx + (Y - ay) * dy) / L2, 0, 1)
    d = np.hypot(X - (ax + t * dx), Y - (ay + t * dy))
    m[d <= r] = v

def deer():                        # broadside, W=1.5 (length) x H=1.0 (height)
    W, H = 1.5, 1.0
    X, Y, m = _grid(W, H)
    for (ax, ay, bx, by) in [(0.55,.52,.52,.05),(0.68,.52,.66,.05),   # back legs
                             (1.02,.52,1.05,.05),(0.90,.52,.92,.05)]: # front legs
        _capsule(m, X, Y, ax, ay, bx, by, 0.035, 0.85)
    _ellipse(m, X, Y, 0.75, 0.62, 0.46, 0.20)                         # body
    _capsule(m, X, Y, 1.02, 0.68, 1.24, 0.92, 0.075)                  # neck
    _ellipse(m, X, Y, 1.33, 0.95, 0.14, 0.095)                        # head
    _capsule(m, X, Y, 1.30, 1.02, 1.24, 1.18, 0.02, 0.9)             # antler-ish
    _capsule(m, X, Y, 1.38, 1.02, 1.44, 1.16, 0.02, 0.9)
    _capsule(m, X, Y, 0.33, 0.60, 0.24, 0.42, 0.03, 0.8)             # tail
    return W, H, m

def person():                      # standing, W=0.5 x H=1.8
    W, H = 0.5, 1.8
    X, Y, m = _grid(W, H)
    _capsule(m, X, Y, 0.19, 0.95, 0.16, 0.06, 0.055)                  # legs
    _capsule(m, X, Y, 0.31, 0.95, 0.34, 0.06, 0.055)
    _ellipse(m, X, Y, 0.25, 1.20, 0.145, 0.30)                        # torso
    _capsule(m, X, Y, 0.12, 1.44, 0.06, 1.00, 0.045, 0.9)           # arms
    _capsule(m, X, Y, 0.38, 1.44, 0.44, 1.00, 0.045, 0.9)
    _ellipse(m, X, Y, 0.25, 1.63, 0.11, 0.12)                        # head
    return W, H, m

# ---------- sensor simulation ----------
def scene(mask):
    rng = np.random.default_rng(7)
    bg = 0.12 + 0.03 * gaussian_filter(rng.standard_normal(mask.shape), 6)  # cool textured ground
    s = np.clip(bg + mask * 0.85, 0, 1)
    return gaussian_filter(s, PPM * 0.01)                                    # slight optical blur

def capture(s, W, H, f, Hm):
    gc, ga = gsd(f, Hm)
    pw, ph = max(1, round(W / gc)), max(1, round(H / ga))
    small = np.asarray(Image.fromarray((s * 255).astype(np.uint8))
                       .resize((pw, ph), Image.BOX), float) / 255.0
    rng = np.random.default_rng(f * 1000 + Hm)
    small = np.clip(small + rng.normal(0, 0.045, small.shape), 0, 1)         # NETD-ish noise
    disp_h = 300; disp_w = max(1, int(disp_h * W / H))
    big = np.asarray(Image.fromarray((small * 255).astype(np.uint8))
                     .resize((disp_w, disp_h), Image.NEAREST), float) / 255.0
    return big, pw, ph

# ---------- figure ----------
def make(target_fn, name, nice):
    W, H, mask = target_fn()
    s = scene(mask)
    fig = plt.figure(figsize=(10.5, 7.6))
    gs = fig.add_gridspec(3, 3, width_ratios=[1.05, 1, 1], wspace=0.16, hspace=0.32,
                          left=0.04, right=0.985, top=0.86, bottom=0.11)
    # reference silhouette (left, spans rows)
    axr = fig.add_subplot(gs[:, 0])
    axr.imshow(s, cmap=CMAP, origin="lower", vmin=0, vmax=1, aspect="auto")
    axr.set_title("actual shape\n(ideal / hi-res)", fontsize=10)
    axr.set_xticks([]); axr.set_yticks([])
    for r, f in enumerate(LENSES):
        for c, Hm in enumerate(HEIGHTS):
            ax = fig.add_subplot(gs[r, c + 1])
            big, pw, ph = capture(s, W, H, f, Hm, )
            ax.imshow(big, cmap=CMAP, origin="lower", vmin=0, vmax=1, aspect="auto")
            small = min(pw, ph)
            tag = "recognize" if small >= 4 else ("detect" if small >= 1.5 else "—")
            col = "#2ca02c" if small >= 4 else ("#ff9900" if small >= 1.5 else "#d62728")
            ax.set_title(f"{f} mm @ {Hm} m   {pw}×{ph}px",
                         fontsize=10.5, color=col, fontweight="bold")
            ax.set_xticks([]); ax.set_yticks([])
            ax.text(0.5, -0.11, tag, transform=ax.transAxes, ha="center",
                    fontsize=8.5, color=col)
    fig.suptitle(f"PurpleRiver Mini 640 (640×512, 12 µm) — {nice} at 45° downlook\n"
                 f"pixels-on-target: horizontal = cross-range, vertical = along-range (foreshortened)",
                 fontsize=12.5, y=0.965)
    fig.text(0.5, 0.03,
             f"{nice} modelled {W:.1f} m × {H:.1f} m. Green ≥4 px (Johnson recognize), "
             f"orange ≥1.5 px (detect), red below. NETD noise + optical blur applied. "
             "45° doubles vertical GSD vs nadir.", ha="center", fontsize=8.6, color="#444")
    out = f"thermal_sim_{name}_45deg.png"
    fig.savefig(out, dpi=125); plt.close(fig)
    print("wrote", out)

if __name__ == "__main__":
    make(deer, "deer", "Deer (broadside)")
    make(person, "person", "Person (standing)")
