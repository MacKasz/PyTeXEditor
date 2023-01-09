import PyTeXEditor
from PyQt6 import QtWidgets


class Window(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setObjectName("MainWindow")
        self.ui_init()
        self.show()

    def ui_init(self) -> None:
        vertical_split = QtWidgets.QVBoxLayout()
        self.ribbon = PyTeXEditor.Ribbon()
        vertical_split.addWidget(self.ribbon)
        vertical_split.setObjectName("VerticalSplit")

        self.sidebar = PyTeXEditor.Sidebar()
        self.textedit = PyTeXEditor.TextEdit()
        self.textedit.sidebar_visable_signal.connect(self.hide_sidebar)

        horizontal_split = QtWidgets.QHBoxLayout()
        horizontal_split.setObjectName("HorizontalSplit")
        horizontal_split.addWidget(self.sidebar)
        horizontal_split.addWidget(self.textedit)
        vertical_split.addLayout(horizontal_split)
        self.setLayout(vertical_split)

        self.setGeometry(0, 0, 500, 300)
        self.setWindowTitle('PyTeXEditor')

    def hide_sidebar(self):
        self.sidebar.setVisible(False)
