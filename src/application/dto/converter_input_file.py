from collections.abc import Callable

from src.application.dto.selector_output_file import SelectorOutputFile


class ConverterInputFile:
    def __init__(
        self,
        output_type: str,
        files_input: list[SelectorOutputFile],
        output_path: str,
        progress: Callable[[int], None],
    ) -> None:
        self.output_type = output_type
        self.files_input = files_input
        self.output_path = output_path
        self.progress = progress
