import re


regex = re.compile(r"((?!\\n)\\\w*(?:\[\w*\])*(?:\{.*\})*(?:\s*\n?)*)")


def delete_comments(line: str) -> str:
    return line.split("%")[0]


def seperate(lines: list[str]) -> list[str]:
    print(lines)
    # output = re.split(r"(\\[\w\s\[\]\{\}]*)", " ".join(lines))
    for i, _ in enumerate(lines):
        lines[i] = delete_comments(lines[i])

    output = regex.split(" ".join(lines))
    print(output)

    i = 0
    while (i < len(output)):
        current_split = re.split(r"(.*)\s*\n\s*\n\s*(.*)", output[i])
        if len(output) > 1:
            print(current_split)
        output[i] = current_split[0]
        output = output[:i] + current_split[1:] + output[i:]

        # output[i] = re.sub(r"\n\s*\n\s*", r"", output[i])
        output[i] = re.sub(r"\n\s*", r"", output[i])
        i += 1

    output = list(filter(lambda x: x != "\n", output))
    output = list(filter(None, output))

    print(output)

    return output
