from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal, Qt


class TextEdit(QtWidgets.QTextEdit):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hide_signal = pyqtSignal(bool)
