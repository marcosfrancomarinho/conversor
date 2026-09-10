import os
import tempfile
import unittest

from PIL import Image
from pypdf import PdfReader, PdfWriter

from src.domain.entities.file import File
from src.domain.valuesobject.path import Path
from src.domain.valuesobject.type import Type
from src.infrastructure.pypdf_converter import PyPDFConverter


class PyPDFConverterTest(unittest.TestCase):
    def test_combines_images_and_pdf_preserving_order_and_all_pages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first_image = os.path.join(directory, "capa.png")
            middle_pdf = os.path.join(directory, "contrato.pdf")
            last_image = os.path.join(directory, "comprovante.jpg")
            output = os.path.join(directory, "resultado.pdf")

            Image.new("RGB", (100, 100), "white").save(first_image)
            Image.new("RGB", (120, 80), "white").save(last_image)

            source_writer = PdfWriter()
            source_writer.add_blank_page(width=100, height=100)
            source_writer.add_blank_page(width=100, height=100)
            with open(middle_pdf, "wb") as pdf_file:
                source_writer.write(pdf_file)

            files = [
                File(Path(first_image), Path(output), Type("PDF")),
                File(Path(middle_pdf), Path(output), Type("PDF")),
                File(Path(last_image), Path(output), Type("PDF")),
            ]
            progress: list[int] = []

            PyPDFConverter().convert_and_save(files, progress.append)

            self.assertEqual(len(PdfReader(output).pages), 4)
            self.assertEqual(progress, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
