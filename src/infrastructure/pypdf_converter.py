import os
from collections.abc import Callable
from io import BytesIO

from PIL import Image, ImageSequence, UnidentifiedImageError
from pypdf import PdfReader, PdfWriter

from src.domain.entities.file import File
from src.domain.gateway.pdf_converter import PDFConverter


class PyPDFConverter(PDFConverter):
    def convert_and_save(
        self,
        files: list[File],
        progress: Callable[[int], None],
    ) -> None:
        if not files:
            raise ValueError("Nenhum arquivo foi informado para gerar o PDF.")

        writer = PdfWriter()
        image_buffers: list[BytesIO] = []

        try:
            for index, file in enumerate(files, start=1):
                if file.is_input_pdf():
                    self.__append_pdf(writer, file.get_path_input())
                else:
                    buffer = self.__image_to_pdf(file.get_path_input())
                    image_buffers.append(buffer)
                    self.__append_reader(writer, PdfReader(buffer))

                progress(index)

            if len(writer.pages) == 0:
                raise ValueError("Não há páginas válidas para gerar o PDF.")

            output_path = files[0].get_path_full_output()
            output_directory = os.path.dirname(output_path)
            if output_directory:
                os.makedirs(output_directory, exist_ok=True)

            with open(output_path, "wb") as output_file:
                writer.write(output_file)
        finally:
            for buffer in image_buffers:
                buffer.close()

    @staticmethod
    def __append_pdf(writer: PdfWriter, path: str) -> None:
        try:
            reader = PdfReader(path)

            if reader.is_encrypted:
                result = reader.decrypt("")
                if result == 0:
                    raise ValueError(
                        f"O PDF está protegido por senha e não pode ser combinado: {path}"
                    )

            PyPDFConverter.__append_reader(writer, reader)
        except ValueError:
            raise
        except Exception as error:
            raise ValueError(f"Não foi possível ler o PDF: {path}") from error

    @staticmethod
    def __append_reader(writer: PdfWriter, reader: PdfReader) -> None:
        for page in reader.pages:
            writer.add_page(page)

    @staticmethod
    def __image_to_pdf(path: str) -> BytesIO:
        try:
            with Image.open(path) as image:
                frames = [
                    PyPDFConverter.__to_rgb(frame.copy())
                    for frame in ImageSequence.Iterator(image)
                ]
        except UnidentifiedImageError as error:
            raise ValueError(
                f"Formato de arquivo não suportado: {path}"
            ) from error

        if not frames:
            raise ValueError(f"A imagem não contém páginas válidas: {path}")

        buffer = BytesIO()
        frames[0].save(
            buffer,
            format="PDF",
            save_all=True,
            append_images=frames[1:],
        )
        buffer.seek(0)
        return buffer

    @staticmethod
    def __to_rgb(image: Image.Image) -> Image.Image:
        if image.mode in ("RGBA", "LA") or "transparency" in image.info:
            rgba = image.convert("RGBA")
            background = Image.new("RGB", rgba.size, "white")
            background.paste(rgba, mask=rgba.getchannel("A"))
            return background

        return image.convert("RGB")
