from PyQt6.QtGui import QTextBlockUserData
from typing import Dict, Tuple, Pattern, Type
from enum import Enum
from abc import ABC, abstractmethod, abstractproperty
import re


class BlockData(QTextBlockUserData):

    __slots__ = ["block_type"]

    def __init__(self, type: Type['Block']) -> None:
        self.block_type = type


class IncludeTerminator(Enum):
    BEFORE = 1   # Seperate before the terminator
    INCLUDE = 2


class Block(ABC):

    __slots__ = ["options", "data"]

    def __init__(self) -> None:
        self.options: Dict[str, str] = dict()
        self.data = ""

    @abstractproperty
    def terminator(self) -> Pattern[str]:
        """A regex pattern to match a terminator.
        """
        return re.compile(r"\\")

    @abstractproperty
    def include_type(self) -> IncludeTerminator:
        """Whether the terminator should be included.
        """
        return IncludeTerminator.BEFORE

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

    pass


class TerminalMacro(Block):

    pass


class Document(Environment):

    @property
    def terminator(self) -> Pattern[str]:
        return re.compile(r"\\end\{document\}")

    @property
    def include_type(self) -> IncludeTerminator:
        return IncludeTerminator.INCLUDE

    def process_data(self, data: str) -> None:
        pass

    def to_plain(self) -> str:
        return ""

    def to_tex(self) -> str:
        raise NotImplementedError


class Itemize(Environment):
    @property
    def terminator(self) -> Pattern[str]:
        return re.compile(r"\\end\{itemize\}")

    @property
    def include_type(self) -> IncludeTerminator:
        return IncludeTerminator.INCLUDE

    def process_data(self, data: str) -> None:
        pass

    def to_plain(self) -> str:
        return ""

    def to_tex(self) -> str:
        raise NotImplementedError


class Item(TerminalMacro):

    points = ["•", "-", "∗", "∙"]

    @property
    def terminator(self) -> Pattern[str]:
        return re.compile(r"\\item|\\end\{itemize\}")

    @property
    def include_type(self) -> IncludeTerminator:
        return IncludeTerminator.BEFORE

    def process_data(self, data: str) -> None:
        pass

    def to_plain(self) -> str:
        return self.points[0]

    def to_tex(self) -> str:
        raise NotImplementedError


class Text(TerminalMacro):

    @property
    def terminator(self) -> Pattern[str]:
        return re.compile(r"\\")

    @property
    def include_type(self) -> IncludeTerminator:
        return IncludeTerminator.BEFORE

    def process_data(self, data: str) -> None:
        self.data = data

    def to_plain(self) -> str:
        return self.data

    def to_tex(self) -> str:
        raise NotImplementedError


def get_env_regex(environment: str) -> Tuple[Pattern[str], Pattern[str]]:
    begin = r"\\begin\{" + str(environment) + r"\}(?:\[.*\])*"
    end = r"\\end\{" + str(environment) + r"\}"
    return re.compile(begin), re.compile(end)


ENVIRONMENTS: Dict[str, Type[Block]] = {
    "document": Document,
    "itemize": Itemize,
}


MACROS: Dict[Type[Block], Pattern[str]] = {
    Text: re.compile(r"^[^\\]+$"),
    Item: re.compile(r"\\item"),
}
