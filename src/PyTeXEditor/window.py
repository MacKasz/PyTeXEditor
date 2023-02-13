from PyTeXEditor.menubar import Menubar
from PyTeXEditor.ribbon import Ribbon
from PyTeXEditor.sidebar import Sidebar
from PyTeXEditor.textedit import TextEdit
from PyTeXEditor.file_dialog import FileDialog
from PyTeXEditor.file_handler import FileHandler
from PyQt6 import QtWidgets


class Window(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        super().setObjectName("MainWindow")
        self.file_handler = FileHandler()
        self.file_dialog = FileDialog()
        self.file_dialog.setVisible(False)
        self.ui_init()
        self.show()

    def ui_init(self) -> None:
        outer_vsplit = QtWidgets.QVBoxLayout()
        vertical_split = QtWidgets.QVBoxLayout()
        horizontal_split = QtWidgets.QHBoxLayout()

        self.menubar = Menubar()
        self.menubar.menu_actions["Open"].\
            triggered.connect(self.__open_file)  # type: ignore
        self.ribbon = Ribbon()
        self.sidebar = Sidebar()
        self.textedit = TextEdit()

        self.textedit.sidebar_visable_signal.connect(self.hide_sidebar)

        horizontal_split.setObjectName("HSplit")
        horizontal_split.addWidget(self.sidebar)
        horizontal_split.addWidget(self.textedit)

        vertical_split.setObjectName("InnerVSplit")
        vertical_split.addWidget(self.ribbon)
        vertical_split.addLayout(horizontal_split)

        outer_vsplit.setObjectName("OuterVSplit")
        outer_vsplit.addWidget(self.menubar)
        outer_vsplit.addLayout(vertical_split)

        self.setLayout(outer_vsplit)

        self.setGeometry(0, 0, 500, 300)
        self.setWindowTitle("PyTeXEditor")

    def __open_file(self) -> None:
        path = self.file_dialog.get_read_file()
        self.file_handler.set_path(path)
        self.file_handler.read_file()
        self.file_handler.convert()
        for node in self.file_handler.doc.object_tree.preorder_traverse():
            print(f"{type(node.data)}")

    def hide_sidebar(self) -> None:
        self.sidebar.setVisible(False)
