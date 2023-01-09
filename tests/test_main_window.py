import pytest # noqa F401
import PyTeXEditor
from PyQt6 import QtWidgets


def test_sanity():
    print("Run")


def test_window_name(qtbot):
    main_window = PyTeXEditor.Window()
    assert main_window.objectName() == "MainWindow"


def test_window_layout(qtbot):
    main_window = PyTeXEditor.Window()

    assert main_window.layout().objectName() == "VerticalSplit"
    assert type(main_window.layout()) is QtWidgets.QVBoxLayout

    assert main_window.layout().itemAt(0).widget().objectName() == "Ribbon"
    assert type(main_window.layout().itemAt(0).widget()) is PyTeXEditor.Ribbon

    assert main_window.layout().children()[0].objectName() == "HorizontalSplit"
    assert type(main_window.layout().children()[0]) is QtWidgets.QHBoxLayout

    assert main_window.layout().children()[0]\
        .itemAt(0).widget().objectName() == "Sidebar"
    assert type(main_window.layout().children()[0].itemAt(0).widget())\
        is PyTeXEditor.Sidebar


def test_hide_sidebar(qtbot):
    main_window = PyTeXEditor.Window()

    assert main_window.sidebar.isVisible() is True

    main_window.hide_sidebar()

    assert main_window.sidebar.isVisible() is False
