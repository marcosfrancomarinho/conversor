
from src.domain.entities.file import File
from src.domain.gateway.image_converter import ImageConverter
from PIL import Image, UnidentifiedImageError

class TkImageConverter(ImageConverter):
    
    def convert_and_save(self, file: File) -> None:
        try:
            with Image.open(file.get_path_input()) as img:
                img.load()
                img.convert(self.__define_mode(file)).save(file.get_path_full_output(), format=file.get_file_type())
        except UnidentifiedImageError:
            raise Exception(f"Ignorado (não é imagem válida): {file.get_path_input()}")
        
    def __define_mode(self,file:File)->str:
        if file.get_file_type() == "JPEG":
            return 'RGB'
        return 'RGBA'