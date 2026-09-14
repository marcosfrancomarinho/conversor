from PIL import Image, ImageOps, UnidentifiedImageError

from src.domain.entities.file import File
from src.domain.gateway.image_converter import ImageConverter


class PillowImageConverter(ImageConverter):
    def convert_and_save(self, file: File) -> None:
        try:
            with Image.open(file.get_path_input()) as image:
                image.load()
                oriented = ImageOps.exif_transpose(image)
                prepared = self.__prepare_image(oriented, file.get_file_type())
                prepared.save(
                    file.get_path_full_output(),
                    format=file.get_file_type(),
                    **self.__save_options(file.get_file_type()),
                )
        except UnidentifiedImageError as error:
            raise ValueError(
                f"O arquivo não é uma imagem válida: {file.get_path_input()}"
            ) from error
        except OSError as error:
            raise ValueError(
                f"Não foi possível converter a imagem: {file.get_path_input()}"
            ) from error

    @staticmethod
    def __prepare_image(image: Image.Image, output_type: str) -> Image.Image:
        if output_type == "JPEG":
            if image.mode in ("RGBA", "LA") or "transparency" in image.info:
                rgba = image.convert("RGBA")
                background = Image.new("RGB", rgba.size, "white")
                background.paste(rgba, mask=rgba.getchannel("A"))
                return background

            return image.convert("RGB")

        return image.convert("RGBA")

    @staticmethod
    def __save_options(output_type: str) -> dict[str, object]:
        if output_type == "JPEG":
            return {"quality": 95, "optimize": True}

        if output_type == "PNG":
            return {"optimize": True}

        return {}
