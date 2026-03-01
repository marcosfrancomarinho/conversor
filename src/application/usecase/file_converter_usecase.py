from src.application.dto.converter_input_file import ConverterInputFile
from src.application.dto.converter_output_file import ConverterOutputFile
from src.domain.entities.file import File
from src.domain.gateway.image_converter import ImageConverter
from src.domain.gateway.pdf_converter import PDFConverter
from src.domain.valuesobject.path import Path
from src.domain.valuesobject.type import Type
from src.domain.gateway.file_save_location_selector import FileSaveLocationSelector

class FileConverterUseCase:
    def __init__(
        self,
        image_converter:ImageConverter,
        pdf_converter:PDFConverter,
        file_save_location_selector:FileSaveLocationSelector
        ) -> None:
        self.__image_converter = image_converter
        self.__pdf_converter = pdf_converter
        self.__file_save_location_selector = file_save_location_selector
    
    def converter(self, input:ConverterInputFile)->ConverterOutputFile:
        File.reset_count()
        file_type = Type(input.type)
        pdf_files:list[File] = []
        path_output = self.__file_save_location_selector.select(file_type)
        
        for index, file in enumerate(input.files_input):
            input.progress(index + 1)
            path_input = Path(file.path)
            file = File(path_input, path_output, file_type)
            if  file.is_pdf():
                pdf_files.append(file)
                continue
            self.__image_converter.convert_and_save(file)
            
        if pdf_files:
            self.__pdf_converter.convert_and_save(pdf_files)
            return ConverterOutputFile(quantity=len(pdf_files))
        
        return ConverterOutputFile(quantity=File.get_count_file())
        
        
            
            
            
            
                
            
        
            
            
        
        
            