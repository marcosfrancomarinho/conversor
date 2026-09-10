from abc import ABC, abstractmethod

from src.domain.valuesobject.type import Type


class FileSaveLocationSelector(ABC):
    @abstractmethod
    def select(self, output_type: Type, suggested_path: str) -> str | None:
        ...
