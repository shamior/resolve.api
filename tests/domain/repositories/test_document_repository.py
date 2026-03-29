import pytest
from faker import Faker
from sqlmodel import Session, inspect

from app.domain.repositories.documents_repository import DocumentsRepository
from app.infra.database.models import Client, Document
from tests.mocks.client_factory import ClientFactory

fake = Faker()


@pytest.fixture
def repository(db: Session):
    return DocumentsRepository(db)


@pytest.fixture
def new_client(db):
    return ClientFactory(db, documents=[])[0]


@pytest.fixture
def documents(repository: DocumentsRepository, new_client: Client):
    documents_amount = 5
    docs = [
        repository.create(
            Document(
                client=new_client,
                name=fake.file_name(extension=".pdf"),
                mime_type="application/pdf",
                path=fake.file_path(extension=".pdf"),
            ),
        )
        for _ in range(documents_amount)
    ]
    return docs


@pytest.fixture
def document_deleted(repository: DocumentsRepository, new_client: Client):
    doc = repository.create(
        Document(
            client=new_client,
            name=fake.file_name(extension=".pdf"),
            mime_type="application/pdf",
            path=fake.file_path(extension=".pdf"),
        ),
    )
    doc_deleted = repository.delete(doc)
    return doc_deleted


def test_create_document(repository: DocumentsRepository, new_client: Client):
    name = fake.file_name(extension=".pdf")
    mime_type = "application/pdf"
    path = fake.file_path(extension=".pdf")
    doc = repository.create(
        Document(
            client=new_client,
            name=name,
            mime_type=mime_type,
            path=path,
        ),
    )
    inspector = inspect(doc)
    assert inspector is not None
    assert inspector.persistent
    assert doc is not None
    assert doc.name == name
    assert doc.mime_type == mime_type
    assert doc.path == path
    assert doc.client_id == new_client.id
    assert doc.deleted_at is None


def test_delete_document(repository: DocumentsRepository, new_client: Client):
    new_doc = repository.create(
        Document(
            client=new_client,
            name=fake.file_name(extension=".pdf"),
            mime_type="application/pdf",
            path=fake.file_path(extension=".pdf"),
        ),
    )
    deleted_doc = repository.delete(new_doc)
    assert deleted_doc is not None
    assert deleted_doc.deleted_at is not None


def test_update_document(repository: DocumentsRepository, new_client: Client):
    old_name = fake.file_name(extension=".pdf")
    new_name = fake.file_name(extension=".pdf")
    new_doc = repository.create(
        Document(
            client=new_client,
            name=old_name,
            mime_type="application/pdf",
            path=fake.file_path(extension=".pdf"),
        ),
    )
    updated_time = new_doc.created_at
    new_doc.name = new_name
    updated_doc = repository.update(new_doc)
    assert updated_doc is not None
    assert updated_doc.name == new_name
    assert updated_time < updated_doc.updated_at


def test_read_documents_by_client_should_bring_only_not_deleted(
    repository: DocumentsRepository,
    new_client: Client,
    documents: list[Document],
    document_deleted: Document,
):
    docs = repository.find_by_client_id(new_client.id)

    assert docs is not None
    assert documents[0].client_id == new_client.id
    assert document_deleted.client_id == new_client.id
    for doc in docs:
        assert doc in documents
    assert document_deleted not in docs
