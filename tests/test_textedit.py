import pytest  # noqa F401
from PyTeXEditor.textedit import TextEdit
from PyTeXEditor.data_structures import Tree, Node
from PyTeXEditor.latex_document import LatexDocument
from PyTeXEditor.document_elements import Document, Text, Block


def test_set_document(qtbot):
    doc = LatexDocument()
    doc.object_tree = Tree[Block](Node[Block](0, Document()))
    doc.object_tree.root.add_child(Node[Block](1, Text()))

    text_edit = TextEdit()
    text_edit.set_document(doc)
