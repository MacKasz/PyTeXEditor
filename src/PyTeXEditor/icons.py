from PyQt6.QtGui import QPixmap, QIcon
from pathlib import Path
from typing import Dict
import os


FILE_DIR = Path(os.path.basename((os.path.realpath(__file__)))).resolve()
BASE_DIR = FILE_DIR.parent
ICONS_DIR = BASE_DIR / "icons/icons"

if not ICONS_DIR.is_dir():
    print("Icons folder not found, did you checkout the feathericons submodule")


class Icons:

    def __init__(self) -> None:
        print(ICONS_DIR)
        self.pixmap: Dict[str, QPixmap] = {
            "list": QPixmap(str(ICONS_DIR / "list-ul.svg"))
        }
        self.icons: Dict[str, QIcon] = dict()
        for name, pmap in self.pixmap.items():
            self.icons.update({name: QIcon(pmap)})
