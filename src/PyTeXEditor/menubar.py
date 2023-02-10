from PyQt6 import QtWidgets


class Menubar(QtWidgets.QMenuBar):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("Menubar")
        self.file_menu = self.addMenu("File")
        self.file_menu = self.addMenu("Edit")
        self.file_menu = self.addMenu("Run")
