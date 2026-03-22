from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import UUID4

from app.domain.repositories.documents_repository import DocumentsRepositoryDep
from app.infra.database.models import Document


class ReadDocumentByIdUseCase:
    def __init__(self, documents_repository: DocumentsRepositoryDep) -> None:
        self.documents_repository = documents_repository

    def execute(self, document_id: UUID4) -> Document:
        document = self.documents_repository.find_document_by_id(document_id)
        if not document:
            raise HTTPException(
                HTTPStatus.NOT_FOUND,
                detail="Documento não encontrado",
            )
        return document


ReadDocumentByIdUseCaseDep = Annotated[ReadDocumentByIdUseCase, Depends()]
