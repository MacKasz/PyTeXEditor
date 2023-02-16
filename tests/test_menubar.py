import pytest # noqa F401
from PyQt6 import QtWidgets
from PyTeXEditor.menubar import Menubar


def test_object_name(qtbot):
    menu = Menubar()
    assert menu.objectName() == "Menubar"


def test_menu_items(qtbot):
    menubar = Menubar()

    menu_list = list(menubar.menus.values())

    assert type(menu_list[0]) is QtWidgets.QMenu
    assert menu_list[0].title() == "File"

    assert type(menu_list[0]) is QtWidgets.QMenu
    assert menu_list[1].title() == "Edit"

    assert type(menu_list[0]) is QtWidgets.QMenu
    assert menu_list[2].title() == "Run"
