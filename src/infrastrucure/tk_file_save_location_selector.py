from typing import Optional
from tkinter import filedialog
from src.domain.gateway.file_save_location_selector import FileSaveLocationSelector
from src.domain.valuesobject.path import Path
from src.domain.valuesobject.type import Type


class TKFileSaveLocationSelector(FileSaveLocationSelector):
    
    def select(self, type:Type) -> Path:
        path: Optional[str] = None
        
        if type.get_value() != "PDF":
           path = filedialog.askdirectory(title="Escolha a pasta de destino")
           return Path(path)
       
        path = filedialog.asksaveasfilename(
                title="Salvar PDF como",
                defaultextension=".pdf",
                filetypes=[("Arquivo PDF", "*.pdf")],
                initialfile="documento"
        )
        return Path(path)
        