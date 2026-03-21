from datetime import datetime

from sqlmodel import Session

from app.domain.entities.user_role_entity import RoleType
from app.domain.helpers.security import get_password_hash
from app.domain.repositories.user_repository import UserRepository
from app.infra.database.database import engine
from app.infra.database.models import User


def create_users(session: Session):
    repository = UserRepository(session)
    repository.create_user_with_roles(
        User(
            name="Comercial da Silva",
            password=get_password_hash("pass123"),
            email="comercial@email.com",
            activated_at=datetime.now(),
        ),
        [RoleType.COMERCIAL],
    )
    repository.create_user_with_roles(
        User(
            name="Executor Divino",
            password=get_password_hash("pass123"),
            email="executor@email.com",
            activated_at=datetime.now(),
        ),
        [RoleType.EXECUTOR],
    )
    repository.create_user_with_roles(
        User(
            name="Financeiro do Dinheiro",
            password=get_password_hash("pass123"),
            email="financeiro@email.com",
            activated_at=datetime.now(),
        ),
        [RoleType.FINANCEIRO],
    )
    repository.create_user_with_roles(
        User(
            name="Adminaldo Manda Tudo",
            password=get_password_hash("pass123"),
            email="admin@email.com",
            activated_at=datetime.now(),
        ),
        [RoleType.ADMIN],
    )


def seed():
    with Session(engine) as session:
        create_users(session)
