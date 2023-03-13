import pytest  # noqa F401
from PyTeXEditor.latex_document import LatexDocument
from PyTeXEditor.document_elements import Document, Text, Block
from PyTeXEditor.data_structures import Tree, Node


def test_processing():
    doc = LatexDocument()
    doc.plain_text = []
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
