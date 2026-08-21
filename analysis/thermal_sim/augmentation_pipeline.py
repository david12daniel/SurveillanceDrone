#!/usr/bin/env python3
"""
D1.3 — Augmentation Pipeline for Thermal LWIR Training Data

Two modes:
  1. **Albumentations** (recommended): full pipeline with every transform specified
     in the D1.1 data collection plan. Install with `pip install albumentations`.
  2. **OpenCV fallback** (no extra deps): a subset of the most important transforms
     for environments where albumentations isn't available.

Usage
-----
    # Quick test — generate augmented samples
    python3 augmentation_pipeline.py --image /path/to/frame.png --label /path/to/label.txt

    # Import in training script
    from augmentation_pipeline import get_train_augmentations, get_val_augmentations

    aug = get_train_augmentations(target_size=(640, 640))
    augmented = aug(image=image, bboxes=bboxes, class_labels=class_labels)

References
----------
- D1.1 data_collection_plan.md §6 "Annotation Strategy" for the full transform list
- Albumentations docs: https://albumentations.ai/docs/
"""

import copy
import logging
import os
import random
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 1.  Constants
# ---------------------------------------------------------------------------

# YOLO-format: class_id cx cy w h (normalised [0, 1])
CLASS_NAMES = ["deer", "turkey", "human", "other_animal", "background"]
NUM_CLASSES = len(CLASS_NAMES)

# Typical altitude bands used for scale-aware augmentation (metres AGL)
ALTITUDE_BANDS = {
    "low": (80, 100),      # closest approach — objects appear largest
    "nominal": (100, 120),  # primary operating band
    "high": (120, 140),     # farthest — objects appear smallest
}

# ---------------------------------------------------------------------------
# 2.  Albumentations pipeline (primary)
# ---------------------------------------------------------------------------

_albumentations_available = False
try:
    import albumentations as A
    from albumentations.core.composition import BboxParams, Compose

    _albumentations_available = True
except ImportError:
    A = None  # type: ignore[assignment]
    Compose = None
    BboxParams = None

    logger.info(
        "albumentations not installed. Install with: pip install albumentations. "
        "Falling back to OpenCV-only transforms."
    )


def get_train_augmentations(
    target_size: Tuple[int, int] = (640, 640),
    altitude_band: Optional[str] = None,
) -> "Compose":
    """Build the training augmentation pipeline.

    Parameters
    ----------
    target_size : (w, h)
        Output image dimensions after resize.
    altitude_band : str or None
        One of ``"low"``, ``"nominal"``, ``"high"``, or ``None`` for the default
        (nominal-level transforms).  When set, certain scale- and blur-sensitive
        transforms are tuned to match the expected apparent object size.

    Returns
    -------
    A.Compose  (or falls back to OpenCV wrapper)
    """
    if not _albumentations_available:
        return _OpenCVPipeline(target_size=target_size, altitude_band=altitude_band)

    # ---- Scale limits tuned to altitude band ----
    if altitude_band == "low":
        # Objects already large — allow more aggressive shrinking
        scale_limits = (0.5, 1.0)
        blur_limit = 5
    elif altitude_band == "high":
        # Objects already small — avoid shrinking them further
        scale_limits = (0.85, 1.25)
        blur_limit = 3
    else:  # nominal
        scale_limits = (0.7, 1.2)
        blur_limit = 5

    return A.Compose(
        [
            # --- Geometric ---
            A.RandomScale(scale_limit=scale_limits[1] - 1.0, p=0.8),
            A.Rotate(limit=15, border_mode=cv2.BORDER_CONSTANT, value=0, p=0.6),
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.05),  # rarely useful for aerial but harmless

            # --- Photometric (thermal contrast) ---
            A.RandomBrightnessContrast(
                brightness_limit=0.2, contrast_limit=0.2, p=0.8
            ),
            A.RandomGamma(gamma_limit=(80, 160), p=0.5),
            A.CLAHE(clip_limit=2.0, tile_grid_size=(8, 8), p=0.3),

            # --- Blur (motion blur, focus, atmosphere) ---
            A.OneOf(
                [
                    A.MotionBlur(blur_limit=blur_limit, p=1.0),
                    A.GaussianBlur(blur_limit=blur_limit, p=1.0),
                    A.MedianBlur(blur_limit=blur_limit, p=1.0),
                ],
                p=0.3,
            ),

            # --- Noise (sensor noise, varying SNR) ---
            A.OneOf(
                [
                    A.GaussNoise(var_limit=(10.0, 50.0), p=1.0),
                    A.ISONoise(color_shift=(0.01, 0.05), intensity=(0.1, 0.5), p=1.0),
                ],
                p=0.2,
            ),

            # --- Occlusion / dropout ---
            A.CoarseDropout(
                max_holes=8,
                max_height=32,
                max_width=32,
                fill_value=0,
                p=0.3,
            ),

            # --- Resize to target ---
            A.Resize(height=target_size[1], width=target_size[0], p=1.0),

            # --- Normalise (keeps pixel values in [0, 255] for uint8 input) ---
            A.Normalize(mean=(0.0,), std=(1.0,), max_pixel_value=255.0, p=1.0),
        ],
        bbox_params=BboxParams(
            format="yolo",
            min_visibility=0.15,
            label_fields=["class_labels"],
        ),
    )


def get_val_augmentations(
    target_size: Tuple[int, int] = (640, 640),
) -> "Compose":
    """Validation / test pipeline — no stochastic transforms.

    Only resize + normalisation, so every evaluation is deterministic.
    """
    if not _albumentations_available:
        return _OpenCVPipeline(
            target_size=target_size, train=False, altitude_band=None
        )

    return A.Compose(
        [
            A.Resize(height=target_size[1], width=target_size[0], p=1.0),
            A.Normalize(mean=(0.0,), std=(1.0,), max_pixel_value=255.0, p=1.0),
        ],
        bbox_params=BboxParams(
            format="yolo",
            min_visibility=0.0,
            label_fields=["class_labels"],
        ),
    )


# ---------------------------------------------------------------------------
# 3.  Mosaic augmentation (YOLO-style)
# ---------------------------------------------------------------------------


def apply_mosaic(
    images: List[np.ndarray],
    labels: List[List[float]],
    target_size: Tuple[int, int] = (640, 640),
    p: float = 0.5,
) -> Tuple[np.ndarray, List[float], List[int]]:
    """Mosaic augmentation: stitch 4 images into one grid.

    Expects 4 images and their YOLO-format labels.  Returns a single mosaic
    image with re-mapped bounding boxes, and a list of (class_id, cx, cy, w, h)
    in the mosaic coordinate system (normalised to the mosaic size).

    Based on the YOLOv4 / Ultralytics mosaic technique.
    """
    if random.random() > p or len(images) < 4:
        # Fall back to first image unchanged
        h, w = images[0].shape[:2]
        resized = cv2.resize(images[0], target_size, interpolation=cv2.INTER_LINEAR)
        scaled_labels = _scale_labels_to_target(labels[0], (w, h), target_size)
        return resized, scaled_labels, [l[0] for l in scaled_labels]

    # Pick a random centre point inside the central 50% of the mosaic
    mosaic_w, mosaic_h = target_size[0] * 2, target_size[1] * 2
    cx = int(random.uniform(mosaic_w * 0.25, mosaic_w * 0.75))
    cy = int(random.uniform(mosaic_h * 0.25, mosaic_h * 0.75))

    # Build the 4-quadrant mosaic
    mosaic_img = np.zeros((mosaic_h, mosaic_w), dtype=np.uint8)
    all_labels = []

    for i, (img, lbls) in enumerate(zip(images, labels)):
        h_i, w_i = img.shape[:2]
        # Resize all images to the same intermediate size (target)
        inter_size = (target_size[0], target_size[1])
        img_resized = cv2.resize(img, inter_size, interpolation=cv2.INTER_LINEAR)
        if len(img_resized.shape) == 3:
            img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        h_r, w_r = img_resized.shape

        # Determine quadrant placement and source/dest slices
        if i == 0:  # top-left
            x1a = max(cx - w_r, 0)
            y1a = max(cy - h_r, 0)
            x2a = cx
            y2a = cy
            x1b = max(w_r - cx, 0)
            y1b = max(h_r - cy, 0)
            x2b = w_r
            y2b = h_r
        elif i == 1:  # top-right
            x1a = cx
            y1a = max(cy - h_r, 0)
            x2a = min(cx + w_r, mosaic_w)
            y2a = cy
            x1b = 0
            y1b = max(h_r - cy, 0)
            x2b = min(w_r, mosaic_w - cx)
            y2b = h_r
        elif i == 2:  # bottom-left
            x1a = max(cx - w_r, 0)
            y1a = cy
            x2a = cx
            y2a = min(cy + h_r, mosaic_h)
            x1b = max(w_r - cx, 0)
            y1b = 0
            x2b = w_r
            y2b = min(h_r, mosaic_h - cy)
        else:  # bottom-right
            x1a = cx
            y1a = cy
            x2a = min(cx + w_r, mosaic_w)
            y2a = min(cy + h_r, mosaic_h)
            x1b = 0
            y1b = 0
            x2b = min(w_r, mosaic_w - cx)
            y2b = min(h_r, mosaic_h - cy)

        # Validate slices
        dw = x2a - x1a  # dest width
        dh = y2a - y1a  # dest height
        sw = x2b - x1b  # source width
        sh = y2b - y1b  # source height
        if dw <= 0 or dh <= 0 or sw <= 0 or sh <= 0:
            continue  # empty quadrant

        # Copy the relevant slice of the resized image into the mosaic
        mosaic_img[y1a:y2a, x1a:x2a] = img_resized[y1b:y2b, x1b:x2b]

        # Re-map labels: convert from original-image coords to mosaic coords
        x_off = x1a
        y_off = y1a
        for lbl in lbls:
            cls_id, cx_n, cy_n, w_n, h_n = lbl
            # Convert to pixel coords in the resized image
            cx_px = cx_n * inter_size[0]
            cy_px = cy_n * inter_size[1]
            w_px = w_n * inter_size[0]
            h_px = h_n * inter_size[1]

            # Shift to mosaic coords
            cx_px_mosaic = cx_px + x_off
            cy_px_mosaic = cy_px + y_off

            # Clip to mosaic bounds
            cx_px_mosaic = max(0, min(cx_px_mosaic, mosaic_w))
            cy_px_mosaic = max(0, min(cy_px_mosaic, mosaic_h))
            w_px_clipped = min(w_px, mosaic_w - cx_px_mosaic)
            h_px_clipped = min(h_px, mosaic_h - cy_px_mosaic)

            if w_px_clipped < 2 or h_px_clipped < 2:
                continue  # too small

            # Normalise to mosaic dimensions
            all_labels.append([
                cls_id,
                cx_px_mosaic / mosaic_w,
                cy_px_mosaic / mosaic_h,
                w_px_clipped / mosaic_w,
                h_px_clipped / mosaic_h,
            ])

    if not all_labels:
        # Fallback: return the first image unchanged
        h, w = images[0].shape[:2]
        resized = cv2.resize(images[0], target_size, interpolation=cv2.INTER_LINEAR)
        if len(resized.shape) == 3:
            resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        scaled_labels = _scale_labels_to_target(labels[0], (w, h), target_size)
        class_ids = [int(l[0]) for l in scaled_labels]
        return resized, scaled_labels, class_ids

    # Resize mosaic to target
    final = cv2.resize(mosaic_img, target_size, interpolation=cv2.INTER_LINEAR)
    # Re-normalise labels after resize
    final_labels = _scale_labels_to_target(
        all_labels,
        (target_size[0] * 2, target_size[1] * 2),
        target_size,
    )
    class_ids = [int(l[0]) for l in final_labels]
    return final, final_labels, class_ids


# ---------------------------------------------------------------------------
# 4.  OpenCV-only fallback pipeline
# ---------------------------------------------------------------------------


class _OpenCVPipeline:
    """Minimal pipeline using only OpenCV (no albumentations).

    Implements a subset of the transforms defined in the albumentations
    pipeline — enough for basic data loading but without the full stochastic
    variety.
    """

    def __init__(
        self,
        target_size: Tuple[int, int] = (640, 640),
        train: bool = True,
        altitude_band: Optional[str] = None,
    ):
        self.target_size = target_size
        self.train = train
        self.altitude_band = altitude_band

    def __call__(
        self,
        *,
        image: np.ndarray,
        bboxes: Optional[List[List[float]]] = None,
        class_labels: Optional[List[int]] = None,
    ) -> Dict[str, any]:
        h, w = image.shape[:2]
        gray = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if self.train:
            # Random horizontal flip
            if random.random() < 0.5:
                gray = cv2.flip(gray, 1)
                if bboxes is not None:
                    bboxes = _flip_bboxes_horizontal(bboxes, w)

            # Random brightness
            if random.random() < 0.5:
                beta = random.randint(-30, 30)
                gray = cv2.convertScaleAbs(gray, alpha=1.0, beta=beta)

            # Random gamma
            if random.random() < 0.3:
                gamma = random.uniform(0.6, 1.6)
                gray = _adjust_gamma(gray, gamma)

            # Random blur
            if random.random() < 0.3:
                k = random.choice([3, 5])
                gray = cv2.GaussianBlur(gray, (k, k), 0)

        # Resize
        resized = cv2.resize(gray, self.target_size, interpolation=cv2.INTER_LINEAR)

        # Normalise to [0, 1]
        normalised = resized.astype(np.float32) / 255.0

        result = {"image": normalised}
        if bboxes is not None and class_labels is not None:
            # Scale bboxes to target size
            scale_x = self.target_size[0] / w
            scale_y = self.target_size[1] / h
            scaled = []
            kept_labels = []
            for bbox, cls in zip(bboxes, class_labels):
                cx, cy, bw, bh = bbox
                cx_s = cx * scale_x / self.target_size[0]
                cy_s = cy * scale_y / self.target_size[1]
                bw_s = bw * scale_x / self.target_size[0]
                bh_s = bh * scale_y / self.target_size[1]
                if bw_s > 0.0 and bh_s > 0.0:
                    scaled.append([cx_s, cy_s, bw_s, bh_s])
                    kept_labels.append(cls)
            result["bboxes"] = scaled
            result["class_labels"] = kept_labels

        return result


# ---------------------------------------------------------------------------
# 5.  Helper utilities
# ---------------------------------------------------------------------------


def _adjust_gamma(img: np.ndarray, gamma: float) -> np.ndarray:
    """Apply gamma correction."""
    inv_gamma = 1.0 / gamma
    table = np.array(
        [((i / 255.0) ** inv_gamma) * 255 for i in np.arange(256)]
    ).astype("uint8")
    return cv2.LUT(img, table)


def _flip_bboxes_horizontal(
    bboxes: List[List[float]], img_width: int
) -> List[List[float]]:
    """Flip YOLO-format cx coordinates horizontally."""
    flipped = []
    for bbox in bboxes:
        cx, cy, bw, bh = bbox
        flipped.append([1.0 - cx, cy, bw, bh])
    return flipped


def _scale_labels_to_target(
    labels: List[List[float]],
    src_size: Tuple[int, int],
    dst_size: Tuple[int, int],
) -> List[List[float]]:
    """Scale YOLO labels from one image size to another."""
    sx = dst_size[0] / src_size[0]
    sy = dst_size[1] / src_size[1]
    scaled = []
    for lbl in labels:
        cls_id, cx, cy, w, h = lbl
        scaled.append([cls_id, cx * sx, cy * sy, w * sx, h * sy])
    return scaled


def yolo_to_xyxy(
    bboxes: List[List[float]], img_w: int, img_h: int
) -> List[Tuple[int, int, int, int]]:
    """Convert YOLO-format (cx, cy, w, h) normalised → (x1, y1, x2, y2) pixel.

    Returns integer pixel coordinates suitable for OpenCV drawing.
    """
    out = []
    for cx, cy, w, h in bboxes:
        x1 = int((cx - w / 2) * img_w)
        y1 = int((cy - h / 2) * img_h)
        x2 = int((cx + w / 2) * img_w)
        y2 = int((cy + h / 2) * img_h)
        out.append((x1, y1, x2, y2))
    return out


def draw_bboxes(
    img: np.ndarray,
    bboxes: List[List[float]],
    class_ids: List[int],
    color: Tuple[int, int, int] = (0, 255, 0),
) -> np.ndarray:
    """Draw YOLO-format bounding boxes on an image for visualisation."""
    h, w = img.shape[:2]
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) if len(img.shape) == 2 else img.copy()
    for bbox, cls_id in zip(bboxes, class_ids):
        x1, y1, x2, y2 = yolo_to_xyxy([bbox], w, h)[0]
        cv2.rectangle(vis, (x1, y1), (x2, y2), color, 2)
        label = f"{CLASS_NAMES[cls_id] if cls_id < len(CLASS_NAMES) else '?'}"
        cv2.putText(vis, label, (x1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return vis


# ---------------------------------------------------------------------------
# 6.  Quick-test CLI
# ---------------------------------------------------------------------------


def _parse_yolo_label(path: str) -> Tuple[List[List[float]], List[int]]:
    """Read a YOLO-format .txt file.

    Returns (bboxes, class_ids) where each bbox is [cx, cy, w, h] normalised.
    """
    bboxes, class_ids = [], []
    with open(path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:
                continue
            cls_id = int(parts[0])
            cx, cy, w, h = map(float, parts[1:5])
            bboxes.append([cx, cy, w, h])
            class_ids.append(cls_id)
    return bboxes, class_ids


def _save_yolo_label(
    path: str, bboxes: List[List[float]], class_ids: List[int]
) -> None:
    """Write YOLO-format .txt file."""
    with open(path, "w") as f:
        for bbox, cls_id in zip(bboxes, class_ids):
            cx, cy, w, h = bbox
            f.write(f"{int(cls_id)} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="D1.3 Augmentation Pipeline — quick test"
    )
    parser.add_argument("--image", required=True, help="Path to input image (grayscale or RGB)")
    parser.add_argument("--label", default=None, help="Path to YOLO-format .txt label")
    parser.add_argument("--output", default="augmented_output", help="Output directory")
    parser.add_argument("--samples", type=int, default=4, help="Number of augmented samples to generate")
    parser.add_argument("--target-size", type=int, nargs=2, default=(640, 640), help="Target (w, h)")
    parser.add_argument("--altitude-band", default=None, choices=["low", "nominal", "high"],
                        help="Altitude band for transform tuning")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # Load image
    img = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {args.image}")
    h, w = img.shape[:2]
    logger.info("Loaded %s — %dx%d", args.image, w, h)

    # Load labels
    bboxes, class_ids = [], []
    if args.label:
        bboxes, class_ids = _parse_yolo_label(args.label)
        logger.info("Loaded %d labels from %s", len(bboxes), args.label)

    # Build pipeline
    aug = get_train_augmentations(
        target_size=tuple(args.target_size),
        altitude_band=args.altitude_band,
    )

    # Generate augmented samples
    for i in range(args.samples):
        if bboxes:
            augmented = aug(
                image=img,
                bboxes=bboxes,
                class_labels=class_ids,
            )
            aug_img = augmented["image"]
            aug_bboxes = augmented["bboxes"]
            aug_class_ids = augmented["class_labels"]
        else:
            aug_img = aug(image=img)["image"]

        # Denormalise for saving (aug_img is in [0, 1] from Normalize)
        if aug_img.max() <= 1.0:
            save_img = (aug_img * 255).astype(np.uint8)
        else:
            save_img = aug_img.astype(np.uint8)

        # Save image
        out_path = os.path.join(args.output, f"sample_{i:04d}.png")
        cv2.imwrite(out_path, save_img)

        # Save labels
        if bboxes and aug_bboxes:
            label_path = os.path.join(args.output, f"sample_{i:04d}.txt")
            _save_yolo_label(label_path, aug_bboxes, aug_class_ids)

        # Save visualisation
        if bboxes and aug_bboxes:
            vis = draw_bboxes(
                save_img, aug_bboxes, aug_class_ids, color=(255, 255, 255)
            )
            vis_path = os.path.join(args.output, f"sample_{i:04d}_vis.png")
            cv2.imwrite(vis_path, vis)

        logger.info("Saved sample %d/%d", i + 1, args.samples)

    logger.info("Done — %d samples written to %s", args.samples, args.output)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()