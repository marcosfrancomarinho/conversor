from abc import ABC, abstractmethod
from src.domain.valuesobject.path import Path
from src.domain.valuesobject.type import Type

class FileSaveLocationSelector(ABC):
    @abstractmethod
    def select(self, type:Type)->Path:
        ...