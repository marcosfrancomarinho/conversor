import os
import tempfile
import unittest

from src.domain.entities.file import File
from src.domain.valuesobject.path import Path
from src.domain.valuesobject.type import Type


class FileTest(unittest.TestCase):
    def test_detects_pdf_from_input_extension(self) -> None:
        file = File(
            path_input=Path("/tmp/contrato.PDF"),
            path_output=Path("/tmp/saida"),
            output_type=Type("PNG"),
        )

        self.assertTrue(file.is_input_pdf())

    def test_image_output_uses_predictable_name_and_avoids_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = os.path.join(directory, "foto.png")
            output_directory = os.path.join(directory, "convertidos")
            os.makedirs(output_directory)

            with open(source, "wb") as source_file:
                source_file.write(b"source")

            existing = os.path.join(output_directory, "foto_convertido.jpg")
            with open(existing, "wb") as existing_file:
                existing_file.write(b"existing")

            file = File(
                path_input=Path(source),
                path_output=Path(output_directory),
                output_type=Type("JPEG"),
            )

            self.assertEqual(
                file.get_path_full_output(),
                os.path.join(output_directory, "foto_convertido_2.jpg"),
            )


if __name__ == "__main__":
    unittest.main()
