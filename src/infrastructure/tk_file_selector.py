from tkinter import filedialog

from src.domain.gateway.file_selector import FileSelector
from src.domain.valuesobject.path import Path


class TkFileSelector(FileSelector):
    def select(self) -> list[Path]:
        files = filedialog.askopenfilenames(
            title="Selecione imagens e PDFs",
            filetypes=[
                (
                    "Imagens, PDFs e arquivos numerados",
                    "*.*",
                ),
                ("PDF", "*.pdf"),
                (
                    "Imagens comuns",
                    "*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tif *.tiff",
                ),
            ],
        )
        return [Path(file) for file in files]
