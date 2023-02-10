import pytest # noqa F401
from PyQt6 import QtWidgets
from PyTeXEditor.GuiElements import Menubar


def test_object_name(qtbot):
    menu = Menubar()
    assert menu.objectName() == "Menubar"


def test_menu_items(qtbot):
    menu = Menubar()
    menu_items = menu.children()[1:]

    type(menu_items[0]) is QtWidgets.QMenu
    assert menu_items[0].title() == "File"

    type(menu_items[1]) is QtWidgets.QMenu
    assert menu_items[1].title() == "Edit"

    type(menu_items[2]) is QtWidgets.QMenu
    assert menu_items[2].title() == "Run"
