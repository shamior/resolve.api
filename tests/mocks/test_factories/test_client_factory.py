import os

import pytest
from faker import Faker
from sqlmodel import Session

from app.domain.config.env_config.settings import Settings
from tests.mocks.client_factory import ClientFactory


def test_client_fields(settings_with_path: Settings, db: Session):
    clients = ClientFactory(db)
    client = clients[0]
    document_quatity_default = 3
    assert len(clients) == 1
    assert client.name is not None
    assert client.phone is not None
    assert client.country_code is not None
    assert client.birthdate is not None
    assert client.email is not None
    assert client.passport is not None
    assert client.logged_in_as is not None
    assert client.country is not None
    assert len(client.documents) == document_quatity_default


test_data = [
    (0, 1),
    (1, 5),
    (3, 10),
    (10, 3),
]


@pytest.mark.parametrize(("documents_quantity", "client_quantity"), test_data)
def test_client_write_file(
    settings_with_path: Settings,
    db: Session,
    documents_quantity: int,
    client_quantity: int,
):
    fake = Faker()
    doc_names = [
        f"{fake.file_name(extension='.pdf')}"
        for _ in range(documents_quantity)
    ]
    doc_names_without_pdf = [
        docname.replace(".pdf", "") for docname in doc_names
    ]
    clients = ClientFactory(
        db,
        create_file=True,
        documents=doc_names,
        batch_size=client_quantity,
    )
    for client in clients:
        if documents_quantity == 0:
            assert len(client.documents) == 0
        else:
            path_created = os.path.join(
                settings_with_path.STORAGE_DIR,
                settings_with_path.DOCUMENTS_DIR,
            )
            files_created = os.listdir(path_created)
            assert os.path.exists(path_created)
            assert len(files_created) == documents_quantity * client_quantity
            assert client.country is not None
            for doc in client.documents:
                assert str(doc.id) in files_created
                assert doc.name in doc_names_without_pdf
