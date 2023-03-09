from typing import Type
from PyQt6.QtGui import QTextBlockUserData


class UserData(QTextBlockUserData):

    __slots__ = ["type"]

    def __init__(self, element_type: Type):
        self.type = element_type
