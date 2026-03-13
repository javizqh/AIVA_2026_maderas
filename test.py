import os
import re
import unittest

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

        imgs, labels = get_images("dataset")
        for img, label in zip(imgs, labels):
            if n_images >= 40:
                break

            n_images += 1

            groundtruth = read_label(label)
            result = detect(img)
            for i in range(result[0]):
                pred_label = result[1 + i * 5 : (i + 1) * 5]

                gt_index = 0
                for gt_label in groundtruth:
                    if np.allclose(gt_label, pred_label, atol=5):
                        correct += 1
                        np.delete(groundtruth, gt_index, 0)
                    gt_index += 1

        self.assertGreaterEqual(correct / n_images, 90)


if __name__ == "__main_":
    unittest.main()
