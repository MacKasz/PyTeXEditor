import pytest # noqa F401
from PyTeXEditor.file_handler import FileHandler
from PyTeXEditor.document_elements import Document, Text
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

    handler_sym.read_file()
    assert handler_sym.doc.plain_text is not None
    handler_sym.convert()

    tree = handler_sym.doc.object_tree
    assert type(tree.root.data) is Document

    assert type(tree.root.children[0].data) == Text
