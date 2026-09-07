#!/usr/bin/env python3
"""
D1.3 — Labeling Pipeline for Thermal LWIR Training Data

Connects raw extracted frames → annotation workspace → final YOLO dataset.
Supports CVAT 1.1 (XML) and labelImg/YOLO-format workflows. Can merge
self-labeled data with existing bootstrap datasets (BIRDSAI, FLIR ADAS).

Workflow
--------
  1. prepare_workspace() — copy extracted frames into a clean annotation directory
  2. Annotate frames in CVAT (import via XML task, export XML 1.1)
  3. import_cvat_xml() — convert CVAT XML 1.1 back to YOLO .txt files
  4. assemble_dataset() — train/val split + dataset.yaml, optionally merge
     with existing bootstraps

Usage
-----
    # Step 1: Set up annotation workspace from extracted frames
    python3 labeling_pipeline.py prepare --input extracted_frames/ --output annotation_workspace/

    # Step 2: (manual) Annotate in CVAT at http://localhost:8080
    #         Import images via CVAT API or "Load images" from annotation_workspace/images/

    # Step 3: Import CVAT XML annotations → YOLO labels
    python3 labeling_pipeline.py import-cvat \
        --cvat-xml annotations.xml \
        --image-dir annotation_workspace/images/ \
        --label-dir annotation_workspace/labels/

    # Step 4: Assemble final training dataset (with optional bootstrap merge)
    python3 labeling_pipeline.py assemble \
        --annotated annotation_workspace/ \
        --output datasets/final_thermal_v1/ \
        --bootstrap /path/to/bootstrap_birdsai/

    # All steps in one shot (after CVAT export is done):
    python3 labeling_pipeline.py full-pipeline \
        --cvat-xml annotations.xml \
        --extracted-frames extracted_frames/ \
        --output datasets/final_thermal_v1/

References
----------
- CVAT XML 1.1 format: https://openvinotoolkit.github.io/cvat/docs/manual/advanced/xml_format/
- BIRDSAI: conservation_drones_train_real.zip (CDLA-Permissive-1.0)
- Class mapping: {0: deer, 1: turkey, 2: other_animal, 3: human}
"""

import argparse
import csv
import logging
import os
import random
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import cv2
import numpy as np

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CLASS_NAMES = ["deer", "turkey", "other_animal", "human"]
CLASS_MAP = {name: idx for idx, name in enumerate(CLASS_NAMES)}  # case-insensitive lookup
NUM_CLASSES = len(CLASS_NAMES)

VALID_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"}

# CVAT label name → our class_id mapping
CVAT_LABEL_MAP: Dict[str, int] = {
    "deer": 0,
    "turkey": 1,
    "other_animal": 2,
    "other animal": 2,
    "other_animal ": 2,
    "human": 3,
    "person": 3,
    "animal": 2,  # generic fallback
}

DEFAULT_TRAIN_SPLIT = 0.85  # 85% train, 15% validation

# ---------------------------------------------------------------------------
# Step 1: Prepare annotation workspace
# ---------------------------------------------------------------------------


def prepare_workspace(
    input_dir: str,
    output_dir: str,
    max_images: Optional[int] = None,
    symmetric_sample: bool = False,
    seed: int = 42,
) -> None:
    """Copy extracted frames into a clean annotation workspace.

    Parameters
    ----------
    input_dir : str or Path
        Input directory containing extracted frames (from extract_frames.py).
        Can be a flat directory of .png images or a clip-structured directory.
    output_dir : str or Path
        Output annotation workspace. Creates ``output_dir/images/``.
    max_images : int or None
        Maximum number of images to include (None = all). Useful for initial
        annotation batches rather than overwhelming the annotator.
    symmetric_sample : bool
        If True and ``max_images`` is set, sample uniformly across input
        subdirectories (for clip-structured input) rather than taking the
        first N from a global shuffle.
    seed : int
        Random seed for shuffling/sampling.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.is_dir():
        raise NotADirectoryError(f"Input directory not found: {input_dir}")

    out_images = output_path / "images"
    out_images.mkdir(parents=True, exist_ok=True)

    # Collect all image files
    all_images: List[Path] = []
    for ext in VALID_IMAGE_EXTS:
        all_images.extend(input_path.rglob(f"*{ext}"))

    # Also check for caps
    for ext in [e.upper() for e in VALID_IMAGE_EXTS]:
        all_images.extend(input_path.rglob(f"*{ext}"))

    # Deduplicate
    all_images = sorted(set(all_images))
    random.seed(seed)
    random.shuffle(all_images)

    if not all_images:
        logger.warning("No image files found in %s", input_dir)
        return

    logger.info(
        "Found %d images in %s", len(all_images), input_dir
    )

    # Sample if needed
    if max_images and len(all_images) > max_images:
        if symmetric_sample:
            # For clip-structured input, sample uniformly per subdirectory
            subdirs: Dict[str, List[Path]] = {}
            for img in all_images:
                # Use the immediate parent directory name as the clip key
                parent_name = img.parent.name if img.parent != input_path else "root"
                subdirs.setdefault(parent_name, []).append(img)
            per_subdir = max(1, max_images // len(subdirs))
            selected: List[Path] = []
            for _name, imgs in sorted(subdirs.items()):
                sample = imgs[:per_subdir]
                selected.extend(sample)
                logger.debug(
                    "  %s: %d → %d images", _name, len(imgs), len(sample)
                )
            # Trim excess from global shuffle
            random.shuffle(selected)
            all_images = selected[:max_images]
        else:
            all_images = all_images[:max_images]

    logger.info("Copying %d images to annotation workspace...", len(all_images))

    for img_path in all_images:
        # Flatten naming: preserve original filename but prefix with subdir to
        # avoid collisions when same filenames exist across clips
        rel = img_path.relative_to(input_path)
        flat_name = "_".join(rel.parts) if len(rel.parts) > 1 else rel.name
        # Replace path separators in the flat name
        flat_name = flat_name.replace("/", "_").replace("\\", "_")
        dest = out_images / flat_name
        shutil.copy2(img_path, dest)

    logger.info(
        "Annotation workspace ready: %s  (%d images)", output_path, len(all_images)
    )
    logger.info("  Images: %s", out_images)
    logger.info(
        "  Next: annotate in CVAT, then run: python3 labeling_pipeline.py import-cvat ..."
    )


# ---------------------------------------------------------------------------
# Step 3 (skipping step 2 — manual CVAT): Import CVAT XML 1.1 → YOLO
# ---------------------------------------------------------------------------


def _parse_cvat_annotation(
    xml_path: str,
) -> Tuple[Dict[str, int], Dict[str, List[Dict]]]:
    """Parse a CVAT 1.1 XML annotation file.

    Returns
    -------
    image_dims : dict of {filename: (width, height)}
    annotations : dict of {filename: [{"label": str, "xtl": float, "ytl": float,
                                        "xbr": float, "ybr": float}]}
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    image_dims: Dict[str, int] = {}
    annotations: Dict[str, List[Dict]] = {}

    for image_elem in root.findall("image"):
        name = image_elem.get("name", "")
        width = int(image_elem.get("width", 0))
        height = int(image_elem.get("height", 0))
        image_dims[name] = (width, height)

        boxes = []
        for box_elem in image_elem.findall("box"):
            label = box_elem.get("label", "")
            xtl = float(box_elem.get("xtl", 0))
            ytl = float(box_elem.get("ytl", 0))
            xbr = float(box_elem.get("xbr", 0))
            ybr = float(box_elem.get("ybr", 0))
            # CVAT coordinates are absolute pixel values
            boxes.append({
                "label": label,
                "xtl": xtl,
                "ytl": ytl,
                "xbr": xbr,
                "ybr": ybr,
            })

        # Also handle points, polylines, polygons if present (skip for now)
        # but log a warning so the user knows they exist
        other_shapes = (
            image_elem.findall("points")
            + image_elem.findall("polyline")
            + image_elem.findall("polygon")
        )
        if other_shapes:
            logger.warning(
                "Image '%s' has %d non-box annotations (skipped). "
                "Only <box> elements are converted to YOLO format.",
                name,
                len(other_shapes),
            )

        if boxes:
            annotations[name] = boxes

    return image_dims, annotations


def _cvat_box_to_yolo(
    xtl: float,
    ytl: float,
    xbr: float,
    ybr: float,
    img_w: int,
    img_h: int,
) -> Tuple[float, float, float, float]:
    """Convert CVAT absolute coordinates to YOLO-format normalized [cx, cy, w, h]."""
    # Sort so x1 < x2, y1 < y2
    x1 = min(xtl, xbr)
    x2 = max(xtl, xbr)
    y1 = min(ytl, ybr)
    y2 = max(ytl, ybr)

    # Clamp to image bounds
    x1 = max(0.0, x1)
    y1 = max(0.0, y1)
    x2 = min(float(img_w), x2)
    y2 = min(float(img_h), y2)

    bw = x2 - x1
    bh = y2 - y1

    # Minimum size guard (skip degenerate boxes)
    if bw < 1 or bh < 1:
        return None

    cx = (x1 + bw / 2) / img_w
    cy = (y1 + bh / 2) / img_h
    nw = bw / img_w
    nh = bh / img_h

    # Clamp to [0, 1]
    cx = max(0.0, min(1.0, cx))
    cy = max(0.0, min(1.0, cy))
    nw = max(0.0, min(1.0, nw))
    nh = max(0.0, min(1.0, nh))

    # Skip boxes that collapsed to nothing
    if nw < 0.001 or nh < 0.001:
        return None

    return cx, cy, nw, nh


def _resolve_label(label: str) -> Optional[int]:
    """Map a CVAT label string to our class ID. Case-insensitive fuzzy match."""
    label_lower = label.strip().lower()
    # Direct match
    if label_lower in CVAT_LABEL_MAP:
        return CVAT_LABEL_MAP[label_lower]

    # Fuzzy: check if any key is a substring
    for key, cls_id in CVAT_LABEL_MAP.items():
        if key in label_lower or label_lower in key:
            return cls_id

    logger.warning("Unknown label '%s' — skipping", label)
    return None


def import_cvat_xml(
    cvat_xml: str,
    image_dir: str,
    label_dir: str,
    skip_unmatched: bool = True,
) -> None:
    """Convert CVAT XML 1.1 annotations to YOLO .txt files.

    Parameters
    ----------
    cvat_xml : str
        Path to CVAT XML 1.1 annotation file.
    image_dir : str
        Directory containing the annotated images. Used to copy images to
        the same location as labels.
    label_dir : str
        Output directory for YOLO .txt label files.
    skip_unmatched : bool
        If True, skip images that have annotations but no corresponding
        image file in ``image_dir``. If False, raise an error.
    """
    xml_path = Path(cvat_xml)
    img_dir = Path(image_dir)
    lbl_dir = Path(label_dir)

    if not xml_path.is_file():
        raise FileNotFoundError(f"CVAT XML not found: {cvat_xml}")

    lbl_dir.mkdir(parents=True, exist_ok=True)

    # Parse
    image_dims, annotations = _parse_cvat_annotation(str(xml_path))
    logger.info(
        "Parsed CVAT XML: %d images with annotations, %d total annotations",
        len(annotations),
        sum(len(v) for v in annotations.values()),
    )

    # Build index of images in the image dir (flat, by filename)
    available_images: Dict[str, Path] = {}
    for f in img_dir.iterdir():
        if f.is_file() and f.suffix.lower() in VALID_IMAGE_EXTS:
            available_images[f.name] = f

    converted = 0
    skipped = 0
    empty = 0

    for img_name, boxes in annotations.items():
        # Find the image file
        img_path = available_images.get(img_name)
        if img_path is None:
            if skip_unmatched:
                logger.debug(
                    "Image '%s' not found in %s — skipping",
                    img_name,
                    image_dir,
                )
                skipped += 1
                continue
            else:
                raise FileNotFoundError(
                    f"Image '{img_name}' from CVAT XML not found in {image_dir}"
                )

        # Get image dimensions
        w, h = image_dims.get(img_name)
        if w is None or h is None:
            # Fallback: read from file
            img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
            if img is None:
                logger.warning(
                    "Cannot read image '%s' — skipping", img_name
                )
                continue
            h, w = img.shape[:2]

        # Convert each box to YOLO format
        yolo_lines: List[str] = []
        for box in boxes:
            cls_id = _resolve_label(box["label"])
            if cls_id is None:
                continue

            yolo = _cvat_box_to_yolo(
                box["xtl"], box["ytl"], box["xbr"], box["ybr"], w, h
            )
            if yolo is None:
                continue

            cx, cy, nw, nh = yolo
            yolo_lines.append(f"{cls_id} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}")

        if not yolo_lines:
            empty += 1
            continue

        # Write label file
        label_name = img_path.stem + ".txt"
        label_path = lbl_dir / label_name
        with open(label_path, "w") as f:
            for line in yolo_lines:
                f.write(line + "\n")

        converted += 1

    logger.info("Conversion complete:")
    logger.info("  Converted: %d images with labels", converted)
    logger.info("  Skipped (no matching image): %d", skipped)
    logger.info("  Empty (all boxes filtered): %d", empty)
    logger.info("  Labels written to: %s", label_dir)

    # Write a summary CSV
    summary_path = lbl_dir / "import_summary.csv"
    with open(summary_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "status",
                "count",
            ]
        )
        writer.writerow(["converted", converted])
        writer.writerow(["skipped_no_image", skipped])
        writer.writerow(["empty", empty])

    logger.info("Summary: %s", summary_path)


# ---------------------------------------------------------------------------
# Step 4: Assemble final dataset (train/val split + optional bootstrap merge)
# ---------------------------------------------------------------------------


def _collect_labeled_pairs(data_dir: Path) -> List[Tuple[Path, Path]]:
    """Collect (image_path, label_path) pairs from a directory that has
    ``images/`` and ``labels/`` subdirectories."""
    images_dir = data_dir / "images"
    labels_dir = data_dir / "labels"

    if not images_dir.is_dir():
        logger.warning("No images directory in %s", data_dir)
        return []

    # Collect label files
    label_index: Dict[str, Path] = {}
    if labels_dir.is_dir():
        for f in labels_dir.iterdir():
            if f.is_file() and f.suffix == ".txt":
                label_index[f.stem] = f

    pairs: List[Tuple[Path, Path]] = []
    for f in images_dir.iterdir():
        if f.is_file() and f.suffix.lower() in VALID_IMAGE_EXTS:
            label_path = label_index.get(f.stem)
            if label_path is not None:
                pairs.append((f, label_path))
    return pairs


def _merge_class_counts(
    existing: Dict[int, int], new_labels_dir: Path
) -> Dict[int, int]:
    """Count class occurrences in a labels directory and merge into existing counts."""
    for f in new_labels_dir.iterdir():
        if f.suffix != ".txt":
            continue
        with open(f) as fh:
            for line in fh:
                parts = line.strip().split()
                if parts:
                    try:
                        cls_id = int(parts[0])
                        existing[cls_id] = existing.get(cls_id, 0) + 1
                    except ValueError:
                        pass
    return existing


def assemble_dataset(
    annotated_dir: Optional[str],
    output_dir: str,
    bootstrap_dirs: Optional[List[str]] = None,
    test_pct: float = 0.15,
    seed: int = 42,
) -> None:
    """Assemble labeled images + YOLO labels into a training-ready dataset.

    Creates ``output_dir/`` with ``images/train/``, ``images/val/``,
    ``labels/train/``, ``labels/val/``, and ``dataset.yaml``.

    Parameters
    ----------
    annotated_dir : str or None
        Path to directory containing ``images/`` and ``labels/`` (from CVAT
        import). If None, only bootstrap data is assembled.
    output_dir : str
        Output dataset directory.
    bootstrap_dirs : list of str or None
        Additional bootstrap dataset directories to merge (e.g., BIRDSAI,
        FLIR ADAS). Each must have ``images/train/`` + ``labels/train/``
        (and optionally ``images/val/`` + ``labels/val/``).
    test_pct : float
        Fraction of annotated data to reserve for validation.
    seed : int
        Random seed.
    """
    out_path = Path(output_dir)
    random.seed(seed)

    # --- Collect annotated pairs ---
    annotated_pairs: List[Tuple[Path, Path]] = []
    class_counts: Dict[int, int] = {}

    if annotated_dir:
        annotated_pairs = _collect_labeled_pairs(Path(annotated_dir))
        logger.info(
            "Found %d annotated image-label pairs in %s",
            len(annotated_pairs),
            annotated_dir,
        )
        class_counts = _merge_class_counts(
            class_counts, Path(annotated_dir) / "labels"
        )

    # --- Collect bootstrap pairs (from train splits) ---
    bootstrap_pairs: List[Tuple[Path, Path]] = []
    bootstrap_val_pairs: List[Tuple[Path, Path]] = []

    if bootstrap_dirs:
        for bdir in bootstrap_dirs:
            bpath = Path(bdir)
            # Train
            train_pairs = _collect_labeled_pairs(bpath / "train") if (bpath / "train" / "images").is_dir() else []
            if not train_pairs:
                train_pairs = _collect_labeled_pairs(bpath)
            if train_pairs:
                bootstrap_pairs.extend(train_pairs)
                _merge_class_counts(class_counts, bpath / "labels" / "train")
                logger.info(
                    "  Bootstrap train: %d pairs from %s",
                    len(train_pairs),
                    bdir,
                )
            # Val
            val_pairs = _collect_labeled_pairs(bpath / "val") if (bpath / "val" / "images").is_dir() else []
            if val_pairs:
                bootstrap_val_pairs.extend(val_pairs)

    # --- Split annotated data ---
    random.shuffle(annotated_pairs)
    n_val = max(1, int(len(annotated_pairs) * test_pct))
    annotated_val = annotated_pairs[:n_val]
    annotated_train = annotated_pairs[n_val:]

    logger.info(
        "Annotated split: %d train, %d val",
        len(annotated_train),
        len(annotated_val),
    )

    # --- Create output directories ---
    for split_name in ("train", "val"):
        (out_path / "images" / split_name).mkdir(parents=True, exist_ok=True)
        (out_path / "labels" / split_name).mkdir(parents=True, exist_ok=True)

    # --- Copy annotated data ---
    def _copy_pairs(pairs: List[Tuple[Path, Path]], split: str) -> None:
        for img_path, label_path in pairs:
            # Copy image
            dest_img = out_path / "images" / split / img_path.name
            shutil.copy2(img_path, dest_img)
            # Copy label
            dest_label = out_path / "labels" / split / label_path.name
            shutil.copy2(label_path, dest_label)

    _copy_pairs(annotated_train, "train")
    _copy_pairs(annotated_val, "val")

    # --- Copy bootstrap data ---
    # Bootstrap train goes to train; bootstrap val goes to val
    _copy_pairs(bootstrap_pairs, "train")
    _copy_pairs(bootstrap_val_pairs, "val")

    # --- Final counts ---
    train_images = len(list((out_path / "images" / "train").iterdir()))
    val_images = len(list((out_path / "images" / "val").iterdir()))
    final_class_counts: Dict[int, int] = {}
    for split in ("train", "val"):
        label_dir = out_path / "labels" / split
        _merge_class_counts(final_class_counts, label_dir)

    # Log summary
    logger.info("=" * 60)
    logger.info("Dataset assembly complete: %s", output_dir)
    logger.info("  Train images: %d", train_images)
    logger.info("  Val images:   %d", val_images)
    for cls_id, count in sorted(final_class_counts.items()):
        cls_name = CLASS_NAMES[cls_id] if cls_id < NUM_CLASSES else f"class_{cls_id}"
        logger.info("  %s boxes: %d", cls_name, count)

    # --- Write dataset.yaml ---
    yaml_path = out_path / "dataset.yaml"
    yaml_content = f"""# DroneThermalModel dataset — assembled {output_dir}
# Auto-generated by labeling_pipeline.py assemble

train: {out_path / 'images' / 'train'}
val: {out_path / 'images' / 'val'}

nc: {NUM_CLASSES}
names:
{chr(10).join(f'  {i}: {name}' for i, name in enumerate(CLASS_NAMES))}
"""
    with open(yaml_path, "w") as f:
        f.write(yaml_content)
    logger.info("  dataset.yaml: %s", yaml_path)

    # --- Write assembly report ---
    report_path = out_path / "assembly_report.txt"
    with open(report_path, "w") as f:
        f.write(f"DroneThermalModel Dataset Assembly Report\n")
        f.write(f"{'=' * 50}\n\n")
        f.write(f"Date: 2026-09-03\n")
        f.write(f"Source annotated dir: {annotated_dir or 'N/A'}\n")
        f.write(f"Bootstrap dirs: {bootstrap_dirs or 'None'}\n")
        f.write(f"\nTrain images: {train_images}\n")
        f.write(f"Val images:   {val_images}\n")
        f.write(f"\nClass distribution:\n")
        for cls_id, count in sorted(final_class_counts.items()):
            cls_name = CLASS_NAMES[cls_id] if cls_id < NUM_CLASSES else f"class_{cls_id}"
            f.write(f"  {cls_name}: {count} boxes\n")
        f.write(f"\ndataset.yaml: {yaml_path}\n")
    logger.info("  Report: %s", report_path)


# ---------------------------------------------------------------------------
# Validation helper
# ---------------------------------------------------------------------------


def validate_dataset(dataset_dir: str) -> None:
    """Validate a YOLO-format dataset for sanity.

    Checks:
    - Each label file has a corresponding image file
    - Each label file has valid YOLO-format lines
    - No class IDs outside [0, nc)
    - dataset.yaml exists and is parseable
    """
    dataset_path = Path(dataset_dir)

    if not dataset_path.is_dir():
        logger.error("Dataset directory not found: %s", dataset_dir)
        return

    # Read dataset.yaml
    yaml_path = dataset_path / "dataset.yaml"
    if not yaml_path.is_file():
        logger.error("dataset.yaml not found in %s", dataset_dir)
        return

    yaml_content = yaml_path.read_text()
    nc = NUM_CLASSES  # default
    for line in yaml_content.splitlines():
        line = line.strip()
        if line.startswith("nc:"):
            try:
                nc = int(line.split(":")[1].strip())
            except (ValueError, IndexError):
                pass

    logger.info("Validating dataset: %s  (nc=%d)", dataset_dir, nc)

    total_issues = 0

    for split in ("train", "val"):
        images_dir = dataset_path / "images" / split
        labels_dir = dataset_path / "labels" / split

        if not images_dir.is_dir():
            logger.warning("  %s: no images directory", split)
            continue

        # Index images
        image_stems: Set[str] = set()
        for f in images_dir.iterdir():
            if f.suffix.lower() in VALID_IMAGE_EXTS:
                image_stems.add(f.stem)

        if not labels_dir.is_dir():
            logger.warning("  %s: no labels directory", split)
            continue

        # Check each label file
        label_stems: Set[str] = set()
        for f in labels_dir.iterdir():
            if f.suffix != ".txt":
                continue
            label_stems.add(f.stem)

            # Validate label content
            with open(f) as fh:
                for line_num, line in enumerate(fh, 1):
                    parts = line.strip().split()
                    if len(parts) < 5:
                        logger.warning(
                            "  %s: %s line %d — malformed (%d fields)",
                            split,
                            f.name,
                            line_num,
                            len(parts),
                        )
                        total_issues += 1
                        continue
                    try:
                        cls_id = int(parts[0])
                        if cls_id < 0 or cls_id >= nc:
                            logger.warning(
                                "  %s: %s line %d — class ID %d out of range [0, %d)",
                                split,
                                f.name,
                                line_num,
                                cls_id,
                                nc,
                            )
                            total_issues += 1
                        # Check values are in [0, 1]
                        for j, val in enumerate(parts[1:5], 1):
                            v = float(val)
                            if v < 0 or v > 1:
                                logger.warning(
                                    "  %s: %s line %d — value %d (%.4f) outside [0,1]",
                                    split,
                                    f.name,
                                    line_num,
                                    j,
                                    v,
                                )
                                total_issues += 1
                    except ValueError as e:
                        logger.warning(
                            "  %s: %s line %d — parse error: %s",
                            split,
                            f.name,
                            line_num,
                            e,
                        )
                        total_issues += 1

        # Check orphan labels (no corresponding image)
        orphan_stems = label_stems - image_stems
        if orphan_stems:
            logger.warning(
                "  %s: %d orphan labels (no matching image)", split, len(orphan_stems)
            )
            total_issues += len(orphan_stems)

        # Check images with no labels
        no_label_stems = image_stems - label_stems
        if no_label_stems:
            logger.info(
                "  %s: %d images with no labels (untracked)", split, len(no_label_stems)
            )

        logger.info(
            "  %s: %d images, %d label files — valid",
            split,
            len(image_stems),
            len(label_stems),
        )

    if total_issues == 0:
        logger.info("✅ Dataset validation passed — no issues found")
    else:
        logger.warning("⚠️  Dataset validation found %d issues", total_issues)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="D1.3 Labeling Pipeline for Thermal LWIR Training Data"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # prepare
    p_prep = subparsers.add_parser(
        "prepare", help="Step 1: Prepare annotation workspace from extracted frames"
    )
    p_prep.add_argument(
        "--input", "-i", required=True, help="Input directory of extracted frames"
    )
    p_prep.add_argument(
        "--output", "-o", required=True, help="Output annotation workspace directory"
    )
    p_prep.add_argument(
        "--max-images",
        type=int,
        default=None,
        help="Max images to include (useful for batch annotation)",
    )
    p_prep.add_argument(
        "--symmetric-sample",
        action="store_true",
        help="Sample uniformly across input subdirectories",
    )
    p_prep.add_argument("--seed", type=int, default=42, help="Random seed")

    # import-cvat
    p_cvat = subparsers.add_parser(
        "import-cvat",
        help="Step 3: Import CVAT XML 1.1 annotations → YOLO .txt labels",
    )
    p_cvat.add_argument("--cvat-xml", required=True, help="CVAT XML 1.1 file")
    p_cvat.add_argument(
        "--image-dir", required=True, help="Directory containing annotated images"
    )
    p_cvat.add_argument(
        "--label-dir",
        required=True,
        help="Output directory for YOLO .txt label files",
    )
    p_cvat.add_argument(
        "--strict",
        action="store_true",
        help="Fail on missing images instead of skipping them",
    )

    # assemble
    p_asm = subparsers.add_parser(
        "assemble", help="Step 4: Assemble final YOLO dataset from annotated data"
    )
    p_asm.add_argument(
        "--annotated",
        default=None,
        help="Directory with images/ and labels/ (from CVAT import)",
    )
    p_asm.add_argument(
        "--output", "-o", required=True, help="Output dataset directory"
    )
    p_asm.add_argument(
        "--bootstrap",
        action="append",
        dest="bootstrap_dirs",
        default=None,
        help="Bootstrap dataset directory (can specify multiple)",
    )
    p_asm.add_argument(
        "--test-pct", type=float, default=0.15, help="Validation split fraction"
    )
    p_asm.add_argument("--seed", type=int, default=42, help="Random seed")

    # validate
    p_val = subparsers.add_parser(
        "validate",
        help="Validate a YOLO-format dataset directory",
    )
    p_val.add_argument("--dataset", "-d", required=True, help="Dataset directory")

    # full-pipeline
    p_full = subparsers.add_parser(
        "full-pipeline",
        help="Run prepare → (manual annotate) → import-cvat → assemble in one workflow",
    )
    p_full.add_argument(
        "--cvat-xml", required=True, help="CVAT XML 1.1 annotation file"
    )
    p_full.add_argument(
        "--extracted-frames",
        required=True,
        help="Directory of extracted frames (from extract_frames.py)",
    )
    p_full.add_argument(
        "--output", "-o", required=True, help="Final output dataset directory"
    )
    p_full.add_argument(
        "--workspace",
        default=None,
        help="Temporary annotation workspace (default: <output>/_annotation_workspace)",
    )
    p_full.add_argument(
        "--bootstrap",
        action="append",
        dest="bootstrap_dirs",
        default=None,
        help="Bootstrap dataset (can specify multiple)",
    )
    p_full.add_argument(
        "--test-pct", type=float, default=0.15, help="Validation split fraction"
    )
    p_full.add_argument("--seed", type=int, default=42, help="Random seed")
    p_full.add_argument(
        "--max-images",
        type=int,
        default=None,
        help="Max images for annotation batch",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    if args.command == "prepare":
        prepare_workspace(
            input_dir=args.input,
            output_dir=args.output,
            max_images=args.max_images,
            symmetric_sample=args.symmetric_sample,
            seed=args.seed,
        )

    elif args.command == "import-cvat":
        import_cvat_xml(
            cvat_xml=args.cvat_xml,
            image_dir=args.image_dir,
            label_dir=args.label_dir,
            skip_unmatched=not args.strict,
        )

    elif args.command == "assemble":
        assemble_dataset(
            annotated_dir=args.annotated,
            output_dir=args.output,
            bootstrap_dirs=args.bootstrap_dirs,
            test_pct=args.test_pct,
            seed=args.seed,
        )

    elif args.command == "validate":
        validate_dataset(args.dataset)

    elif args.command == "full-pipeline":
        workspace = args.workspace or os.path.join(args.output, "_annotation_workspace")

        logger.info("=== Step 1: Prepare annotation workspace ===")
        prepare_workspace(
            input_dir=args.extracted_frames,
            output_dir=workspace,
            max_images=args.max_images,
            seed=args.seed,
        )

        logger.info("")
        logger.info("=== Step 2: MANUAL — Annotate in CVAT ===")
        logger.info(
            "  Import images from: %s/images/", workspace
        )
        logger.info(
            "  After annotation, export CVAT XML 1.1 and pass to step 3."
        )
        logger.info("")
        logger.info("=== Step 3: Import CVAT XML ===")
        import_cvat_xml(
            cvat_xml=args.cvat_xml,
            image_dir=os.path.join(workspace, "images"),
            label_dir=os.path.join(workspace, "labels"),
        )

        logger.info("")
        logger.info("=== Step 4: Assemble final dataset ===")
        assemble_dataset(
            annotated_dir=workspace,
            output_dir=args.output,
            bootstrap_dirs=args.bootstrap_dirs,
            test_pct=args.test_pct,
            seed=args.seed,
        )

        logger.info("")
        logger.info("=== Pipeline complete ===")
        logger.info("Final dataset: %s", args.output)


if __name__ == "__main__":
    main()