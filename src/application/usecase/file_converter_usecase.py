import os

from src.application.dto.converter_input_file import ConverterInputFile
from src.application.dto.converter_output_file import ConverterOutputFile
from src.domain.entities.file import File
from src.domain.gateway.image_converter import ImageConverter
from src.domain.gateway.pdf_converter import PDFConverter
from src.domain.valuesobject.path import Path
from src.domain.valuesobject.type import Type


class FileConverterUseCase:
    def __init__(
        self,
        image_converter: ImageConverter,
        pdf_converter: PDFConverter,
    ) -> None:
        self.__image_converter = image_converter
        self.__pdf_converter = pdf_converter

    def converter(self, input_data: ConverterInputFile) -> ConverterOutputFile:
        if not input_data.files_input:
            raise ValueError("Nenhum arquivo foi selecionado.")

        output_type = Type(input_data.output_type)
        output_path = Path(input_data.output_path)

        files = [
            File(
                path_input=Path(file.path),
                path_output=output_path,
                output_type=output_type,
            )
            for file in input_data.files_input
        ]

        if output_type.get_value() == "PDF":
            self.__pdf_converter.convert_and_save(files, input_data.progress)
            return ConverterOutputFile(
                quantity=len(files),
                output_path=output_path.get_value(),
            )

        pdf_inputs = [file.get_path_input() for file in files if file.is_input_pdf()]
        if pdf_inputs:
            raise ValueError(
                "PDFs só podem ser combinados quando o formato de saída é PDF. "
                "Selecione PDF ou remova os PDFs da lista."
            )

        os.makedirs(output_path.get_value(), exist_ok=True)

        for index, file in enumerate(files, start=1):
            self.__image_converter.convert_and_save(file)
            input_data.progress(index)

        return ConverterOutputFile(
            quantity=len(files),
            output_path=output_path.get_value(),
        )
