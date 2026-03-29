import os
import uuid
from http import HTTPStatus
from mimetypes import guess_extension
from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import UUID4

from app.domain.config.env_config.settings import settings
from app.domain.repositories.client_repository import ClientRepositoryDep
from app.domain.repositories.documents_repository import DocumentsRepositoryDep
from app.infra.database.models import Client, Document
from app.infra.services.file_storage.local_file_storage import FileStorageDep


class CreateDocumentUseCase:
    def __init__(
        self,
        documents_repository: DocumentsRepositoryDep,
        file_storage: FileStorageDep,
        client_repository: ClientRepositoryDep,
    ) -> None:
        self.documents_repository = documents_repository
        self.file_storage = file_storage
        self.client_repository = client_repository

    def execute(
        self,
        name: str | None,
        mime_type: str | None,
        client_id: UUID4,
        file_content: bytes,
    ) -> Document:
        client = self.check_client_existence(client_id)
        name = self.extract_file_name(name, mime_type)

        document_id = uuid.uuid4()
        file_path = os.path.join(settings.DOCUMENTS_DIR, str(document_id))

        full_path = self.file_storage.write(file_content, file_path)

        document = Document(
            id=document_id,
            name=name,
            path=full_path,
            mime_type=mime_type or "application/octet-stream",
            client=client,
        )

        return self.documents_repository.create(document)

    def check_client_existence(self, client_id: UUID4) -> Client:
        client = self.client_repository.find_by_id(client_id)
        if not client:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Cliente não encontrado",
            )
        return client

    @staticmethod
    def extract_file_name(name: str | None, mime_type: str | None) -> str:
        # TODO: SANITIZE FILENAME
        name = name if name else "sem_nome"
        extension = None
        if mime_type:
            extension = guess_extension(mime_type)

        if extension:
            name = name.replace(extension, "")

        return name


CreateDocumentUseCaseDep = Annotated[CreateDocumentUseCase, Depends()]
