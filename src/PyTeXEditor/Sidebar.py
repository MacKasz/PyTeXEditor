from PyQt6 import QtWidgets


class Sidebar(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.box = QtWidgets.QVBoxLayout()
        self.setLayout(self.box)
        self.temp()
        self.box.addStretch(1)

    def temp(self):
        button = QtWidgets.QPushButton("asd")
        print(type(button.clicked))
        self.box.addWidget(button)
