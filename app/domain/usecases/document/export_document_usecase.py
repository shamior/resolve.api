import os
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import UUID4

from app.domain.repositories.documents_repository import DocumentsRepositoryDep
from app.infra.database.models import Document
from app.infra.services.file_storage.local_file_storage import FileStorageDep


class ExportDocumentUseCase:
    def __init__(
        self,
        documents_repository: DocumentsRepositoryDep,
        file_storage: FileStorageDep,
    ) -> None:
        self.documents_repository = documents_repository
        self.file_storage = file_storage

    def execute(self, document_id: UUID4) -> tuple[Document, bytes]:
        document = self.documents_repository.find_by_id(document_id)
        if not document:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Documento não encontrado",
            )

        if not os.path.exists(document.path):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Arquivo não encontrado no armazenamento",
            )

        file_content = self.file_storage.read(document.path)
        return document, file_content


ExportDocumentUseCaseDep = Annotated[ExportDocumentUseCase, Depends()]
