from PIL import Image, UnidentifiedImageError

from src.domain.entities.file import File
from src.domain.gateway.image_converter import ImageConverter


class PillowImageConverter(ImageConverter):
    def convert_and_save(self, file: File) -> None:
        try:
            with Image.open(file.get_path_input()) as image:
                image.load()
                prepared = self.__prepare_image(image, file.get_file_type())
                prepared.save(
                    file.get_path_full_output(),
                    format=file.get_file_type(),
                )
        except UnidentifiedImageError as error:
            raise ValueError(
                f"O arquivo não é uma imagem válida: {file.get_path_input()}"
            ) from error

    @staticmethod
    def __prepare_image(image: Image.Image, output_type: str) -> Image.Image:
        if output_type != "JPEG":
            return image.convert("RGBA")

        if image.mode in ("RGBA", "LA") or "transparency" in image.info:
            rgba = image.convert("RGBA")
            background = Image.new("RGB", rgba.size, "white")
            background.paste(rgba, mask=rgba.getchannel("A"))
            return background

        return image.convert("RGB")
