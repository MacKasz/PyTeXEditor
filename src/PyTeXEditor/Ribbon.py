from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget


class Ribbon(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setObjectName("Ribbon")

        self.grid = QtWidgets.QGridLayout()
        self.grid.setObjectName("RibbonGrid")

        self.ui_init()
        self.setLayout(self.grid)

    def ui_init(self) -> None:
        self.add_buttons()

    def add_buttons(self) -> None:
        button = QtWidgets.QPushButton("asd")
        self.grid.addWidget(button)
