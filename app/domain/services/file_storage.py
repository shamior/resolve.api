from abc import ABC, abstractmethod


class FileStorage(ABC):  # pragma: no cover
    @abstractmethod
    def write(self, file_content: bytes, file_path: str) -> str:
        pass

    @abstractmethod
    def read(self, file_path: str) -> bytes:
        pass
