import pytest  # noqa F401
from PyTeXEditor.latex_document import LatexDocument
from PyTeXEditor.document_elements import Document, Text, Block
from PyTeXEditor.data_structures import Tree, Node
from pathlib import Path
from sys import platform
import os

test_dir = Path(os.path.dirname(os.path.realpath(__file__))).resolve()
base_dir = test_dir.parent.resolve()
resources_dir = (base_dir / "resources").resolve()


def test_processing():
    doc = LatexDocument()
    doc.plain_text = []
    doc.plain_to_tex()
    assert not doc.object_tree

    doc = LatexDocument()
    doc.plain_text = [r"line", r"\end{document}"]
    doc.plain_to_tex()
    assert not doc.object_tree

    doc = LatexDocument()
    with open(resources_dir / "good_document.tex") as file:
        doc.plain_text = file.readlines()
    doc.plain_to_tex()
    assert doc.object_tree
    root = doc.object_tree.root
    assert isinstance(root.data, Document)
    assert isinstance(root.children[0].data, Text)

    doc = LatexDocument()
    with open(resources_dir / "broken_document.tex") as file:
        doc.plain_text = file.readlines()
    with pytest.raises(RuntimeError):
        doc.plain_to_tex()


def test_traverse():
    doc = LatexDocument()
    with pytest.raises(RuntimeError):
        doc.big_brain_traverse()

    doc.object_tree = Tree[Block](Node[Block](1, Document()))

    element_list = doc.big_brain_traverse()
    assert len(element_list) == 2
    assert isinstance(element_list[0], Node)
    assert isinstance(element_list[0].data, Document)

    assert isinstance(element_list[1], str)
    assert element_list[1] == Document.name

    doc.object_tree.root.add_child(Node[Block](2, Text()))
    element_list = doc.big_brain_traverse()
    assert len(element_list) == 3
    assert isinstance(element_list[0], Node)
    assert isinstance(element_list[0].data, Document)

    assert isinstance(element_list[1], Node)
    assert isinstance(element_list[1].data, Text)

    assert isinstance(element_list[2], str)
    assert element_list[2] == Document.name

    doc.object_tree.root = Node(0, "bad")  # type: ignore
    with pytest.raises(TypeError):
        doc.big_brain_traverse()


def test_qt_processing():
    doc = LatexDocument()
    doc.internal_to_qt()


def test_compile():
    doc = LatexDocument()
    with pytest.raises(RuntimeError):
        doc.get_tex()

    doc = LatexDocument()
    doc.object_tree = Tree[Block](Node[Block](0, Document()))
    doc.object_tree.root.add_child(Node[Block](1, Text()))
    doc.object_tree.root.children[0].data.process_data("test")

    # Will probably have to check the contents manually?
    if platform == "linux" or platform == "linux2":
        doc.compile()


def test_get_tex():
    doc = LatexDocument()
    with pytest.raises(RuntimeError):
        doc.get_tex()

    doc = LatexDocument()
    doc.object_tree = Tree[Block](Node[Block](0, Document()))
    doc.object_tree.root.add_child(Node[Block](1, Text()))
    doc.object_tree.root.children[0].data.process_data("test")
    tex_source = doc.get_tex()

    # Might have to change this
    assert tex_source[0] == "\\documentclass{article}"
    assert tex_source[1] == "\\begin{document}\n"
    assert tex_source[2] == "test\n\n"
    assert tex_source[3] == "\\end{document}\n"
