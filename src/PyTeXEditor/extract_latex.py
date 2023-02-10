import re


# regex = re.compile(r"((?!\\n)\\\w*(?:\[\w*\])*(?:\{\w*\})*)")
regex = re.compile(r"((?!\\n)\\\w*(?:\[\w*\])*(?:\{.*\})*(?:\s*\n?)*)")


def delete_comments(line: str) -> str:
    return line.split("%")[0]


def seperate(lines: list[str]) -> list[str]:
    # output = re.split(r"(\\[\w\s\[\]\{\}]*)", " ".join(lines))
    output = regex.split(" ".join(lines))

    i = 0
    while i < len(output):
        output[i] = delete_comments(output[i])
        i += 1
    output = list(filter(lambda x: x != "\n", output))

    return list(filter(None, output))
