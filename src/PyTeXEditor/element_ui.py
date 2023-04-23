from typing import Callable, Union
from PyTeXEditor.document_elements import ElementProperties
from PyQt6.QtWidgets import (
    QComboBox,
    QWidget,
    QSpinBox,
    QPushButton,
    QHBoxLayout,
    QBoxLayout
)
from PyQt6.QtGui import QTextCursor, QFontDatabase, QFont


def __font_box(cursor: QTextCursor) -> QWidget:

    fonts = QFontDatabase.families()

    def change_font(index: int,
                    cursor: QTextCursor) -> None:  # pragma: no cover
        current = cursor.charFormat()
        current.setFont(QFont(fonts[index]))
        cursor.setCharFormat(current)

    output = QComboBox()
    output.setObjectName("FontFamily")
    output.addItems(fonts)

    try:
        current_font = cursor.blockCharFormat().font().family()
        output.setCurrentIndex(fonts.index(current_font))
    except ValueError:
        pass

    output.activated.\
        connect(lambda index: change_font(index, cursor))  # type: ignore
    return output


def __style(cursor: QTextCursor) -> Union[QWidget, QBoxLayout]:

    output = []
    output.append(QPushButton("Bold"))
    output[0].setObjectName("BoldBox")
    output.append(QPushButton("Italic"))
    output[1].setObjectName("ItalicBox")
    output.append(QPushButton("Underline"))
    output[2].setObjectName("UnderlineBox")

    def bold(cursor: QTextCursor):  # pragma: no cover
        current = cursor.charFormat()
        current.setFontWeight(QFont.Weight.Bold)
        cursor.setCharFormat(current)

    def italic(cursor: QTextCursor):  # pragma: no cover
        current = cursor.charFormat()
        current.setFontItalic(True)
        cursor.setCharFormat(current)

    def underline(cursor: QTextCursor):  # pragma: no cover
        current = cursor.charFormat()
        current.setFontUnderline(True)
        cursor.setCharFormat(current)

    output[0].clicked.\
        connect(lambda: bold(cursor))  # type: ignore
    output[1].clicked.\
        connect(lambda: italic(cursor))  # type: ignore
    output[2].clicked.\
        connect(lambda: underline(cursor))  # type: ignore

    hsplit = QHBoxLayout()
    hsplit.addWidget(output[0])
    hsplit.addWidget(output[1])
    hsplit.addWidget(output[2])

    return hsplit


def __size_box(cursor: QTextCursor) -> QWidget:

    def change_size(size: int, cursor: QTextCursor) -> None:  # pragma: no cover
        current = cursor.charFormat()
        current.setFontPointSize(size)
        cursor.setCharFormat(current)

    current_size = cursor.blockCharFormat().font().pointSize()
    output = QSpinBox()
    output.setObjectName("FontSize")
    output.setSuffix("pt")
    output.setValue(current_size)
    output.valueChanged.\
        connect(lambda size: change_size(size, cursor))  # type: ignore
    return output


CONVERT: dict[ElementProperties,
              Callable[[QTextCursor], Union[QWidget, QBoxLayout]]] = {
    ElementProperties.FontSize: __size_box,
    ElementProperties.FontFamily: __font_box,
    ElementProperties.Styled: __style,
}
