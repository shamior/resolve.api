import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException
from sqlmodel import Session

from app.domain.config.env_config.settings import Settings
from app.domain.repositories.documents_repository import DocumentsRepository
from app.domain.usecases.document.export_document_usecase import (
    ExportDocumentUseCase,
)
from app.infra.database.models import Client, Document
from app.infra.services.file_storage.local_file_storage import LocalFileStorage
from tests.mocks.client_factory import ClientFactory


@pytest.fixture
def client_with_documents(db: Session, settings_with_path: Settings) -> Client:
    return ClientFactory(db, create_file=True)[0]


@pytest.fixture
def document_not_persisted(db: Session) -> Document:
    return ClientFactory(db)[0].documents[0]


@pytest.fixture
def usecase_local(db: Session) -> ExportDocumentUseCase:
    documents_repository = DocumentsRepository(db)
    file_storage = LocalFileStorage()
    return ExportDocumentUseCase(
        documents_repository=documents_repository,
        file_storage=file_storage,
    )


@pytest.fixture
def existing_document(
    db: Session,
    client_with_documents: Client,
) -> Document:
    documents_repository = DocumentsRepository(db)
    return documents_repository.find_by_client_id(
        client_with_documents.id,
    )[0]


def test_export_document_returns_document(
    existing_document: Document,
    usecase_local: ExportDocumentUseCase,
):
    document, content = usecase_local.execute(existing_document.id)

    assert len(content) > 0
    assert document.id == existing_document.id
    assert document.name == existing_document.name
    assert document.path == existing_document.path
    assert document.client_id == existing_document.client_id


def test_export_document_raise_file_not_found(
    document_not_persisted: Document,
    usecase_local: ExportDocumentUseCase,
):
    with pytest.raises(HTTPException) as exc:
        usecase_local.execute(document_not_persisted.id)

    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Arquivo não encontrado no armazenamento"


def test_export_document_raises_not_found(
    usecase_local: ExportDocumentUseCase,
):
    with pytest.raises(HTTPException) as exc:
        usecase_local.execute(uuid.uuid4())

    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Documento não encontrado"
