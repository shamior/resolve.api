from datetime import datetime

from sqlmodel import Session

from app.database import engine
from app.helpers.security import get_password_hash
from app.models.user_model import User, UserRoles


def create_users(session: Session):
    comercial = User(
        name="Comercial da Silva",
        role=UserRoles.COMERCIAL,
        password=get_password_hash("pass123"),
        email="comercial@email.com",
        activated_at=datetime.now(),
    )
    executor = User(
        name="Executor Divino",
        role=UserRoles.EXECUTOR,
        password=get_password_hash("pass123"),
        email="executor@email.com",
        activated_at=datetime.now(),
    )
    financeiro = User(
        name="Financeiro do Dinheiro",
        role=UserRoles.FINANCEIRO,
        password=get_password_hash("pass123"),
        email="financeiro@email.com",
        activated_at=datetime.now(),
    )
    admin = User(
        name="Adminaldo Manda Tudo",
        role=UserRoles.ADMIN,
        password=get_password_hash("pass123"),
        email="admin@email.com",
        activated_at=datetime.now(),
    )
    session.add_all([comercial, executor, financeiro, admin])
    session.commit()


def seed():
    with Session(engine) as session:
        create_users(session)
