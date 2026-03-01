import os
import random
from src.domain.valuesobject.path import Path
from src.domain.valuesobject.type import Type


class File:
    
    __count_file:int = 0
    
    @staticmethod
    def reset_count()->None:
        File.__count_file = 0
    
    @staticmethod
    def get_count_file()->int:
        return File.__count_file
    
    def __init__(self, path_input:Path, path_output:Path, type:Type) -> None:
        self.__path_input = path_input
        self.__path_output = path_output
        self.__type = type
        File.__count_file += 1
        
    def __get_file_extension(self)-> str:
        file_type= self.__type.get_value()
        formats = {
            "PDF":".pdf",
            "JPEG":".jpg",
            "PNG":".png"
        }
        extension = formats.get(file_type)
        if not extension:
            raise Exception("formato do documento  não foi definido")
        return extension
    
    def get_path_input(self)->str:
        return self.__path_input.get_value()
    
    def get_file_type(self)->str:
        return self.__type.get_value()
    
    def is_pdf(self)->bool:
        return self.__type.get_value() == "PDF"
    
    def get_path_full_output(self)->str:
        if self.__path_output.get_value().endswith(".pdf"):
            return self.__path_output.get_value()
        
        basename = os.path.basename(self.__path_input.get_value())
        name = os.path.splitext(basename)[0]
        number_random = random.randint(100000,999999)
        path = os.path.join(self.__path_output.get_value(), f"{name}_{number_random}{self.__get_file_extension()}")
        return path
            