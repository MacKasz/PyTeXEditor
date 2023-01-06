from TextEdit import TextEdit
from Sidebar import Sidebar
from Ribbon import Ribbon
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import pyqtSlot


def test():
    print("test")

class Window(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setObjectName("MainWindow")
        self.ui_init()
        self.show()

    def ui_init(self) -> None:
        vertical_split = QtWidgets.QVBoxLayout()
        self.ribbon = Ribbon()
        vertical_split.addWidget(self.ribbon)
        vertical_split.setObjectName("VerticalSplit")

        self.hide = False

        self.sidebar = Sidebar()
        self.textedit = TextEdit()
        self.textedit.hide_signal[bool].connect(test)

        horizontal_split = QtWidgets.QHBoxLayout()
        horizontal_split.addWidget(self.sidebar)
        horizontal_split.addWidget(self.textedit)
        vertical_split.addLayout(horizontal_split)
        self.setLayout(vertical_split)

        self.setGeometry(0, 0, 500, 300)
        self.setWindowTitle('PyTeXEditor')

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        return super().resizeEvent(a0)

    @pyqtSlot(bool)
    def hide_sidebar():
        print("a")
