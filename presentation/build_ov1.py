# -*- coding: utf-8 -*-
"""OV-1 High-Level Operational Concept graphic for the Thermal Surveillance UAS."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (Rectangle, Circle, Ellipse, Polygon, FancyBboxPatch,
                                FancyArrowPatch, Wedge)
from matplotlib.colors import LinearSegmentedColormap
import os

NAVY="#0F2540"; SLATE="#1F3A5F"; ACCENT="#2E86AB"; AMBER="#D9821E"; TEXT="#20303f"
SKY_TOP="#b7dcf0"; SKY_BOT="#e9f4fb"
GROUND="#cdbb86"; GRASS="#8aad60"; GRASS_D="#6f9350"
TREE="#3f7d4e"; TRUNK="#7a5230"
HEAT="#ef6a3d"; HEAT_CORE="#ffd23f"; WHITE="#ffffff"; MUTED="#5c6b7a"

OUT = r"c:\Users\Josiah Laperriere\Documents\Coding\SurveillanceDrone\SurveillanceDrone\presentation\assets\diagrams\ov1_operational_concept.png"

fig, ax = plt.subplots(figsize=(13.4, 6.2), dpi=150)
ax.set_xlim(0, 100); ax.set_ylim(0, 46); ax.axis("off")

# ── Sky (gradient) + ground ──
skycmap = LinearSegmentedColormap.from_list("sky", [SKY_BOT, SKY_TOP])
ax.imshow(np.linspace(0, 1, 256).reshape(-1, 1), extent=[0, 100, 10.5, 46],
          origin="lower", cmap=skycmap, aspect="auto", zorder=0)
ax.add_patch(Rectangle((0, 0), 100, 11, fc=GROUND, ec="none", zorder=1))
ax.add_patch(Rectangle((0, 10.2), 100, 1.0, fc=GRASS, ec="none", zorder=2))
# gentle rolling hills
for hx, hr in [(18, 9), (46, 7), (72, 8)]:
    ax.add_patch(Wedge((hx, 11), hr, 0, 180, width=hr, fc=GRASS_D, ec="none", alpha=0.35, zorder=1))

# ── Sun (daytime) ──
ax.add_patch(Circle((8.5, 39.5), 2.6, fc=HEAT_CORE, ec="none", zorder=3))
for a in range(0, 360, 30):
    r = np.radians(a)
    ax.plot([8.5+3.3*np.cos(r), 8.5+4.5*np.cos(r)],
            [39.5+3.3*np.sin(r), 39.5+4.5*np.sin(r)], color=HEAT_CORE, lw=2, zorder=3)
ax.text(13.6, 39.5, "Daytime operations", color=SLATE, fontsize=10, va="center",
        fontweight="bold", zorder=4)

# ── Helpers ──
def tree(x, s=1.0):
    ax.add_patch(Rectangle((x-0.25*s, 11), 0.5*s, 1.6*s, fc=TRUNK, ec="none", zorder=2))
    ax.add_patch(Polygon([(x-1.5*s, 12.4), (x+1.5*s, 12.4), (x, 16.2*s/1.0+ (11-11))],
                 closed=True, fc=TREE, ec="none", zorder=2))
    ax.add_patch(Polygon([(x-1.2*s, 13.6), (x+1.2*s, 13.6), (x, 16.8*s)],
                 closed=True, fc=TREE, ec="none", zorder=2))
for tx, ts in [(5,0.9),(12,1.1),(40,1.0),(55,0.85),(63,1.15),(90,1.0),(95,0.8)]:
    tree(tx, ts)

def heat_blob(x, y, label):
    for r, c, a in [(2.3, HEAT, 0.18), (1.5, HEAT, 0.30), (0.85, HEAT, 0.55), (0.4, HEAT_CORE, 0.95)]:
        ax.add_patch(Circle((x, y), r, fc=c, ec="none", alpha=a, zorder=5))
    ax.text(x, y-2.7, label, color=NAVY, fontsize=9, ha="center", va="top",
            fontweight="bold", zorder=6)

def drone(cx, cy):
    # top arm bar + rotor discs
    ax.add_patch(FancyBboxPatch((cx-3.3, cy+0.55), 6.6, 0.5, boxstyle="round,pad=0.05,rounding_size=0.2",
                 fc=SLATE, ec="none", zorder=6))
    for dx in (-3.0, 3.0):
        ax.add_patch(Ellipse((cx+dx, cy+1.15), 2.8, 0.55, fc=ACCENT, ec="none", alpha=0.45, zorder=6))
        ax.add_patch(Rectangle((cx+dx-0.12, cy+0.6), 0.24, 0.55, fc=NAVY, ec="none", zorder=7))
    # body
    ax.add_patch(FancyBboxPatch((cx-1.7, cy-0.55), 3.4, 1.15, boxstyle="round,pad=0.05,rounding_size=0.3",
                 fc=NAVY, ec="none", zorder=7))
    # thermal gimbal
    ax.add_patch(FancyBboxPatch((cx-0.55, cy-1.6), 1.1, 1.05, boxstyle="round,pad=0.03,rounding_size=0.2",
                 fc=AMBER, ec="none", zorder=7))
    ax.add_patch(Circle((cx, cy-1.15), 0.28, fc=NAVY, ec="none", zorder=8))

def gcs(x, y):
    # operator
    ax.add_patch(Circle((x, y+2.2), 0.62, fc=SLATE, ec="none", zorder=6))
    ax.add_patch(Polygon([(x-0.9, y), (x+0.9, y), (x+0.6, y+1.7), (x-0.6, y+1.7)], closed=True,
                 fc=SLATE, ec="none", zorder=6))
    # laptop
    ax.add_patch(Polygon([(x+1.5, y), (x+3.6, y), (x+3.9, y+0.25), (x+1.2, y+0.25)], closed=True,
                 fc="#3a3a3a", ec="none", zorder=6))
    ax.add_patch(Rectangle((x+1.7, y+0.25), 1.9, 1.35, fc="#2b2b2b", ec="none", zorder=6))
    ax.add_patch(Rectangle((x+1.85, y+0.42), 1.6, 1.05, fc=ACCENT, ec="none", alpha=0.85, zorder=7))
    # antenna mast + patch panel (aimed up-left toward drone)
    ax.plot([x-3.2, x-3.2], [y, y+3.4], color=NAVY, lw=2.2, zorder=6)
    ax.plot([x-4.0, x-3.2, x-2.4], [y, y, y], color=NAVY, lw=2.0, zorder=6)  # tripod base
    panel = Polygon([(x-4.3, y+3.2), (x-2.6, y+3.9), (x-2.35, y+3.35), (x-4.05, y+2.65)],
                    closed=True, fc=AMBER, ec=NAVY, lw=0.8, zorder=7)
    ax.add_patch(panel)

# ── Terrain targets under the sensor footprint ──
heat_blob(26.5, 7.6, "Deer")
heat_blob(31.5, 6.9, "Human")
heat_blob(36.0, 7.9, "Turkey")

# ── Drone + thermal sensor footprint ──
DX, DY = 30, 33
ax.add_patch(Polygon([(DX-0.5, DY-1.6), (DX+0.5, DY-1.6), (37.5, 11), (24.0, 11)],
             closed=True, fc=HEAT, ec="none", alpha=0.16, zorder=4))
ax.plot([DX-0.5, 24.0], [DY-1.6, 11], color=HEAT, lw=0.8, alpha=0.5, zorder=4)
ax.plot([DX+0.5, 37.5], [DY-1.6, 11], color=HEAT, lw=0.8, alpha=0.5, zorder=4)
drone(DX, DY)

# survey serpentine path (dashed) at altitude
sx = np.linspace(14, 52, 400)
sy = 30.4 + 0.9*np.sin((sx-14)/38*3*np.pi)
ax.plot(sx, sy, color=SLATE, lw=1.6, ls=(0, (5, 3)), alpha=0.9, zorder=5)
ax.annotate("", xy=(52.4, sy[-1]), xytext=(50.5, sy[-1]-0.1),
            arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=1.6), zorder=5)
ax.text(33, 28.3, "Autonomous survey pattern · 2.23 m/s (R2)", color=SLATE, fontsize=9,
        ha="center", fontweight="bold", zorder=6)

# altitude band annotation (left)
ax.annotate("", xy=(6, 31.4), xytext=(6, 11.2),
            arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.6), zorder=6)
ax.text(6.6, 21, "90–120 m\nAGL (R1)", color=NAVY, fontsize=9.5, va="center",
        fontweight="bold", zorder=6,
        bbox=dict(boxstyle="round,pad=0.28", fc=WHITE, ec=NAVY, lw=0.8, alpha=0.92))

# ── Ground Control Station ──
GX, GY = 82, 2.6
gcs(GX, GY)
ax.text(GX-0.5, 11.4, "Ground Control Station\nLaptop (QGroundControl) + ELRS + directional patch antenna",
        color=NAVY, fontsize=8.6, ha="center", va="bottom", fontweight="bold", zorder=8,
        bbox=dict(boxstyle="round,pad=0.3", fc=WHITE, ec=SLATE, lw=0.8, alpha=0.92))

# ── RF links (drone -> GCS antenna) ──
ant = (GX-3.4, GY+3.6)
def rf(rad, color, label, lx, ly, style="<->"):
    ax.add_patch(FancyArrowPatch((DX+3.4, DY+0.5), ant, connectionstyle=f"arc3,rad={rad}",
                 arrowstyle=style, mutation_scale=13, color=color, lw=2.0, zorder=6, alpha=0.9))
    ax.text(lx, ly, label, color=color, fontsize=8.8, ha="center", fontweight="bold", zorder=7,
            bbox=dict(boxstyle="round,pad=0.22", fc=WHITE, ec=color, lw=0.7, alpha=0.92))
rf(-0.30, ACCENT, "2.4 GHz ELRS · control + telemetry", 57, 33.2)
rf(-0.13, AMBER,  "5.8 GHz · FPV video", 60, 24.2, style="-|>")

# ── Standoff range double-arrow along the ground ──
ax.annotate("", xy=(79, 1.3), xytext=(14, 1.3),
            arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.8), zorder=6)
ax.text(46, 1.5, "≥ 2.8 km surveillance range in ≤ 4.5 m/s wind (R7)", color=NAVY, fontsize=9.2,
        ha="center", va="bottom", fontweight="bold", zorder=7,
        bbox=dict(boxstyle="round,pad=0.2", fc="#f4f7fa", ec=NAVY, lw=0.7, alpha=0.9))

# ── Callouts ──
# onboard AI
ax.annotate("Onboard AI inference →\nautonomous re-route (no downlink required)",
            xy=(DX+1.2, DY+0.4), xytext=(46, 40.2), fontsize=8.8, color=NAVY, fontweight="bold",
            ha="center", zorder=8, arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=1.2),
            bbox=dict(boxstyle="round,pad=0.3", fc="#fff6e9", ec=AMBER, lw=1.0))
# detection
ax.annotate("Detect & classify wildlife / humans by thermal (IR) signature\nR3 · R3.1 detect @ 120 m · R3.2 classify @ 90 m",
            xy=(31, 9.5), xytext=(60, 15.0), fontsize=8.8, color=NAVY, fontweight="bold",
            ha="center", zorder=8, arrowprops=dict(arrowstyle="-|>", color=HEAT, lw=1.3),
            bbox=dict(boxstyle="round,pad=0.3", fc="#fdeee8", ec=HEAT, lw=1.0))
# wind
ax.annotate("", xy=(23.5, 35.2), xytext=(19.5, 35.2),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4), zorder=6)
ax.text(19.2, 35.2, "wind", color=MUTED, fontsize=8, ha="right", va="center", zorder=6)

# ── OV-1 tag + subtitle ──
ax.add_patch(FancyBboxPatch((1.2, 43.0), 8.4, 2.4, boxstyle="round,pad=0.1,rounding_size=0.4",
             fc=NAVY, ec="none", zorder=9))
ax.text(5.4, 44.2, "OV-1", color=WHITE, fontsize=13, ha="center", va="center",
        fontweight="bold", zorder=10)

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT, dpi=150, bbox_inches="tight", pad_inches=0.06, facecolor=WHITE)
from PIL import Image
w, h = Image.open(OUT).size
print("saved", OUT, f"{w}x{h} aspect={w/h:.2f}")
