from src.application.dto.selector_output_file import SelectorOutputFile
from src.domain.gateway.file_selector import FileSelector


class FileSelectorUseCase:
    def __init__(self,file_selector:FileSelector ) -> None:
        self.__file_selector = file_selector
    
    def select(self)-> list[SelectorOutputFile]:
        output_file:list[SelectorOutputFile] = []
        paths = self.__file_selector.select()
        
        for path in paths:
            output_file.append(SelectorOutputFile(path.get_value()))
        
        return output_file