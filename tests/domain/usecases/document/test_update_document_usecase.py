import uuid
from http import HTTPStatus

import pytest
from faker import Faker
from fastapi import HTTPException
from sqlmodel import Session

from app.domain.repositories.documents_repository import DocumentsRepository
from app.domain.usecases.document.update_document_usecase import (
    UpdateDocumentUseCase,
)
from app.infra.database.models import Client, Document
from tests.mocks.client_factory import ClientFactory


@pytest.fixture
def client_with_documents(db: Session):
    return ClientFactory(db)[0]


@pytest.fixture
def usecase(db: Session):
    documents_repository = DocumentsRepository(db)
    return UpdateDocumentUseCase(documents_repository=documents_repository)


@pytest.fixture
def existing_document(db: Session, client_with_documents: Client):
    documents_repository = DocumentsRepository(db)
    return documents_repository.find_by_client_id(
        client_with_documents.id,
    )[0]


def test_update_document_name(
    existing_document: Document,
    usecase: UpdateDocumentUseCase,
):
    fake = Faker()
    new_name = fake.file_name()
    original_path = existing_document.path

    updated_document = usecase.execute(
        existing_document.id,
        name=new_name,
    )

    assert updated_document.id == existing_document.id
    assert updated_document.name == new_name
    assert updated_document.path == original_path
    assert updated_document.client_id == existing_document.client_id


def test_update_document_raises_not_found(
    usecase: UpdateDocumentUseCase,
):
    fake = Faker()
    with pytest.raises(HTTPException) as exc:
        usecase.execute(uuid.uuid4(), name=fake.file_name())

    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Documento não encontrado"
