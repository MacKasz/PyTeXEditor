import pytest  # noqa F401
from PyTeXEditor.latex_document import LatexDocument


def test_processing():
    doc = LatexDocument()
    doc.plain_text = []
    doc.plain_to_tex()
