from tkinter import filedialog
from src.domain.gateway.file_selector import FileSelector
from src.domain.valuesobject.path import Path


class TkFileSelector(FileSelector):
    
    def select(self) -> list[Path]:
        paths:list[Path] = []
        files = filedialog.askopenfilenames(
            title="Selecione os arquivos",
            filetypes=[("Todos os arquivos", "*")]
        )
        for file in files:
            paths.append(Path(file))
        
        return paths
        
        
        