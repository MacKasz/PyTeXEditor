from pathlib import Path
from os import access, linesep, R_OK, W_OK
from PyTeXEditor.latex_document import LatexDocument
import logging


class FileHandler:
    log = logging.getLogger("FileHandler")

    def __init__(self):

        self.file_created = False
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

        return output_path

    def set_path(self, path: Path) -> None:
        self.file_path = self.__resolve_file(path)

    def read_file(self) -> None:
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        self.doc.plain_text = lines

    def write_file(self, data: list[str]) -> None:
        # Add the correct line seperator
        data = [line + linesep for line in data]

        with open(self.file_path, "w") as file:
            file.writelines(data)
