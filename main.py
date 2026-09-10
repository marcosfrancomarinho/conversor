import sys
import tkinter as tk
from pathlib import Path

from src.application.usecase.file_converter_usecase import FileConverterUseCase
from src.application.usecase.file_selector_usecase import FileSelectorUseCase
from src.infrastructure.pillow_image_converter import PillowImageConverter
from src.infrastructure.pypdf_converter import PyPDFConverter
from src.infrastructure.tk_file_save_location_selector import TkFileSaveLocationSelector
from src.infrastructure.tk_file_selector import TkFileSelector
from src.presentation.tk_app import ConverterApp


def resource_path(filename: str) -> str:
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return str(base_path / filename)


def main() -> None:
    root = tk.Tk()

    try:
        root.iconbitmap(resource_path("icone.ico"))
    except tk.TclError:
        pass

    file_selector = TkFileSelector()
    save_location_selector = TkFileSaveLocationSelector()
    image_converter = PillowImageConverter()
    pdf_converter = PyPDFConverter()

    file_selector_usecase = FileSelectorUseCase(file_selector)
    file_converter_usecase = FileConverterUseCase(
        image_converter=image_converter,
        pdf_converter=pdf_converter,
    )

    ConverterApp(
        root=root,
        file_selector_usecase=file_selector_usecase,
        file_converter_usecase=file_converter_usecase,
        save_location_selector=save_location_selector,
    )
    root.mainloop()


if __name__ == "__main__":
    main()
