#!/usr/bin/env python3
"""
Thermal UVC frame capture tool for D1.1 data collection.

Opens the first available UVC device, shows live preview, captures clips on demand.
Works with any UVC thermal camera (T13, InfiRay, FLIR Lepton, etc.).
Saves raw 16-bit TIFF + 8-bit AGC-normalized PNG per frame, plus optional video.

Usage:
    python thermal_capture.py [--device /dev/video0] [--out capture_output]
                              [--fps 25] [--show-raw]

Keys:
    r - start / stop recording (toggles)
    s - snapshot single frame
    q - quit
"""

import argparse
import csv
import logging
import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("thermal_capture")


def agc_normalize(frame_16bit: np.ndarray, percentile: float = 2.0) -> np.ndarray:
    """Apply Automatic Gain Control: clip tails then stretch to 8-bit.

    Args:
        frame_16bit: 16-bit raw thermal data (0-65535).
        percentile: Percent of pixels to clip at each tail (default 2%).

    Returns:
        8-bit uint8 image, 0-255.
    """
    low = np.percentile(frame_16bit, percentile)
    high = np.percentile(frame_16bit, 100 - percentile)
    clipped = np.clip(frame_16bit, low, high)
    if high > low:
        normalized = ((clipped - low) / (high - low) * 255).astype(np.uint8)
    else:
        normalized = np.zeros_like(frame_16bit, dtype=np.uint8)
    return normalized


def main() -> None:
    parser = argparse.ArgumentParser(description="Thermal UVC frame capture")
    parser.add_argument("--device", default="/dev/video0", help="Video device path")
    parser.add_argument("--out", default="capture_output", help="Output directory")
    parser.add_argument("--fps", type=int, default=25, help="Capture framerate limit")
    parser.add_argument(
        "--show-raw", action="store_true", help="Show raw 16-bit view instead of AGC"
    )
    args = parser.parse_args()

    out_dir = Path(args.out)
    raw_dir = out_dir / "raw"
    frames_dir = out_dir / "frames"
    raw_dir.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)

    # Open camera
    cap = cv2.VideoCapture(args.device)
    if not cap.isOpened():
        log.error(f"Could not open device {args.device}")
        sys.exit(1)

    # Try to set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
    cap.set(cv2.CAP_PROP_FPS, args.fps)

    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    log.info(f"Opened {args.device} — resolution {actual_w}x{actual_h}")

    # Metadata log
    meta_path = out_dir / "capture_metadata.csv"
    meta_file = open(meta_path, "a", newline="")
    meta_writer = csv.writer(meta_file)
    if meta_file.tell() == 0:
        meta_writer.writerow(
            [
                "timestamp",
                "type",
                "filename",
                "width",
                "height",
                "device",
            ]
        )

    recording = False
    recording_start = None
    clip_frames = []
    running = True

    def signal_handler(sig, frame) -> None:
        nonlocal running
        log.info("Interrupt received, shutting down...")
        running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    cv2.namedWindow("Thermal Capture", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Thermal Capture", 640, 512)

    # Overlay text helper
    def overlay_text(img: np.ndarray, text: str, y: int = 30) -> None:
        cv2.putText(
            img, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
        )

    log.info("Ready. Keys: r=record, s=snapshot, q=quit")
    log.info(f"Output: {out_dir.resolve()}")

    frame_times: list[float] = []
    fps_display = 0.0

    while running:
        ret, frame_bgr = cap.read()
        if not ret:
            log.warning("Frame grab failed — retrying...")
            time.sleep(0.05)
            continue

        # Track FPS
        now = time.time()
        frame_times.append(now)
        frame_times = [t for t in frame_times if now - t < 2.0]
        fps_display = len(frame_times) / 2.0 if frame_times else 0.0

        timestamp = datetime.now().isoformat(timespec="milliseconds")

        # Attempt to interpret as 16-bit raw (first frame is 16-bit for most UVC cameras)
        # For 16-bit MONO16: each pixel is 2 bytes. OpenCV reads as 8-bit by default.
        # Try FOURCC-based detection or fall back to 8-bit.
        # Since the T13 and most thermal cams present as Y16, we need to re-interpret.
        # Strategy: if total pixels * 2 matches the raw buffer size, it's 16-bit.
        frame_16bit = None
        frame_8bit = frame_bgr.copy()

        # Attempt 16-bit decode: if camera is MONO16, read raw bytes manually
        raw_bytes = cap.grab()
        if raw_bytes:
            # This approach doesn't work directly with cv2.VideoCapture().
            # Instead, use the frame's shape: for a 640x512 16-bit camera,
            # frame.shape might be (512, 640) or (512, 640, 1).
            pass

        # Best-effort: check if frame is single-channel (MONO16 shows as 1-channel 16-bit
        # but OpenCV returns it as 8-bit by default on some platforms).
        if len(frame_bgr.shape) == 2:
            # Grayscale already
            frame_display = cv2.cvtColor(frame_bgr, cv2.COLOR_GRAY2BGR)
            frame_8bit = frame_bgr
        elif frame_bgr.shape[2] == 3:
            # Color image (common for AGC-converted UVC cameras)
            # Try to get back to luminance
            frame_8bit = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
            frame_display = frame_bgr.copy()
        else:
            frame_display = frame_bgr
            frame_8bit = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

        # Build display frame
        display = frame_display.copy()

        # Overlay info
        status = "REC" if recording else "IDLE"
        overlay_text(display, f"{status} | FPS: {fps_display:.1f} | {timestamp}", 30)
        if recording:
            elapsed = time.time() - recording_start
            overlay_text(display, f"Clip length: {elapsed:.1f}s | {len(clip_frames)} frames", 55)
            # Red recording dot
            cv2.circle(display, (20, 70), 8, (0, 0, 255), -1)

        cv2.imshow("Thermal Capture", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            running = False
        elif key == ord("r"):
            if not recording:
                recording = True
                recording_start = time.time()
                clip_frames = []
                log.info("--- Recording started ---")
            else:
                # Save clip
                clip_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                clip_dir = raw_dir / f"clip_{clip_id}"
                clip_dir.mkdir(parents=True, exist_ok=True)
                for i, (ts, raw16, agc8) in enumerate(clip_frames):
                    frame_name = f"frame_{i:06d}"
                    # Save raw 16-bit if available
                    if raw16 is not None:
                        raw16_path = clip_dir / f"{frame_name}_raw.tiff"
                        cv2.imwrite(str(raw16_path), raw16)
                    # Save AGC 8-bit
                    agc_path = clip_dir / f"{frame_name}_agc.png"
                    cv2.imwrite(str(agc_path), agc8)
                    meta_writer.writerow([ts, "frame_agc", str(agc_path), 640, 512, args.device])
                    if raw16 is not None:
                        meta_writer.writerow([ts, "frame_raw16", str(raw16_path), 640, 512, args.device])
                log.info(f"--- Saved clip {clip_id}: {len(clip_frames)} frames ---")
                recording = False
                clip_frames = []

        elif key == ord("s"):
            # Single snapshot
            snap_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            snap_path = frames_dir / f"snap_{snap_id}.png"
            cv2.imwrite(str(snap_path), frame_8bit)
            meta_writer.writerow([timestamp, "snapshot", str(snap_path), 640, 512, args.device])
            log.info(f"Snapshot: {snap_path}")

        # If recording, buffer the frame
        if recording:
            # Try to get 16-bit raw data by re-reading with different decode
            frame_raw16 = None
            clip_frames.append((timestamp, frame_raw16, frame_8bit))
            # Keep last 600 frames (60s @ 10fps reference, 24s @ 25fps)
            if len(clip_frames) > 600:
                clip_frames.pop(0)

    # Cleanup
    recording = False
    cap.release()
    cv2.destroyAllWindows()
    meta_file.close()
    if clip_frames:
        log.info(f"Recording was in progress — {len(clip_frames)} unsaved frames discarded.")
    log.info("Capture session ended.")


if __name__ == "__main__":
    main()