from typing import Dict, Pattern, Type
from enum import Enum
from abc import ABC, abstractmethod
import re
import sys
import inspect


class ElementProperties(Enum):
    FontFamily = 1
    FontSize = 2
    Styled = 3
    Heading = 4


class IncludeTerminator(Enum):
    BEFORE = 1   # Seperate before the terminator
    INCLUDE = 2


class Block(ABC):  # pragma: no cover
    """Abstract base class for LaTeX elements

    Attributes
    ----------
    data: str
        The data of the element.
    initiator: Pattern[str]
        How the element is started.
    include_type: IncludeTerminator
        When ending should the terminator be included or excluded in the data.
    terminator: Pattern[str]
        How the element is ended.

    Methods
    -------
    process_data(data)
        Given data process it.
    to_plain()
        Returns the element as plain text.
    to_tex()
        Returns the element as LaTeX.
    """

    __slots__ = ["options", "data", "initiator", "include_type", "terminator",
                 "properties"]
    data: str
    initiator: Pattern[str]
    include_type: IncludeTerminator
    terminator: Pattern[str]
    properties: list[ElementProperties]

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


class Environment(Block):  # pragma: no cover
    """Inherits from Block

    Attributes
    ----------
    name: str
        The name of the environment.
    """

    __slots__ = ["name"]
    name: str

    pass


class TerminalMacro(Block):  # pragma: no cover

    pass


class Document(Environment):
    name = "document"
    initiator = re.compile(r"\\begin\{document\}")
    include_type = IncludeTerminator.INCLUDE
    terminator = re.compile(r"\\end\{document\}")
    properties = []

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
    properties = []

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
    properties = []

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
    properties = [ElementProperties.FontFamily,
                  ElementProperties.FontSize,
                  ElementProperties.Styled]

    def process_data(self, data: str) -> None:
        self.data = data

    def to_plain(self) -> str:
        return f"{self.data}\n"

    def to_tex(self) -> str:
        return f"{self.data}\n\n"


ENVIRONMENTS: list[Type[Environment]] = []
MACROS: list[Type[TerminalMacro]] = []


for name, full_class in inspect.getmembers(sys.modules[__name__],
                                           inspect.isclass):
    if TerminalMacro in full_class.mro() and full_class != TerminalMacro:
        MACROS.append(full_class)
    elif Environment in full_class.mro() and full_class != Environment:
        ENVIRONMENTS.append(full_class)
