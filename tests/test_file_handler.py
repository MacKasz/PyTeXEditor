import pytest # noqa F401
from PyTeXEditor.file_handler import FileHandler
from PyTeXEditor.document_elements import Document, Text
from PyTeXEditor.latex_document import LatexDocument
from pathlib import Path
import os

test_dir = Path(os.path.dirname(os.path.realpath(__file__))).resolve()
print(test_dir)
base_dir = test_dir.parent.resolve()
print(base_dir)
resources_dir = (base_dir / "resources").resolve()
print(resources_dir)


def test_init():
    handler = FileHandler()
    assert handler.file_created is False

    assert type(handler.doc) is LatexDocument

    with pytest.raises(AttributeError):
        if handler.file_path:
            pytest.fail()


def test_resolve():
    handler = FileHandler()

    handler.set_path(resources_dir / "good_document.tex")
    assert type(handler) is FileHandler

    handler_sym = FileHandler()
    handler_sym.set_path(resources_dir / "linked_document.tex")
    assert handler_sym.file_path == resources_dir / "actual_document.tex"

    handler_sym.read_file()
    assert handler_sym.doc.plain_text is not None
    handler_sym.doc.plain_to_tex()

    tree = handler_sym.doc.object_tree
    assert type(tree.root.data) is Document

    assert type(tree.root.children[0].data) == Text

    with pytest.raises(IsADirectoryError):
        handler.set_path(resources_dir)

    # Can test this locally but cannot upload an unreadable file
    # to git.
    # with pytest.raises(PermissionError):
    #     handler.set_path(resources_dir / "unreadable_document.tex")


def test_write():
    handler = FileHandler()
    handler.set_path(resources_dir / "write_test.tex")

    handler.write_file(["test1", "test2"])

    with open(Path(resources_dir / "write_test.tex"), 'rb') as file:
        assert file.read().decode() == f"test1{os.linesep}test2{os.linesep}"
