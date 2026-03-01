from typing import Callable

from src.application.dto.selector_output_file import SelectorOutputFile


class ConverterInputFile:
    def __init__(self, type:str, files_input:list[SelectorOutputFile], progress:Callable[[int], None]) -> None:
        self.type = type
        self.files_input = files_input
        self.progress = progress
