#!/usr/bin/env python3
"""
Frame extraction tool for D1.1 field capture.

Takes raw video clips (.mp4, .mkv, .avi) and extracts individual frames at a
configurable rate. Filters blurry frames, normalizes thermal data, and outputs
8-bit PNG files in a structured directory tree.

Usage:
    python extract_frames.py --input raw_clips/ --output extracted_frames/
        [--rate 1.0] [--blur-threshold 50] [--normalize agc]
"""

import argparse
import csv
import logging
import os
import sys
from pathlib import Path

import cv2
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("extract_frames")


def laplacian_variance(image: np.ndarray) -> float:
    """Compute the variance of the Laplacian as a blur metric.

    Lower variance = blurrier image. Threshold ~50-100 works well for
    thermal imagery (which has less texture than visible-light photos).
    """
    return cv2.Laplacian(image, cv2.CV_64F).var()


def agc_normalize(
    frame: np.ndarray, percentile: float = 2.0
) -> np.ndarray:
    """AGC normalization: clip tails, stretch to 8-bit."""
    low = np.percentile(frame, percentile)
    high = np.percentile(frame, 100 - percentile)
    clipped = np.clip(frame, low, high)
    if high > low:
        return ((clipped - low) / (high - low) * 255).astype(np.uint8)
    return np.zeros_like(frame, dtype=np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract frames from thermal video")
    parser.add_argument(
        "--input", "-i", required=True, help="Input directory containing .mp4/.mkv/.avi clips"
    )
    parser.add_argument(
        "--output", "-o", required=True, help="Output directory for extracted frames"
    )
    parser.add_argument(
        "--rate",
        "-r",
        type=float,
        default=1.0,
        help="Frame extraction rate in fps (default: 1.0)",
    )
    parser.add_argument(
        "--blur-threshold",
        type=float,
        default=50.0,
        help="Minimum Laplacian variance to keep a frame (default: 50)",
    )
    parser.add_argument(
        "--normalize",
        choices=["none", "agc"],
        default="agc",
        help="Normalization method (default: agc)",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=0,
        help="Maximum frames per clip (0 = unlimited)",
    )
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    if not input_dir.is_dir():
        log.error(f"Input directory not found: {input_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Find video files
    extensions = (".mp4", ".mkv", ".avi", ".mov", ".m4v")
    clips = sorted([f for f in input_dir.iterdir() if f.suffix.lower() in extensions])
    if not clips:
        log.warning(f"No video files found in {input_dir}")
        sys.exit(0)

    log.info(f"Found {len(clips)} clips")

    # Metadata CSV
    meta_path = output_dir / "extraction_log.csv"
    meta_file = open(meta_path, "w", newline="")
    meta_writer = csv.writer(meta_file)
    meta_writer.writerow(
        [
            "source_clip",
            "frame_number",
            "output_file",
            "blur_score",
            "width",
            "height",
        ]
    )

    total_frames = 0
    kept_frames = 0
    skipped_blur = 0
    skipped_rate = 0

    for clip_path in clips:
        clip_name = clip_path.stem
        log.info(f"Processing: {clip_path.name}")

        cap = cv2.VideoCapture(str(clip_path))
        if not cap.isOpened():
            log.warning(f"  Could not open, skipping")
            continue

        clip_fps = cap.get(cv2.CAP_PROP_FPS)
        if clip_fps <= 0:
            clip_fps = 25.0  # fallback

        # Extraction interval in frames
        extract_interval = max(1, int(round(clip_fps / args.rate)))

        clip_out_dir = output_dir / clip_name
        clip_out_dir.mkdir(parents=True, exist_ok=True)

        frame_num = 0
        clip_kept = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_num += 1

            # Rate-limiting: only process every Nth frame
            if frame_num % extract_interval != 0:
                skipped_rate += 1
                continue

            # Ensure grayscale
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray = frame

            # Blur check
            blur_score = laplacian_variance(gray)
            if blur_score < args.blur_threshold:
                skipped_blur += 1
                continue

            # Normalize
            if args.normalize == "agc":
                normalized = agc_normalize(gray)
            else:
                normalized = gray

            # Save
            out_path = clip_out_dir / f"frame_{frame_num:06d}.png"
            cv2.imwrite(str(out_path), normalized)

            meta_writer.writerow(
                [
                    clip_path.name,
                    frame_num,
                    str(out_path.resolve()),
                    f"{blur_score:.1f}",
                    gray.shape[1],
                    gray.shape[0],
                ]
            )

            kept_frames += 1
            clip_kept += 1
            total_frames += 1

            if args.max_frames and clip_kept >= args.max_frames:
                break

        cap.release()
        log.info(
            f"  Extracted {clip_kept} frames from {frame_num} total"
        )

    meta_file.close()
    log.info("-" * 50)
    log.info(f"Total frames in clips: ~{total_frames + skipped_rate}")
    log.info(f"  Kept:  {kept_frames}")
    log.info(f"  Blur:  {skipped_blur} (below threshold)")
    log.info(f"  Rate:  {skipped_rate} (skipped by rate-limiting)")
    log.info(f"Output: {output_dir.resolve()}")
    log.info(f"Log:    {meta_path.resolve()}")


if __name__ == "__main__":
    main()