from PyTeXEditor.window import Window
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSize
import sys
import logging


if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
    app = QApplication(sys.argv)
    ex = Window()
    size = QSize()
    size.setHeight(600)
    size.setWidth(800)
    ex.resize(size)
    sys.exit(app.exec())
