# -*- coding: utf-8 -*-
"""Overlay amber highlight boxes around the to-be-developed SBC software items
(D-1 thermalModel, D-2 missionApp) on the SysON SBC internal block diagram."""
from PIL import Image, ImageDraw
import os

BASE = r"c:\Users\Josiah Laperriere\Documents\Coding\SurveillanceDrone\SurveillanceDrone\presentation\assets\diagrams\sbc_internal_block_diagram.png"
OUT  = r"c:\Users\Josiah Laperriere\Documents\Coding\SurveillanceDrone\SurveillanceDrone\presentation\assets\diagrams\sbc_internal_block_diagram_dev.png"
AMBER = (217, 130, 30)

img = Image.open(BASE).convert("RGBA")
W, H = img.size
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(overlay)

# Bounding boxes (px) of the two TO_DEVELOP part boxes, with a little padding.
boxes = {
    "missionApp (D-2)":  (150, 218, 323, 295),
    "thermalModel (D-1)": (410, 319, 576, 399),
}
for label, (x0, y0, x1, y1) in boxes.items():
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, outline=AMBER + (255,), width=5,
                        fill=AMBER + (26,))

img = Image.alpha_composite(img, overlay).convert("RGB")
img.save(OUT)
print("saved", OUT, img.size)
