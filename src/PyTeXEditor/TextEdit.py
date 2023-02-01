from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSignal


class TextEdit(QtWidgets.QTextEdit):

    sidebar_visable_signal = pyqtSignal(bool)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def hide_sidebar(self) -> None:
        self.sidebar_visable_signal.emit(False)

    def show_sidebar(self) -> None:
        self.sidebar_visable_signal.emit(True)

    def changeEvent(self, e: QtCore.QEvent) -> None:
        print("a")
        return super().changeEvent(e)
