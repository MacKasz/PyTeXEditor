from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QDir
from pathlib import Path
from PyTeXEditor.file_handler import FileHandler
import logging
import os


class FileDialog(QFileDialog):

    user_dir = Path(os.path.expanduser('~user'))

    def __init__(self):
        super().__init__()
        self.file_handler = FileHandler()

    def get_read_file(self) -> Path:
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setDirectory(QDir.homePath())
        self.setMimeTypeFilters(["application/x-tex"])
        self.setVisible(True)
        return_value = self.exec()
        print(return_value)
        if return_value == 1:
            selected = self.selectedFiles()
            if len(selected) != 1:
                logging.error(f"FileDialog expected 1 item,\
                     got {len(selected)} (taking 1st item)")

            return Path(selected[0]).resolve()
        else:
            logging.debug("No file selected")
            return Path("")

    def get_write_file(self) -> Path:
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        self.setFileMode(QFileDialog.FileMode.AnyFile)
        self.setDirectory(QDir.homePath())
        self.setFilter(QDir.Filter.Writable)
        self.setMimeTypeFilters(["application/x-tex"])
        self.setVisible(True)
        self.setFocus()
        return_value = self.exec()
        if return_value == 1:
            selected = self.selectedFiles()
            if len(selected) != 1:
                logging.error(f"FileDialog expected 1 item,\
                     got {len(selected)} (taking 1st item)")
            return Path(selected[0]).resolve()
        else:
            return Path("")
