import pytest  # noqa F401
from PyTeXEditor.window import Window
from PyTeXEditor.menubar import Menubar
from PyTeXEditor.ribbon import Ribbon
from PyTeXEditor.sidebar import Sidebar
from PyTeXEditor.textedit import TextEdit
from PyQt6 import QtWidgets


def test_sanity():
    print("Run")


def test_window_name(qtbot):
    main_window = Window()
    assert main_window.objectName() == "MainWindow"


@pytest.mark.skip(reason="This will change")
def test_window_layout(qtbot):
    main_window = Window()
    first = main_window.layout()
    second = first.children()[0]
    third = second.children()[0]

    assert type(first) is QtWidgets.QVBoxLayout
    assert first.objectName() == "OuterVSplit"
    assert type(first.itemAt(0).widget()) is Menubar
    assert first.itemAt(0).widget().objectName() == "Menubar"

    assert type(second) is QtWidgets.QVBoxLayout
    assert second.objectName() == "InnerVSplit"
    assert type(second.itemAt(0).widget()) is Ribbon
    assert second.itemAt(0).widget().objectName() == "Ribbon"

    assert type(third) is QtWidgets.QHBoxLayout
    assert third.objectName() == "HSplit"
    assert type(third.itemAt(0).widget()) is Sidebar
    assert third.itemAt(0).widget().objectName() == "Sidebar"
    assert type(third.itemAt(1).widget()) is TextEdit
    assert third.itemAt(1).widget().objectName() == "TextEdit"


def test_hide_sidebar(qtbot):
    main_window = Window()

    assert main_window.sidebar.isVisible() is True

    main_window.hide_sidebar()

    assert main_window.sidebar.isVisible() is False
