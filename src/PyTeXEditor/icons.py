from PyQt6.QtGui import QColor, QPixmap, QPainter
from PyQt6.QtCore import Qt, QByteArray
from typing import Dict
import os

import xml.etree.ElementTree as Et


class Icon:

    def __init__(self, icon_path, color="white"):

        self.tree = Et.parse(icon_path)
        self.root = self.tree.getroot()

        self._change_path_color(color)

    def _change_path_color(self, color):
        c = QColor(color)
        paths = self.root.findall('.//{*}path')
        for path in paths:
            path.set('fill', c.name())

    def get_QByteArray(self):
        xmlstr = Et.tostring(self.root, encoding='utf8', method='xml')
        return QByteArray(xmlstr)
