import pytest # noqa F401
from PyTeXEditor.file_handler import FileHandler
from PyTeXEditor.document_elements import Document, Text
from PyTeXEditor.latex_document import LatexDocument
from pathlib import Path
from sys import platform
import os

test_dir = Path(os.path.dirname(os.path.realpath(__file__))).resolve()
print(test_dir)
base_dir = test_dir.parent.resolve()
print(base_dir)
resources_dir = (base_dir / "resources").resolve()
print(resources_dir)


def test_init():
    handler = FileHandler()

    assert isinstance(handler, FileHandler)
    assert handler.file_created is False

    assert isinstance(handler.doc, LatexDocument)

    with pytest.raises(AttributeError):
        if handler.file_path:
            pytest.fail()


def test_make_new_file():
    handler = FileHandler()
    handler.set_path(resources_dir / "new_file")
    assert os.path.exists(resources_dir / "new_file")
    assert os.access(resources_dir / "new_file", os.R_OK)
    assert os.access(resources_dir / "new_file", os.W_OK)

    handler = FileHandler()
    if platform == "linux" or platform == "linux2":
        with pytest.raises(PermissionError):
            handler.set_path(Path("/file"))
    if platform == "win32":
        with pytest.raises(PermissionError):
            handler.set_path(Path("C:/Windows/System32/file"))


def test_resolve():
    handler = FileHandler()

    handler.set_path(resources_dir / "good_document.tex")
    handler_sym = FileHandler()
    handler_sym.set_path(resources_dir / "linked_document.tex")
    assert handler_sym.file_path == resources_dir / "actual_document.tex"

    handler_sym.read_file()
    assert handler_sym.doc.plain_text is not None
    handler_sym.doc.plain_to_tex()

    tree = handler_sym.doc.object_tree
    assert tree
    assert isinstance(tree.root.data, Document)

    assert isinstance(tree.root.children[0].data, Text)

    with pytest.raises(IsADirectoryError):
        handler.set_path(resources_dir)


@pytest.mark.skip(reason="Cannot test on cloud")
def test_permission(qtbot):
    # Can only test this locally as you cannot upload an unreadable file to git.

    handler = FileHandler()
    with pytest.raises(PermissionError):
        handler.set_path(resources_dir / "unreadable_document.tex")
