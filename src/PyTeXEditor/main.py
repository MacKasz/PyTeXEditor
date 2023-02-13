from PyTeXEditor.window import Window
from PyQt6.QtWidgets import QApplication
from pathlib import Path
import sys
import os
import logging

FILE_DIR = Path(os.path.basename((os.path.realpath(__file__)))).resolve()
BASE_DIR = FILE_DIR.parent
ICONS_DIR = BASE_DIR / "icons/feather"

print(f"FILE: {ICONS_DIR}")

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec())
