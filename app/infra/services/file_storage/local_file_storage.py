from fastapi import Depends
from typing_extensions import Annotated

from app.domain.config.env_config.settings import settings
from app.domain.services.file_storage import FileStorage


class LocalFileStorage(FileStorage):
    def __init__(self):
        self.storage_dir = settings.STORAGE_DIR

    def write(self, file_content: bytes, file_path: str) -> str:
        path = f"{self.storage_dir}/{file_path}"
        with open(path, "wb") as f:
            f.write(file_content)
        return path

    def read(self, file_path: str) -> bytes:
        with open(f"{self.storage_dir}/{file_path}", "rb") as f:
            file = f.read()
        return file


FileStorageDep = Annotated[FileStorage, Depends(LocalFileStorage)]
