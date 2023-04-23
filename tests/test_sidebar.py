import pytest  # noqa F401
from PyTeXEditor.sidebar import Sidebar
from PyTeXEditor.document_elements import Text
from PyQt6.QtGui import QTextCursor


def test_clear(qtbot):
    sidebar = Sidebar()
    assert len(sidebar.children()) == 1
    sidebar.clear()
    assert len(sidebar.children()) == 1

    cursor = QTextCursor()
    sidebar.recieve_selection(cursor, Text)
    assert len(sidebar.children()) == 6
    sidebar.clear()
    assert len(sidebar.children()) == 1
