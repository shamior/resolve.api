import os
import uuid
from http import HTTPStatus

import pytest
from faker import Faker
from fastapi import HTTPException
from sqlmodel import Session, inspect

from app.domain.config.env_config.settings import Settings
from app.domain.repositories.client_repository import ClientRepository
from app.domain.repositories.documents_repository import DocumentsRepository
from app.domain.usecases.document.create_document_usecase import (
    CreateDocumentUseCase,
)
from app.infra.database.models import Client
from app.infra.services.file_storage.local_file_storage import LocalFileStorage
from tests.mocks.client_factory import ClientFactory


@pytest.fixture
def new_client(db: Session):
    return ClientFactory(db, documents=[])[0]


@pytest.fixture
def usecase_local(db: Session):
    client_repository = ClientRepository(db)
    documents_repository = DocumentsRepository(db)
    file_storage = LocalFileStorage()
    return CreateDocumentUseCase(
        client_repository=client_repository,
        documents_repository=documents_repository,
        file_storage=file_storage,
    )


def test_create_document_local(
    settings_with_path: Settings,
    new_client: Client,
    usecase_local: CreateDocumentUseCase,
):
    fake = Faker()
    content = b"legal"
    doc = usecase_local.execute(
        client_id=new_client.id,
        name=fake.file_name(extension=".pdf"),
        mime_type="application/pdf",
        file_content=content,
    )
    file_path = os.path.join(
        settings_with_path.STORAGE_DIR,
        settings_with_path.DOCUMENTS_DIR,
        str(doc.id),
    )
    doc_inspector = inspect(doc)

    assert doc_inspector is not None
    assert doc_inspector.persistent

    assert ".pdf" not in doc.name
    assert file_path == doc.path
    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        assert f.read() == content


def test_create_document_local_without_client_id(
    settings_with_path: Settings,
    usecase_local: CreateDocumentUseCase,
):
    fake = Faker()
    content = b"legal"
    with pytest.raises(HTTPException) as exc:
        usecase_local.execute(
            client_id=uuid.uuid4(),
            name=fake.file_name(extension=".pdf"),
            mime_type="application/pdf",
            file_content=content,
        )

    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Cliente não encontrado"
