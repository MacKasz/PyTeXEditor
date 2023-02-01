import PyTeXEditor
from PyQt6 import QtWidgets


class Window(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setObjectName("MainWindow")
        self.ui_init()
        self.show()

    def ui_init(self) -> None:
        outer_vsplit = QtWidgets.QVBoxLayout()
        vertical_split = QtWidgets.QVBoxLayout()
        horizontal_split = QtWidgets.QHBoxLayout()

        self.menubar = PyTeXEditor.Menubar()
        self.ribbon = PyTeXEditor.Ribbon()
        self.sidebar = PyTeXEditor.Sidebar()
        self.textedit = PyTeXEditor.TextEdit()

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

    def hide_sidebar(self):
        self.sidebar.setVisible(False)
