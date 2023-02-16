import pytest  # noqa F401
from PyTeXEditor.file_dialog import FileDialog
from PyTeXEditor.file_handler import FileHandler


def test_init(qtbot):
    dialog = FileDialog()
    assert dialog.objectName() == "FileDialog"

    assert type(dialog.file_handler) is FileHandler
