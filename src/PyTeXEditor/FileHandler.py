from pathlib import Path
from os import access, linesep, R_OK, W_OK


class FileHandler:
    def __init__(self, file_path: Path):

        self.file_created = False
        self.file_path = self.__resolve_file(file_path)

    def __resolve_file(self, input_path: Path) -> Path:
        """Resolves the given path

        Parameters
        ----------
        input_path : Path
            _description_

        Returns
        -------
        Path
            _description_

        Raises
        ------
        IsADirectoryError
            _description_
        ValueError
            _description_
        """
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

    def __read_file(self) -> list[str]:
        with open(self.file_path, "r") as file:
            return file.readlines()

    def __write_file(self, data: list[str]) -> None:
        data = [line + linesep for line in data]

        with open(self.file_path, "w") as file:
            file.writelines(data)


if __name__ == "__main__":
    # a = FileHandler("/home/maciej/unreadable")
    b = FileHandler(Path("/home/maciej/a/readable2"))
