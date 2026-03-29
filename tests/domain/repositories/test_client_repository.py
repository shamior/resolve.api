import pytest
from sqlmodel import Session

from app.domain.repositories.client_repository import ClientRepository


@pytest.fixture
def client_repository(db: Session):
    return ClientRepository(db)
