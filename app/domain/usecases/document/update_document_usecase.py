from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import UUID4

from app.api.document.dto.document_update_dto import DocumentUpdate
from app.domain.repositories.documents_repository import DocumentsRepositoryDep
from app.infra.database.models import Document


class UpdateDocumentUseCase:
    def __init__(self, documents_repository: DocumentsRepositoryDep) -> None:
        self.documents_repository = documents_repository

    def execute(
        self,
        document_id: UUID4,
        document_data: DocumentUpdate,
    ) -> Document:
        document = self.documents_repository.find_document_by_id(document_id)
        if not document:
            raise HTTPException(
                HTTPStatus.NOT_FOUND,
                detail="Documento não encontrado",
            )

        update_data = document_data.model_dump(exclude_unset=True)
        document.sqlmodel_update(update_data)

        return self.documents_repository.update_document(document)


UpdateDocumentUseCaseDep = Annotated[UpdateDocumentUseCase, Depends()]
