#!/usr/bin/env python3
"""Tests for the D1.3 labeling pipeline."""

import csv
import os
import sys
import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

# Add the repo root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from analysis.thermal_sim.labeling_pipeline import (
    _cvat_box_to_yolo,
    _resolve_label,
    _parse_cvat_annotation,
    assemble_dataset,
    import_cvat_xml,
    prepare_workspace,
    validate_dataset,
    CLASS_MAP,
    CLASS_NAMES,
    NUM_CLASSES,
    CVAT_LABEL_MAP,
)

# Create a simple XML builder for CVAT 1.1 format
def _make_cvat_xml(image_annotations):
    """Build CVAT 1.1 XML string from image_annotations dict.

    image_annotations: {filename: [(label, xtl, ytl, xbr, ybr), ...]}
    """
    lines = ['<?xml version="1.0" encoding="utf-8"?>', "<annotations>"]
    lines.append('  <version>1.1</version>')
    lines.append('  <meta><task><labels>')
    for label in ["deer", "turkey", "other_animal", "human"]:
        lines.append(f'    <label><name>{label}</name></label>')
    lines.append('  </labels></task></meta>')

    for fname, boxes in image_annotations.items():
        w, h = 640, 512  # assume fixed for test
        lines.append(f'  <image id="0" name="{fname}" width="{w}" height="{h}">')
        for label, xtl, ytl, xbr, ybr in boxes:
            lines.append(
                f'    <box label="{label}" xtl="{xtl}" ytl="{ytl}" '
                f'xbr="{xbr}" ybr="{ybr}" occluded="0">'
            )
            lines.append('      <attribute name="type">thermal</attribute>')
            lines.append('    </box>')
        lines.append('  </image>')

    lines.append("</annotations>")
    return "\n".join(lines)


class TestConstants(unittest.TestCase):
    def test_class_count(self):
        self.assertEqual(NUM_CLASSES, 4)
        self.assertEqual(len(CLASS_NAMES), 4)

    def test_class_names(self):
        self.assertEqual(CLASS_NAMES, ["deer", "turkey", "other_animal", "human"])

    def test_class_map(self):
        self.assertEqual(CLASS_MAP["deer"], 0)
        self.assertEqual(CLASS_MAP["human"], 3)
        self.assertEqual(CLASS_MAP["other_animal"], 2)

    def test_cvat_label_map_len(self):
        self.assertIn("person", CVAT_LABEL_MAP)
        self.assertEqual(CVAT_LABEL_MAP["person"], 3)


class TestHelpers(unittest.TestCase):
    def test_resolve_label_exact(self):
        self.assertEqual(_resolve_label("human"), 3)
        self.assertEqual(_resolve_label("deer"), 0)

    def test_resolve_label_case_insensitive(self):
        self.assertEqual(_resolve_label("Human"), 3)
        self.assertEqual(_resolve_label("OTHER_ANIMAL"), 2)

    def test_resolve_label_fuzzy(self):
        self.assertEqual(_resolve_label("person"), 3)
        self.assertEqual(_resolve_label("animal"), 2)

    def test_resolve_label_unknown(self):
        self.assertIsNone(_resolve_label("bicycle"))
        self.assertIsNone(_resolve_label("car"))

    def test_cvat_box_to_yolo_center(self):
        """Box centered in a 640x512 image."""
        result = _cvat_box_to_yolo(160, 128, 480, 384, 640, 512)
        self.assertIsNotNone(result)
        cx, cy, w, h = result
        self.assertAlmostEqual(cx, 0.5, places=4)
        self.assertAlmostEqual(cy, 0.5, places=4)
        self.assertAlmostEqual(w, 0.5, places=4)  # 320/640
        self.assertAlmostEqual(h, 0.5, places=4)  # 256/512

    def test_cvat_box_to_yolo_swapped_coords(self):
        """xbr < xtl should still work."""
        result = _cvat_box_to_yolo(480, 384, 160, 128, 640, 512)
        self.assertIsNotNone(result)
        cx, cy, w, h = result
        self.assertAlmostEqual(cx, 0.5, places=4)
        self.assertAlmostEqual(cy, 0.5, places=4)

    def test_cvat_box_to_yolo_edge(self):
        """Box at top-left edge."""
        result = _cvat_box_to_yolo(0, 0, 100, 100, 640, 512)
        self.assertIsNotNone(result)
        cx, cy, w, h = result
        self.assertAlmostEqual(cx, 0.078125, places=4)  # 50/640
        self.assertAlmostEqual(cy, 0.09765625, places=4)  # 50/512

    def test_cvat_box_to_yolo_degenerate(self):
        """Box with 0 width should be skipped."""
        result = _cvat_box_to_yolo(100, 100, 100, 200, 640, 512)
        self.assertIsNone(result)

    def test_cvat_box_to_yolo_clamped(self):
        """Box extending beyond image should be clamped."""
        result = _cvat_box_to_yolo(-50, -50, 100, 100, 640, 512)
        self.assertIsNotNone(result)
        cx, cy, w, h = result
        self.assertGreaterEqual(cx, 0.0)
        self.assertGreaterEqual(cy, 0.0)
        self.assertLessEqual(cx, 1.0)
        self.assertLessEqual(cy, 1.0)


class TestCvatXmlParsing(unittest.TestCase):
    def test_parse_simple(self):
        xml_str = _make_cvat_xml({
            "frame_001.png": [("human", 100, 100, 300, 400)],
            "frame_002.png": [("deer", 200, 150, 400, 350)],
        })

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = os.path.join(tmpdir, "annotations.xml")
            with open(xml_path, "w") as f:
                f.write(xml_str)

            image_dims, annotations = _parse_cvat_annotation(xml_path)

        self.assertEqual(len(annotations), 2)
        self.assertIn("frame_001.png", annotations)
        self.assertIn("frame_002.png", annotations)

    def test_parse_unknown_label(self):
        """Should still parse, label resolution happens at conversion time."""
        xml_str = _make_cvat_xml({
            "frame_001.png": [("bicycle", 100, 100, 200, 200)],
        })

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = os.path.join(tmpdir, "annotations.xml")
            with open(xml_path, "w") as f:
                f.write(xml_str)

            image_dims, annotations = _parse_cvat_annotation(xml_path)

        self.assertEqual(len(annotations), 1)
        self.assertEqual(annotations["frame_001.png"][0]["label"], "bicycle")

    def test_parse_empty_annotations(self):
        xml_str = '<?xml version="1.0"?><annotations><version>1.1</version></annotations>'

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = os.path.join(tmpdir, "annotations.xml")
            with open(xml_path, "w") as f:
                f.write(xml_str)

            image_dims, annotations = _parse_cvat_annotation(xml_path)

        self.assertEqual(len(annotations), 0)
        self.assertEqual(len(image_dims), 0)


class TestPrepareWorkspace(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    def _make_test_frames(self, n: int = 5):
        """Create n test image files in a directory."""
        src = os.path.join(self.tmpdir.name, "extracted")
        os.makedirs(src, exist_ok=True)
        for i in range(n):
            img = np.random.randint(0, 256, (512, 640), dtype=np.uint8)
            path = os.path.join(src, f"frame_{i:06d}.png")
            import cv2
            cv2.imwrite(path, img)
        return src

    def test_prepare_basic(self):
        src = self._make_test_frames(5)
        dst = os.path.join(self.tmpdir.name, "workspace")

        prepare_workspace(src, dst)

        dst_images = os.path.join(dst, "images")
        self.assertTrue(os.path.isdir(dst_images))
        files = [f for f in os.listdir(dst_images) if f.endswith(".png")]
        self.assertEqual(len(files), 5)

    def test_prepare_with_max_images(self):
        src = self._make_test_frames(20)
        dst = os.path.join(self.tmpdir.name, "workspace_max")

        prepare_workspace(src, dst, max_images=5)

        dst_images = os.path.join(dst, "images")
        files = [f for f in os.listdir(dst_images) if f.endswith(".png")]
        self.assertEqual(len(files), 5)

    def test_prepare_empty(self):
        src = os.path.join(self.tmpdir.name, "empty")
        os.makedirs(src, exist_ok=True)
        dst = os.path.join(self.tmpdir.name, "workspace_empty")

        prepare_workspace(src, dst)

        dst_images = os.path.join(dst, "images")
        self.assertTrue(os.path.isdir(dst_images))
        files = os.listdir(dst_images)
        self.assertEqual(len(files), 0)

    def test_prepare_nonexistent(self):
        dst = os.path.join(self.tmpdir.name, "workspace_nonexistent")
        with self.assertRaises(NotADirectoryError):
            prepare_workspace("/nonexistent/path", dst)


class TestImportCvatXml(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_import_basic(self):
        # Create test images
        img_dir = os.path.join(self.tmpdir.name, "images")
        os.makedirs(img_dir, exist_ok=True)

        img_paths = {}
        for fname in ["frame_001.png", "frame_002.png"]:
            img = np.random.randint(0, 256, (512, 640), dtype=np.uint8)
            path = os.path.join(img_dir, fname)
            import cv2
            cv2.imwrite(path, img)
            img_paths[fname] = path

        # Create CVAT XML
        xml_str = _make_cvat_xml({
            "frame_001.png": [("human", 100, 100, 300, 400)],
            "frame_002.png": [("deer", 200, 150, 400, 350)],
        })
        xml_path = os.path.join(self.tmpdir.name, "annotations.xml")
        with open(xml_path, "w") as f:
            f.write(xml_str)

        # Import
        label_dir = os.path.join(self.tmpdir.name, "labels")
        import_cvat_xml(xml_path, img_dir, label_dir)

        # Check labels
        self.assertTrue(os.path.isdir(label_dir))
        labels = [f for f in os.listdir(label_dir) if f.endswith(".txt")]
        self.assertEqual(len(labels), 2)

        # Read label content
        label_path = os.path.join(label_dir, "frame_001.txt")
        with open(label_path) as f:
            line = f.readline().strip()
        parts = line.split()
        self.assertEqual(len(parts), 5)
        self.assertEqual(int(parts[0]), 3)  # human

    def test_import_unknown_label_skipped(self):
        img_dir = os.path.join(self.tmpdir.name, "images2")
        os.makedirs(img_dir, exist_ok=True)

        img = np.random.randint(0, 256, (512, 640), dtype=np.uint8)
        path = os.path.join(img_dir, "frame_001.png")
        import cv2
        cv2.imwrite(path, img)

        xml_str = _make_cvat_xml({
            "frame_001.png": [("bicycle", 100, 100, 200, 200)],
        })
        xml_path = os.path.join(self.tmpdir.name, "annotations2.xml")
        with open(xml_path, "w") as f:
            f.write(xml_str)

        label_dir = os.path.join(self.tmpdir.name, "labels2")
        import_cvat_xml(xml_path, img_dir, label_dir)

        # Label file should not exist (all boxes had unknown labels)
        label_path = os.path.join(label_dir, "frame_001.txt")
        self.assertFalse(os.path.exists(label_path))


class TestAssembleDataset(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        # Create annotated workspace
        self.annotated = os.path.join(self.tmpdir.name, "annotated")
        os.makedirs(os.path.join(self.annotated, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.annotated, "labels"), exist_ok=True)

        for i in range(10):
            img = np.random.randint(0, 256, (512, 640), dtype=np.uint8)
            img_path = os.path.join(self.annotated, "images", f"img_{i:04d}.png")
            import cv2
            cv2.imwrite(img_path, img)

            # Write YOLO label
            label_path = os.path.join(self.annotated, "labels", f"img_{i:04d}.txt")
            with open(label_path, "w") as f:
                f.write(f"0 0.5 0.5 0.3 0.2\n")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_assemble_basic(self):
        output = os.path.join(self.tmpdir.name, "dataset1")
        assemble_dataset(
            annotated_dir=self.annotated,
            output_dir=output,
            test_pct=0.2,
            seed=42,
        )

        # Check structure
        self.assertTrue(os.path.isdir(os.path.join(output, "images", "train")))
        self.assertTrue(os.path.isdir(os.path.join(output, "images", "val")))
        self.assertTrue(os.path.isdir(os.path.join(output, "labels", "train")))
        self.assertTrue(os.path.isdir(os.path.join(output, "labels", "val")))
        self.assertTrue(os.path.isfile(os.path.join(output, "dataset.yaml")))

        # Check split (10 images, 0.2 -> 2 val, 8 train)
        train_imgs = len(os.listdir(os.path.join(output, "images", "train")))
        val_imgs = len(os.listdir(os.path.join(output, "images", "val")))
        self.assertEqual(train_imgs + val_imgs, 10)
        self.assertGreaterEqual(val_imgs, 1)

    def test_assemble_dataset_yaml(self):
        output = os.path.join(self.tmpdir.name, "dataset2")
        assemble_dataset(
            annotated_dir=self.annotated,
            output_dir=output,
            seed=0,
        )

        yaml_path = os.path.join(output, "dataset.yaml")
        with open(yaml_path) as f:
            content = f.read()

        self.assertIn("nc: 4", content)
        self.assertIn("deer", content)
        self.assertIn("human", content)

    def test_assemble_assembly_report(self):
        output = os.path.join(self.tmpdir.name, "dataset3")
        assemble_dataset(
            annotated_dir=self.annotated,
            output_dir=output,
            seed=0,
        )

        report_path = os.path.join(output, "assembly_report.txt")
        self.assertTrue(os.path.isfile(report_path))
        with open(report_path) as f:
            content = f.read()
        self.assertIn("Dataset Assembly Report", content)
        self.assertIn("deer", content)

    def test_assemble_no_annotated(self):
        """Should still produce dataset.yaml with empty directories."""
        output = os.path.join(self.tmpdir.name, "dataset4")
        assemble_dataset(
            annotated_dir=None,
            output_dir=output,
            seed=0,
        )

        self.assertTrue(os.path.isfile(os.path.join(output, "dataset.yaml")))


class TestValidateDataset(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    def _make_test_dataset(self, clean=True):
        """Create a minimal valid dataset."""
        dataset = os.path.join(self.tmpdir.name, "dataset")
        for split in ("train", "val"):
            os.makedirs(os.path.join(dataset, "images", split), exist_ok=True)
            os.makedirs(os.path.join(dataset, "labels", split), exist_ok=True)

        # Write dataset.yaml
        with open(os.path.join(dataset, "dataset.yaml"), "w") as f:
            f.write("nc: 4\nnames:\n  0: deer\n  1: turkey\n  2: other_animal\n  3: human\n")

        # Write 5 images + labels for train
        for i in range(5):
            img = np.random.randint(0, 256, (512, 640), dtype=np.uint8)
            cv2.imwrite(os.path.join(dataset, "images", "train", f"img_{i}.png"), img)
            with open(os.path.join(dataset, "labels", "train", f"img_{i}.txt"), "w") as f:
                f.write(f"0 0.5 0.5 0.3 0.2\n")
                if not clean and i == 0:
                    f.write("99 0.5 0.5 0.3 0.2\n")  # bad class ID
        return dataset

    def test_validate_clean_dataset(self):
        dataset = self._make_test_dataset(clean=True)
        validate_dataset(dataset)
        # No assertion needed — just check it runs without error

    def test_validate_no_dataset_yaml(self):
        dataset = os.path.join(self.tmpdir.name, "no_yaml")
        os.makedirs(dataset, exist_ok=True)
        validate_dataset(dataset)
        # Should log error, not crash


class TestIntegration(unittest.TestCase):
    """Integration tests that exercise multiple pipeline steps."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_prepare_then_import_then_assemble(self):
        """Full pipeline: prepare workspace → CVAT import → assemble."""
        # 1. Create extracted frames (simulating extract_frames.py output)
        extracted = os.path.join(self.tmpdir.name, "extracted")
        os.makedirs(extracted, exist_ok=True)
        for i in range(6):
            img = np.random.randint(0, 256, (512, 640), dtype=np.uint8)
            import cv2
            cv2.imwrite(os.path.join(extracted, f"frame_{i:06d}.png"), img)

        # 2. Prepare workspace
        workspace = os.path.join(self.tmpdir.name, "workspace")
        prepare_workspace(extracted, workspace)

        # 3. Simulate CVAT annotation: write XML for all 6 images
        image_anns = {}
        for i in range(6):
            fname = f"frame_{i:06d}.png"
            image_anns[fname] = [("human", 200, 150, 400, 350)]
        xml_str = _make_cvat_xml(image_anns)
        xml_path = os.path.join(self.tmpdir.name, "ann.xml")
        with open(xml_path, "w") as f:
            f.write(xml_str)

        # 4. Import CVAT
        label_dir = os.path.join(workspace, "labels")
        import_cvat_xml(xml_path, os.path.join(workspace, "images"), label_dir)

        # 5. Check labels were created
        labels = [f for f in os.listdir(label_dir) if f.endswith(".txt")]
        self.assertEqual(len(labels), 6)

        # 6. Assemble final dataset
        output = os.path.join(self.tmpdir.name, "final_dataset")
        assemble_dataset(
            annotated_dir=workspace,
            output_dir=output,
            test_pct=0.2,
            seed=42,
        )

        # 7. Verify output structure
        self.assertTrue(os.path.isfile(os.path.join(output, "dataset.yaml")))
        train_img_count = len(os.listdir(os.path.join(output, "images", "train")))
        val_img_count = len(os.listdir(os.path.join(output, "images", "val")))
        self.assertEqual(train_img_count + val_img_count, 6)

        # 8. Validate
        validate_dataset(output)

    def test_cvat_xml_with_non_box_shapes(self):
        """CVAT XML with polygons should warn but not crash."""
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
<annotations>
  <version>1.1</version>
  <image id="0" name="test.png" width="640" height="512">
    <box label="human" xtl="100" ytl="100" xbr="300" ybr="400" occluded="0"/>
    <polygon label="human" points="100,100;200,100;150,200"/>
  </image>
</annotations>"""

        xml_path = os.path.join(self.tmpdir.name, "mixed.xml")
        with open(xml_path, "w") as f:
            f.write(xml_content)

        img_dir = os.path.join(self.tmpdir.name, "img")
        os.makedirs(img_dir, exist_ok=True)
        img = np.random.randint(0, 256, (512, 640), dtype=np.uint8)
        import cv2
        cv2.imwrite(os.path.join(img_dir, "test.png"), img)

        label_dir = os.path.join(self.tmpdir.name, "lbl")
        import_cvat_xml(xml_path, img_dir, label_dir)

        # The box should still be imported
        label_path = os.path.join(label_dir, "test.txt")
        self.assertTrue(os.path.isfile(label_path))
        with open(label_path) as f:
            line = f.readline().strip()
        self.assertGreater(len(line), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)