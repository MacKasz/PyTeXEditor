from typing import Type, Union
from PyQt6.QtWidgets import QWidget, QBoxLayout, QVBoxLayout
from PyQt6.QtGui import QTextCursor
from PyTeXEditor.document_elements import Block
from PyTeXEditor.element_ui import CONVERT


class Sidebar(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_widgets: list[Union[QWidget, QBoxLayout, None]] = []
        self.setObjectName("Sidebar")
        self.box = QVBoxLayout()
        self.setLayout(self.box)
        self.box.addStretch(1)

    def clear(self) -> None:
        """Clears the sidebar of all widgets
        """
        for element in self.current_widgets:
            if isinstance(element, QWidget):
                self.box.removeWidget(element)
            if isinstance(element, QBoxLayout):
                c = element.itemAt(0)
                while c:
                    element.removeWidget(element.itemAt(0).widget())
                    c = element.itemAt(0)
                self.box.removeItem(element)
        self.current_widgets = []

    def recieve_selection(self, cursor: QTextCursor,
                          block_type: Type[Block]) -> None:
        """Recieves the selected element.

        Parameters
        ----------
        cursor : QTextCursor
            The cursor.
        block_type : Type[Block]
            The type of document element that is selected.
        """
        self.clear()
        for property in block_type.properties:
            ui_element = CONVERT[property](cursor)
            if isinstance(ui_element, QBoxLayout):
                self.box.insertLayout(0, ui_element)
            else:
                self.box.insertWidget(0, ui_element)
            self.current_widgets.append(ui_element)

        self.setHidden(False)
