from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from typing import Dict


class Ribbon(QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setObjectName("Ribbon")
        self.__ui_setup()

    def __make_hline(self) -> QtWidgets.QFrame:
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        return hline

    def __make_vline(self) -> QtWidgets.QFrame:
        vline = QtWidgets.QFrame()
        vline.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        return vline

    def __ui_setup(self) -> None:
        """Sets up the UI elements.
        """
        self.buttons: Dict[str, QtWidgets.QPushButton] = dict()
        horizontal = QtWidgets.QHBoxLayout()

        # == Text ==
        v = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Text")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        v.addWidget(label)
        v.addWidget(self.__make_hline())

        self.buttons.update({"itemize": QtWidgets.QPushButton()})
        self.buttons["itemize"].setToolTip("Bulleted List")
        self.buttons["itemize"].setText("List")
        v.addWidget(self.buttons["itemize"])
        self.buttons.update({"enum": QtWidgets.QPushButton()})
        self.buttons["enum"].setToolTip("Enumarated List")
        self.buttons["enum"].setText("Enumerated List")
        v.addWidget(self.buttons["enum"])
        horizontal.addLayout(v)
        horizontal.addWidget(self.__make_vline())

        # == Image ==
        v = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Image")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        v.addWidget(label)
        v.addWidget(self.__make_hline())

        self.buttons.update({"image": QtWidgets.QPushButton()})
        self.buttons["image"].setToolTip("Image")
        self.buttons["image"].setText("Image")
        v.addWidget(self.buttons["image"])
        horizontal.addLayout(v)
        horizontal.addWidget(self.__make_vline())

        horizontal.addWidget(QtWidgets.QFrame())
        self.setLayout(horizontal)
