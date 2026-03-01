from abc import ABC, abstractmethod
from src.domain.entities.file import File


class PDFConverter(ABC):
    @abstractmethod
    def convert_and_save(self,files:list[File])->None:
        ...