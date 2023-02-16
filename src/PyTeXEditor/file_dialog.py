from typing import Tuple
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QDir, pyqtSignal
from pathlib import Path
from PyTeXEditor.file_handler import FileHandler
from PyTeXEditor.latex_document import LatexDocument
import logging
import os


class FileDialog(QFileDialog):

    log = logging.getLogger("FileDialog")

    sidebar_visable_signal = pyqtSignal(LatexDocument)

    user_dir = Path(os.path.expanduser('~user'))

    def __init__(self):
        super().__init__()
        self.file_handler = FileHandler()
        super().setObjectName("FileDialog")

    def get_read_file(self) -> Tuple[Path, int]:  # pragma: no cover

        # Settings
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setDirectory(QDir.homePath())
        self.setMimeTypeFilters(["application/x-tex"])

        self.setVisible(True)
        return_value = self.exec()
        selected = self.selectedFiles()
        if len(selected) != 1:
            self.log.error(f"FileDialog expected 1 item,\
                    got {len(selected)} (taking 1st item)")

        return Path(selected[0]).resolve(), return_value

    def get_write_file(self) -> Tuple[Path, int]:  # pragma: no cover

        # Settings
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        self.setFileMode(QFileDialog.FileMode.AnyFile)
        self.setDirectory(QDir.homePath())
        self.setFilter(QDir.Filter.Writable)
        self.setMimeTypeFilters(["application/x-tex"])
        self.setVisible(True)

        self.setFocus()
        return_value = self.exec()
        selected = self.selectedFiles()
        if len(selected) != 1:
            self.log.error(f"FileDialog expected 1 item,\
                    got {len(selected)} (taking 1st item)")
        return Path(selected[0]).resolve(), return_value
