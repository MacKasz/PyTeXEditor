from PyQt6 import QtWidgets


class Sidebar(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setObjectName("Sidebar")
        self.box = QtWidgets.QVBoxLayout()
        self.setLayout(self.box)
        self.box.addStretch(1)
