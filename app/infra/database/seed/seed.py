from datetime import datetime

from sqlmodel import Session

from app.domain.entities.user_role_entity import RoleType
from app.domain.helpers.security import get_password_hash
from app.infra.database.database import engine
from tests.mocks.client_factory import ClientFactory
from tests.mocks.user_factory import UserFactory


def create_users(session: Session):
    UserFactory(
        db=session,
        name="Comercial da Silva",
        password=get_password_hash("pass123"),
        email="comercial@email.com",
        activated_at=datetime.now(),
        roles=[RoleType.COMERCIAL],
    )

    UserFactory(
        db=session,
        name="Executor Divino",
        password=get_password_hash("pass123"),
        email="executor@email.com",
        activated_at=datetime.now(),
        roles=[RoleType.EXECUTOR],
    )
    UserFactory(
        db=session,
        name="Financeiro do Dinheiro",
        password=get_password_hash("pass123"),
        email="financeiro@email.com",
        activated_at=datetime.now(),
        roles=[RoleType.FINANCEIRO],
    )
    UserFactory(
        db=session,
        name="Adminaldo Manda Tudo",
        password=get_password_hash("pass123"),
        email="admin@email.com",
        activated_at=datetime.now(),
        roles=[RoleType.ADMIN],
    )


def create_client(session: Session):
    ClientFactory(
        db=session,
        documents=[],
        country_code="BRA",
        country_name="Brasil",
        fetch_country=True,
    )


def seed():  # pragma: no cover
    with Session(engine) as session:
        create_users(session)
        create_client(session)


if __name__ == "__main__":
    seed()
