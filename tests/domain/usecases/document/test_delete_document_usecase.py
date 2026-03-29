import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException
from sqlmodel import Session

from app.domain.repositories.documents_repository import DocumentsRepository
from app.domain.usecases.document.delete_document_usecase import (
    DeleteDocumentUseCase,
)
from app.infra.database.models import Client, Document
from tests.mocks.client_factory import ClientFactory


@pytest.fixture
def client_with_documents(db: Session) -> Client:
    return ClientFactory(db)[0]


@pytest.fixture
def usecase(db: Session) -> DeleteDocumentUseCase:
    documents_repository = DocumentsRepository(db)
    return DeleteDocumentUseCase(document_repository=documents_repository)


@pytest.fixture
def existing_document(
    db: Session,
    client_with_documents: Client,
) -> Document:
    documents_repository = DocumentsRepository(db)
    return documents_repository.find_by_client_id(
        client_with_documents.id,
    )[0]


def test_delete_document_returns_document(
    existing_document: Document,
    usecase: DeleteDocumentUseCase,
):
    document = usecase.execute(existing_document.id)

    assert document.id == existing_document.id
    assert document.name == existing_document.name
    assert document.path == existing_document.path
    assert document.client_id == existing_document.client_id
    assert document.deleted_at is not None


def test_delete_document_raises_not_found(
    usecase: DeleteDocumentUseCase,
):
    with pytest.raises(HTTPException) as exc:
        usecase.execute(uuid.uuid4())

    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Documento não encontrado"
