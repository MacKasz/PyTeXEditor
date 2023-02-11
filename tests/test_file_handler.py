import pytest # noqa F401
from PyTeXEditor.file_handler import FileHandler
from pathlib import Path
import os

test_dir = Path(os.path.basename(os.path.realpath(__file__))).resolve()
base_dir = test_dir.parent.resolve()
resources_dir = (base_dir / "resources").resolve()


def test_init():
    handler = FileHandler(resources_dir / "good_document.tex")
    assert type(handler) is FileHandler

    handler_sym = FileHandler(resources_dir / "linked_document.tex")
    assert handler_sym.file_path == resources_dir / "actual_document.tex"
