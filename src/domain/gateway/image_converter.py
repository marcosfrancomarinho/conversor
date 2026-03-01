from abc import ABC, abstractmethod
from src.domain.entities.file import File


class ImageConverter(ABC):
    @abstractmethod
    def convert_and_save(self,file:File)->None:
        ...