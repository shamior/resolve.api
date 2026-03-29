import pytest
from sqlmodel import Session

from app.domain.repositories.documents_repository import DocumentsRepository
from app.domain.usecases.client.read_documents_by_client_id_usecase import (
    ReadDocumentsByClientIdUseCase,
)
from app.infra.database.models import Client
from tests.mocks.client_factory import ClientFactory


@pytest.fixture
def new_client(db: Session):
    return ClientFactory(db)[0]


@pytest.fixture
def usecase(db: Session):
    document_repository = DocumentsRepository(db)
    return ReadDocumentsByClientIdUseCase(document_repository)


def test_read_documents_by_client_id_returns_documents(
    new_client: Client,
    usecase: ReadDocumentsByClientIdUseCase,
):
    document_amount = 3
    documents = usecase.execute(new_client.id)
    assert len(documents) == document_amount
    assert documents[0].client_id == new_client.id
