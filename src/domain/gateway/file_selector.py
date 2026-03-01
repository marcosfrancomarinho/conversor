from abc import ABC, abstractmethod
from src.domain.valuesobject.path import Path


class FileSelector(ABC):
    @abstractmethod
    def select(self)->list[Path]:
        ...