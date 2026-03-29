from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import UUID4

from app.domain.repositories.documents_repository import DocumentsRepositoryDep
from app.infra.database.models import Document


class DeleteDocumentUseCase:
    def __init__(self, document_repository: DocumentsRepositoryDep):
        self.document_repository = document_repository

    def execute(self, document_id: UUID4) -> Document:
        document = self.verify_existence(document_id)
        self.document_repository.delete(document)
        return document

    def verify_existence(self, document_id) -> Document:
        document = self.document_repository.find_by_id(document_id)
        if document is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Documento não encontrado",
            )
        return document


DeleteDocumentUseCaseDep = Annotated[DeleteDocumentUseCase, Depends()]
