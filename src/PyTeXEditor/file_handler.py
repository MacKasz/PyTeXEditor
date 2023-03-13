from pathlib import Path
from os import access, R_OK, W_OK
from PyTeXEditor.latex_document import LatexDocument


class FileHandler:

    def __init__(self):

        self.file_created = False
        self.doc = LatexDocument()

    def __resolve_file(self, input_path: Path) -> Path:
        # Resolve path
        output_path = input_path.absolute()

        if output_path.is_dir():
            raise IsADirectoryError(f"{output_path} is a dir, not a file")

        # Check if its a file
        if not output_path.is_file():
            try:
                output_path.touch(0o664, True)
            except PermissionError as e:
                raise e

        # Can only test this offline
        if not (access(output_path, R_OK) or
                access(output_path, W_OK)):  # pragma: no cover
            raise PermissionError(f"{output_path} cannot be read or written to")

        if output_path.is_symlink():
            output_path = output_path.resolve()

        return output_path

    def set_path(self, path: Path) -> None:
        self.file_path = self.__resolve_file(path)

    def read_file(self) -> None:
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        self.doc.plain_text = lines

    def write_file(self) -> None:

        stack = self.doc.big_brain_traverse()

        with open(self.file_path, "w") as file:
            for node in stack:
                if isinstance(node, str):
                    output = r"\end{" + node + r"}" + "\n"
                    file.write(output)
                    continue
                file.write(node.data.to_tex())
