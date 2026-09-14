import os
from tkinter import filedialog

from src.domain.gateway.file_save_location_selector import FileSaveLocationSelector
from src.domain.valuesobject.type import Type


class TkFileSaveLocationSelector(FileSaveLocationSelector):
    def select(self, output_type: Type, suggested_path: str) -> str | None:
        if output_type.get_value() == "PDF":
            initial_dir = os.path.dirname(suggested_path)
            initial_file = os.path.basename(suggested_path)

            selected = filedialog.asksaveasfilename(
                title="Alterar destino do PDF",
                initialdir=initial_dir,
                initialfile=initial_file,
                defaultextension=".pdf",
                filetypes=[("Arquivo PDF", "*.pdf")],
            )
            return selected or None

        selected = filedialog.askdirectory(
            title="Alterar pasta de destino",
            initialdir=suggested_path,
        )
        return selected or None
