from PyQt6 import QtWidgets, QtGui
from typing import Dict


class Menubar(QtWidgets.QMenuBar):
    def __init__(self) -> None:
        super().__init__()
        super().setObjectName("Menubar")
        self.__init_ui()

    def __init_ui(self) -> None:
        self.menus: Dict[str, QtWidgets.QMenu] = dict()
        self.menu_actions: Dict[str, QtGui.QAction] = dict()

        # == File ==
        file = QtWidgets.QMenu("File")
        self.menus.update({"File": file})
        self.addMenu(file)

        self.menu_actions.update({"Open": file.addAction("Open")})
        self.menu_actions["Open"].setShortcut("Ctrl+O")
        file.addSeparator()
        self.menu_actions.update({"Save": file.addAction("Save")})
        self.menu_actions["Save"].setShortcut("Ctrl+S")
        self.menu_actions.update({"Save as": file.addAction("Save as")})
        self.menu_actions["Save as"].setShortcut("Ctrl+Shift+S")
        file.addSeparator()

        # == Edit ==
        edit = QtWidgets.QMenu("Edit")
        self.menus.update({"Edit": edit})
        self.addMenu(edit)

        self.menu_actions.update({"Copy": edit.addAction("Copy")})
        self.menu_actions["Copy"].setShortcut("Ctrl+C")
        self.menu_actions.update({"Cut": edit.addAction("Cut")})
        self.menu_actions["Cut"].setShortcut("Ctrl+X")
        self.menu_actions.update({"Paste": edit.addAction("Paste")})
        self.menu_actions["Paste"].setShortcut("Ctrl+V")

        # == Run ==
        run = QtWidgets.QMenu("Run")
        self.menus.update({"Run": run})
        self.addMenu(run)

        self.menu_actions.update({"Compile": run.addAction("Compile")})
