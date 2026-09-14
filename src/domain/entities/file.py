import os

from src.domain.valuesobject.path import Path
from src.domain.valuesobject.type import Type


class File:
    _OUTPUT_EXTENSIONS = {
        "PDF": ".pdf",
        "JPEG": ".jpg",
        "PNG": ".png",
    }

    def __init__(self, path_input: Path, path_output: Path, output_type: Type) -> None:
        self.__path_input = path_input
        self.__path_output = path_output
        self.__output_type = output_type

    def get_path_input(self) -> str:
        return self.__path_input.get_value()

    def get_file_type(self) -> str:
        return self.__output_type.get_value()

    def get_input_extension(self) -> str:
        return os.path.splitext(self.get_path_input())[1].lower()

    def is_input_pdf(self) -> bool:
        return self.get_input_extension() == ".pdf"

    def get_path_full_output(self) -> str:
        if self.get_file_type() == "PDF":
            return self.__path_output.get_value()

        extension = self._OUTPUT_EXTENSIONS.get(self.get_file_type())
        if not extension:
            raise ValueError("Formato de saída não suportado.")

        basename = os.path.basename(self.get_path_input())
        name = os.path.splitext(basename)[0]
        candidate = os.path.join(
            self.__path_output.get_value(),
            f"{name}_convertido{extension}",
        )
        return self.__next_available_path(candidate)

    @staticmethod
    def __next_available_path(candidate: str) -> str:
        if not os.path.exists(candidate):
            return candidate

        directory, filename = os.path.split(candidate)
        name, extension = os.path.splitext(filename)
        index = 2

        while True:
            alternative = os.path.join(directory, f"{name}_{index}{extension}")
            if not os.path.exists(alternative):
                return alternative
            index += 1
