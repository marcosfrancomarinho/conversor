import os
import tempfile
import unittest

from PIL import Image

from src.domain.entities.file import File
from src.domain.valuesobject.path import Path
from src.domain.valuesobject.type import Type
from src.infrastructure.pillow_image_converter import PillowImageConverter


class PillowImageConverterTest(unittest.TestCase):
    def test_converts_image_with_numeric_extension_using_file_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = os.path.join(directory, "foto.002")
            output_directory = os.path.join(directory, "convertidos")
            expected_output = os.path.join(output_directory, "foto_convertido.png")

            Image.new("RGB", (80, 60), "white").save(source, format="JPEG")
            os.makedirs(output_directory, exist_ok=True)

            file = File(Path(source), Path(output_directory), Type("PNG"))
            PillowImageConverter().convert_and_save(file)

            self.assertTrue(os.path.isfile(expected_output))
            with Image.open(expected_output) as converted:
                self.assertEqual(converted.format, "PNG")


if __name__ == "__main__":
    unittest.main()
