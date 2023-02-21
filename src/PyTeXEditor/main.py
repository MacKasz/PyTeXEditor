from PyTeXEditor.window import Window
from PyQt6.QtWidgets import QApplication
import sys
import logging


if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec())
