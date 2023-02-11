from pathlib import Path
from os import access, linesep, R_OK, W_OK
from PyTeXEditor.latex_document import LatexDocument
import logging


class FileHandler:
    def __init__(self, file_path: Path):

        self.file_created = False
        self.file_path = self.__resolve_file(file_path)
        self.doc = LatexDocument()

    def __resolve_file(self, input_path: Path) -> Path:
        # Resolve path
        output_path = input_path.absolute()

        if not (access(output_path, R_OK) or access(output_path, W_OK)):
            raise PermissionError(f"{output_path} cannot be read or written to")

        if output_path.is_symlink():
            output_path = output_path.resolve()

        # Check if its a file
        if output_path.is_file():
            self.file_created = True
        else:
            if output_path.is_dir():
                raise IsADirectoryError(f"{output_path} is a dir, not a file")

            output_path.touch()

        return output_path

    def read_file(self) -> None:
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        self.doc.plain_text = lines

    def convert(self) -> None:
        self.doc.plain_to_tex()

    def __write_file(self, data: list[str]) -> None:
        data = [line + linesep for line in data]

        with open(self.file_path, "w") as file:
            file.writelines(data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # a = FileHandler("/home/maciej/unreadable")
    b = FileHandler(Path("/mnt/Media/Dev/PyTeXEditor/resources/good_document.tex"))
    b.read_file()
    b.convert()
    for node in b.doc.object_tree.preorder_traverse():
        print(f"{type(node.data)}: s'{node.data.data}'e")


if __name__ == "__main__":
    a = FileHandler(Path("/mnt/Media/Dev/PyTeXEditor/resources/linked_document.tex"))
    print(a.file_path)
