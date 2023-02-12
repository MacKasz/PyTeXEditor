from typing import Dict, Tuple, Pattern, Type
from enum import Enum
from abc import ABC, abstractmethod
import re


class BlockType(Enum):
    ENV = 1
    TERMINAL_MACRO = 3
    NON_TERMINAL_MACRO = 4


class IncludeTerminator(Enum):
    BEFORE = 1  # Seperate before the terminator
    INCLUDE = 2  #


class Block(ABC):

    __slots__ = ["options", "data"]

    def __init__(self) -> None:
        self.options: Dict[str, str] = dict()
        self.data = ""

    @abstractmethod
    def starter(self) -> Pattern[str]:
        pass

    @abstractmethod
    def terminator(self) -> Pattern[str]:
        pass

    @abstractmethod
    def include_type(self) -> IncludeTerminator:
        pass

    @abstractmethod
    def set_data(self, data: str) -> None:
        pass

    def set_option(self, key: str, value: str) -> None:
        self.options.update({key: value})

    def set_options(self, option_list: Dict[str, str]) -> None:
        for key, value in option_list.items():
            self.options.update({key: value})

    @abstractmethod
    def process_options(self, raw_options: list[str]) -> None:
        pass


class Environment(Block):

    pass


class TerminalMacro(Block):

    pass


class NonTerminalMacro(Block):
    pass


class Document(Environment):
    def starter(self) -> Pattern[str]:
        return re.compile(r"\\begin\{document\}")

    def terminator(self) -> Pattern[str]:
        return re.compile(r"\\end\{document\}")

    def include_type(self) -> IncludeTerminator:
        return IncludeTerminator.INCLUDE

    def set_data(self, data: str) -> None:
        pass

    def process_options(self, raw_options: list[str]) -> None:
        pass


class Itemize(Environment):
    def __init__(self) -> None:
        super().__init__()

    def starter(self) -> Pattern[str]:
        return re.compile(r"\\begin\{itemize\}")

    def terminator(self) -> Pattern[str]:
        return re.compile(r"\\end\{itemize\}")

    def include_type(self) -> IncludeTerminator:
        return IncludeTerminator.INCLUDE

    def set_data(self, data: str) -> None:
        pass

    def process_options(self, raw_options: list[str]) -> None:
        pass


class Item(TerminalMacro):
    def __init__(self) -> None:
        super().__init__()

    def starter(self) -> Pattern[str]:
        return re.compile(r"\\item")

    def terminator(self) -> Pattern[str]:
        return re.compile(r"\\item|\\end\{itemize\}")

    def include_type(self) -> IncludeTerminator:
        return IncludeTerminator.BEFORE

    def set_data(self, data: str) -> None:
        pass

    def process_options(self, raw_options: list[str]) -> None:
        pass


class Text(TerminalMacro):
    def __init__(self) -> None:
        self.data: str = ""

    def set_text(self, text: str) -> None:
        self.data = text

    def to_latex(self) -> str:
        return "test"

    def starter(self) -> Pattern[str]:
        return re.compile(r"^[^\\]+$")

    def terminator(self) -> Pattern[str]:
        return re.compile(r"\\")

    def include_type(self) -> IncludeTerminator:
        return IncludeTerminator.BEFORE

    def set_data(self, data: str) -> None:
        self.data = data

    def process_options(self, raw_options: list[str]) -> None:
        pass


ENVIRONMENTS: Dict[str, Type[Block]] = {
    "document": Document,
    "itemize": Itemize,
}


MACROS: Dict[Type[Block], Pattern[str]] = {
    Text: re.compile(r"^[^\\]+$"),
    Item: re.compile(r"\\item"),
}


def get_env_regex(environment: str) -> Tuple[Pattern[str], Pattern[str]]:
    begin = r"\\begin\{" + str(environment) + r"\}(?:\[.*\])*"
    end = r"\\end\{" + str(environment) + r"\}"
    return re.compile(begin), re.compile(end)
