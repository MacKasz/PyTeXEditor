from typing import Tuple
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QDir, pyqtSignal
from pathlib import Path
from PyTeXEditor.file_handler import FileHandler
from PyTeXEditor.latex_document import LatexDocument
import logging


class FileDialog(QFileDialog):
    """Extension of `QFileDialog`

    Signals
    -------
    sidebar_visable_signal()

    Methods
    -------
    get_read_file()
        Gets the path of a file to read, and the dialog code.
    get_write_file()
        Gets the path of a file to write, and the dialog code.
    """

    __log = logging.getLogger("FileDialog")

    sidebar_visable_signal = pyqtSignal(LatexDocument)

    def __init__(self):
        super().__init__()
        self.file_handler = FileHandler()
        super().setObjectName("FileDialog")

    def get_read_file(self) -> Tuple[Path, int]:  # pragma: no cover
        """Using the OS's native file dialog retrieves a path for reading
        a file.

        Returns
        -------
        Tuple[Path, int]
            Returns the path of the file and the return code.
            (1 = Accepted, 0 = Rejected)
        """

        # Settings
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setDirectory(QDir.homePath())
        self.setMimeTypeFilters(["application/x-tex"])

        self.setVisible(True)
        return_value = self.exec()
        selected = self.selectedFiles()
        if len(selected) != 1:
            self.__log.error(f"FileDialog expected 1 item,\
                    got {len(selected)} (taking 1st item)")

        return Path(selected[0]).resolve(), return_value

    def get_write_file(self) -> Tuple[Path, int]:  # pragma: no cover
        """Using the OS's native file dialog retrieves a path for writing
        a file.

        Returns
        -------
        Tuple[Path, int]
            Returns the path of the file and the return code.
            (1 = Accepted, 0 = Rejected)
        """

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
            self.__log.error(f"FileDialog expected 1 item,\
                    got {len(selected)} (taking 1st item)")
        return Path(selected[0]).resolve(), return_value
