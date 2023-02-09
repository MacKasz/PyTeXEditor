from typing import Pattern
import re


keyword_patterns: list[Pattern[str]] = [
    re.compile(r"(\\begin\{[a-zA-Z0-9]+\}(?:\[.*\])*)\s?"),
    re.compile(r"(\\end\{[a-zA-Z0-9]+\})\s?"),
    re.compile(r"(\\(?!begin)(?!end)(?:[a-z]*)(?:\[.*\])*(?:\{.*\})*)\s?"),
]


def delete_comments(line: str) -> str:
    return line.split("%")[0]


def seperate(line: str) -> list[str]:
    output = [line]
    for regex in keyword_patterns:
        working: list[str] = []
        for word in output:
            working += regex.split(word)
            working = list(filter(None, working))
        output = working

    return list(filter(None, output))


if __name__ == "__main__":
    text = r"""
    \begin{environ}[option] asd
    \begin{itemize}
        \item asd
        \item asd
    \end{itemize}
    """
    print(seperate(text))
