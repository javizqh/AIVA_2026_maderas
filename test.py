import os
import re
import unittest
import time

import cv2

import numpy as np
import xml.etree.ElementTree as ET


from src.defect_detector import detectar


def tryint(s):
    try:
        return int(s)
    except Exception:
        return s


def alphanum_key(s):
    """Turn a string into a list of string and number chunks.
    "z23a" -> ["z", 23, "a"]
    """
    return [tryint(c) for c in re.split("([0-9]+)", s)]


def get_images(dir_path):
    files = [
        os.path.join(dir_path, x)
        for x in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, x))
    ]

    files.sort(key=alphanum_key)

    imgs = []
    labels = []

    index = 0
    for file in files:
        if index % 2 == 0:
            imgs.append(file)
        else:
            labels.append(file)
        index += 1

    return (imgs, labels)


def read_label(path):
    try:
        s = cv2.FileStorage()
        s.open(path, cv2.FileStorage_READ)
        matrix = s.getNode("rectangles").mat()
        matrix = matrix.T
        s.release()
    except Exception:
        matrix = []

    return matrix


def read_result_classes(path):
    tree = ET.parse(path)
    root = tree.getroot()
    types = []
    for i in range(len(root)):
        types.append(root[i].attrib["tipo"])
    return list(set(types))


def get_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    """

    # Determine the coordinates of the intersection rectangle
    x_left = max(bb1[0] - bb1[2] / 2, bb2[0] - bb2[2] / 2)
    y_top = max(bb1[1] - bb1[3] / 2, bb2[1] - bb2[3] / 2)
    x_right = max(bb1[0] + bb1[2] / 2, bb2[0] + bb2[2] / 2)
    y_bottom = min(bb1[1] + bb1[3] / 2, bb2[1] + bb2[3] / 2)

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # Compute the area of both bbox
    bb1_area = (bb1[2]) * (bb1[3])
    bb2_area = (bb2[2]) * (bb2[3])

    # Compute the intersection over union
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)

    return iou


class TestDetect(unittest.TestCase):
    def test_callable(self):
        """
        Test that it can be called from other app
        """
        result = detectar("dataset/01.png")
        self.assertGreater(len(result), 0)

    def test_bbox_detection(self):
        """
        Test that it can detect the defect with over 80% mean average accuracy
        """
        correct = 0
        n_images = 0
        n_instances = 0

        imgs, labels = get_images("dataset")
        for img, label in zip(imgs, labels):
            if n_images >= 40:
                break

            n_images += 1

            groundtruth = read_label(label)
            n_instances += len(groundtruth)

            result = detectar(img)
            for i in range(result[0]):
                pred_label = result[1 + i * 5 : (i + 1) * 5]

                gt_index = 0
                for gt_label in groundtruth:
                    if get_iou(gt_label, pred_label) > 0.25:
                        correct += 1
                        np.delete(groundtruth, gt_index, 0)
                    gt_index += 1

        self.assertGreaterEqual(correct / n_instances, 0.80)

    def test_confidence(self):
        """
        Test that it outputs predictions only with over 50% confidence
        """
        correct = 0
        n_images = 0
        n_instances = 0

        imgs, _ = get_images("dataset")
        for img in imgs:
            if n_images >= 20:
                break

            n_images += 1

            result = detectar(img)
            for i in range(result[0]):
                confidence = result[1 + 4 + i * 5]
                n_instances += 1
                if confidence >= 50:
                    correct += 1

        self.assertEqual(correct, n_instances)

    def test_types(self):
        """
        Test that it outputs class predictions for the correct type
        """
        correct = 0
        n_images = 0
        n_instances = 0

        imgs, _ = get_images("dataset")
        for img in imgs:
            if n_images >= 40:
                break

            n_images += 1

            result = detectar(img, "tmp.xml")
            diff_types = read_result_classes("tmp.xml")
            for diff_type in diff_types:
                self.assertTrue(diff_type == "nudo" or diff_type == "grieta")

    def test_inference_time(self):
        """
        Test that the inference time is less than 1 seconds per image
        """
        n_images = 0

        imgs, _ = get_images("dataset")
        for img in imgs:
            if n_images >= 20:
                break

            n_images += 1

            start = time.time()
            result = detectar(img)
            end = time.time()

            self.assertLess(end - start, 1)

    def test_bad_image(self):
        """
        Test that the function raises an error if the image does not exist
        """
        with self.assertRaises(Exception):
            result = detectar("img")

    def test_only_image(self):
        """
        Test that the function works properly if the image path has been passed
        and returns a correct result, at least in structure
        """
        result = detectar("dataset/01.png")
        self.assertEqual(len(result), result[0] * 5 + 1)
        self.assertFalse(
            os.path.exists("test.xml"),
            "The file exists in the specified directory",
        )

    def test_image_and_xml(self):
        """
        Test that the function works properly if the image path has been passed
        and returns a correct result, at least in structure. Also checks if the
        xml has been outputed.
        """
        result = detectar("dataset/01.png", "test.xml")
        self.assertEqual(len(result), result[0] * 5 + 1)
        self.assertTrue(
            os.path.exists("test.xml"),
            "The file exists in the specified directory",
        )
        os.remove("test.xml")


if __name__ == "__main__":
    unittest.main()
