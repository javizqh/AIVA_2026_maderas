import os
import re
import unittest
import time

import cv2

import numpy as np

from src.main import detect


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


class TestDetect(unittest.TestCase):
    def test_callable(self):
        """
        Test that it can be called from other app
        """
        data = [2, 700, 770, 40, 46, 99, 20, 30, 43, 45, 80]
        result = detect("dataset/01.png")
        self.assertEqual(result, data)

    def test_bbox_detection(self):
        """
        Test that it can detect the defect with over 90% mean average accuracy
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

            result = detect(img)
            for i in range(result[0]):
                pred_label = result[1 + i * 5 : (i + 1) * 5]

                gt_index = 0
                for gt_label in groundtruth:
                    if np.allclose(gt_label, pred_label, atol=5):
                        correct += 1
                        np.delete(groundtruth, gt_index, 0)
                    gt_index += 1

        self.assertGreaterEqual(correct / n_instances, 90)

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

            result = detect(img)
            for i in range(result[0]):
                confidence = result[1 + 4 + i * 5]
                n_instances += 1
                if confidence >= 50:
                    correct += 1

        self.assertEqual(correct, n_instances)

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
            result = detect(img)
            end = time.time()

            self.assertLess(end - start, 1)


if __name__ == "__main_":
    unittest.main()
