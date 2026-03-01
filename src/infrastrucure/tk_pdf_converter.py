from src.domain.entities.file import File
from src.domain.gateway.pdf_converter import PDFConverter
from PIL import Image

class TkPDFConverter(PDFConverter):
    def convert_and_save(self, files: list[File]) -> None:
        imagens_pdf: list[Image.Image] = []
        
        for file in files:
            with Image.open(file.get_path_input()) as img:
                img.load()
                imagens_pdf.append(img.convert("RGB").copy())
                
        
        imagens_pdf[0].save(
            files[0].get_path_full_output(),
            save_all=True,
            append_images=imagens_pdf[1:]
        )
        
        
        