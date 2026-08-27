#!/usr/bin/env python3
"""Tests for the D1.3 augmentation pipeline."""

import os
import sys
import tempfile
import unittest

import numpy as np

# Add the repo root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from analysis.thermal_sim.augmentation_pipeline import (
    _adjust_gamma,
    _flip_bboxes_horizontal,
    _scale_labels_to_target,
    apply_mosaic,
    draw_bboxes,
    get_train_augmentations,
    get_val_augmentations,
    yolo_to_xyxy,
    CLASS_NAMES,
    NUM_CLASSES,
)


class TestConstants(unittest.TestCase):
    def test_class_names(self):
        self.assertEqual(len(CLASS_NAMES), 5)
        self.assertIn("deer", CLASS_NAMES)
        self.assertIn("human", CLASS_NAMES)

    def test_num_classes(self):
        self.assertEqual(NUM_CLASSES, 5)


class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.img = np.random.randint(0, 256, (480, 640), dtype=np.uint8)
        self.bboxes = [[0.5, 0.5, 0.3, 0.2]]  # cx, cy, w, h

    def test_adjust_gamma(self):
        result = _adjust_gamma(self.img, 1.0)
        self.assertEqual(result.shape, self.img.shape)
        np.testing.assert_array_equal(result, self.img)

        result_high = _adjust_gamma(self.img, 2.0)
        self.assertEqual(result_high.shape, self.img.shape)

    def test_flip_bboxes_horizontal(self):
        flipped = _flip_bboxes_horizontal(self.bboxes, 640)
        self.assertEqual(len(flipped), 1)
        self.assertAlmostEqual(flipped[0][0], 0.5)  # cx stays at 0.5
        self.assertEqual(flipped[0][1], 0.5)  # cy unchanged
        self.assertEqual(flipped[0][2], 0.3)  # w unchanged
        self.assertEqual(flipped[0][3], 0.2)  # h unchanged

        # off-centre
        bbox_off = [[0.3, 0.5, 0.2, 0.2]]
        flipped_off = _flip_bboxes_horizontal(bbox_off, 640)
        self.assertAlmostEqual(flipped_off[0][0], 0.7)  # 1.0 - 0.3

    def test_scale_labels_to_target(self):
        labels = [[0, 0.5, 0.5, 0.3, 0.2]]
        scaled = _scale_labels_to_target(labels, (640, 480), (320, 240))
        self.assertAlmostEqual(scaled[0][1], 0.25)  # 0.5 * (320/640) = 0.25
        self.assertAlmostEqual(scaled[0][2], 0.25)  # 0.5 * (240/480) = 0.25
        self.assertAlmostEqual(scaled[0][3], 0.15)  # 0.3 * (320/640) = 0.15
        self.assertAlmostEqual(scaled[0][4], 0.10)  # 0.2 * (240/480) = 0.10

    def test_yolo_to_xyxy(self):
        # 640x480 image, bbox at centre 0.5,0.5 with 0.2,0.2
        # cx=320, cy=240, w=128, h=96
        # x1=320-64=256, y1=240-48=192, x2=384, y2=288
        xyxy = yolo_to_xyxy([[0.5, 0.5, 0.2, 0.2]], 640, 480)
        self.assertEqual(xyxy[0], (256, 192, 384, 288))

    def test_draw_bboxes(self):
        vis = draw_bboxes(self.img, self.bboxes, [0], color=(0, 255, 0))
        self.assertEqual(vis.shape, (480, 640, 3))  # greyscale → BGR

    def test_scale_labels_to_target_same(self):
        """Scaling to the same size should be identity."""
        labels = [[2, 0.5, 0.5, 0.3, 0.2]]
        scaled = _scale_labels_to_target(labels, (640, 480), (640, 480))
        for a, b in zip(labels[0], scaled[0]):
            self.assertAlmostEqual(a, b)


class TestPipelines(unittest.TestCase):
    def setUp(self):
        self.img = np.random.randint(0, 256, (480, 640), dtype=np.uint8)
        self.bboxes = [[0.5, 0.5, 0.3, 0.2]]
        self.class_labels = [0]

    def test_train_pipeline_uses_opencv_fallback(self):
        """Should work without albumentations."""
        aug = get_train_augmentations(target_size=(640, 640))
        self.assertEqual(type(aug).__name__, "_OpenCVPipeline")

    def test_train_pipeline_no_boxes(self):
        aug = get_train_augmentations(target_size=(640, 640))
        result = aug(image=self.img)
        self.assertIn("image", result)
        # Without bboxes, result should not have bbox fields
        self.assertNotIn("bboxes", result)

    def test_train_pipeline_with_boxes(self):
        aug = get_train_augmentations(target_size=(640, 640))
        result = aug(
            image=self.img,
            bboxes=self.bboxes,
            class_labels=self.class_labels,
        )
        self.assertIn("image", result)
        self.assertIn("bboxes", result)
        self.assertIn("class_labels", result)
        self.assertEqual(result["image"].shape, (640, 640))
        self.assertEqual(len(result["bboxes"]), len(self.bboxes))

    def test_train_pipeline_altitude_bands(self):
        for band in ["low", "nominal", "high"]:
            aug = get_train_augmentations(target_size=(640, 640), altitude_band=band)
            result = aug(image=self.img, bboxes=self.bboxes, class_labels=self.class_labels)
            self.assertIn("image", result)
            self.assertEqual(result["image"].shape, (640, 640))

    def test_val_pipeline_deterministic(self):
        aug = get_val_augmentations(target_size=(640, 640))
        r1 = aug(image=self.img, bboxes=self.bboxes, class_labels=self.class_labels)
        r2 = aug(image=self.img, bboxes=self.bboxes, class_labels=self.class_labels)
        # Val pipeline has no stochastic transforms, so results should be identical
        np.testing.assert_array_equal(r1["image"], r2["image"])
        np.testing.assert_array_equal(r1["bboxes"], r2["bboxes"])

    def test_val_pipeline_image_shape(self):
        aug = get_val_augmentations(target_size=(320, 320))
        result = aug(image=self.img, bboxes=self.bboxes, class_labels=self.class_labels)
        self.assertEqual(result["image"].shape, (320, 320))


class TestMosaic(unittest.TestCase):
    def setUp(self):
        self.img = np.random.randint(0, 256, (480, 640), dtype=np.uint8)
        self.labels = [[0, 0.5, 0.5, 0.3, 0.2]]

    def test_mosaic_with_4_images(self):
        imgs = [self.img for _ in range(4)]
        labels = [self.labels for _ in range(4)]
        result_img, result_bboxes, result_classes = apply_mosaic(
            imgs, labels, target_size=(640, 640), p=1.0
        )
        self.assertEqual(result_img.shape, (640, 640))
        self.assertGreater(len(result_bboxes), 0)
        self.assertEqual(len(result_bboxes), len(result_classes))

    def test_mosaic_fallback_with_fewer_images(self):
        """Mosaic with 2 images should fall back to the first image."""
        imgs = [self.img for _ in range(2)]
        labels = [self.labels for _ in range(2)]
        result_img, result_bboxes, result_classes = apply_mosaic(
            imgs, labels, target_size=(640, 640), p=1.0
        )
        self.assertEqual(result_img.shape, (640, 640))
        self.assertGreater(len(result_bboxes), 0)

    def test_mosaic_p_zero(self):
        """p=0 should always fall back to first image."""
        imgs = [self.img for _ in range(4)]
        labels = [self.labels for _ in range(4)]
        # Run multiple times to ensure consistency
        for _ in range(5):
            result_img, result_bboxes, result_classes = apply_mosaic(
                imgs, labels, target_size=(640, 640), p=0.0
            )
            self.assertEqual(result_img.shape, (640, 640))

    def test_mosaic_with_no_labels(self):
        imgs = [self.img for _ in range(4)]
        labels = [[] for _ in range(4)]  # no labels
        result_img, result_bboxes, result_classes = apply_mosaic(
            imgs, labels, target_size=(640, 640), p=1.0
        )
        self.assertEqual(result_img.shape, (640, 640))
        self.assertEqual(len(result_bboxes), 0)

    def test_mosaic_with_rgb_input(self):
        h, w = self.img.shape
        rgb_img = np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)
        imgs = [rgb_img for _ in range(4)]
        labels = [self.labels for _ in range(4)]
        result_img, result_bboxes, result_classes = apply_mosaic(
            imgs, labels, target_size=(640, 640), p=1.0
        )
        self.assertEqual(result_img.shape, (640, 640))  # output is grayscale


class TestCLI(unittest.TestCase):
    def test_parse_yolo_label(self):
        from analysis.thermal_sim.augmentation_pipeline import _parse_yolo_label, _save_yolo_label

        with tempfile.TemporaryDirectory() as tmpdir:
            label_path = os.path.join(tmpdir, "test.txt")
            _save_yolo_label(label_path, [[0.5, 0.5, 0.3, 0.2]], [0])
            bboxes, class_ids = _parse_yolo_label(label_path)
            self.assertEqual(len(bboxes), 1)
            self.assertEqual(class_ids, [0])
            self.assertAlmostEqual(bboxes[0][0], 0.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)