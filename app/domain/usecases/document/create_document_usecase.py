import uuid
from typing import Annotated

from fastapi import Depends
from pydantic import UUID4

from app.domain.config.env_config.settings import settings
from app.domain.repositories.documents_repository import DocumentsRepositoryDep
from app.infra.database.models import Document
from app.infra.services.file_storage.local_file_storage import FileStorageDep


class CreateDocumentUseCase:
    def __init__(
        self,
        documents_repository: DocumentsRepositoryDep,
        file_storage: FileStorageDep,
    ) -> None:
        self.documents_repository = documents_repository
        self.file_storage = file_storage

    def execute(
        self,
        name: str,
        client_id: UUID4,
        file_content: bytes,
    ) -> Document:
        document_id = uuid.uuid4()
        file_path = f"{settings.DOCUMENTS_DIR}/{document_id}"

        full_path = self.file_storage.write(file_content, file_path)

        document = Document(
            id=document_id,
            name=name,
            client_id=client_id,
            path=full_path,
        )

        return self.documents_repository.create_document(document)


CreateDocumentUseCaseDep = Annotated[CreateDocumentUseCase, Depends()]
