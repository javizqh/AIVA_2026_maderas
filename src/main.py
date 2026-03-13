import xml.etree.ElementTree as ET
from enum import Enum
from typing import List

import cv2

import numpy as np


class WoodDeftect(Enum):
    """Types of defects found in the woods:

    0 -- grieta
    1 -- nudo
    """

    grieta = 0
    nudo = 1


class WoodErrorsOutput:
    """Contains the methods related to the xml output as well as sanitizing the detection output"""

    def __init__(self, image: str, path: str | None = None):
        """Initialises the WoodErrorsOutput class.

        Keyword arguments:
        image -- the image path
        path -- the xml output file to save the results (default None)
        """

        self.path = path
        self.root = ET.Element("Tabla")
        self.root.set("filename", image)

    def add_defect(self, defect: List[int]) -> List[int]:
        """Adds defect to the xml tree and returns the defect without the type.

        Keyword arguments:
        defect -- needs to contain the next 6 values:
            x -- X coordinate of the top left corner of the bbox
            y -- Y coordinate of the top left corner of the bbox
            width -- width of the bbox
            height -- height of the bbox
            gravity -- confidence of the bbox detection
            type -- type of the defect. Can be 0 or 1 complying with WoodDeftect enum
        """

        x, y, width, height, conf, def_type = defect

        xml_defect = ET.SubElement(self.root, "Defecto")
        xml_defect.set("x0", str(x))
        xml_defect.set("y0", str(y))
        xml_defect.set("width", str(width))
        xml_defect.set("height", str(height))
        xml_defect.set("gravedad", f"{conf}%")
        xml_defect.set("tipo", WoodDeftect(def_type).name)

        return [x, y, width, height, conf]

    def save(self):
        """Saves the results to the xml file when it has been defined."""

        if self.path is None:
            return

        xml_data = ET.tostring(self.root)

        with open(self.path, "wb") as f:
            f.write(xml_data)


def load_image(path: str) -> np.array:
    """Loads an image using opencv and return it.

    Keyword arguments:
    path -- the image path
    """

    img = cv2.imread(path, cv2.IMREAD_COLOR_BGR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb


def detect_defects(img: np.array) -> List[int]:
    """Return a list of defect detections given an image.

    Each element in the list contains 6 numbers:
    x -- X coordinate of the top left corner of the bbox
    y -- Y coordinate of the top left corner of the bbox
    width -- width of the bbox
    height -- height of the bbox
    gravity -- confidence of the bbox detection
    type -- type of the defect. Can be 0 or 1 complying with WoodDeftect enum
    """

    # TODO: this is an mockup
    return [[700, 770, 40, 46, 99, 0], [20, 30, 43, 45, 80, 1]]


def detect(image_filename: str, xml_file: str | None = None) -> List[int]:
    """Detect defects in the wood image passed and return a list of defects.

    Keyword arguments:
    image_filename -- the image path
    xml_file -- the xml output file to save the results (default None)
    """

    defects = [0]
    woodErrorOutput = WoodErrorsOutput(image_filename, xml_file)
    img = load_image(image_filename)

    for defect in detect_defects(img):
        defects[0] = defects[0] + 1
        defects += woodErrorOutput.add_defect(defect)

    woodErrorOutput.save()
    return defects
