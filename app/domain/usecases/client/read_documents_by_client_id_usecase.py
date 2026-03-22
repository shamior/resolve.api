from typing import Annotated

from fastapi import Depends
from pydantic import UUID4

from app.domain.repositories.documents_repository import DocumentsRepositoryDep
from app.infra.database.models import Document


class ReadDocumentsByClientIdUseCase:
    def __init__(self, documents_repository: DocumentsRepositoryDep) -> None:
        self.documents_repository = documents_repository

    def execute(self, client_id: UUID4) -> list[Document]:
        return self.documents_repository.find_documents_by_client_id(client_id)


ReadDocumentsByClientIdUseCaseDep = Annotated[
    ReadDocumentsByClientIdUseCase,
    Depends(),
]
