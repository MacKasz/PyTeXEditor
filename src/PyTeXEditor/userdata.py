from typing import Type
from PyQt6.QtGui import QTextBlockUserData
from PyTeXEditor.document_elements import Block


class UserData(QTextBlockUserData):

    __slots__ = ["type"]

    def __init__(self, block_type: Type[Block], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = block_type
