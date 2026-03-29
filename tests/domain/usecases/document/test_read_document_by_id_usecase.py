import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException
from sqlmodel import Session

from app.domain.repositories.documents_repository import DocumentsRepository
from app.domain.usecases.document.read_document_by_id_usecase import (
    ReadDocumentByIdUseCase,
)
from app.infra.database.models import Client, Document
from tests.mocks.client_factory import ClientFactory


@pytest.fixture
def client_with_documents(db: Session) -> Client:
    return ClientFactory(db)[0]


@pytest.fixture
def usecase(db: Session) -> ReadDocumentByIdUseCase:
    documents_repository = DocumentsRepository(db)
    return ReadDocumentByIdUseCase(documents_repository=documents_repository)


@pytest.fixture
def existing_document(
    db: Session,
    client_with_documents: Client,
) -> Document:
    documents_repository = DocumentsRepository(db)
    return documents_repository.find_by_client_id(
        client_with_documents.id,
    )[0]


def test_read_document_by_id_returns_document(
    existing_document: Document,
    usecase: ReadDocumentByIdUseCase,
):
    document = usecase.execute(existing_document.id)

    assert document.id == existing_document.id
    assert document.name == existing_document.name
    assert document.path == existing_document.path
    assert document.client_id == existing_document.client_id


def test_read_document_by_id_raises_not_found(
    usecase: ReadDocumentByIdUseCase,
):
    with pytest.raises(HTTPException) as exc:
        usecase.execute(uuid.uuid4())

    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Documento não encontrado"
