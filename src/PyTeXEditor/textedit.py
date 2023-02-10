from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal


class TextEdit(QtWidgets.QTextEdit):

    sidebar_visable_signal = pyqtSignal(bool)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setObjectName("TextEdit")

    def hide_sidebar(self) -> None:
        self.sidebar_visable_signal.emit(False)

    def show_sidebar(self) -> None:
        self.sidebar_visable_signal.emit(True)
