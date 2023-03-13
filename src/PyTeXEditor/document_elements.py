from typing import Dict, Pattern, Type
from enum import Enum
from abc import ABC, abstractmethod
import re


class IncludeTerminator(Enum):
    BEFORE = 1   # Seperate before the terminator
    INCLUDE = 2


class Block(ABC):

    __slots__ = ["options", "data", "initiator", "include_type", "terminator"]
    data: str
    initiator: Pattern[str]
    include_type: IncludeTerminator
    terminator: Pattern[str]

    def __init__(self) -> None:
        self.options: Dict[str, str] = dict()
        self.data = ""

    @abstractmethod
    def process_data(self, data: str) -> None:
        """Processes the dat for the element.

        Parameters
        ----------
        data : str
            The data to process
        """
        pass

    @abstractmethod
    def to_plain(self) -> str:
        """Gives the element as plain text.

        Returns
        -------
        str
            The plaintext.
        """
        pass

    @abstractmethod
    def to_tex(self) -> str:
        """Gives the element as LaTeX text.

        Returns
        -------
        str
            The LaTeX text.
        """
        pass


class Environment(Block):

    __slots__ = ["name"]
    name: str

    pass


class TerminalMacro(Block):

    pass


class Document(Environment):
    name = "document"
    initiator = re.compile(r"\\begin\{document\}")
    include_type = IncludeTerminator.INCLUDE
    terminator = re.compile(r"\\end\{document\}")

    def process_data(self, data: str) -> None:
        pass

    def to_plain(self) -> str:
        return ""

    def to_tex(self) -> str:
        return r"\begin{document}" + "\n"


class Itemize(Environment):
    name = "itemize"
    initiator = re.compile(r"\\begin\{itemize\}")
    terminator = re.compile(r"\\end\{itemize\}")
    include_type = IncludeTerminator.INCLUDE

    def process_data(self, data: str) -> None:
        pass

    def to_plain(self) -> str:
        return ""

    def to_tex(self) -> str:
        return r"\begin{itemize}" + "\n"


class Item(TerminalMacro):

    __points = ["•", "-", "∗", "∙"]
    initiator = re.compile(r"\\item")
    terminator = re.compile(r".")
    include_type = IncludeTerminator.INCLUDE

    def process_data(self, data: str) -> None:
        pass

    def to_plain(self) -> str:
        return f"{self.__points[0]} "

    def to_tex(self) -> str:
        return r"\item "


class Text(TerminalMacro):

    initiator = re.compile(r"^[^\\]+$")
    terminator = re.compile(r".*")
    include_type = IncludeTerminator.BEFORE

    def process_data(self, data: str) -> None:
        self.data = data

    def to_plain(self) -> str:
        return f"{self.data}\n"

    def to_tex(self) -> str:
        return f"{self.data}\n"


# TODO make this automatic
ENVIRONMENTS: list[Type[Environment]] = [
    Document,
    Itemize,
]


MACROS: list[Type[TerminalMacro]] = [
    Text,
    Item,
]
