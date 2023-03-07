from PyTeXEditor.latex_document import LatexDocument
from typing import Generator
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import (
    QPalette,
    QColor,
    QTextBlock,
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

    def get_blocks(self) -> Generator[QTextBlock, None, None]:
        for i in range(self.document().blockCount()):
            yield self.document().findBlock(i)

    def set_document(self, doc: LatexDocument) -> None:
        doc.internal_to_qt()
        self.setDocument(doc)

    def __send_selection(self) -> None:
        cursor = self.textCursor()
        print(f"{cursor.selectionStart()} - {cursor.selectionEnd()}")
