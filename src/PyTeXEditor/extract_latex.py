import re


regex = re.compile(r"((?!\\n)\\\w*(?:\[\w*\])*(?:\{.*\})*(?:\s*\n?)*)")


def delete_comments(line: str) -> str:
    return line.split("%")[0]


def seperate(lines: list[str]) -> list[str]:

    for i, _ in enumerate(lines):
        lines[i] = delete_comments(lines[i])

    # Join all lines together
    output = regex.split(" ".join(lines))

    i = 0
    while (i < len(output)):
        current_split = re.split(r"(.*)\s*\n\s*\n\s*(.*)", output[i])

        # Some new line fixing
        output[i] = current_split[0]
        output = output[:i] + current_split[1:] + output[i:]

        # Remove single newline elements
        output[i] = re.sub(r"\n\s*", r"", output[i])
        i += 1

    # Filter out Empty lines
    output = list(filter(lambda x: x != "\n", output))
    output = list(filter(None, output))

    print(output)

    return output
