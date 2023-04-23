from typing import Tuple, Type
from PyTeXEditor.latex_document import LatexDocument
from PyTeXEditor.document_elements import Block, Text
from PyTeXEditor.userdata import UserData
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import (
    QPalette,
    QColor,
    QTextCursor
)


class TextEdit(QtWidgets.QTextEdit):

    sidebar_visable_signal = pyqtSignal(bool)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        super().setObjectName("TextEdit")
        self.setDocument(LatexDocument())
        self.__set_style()

    def __set_style(self) -> None:
        """Sets the TextEdit style.
        """
        temp = self.palette()
        temp.setColor(QPalette.ColorGroup.All,
                      QPalette.ColorRole.Base,
                      QColor.fromRgb(255, 255, 255))
        temp.setColor(QPalette.ColorGroup.All,
                      QPalette.ColorRole.Text,
                      QColor.fromRgb(0, 0, 0))
        self.setPalette(temp)

    def set_document(self, doc: LatexDocument) -> None:
        doc.internal_to_qt()
        self.setDocument(doc)

    def get_selected_element(self) -> Tuple[QTextCursor, Type[Block]]:
        cursor = self.textCursor()
        block = cursor.block()
        userdata = block.userData()
        if not userdata:
            block_type: Type[Block] = Text
        else:
            if not isinstance(userdata, UserData):
                raise TypeError()
            block_type = userdata.type

        return (cursor, block_type)
