import uuid
from datetime import datetime

from factory.base import Factory
from factory.declarations import LazyFunction, Sequence
from faker import Faker
from pydantic import UUID4
from sqlmodel import Field, Session

from app.domain.entities.user_entity import UserEntity, UserRoles
from app.domain.entities.with_date_entity import WithDateModel
from app.domain.helpers.security import get_password_hash
from app.infra.database.models import User

fake = Faker()


class UserMockWithPassword(UserEntity, WithDateModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    clean_password: str = Field(default="")


class UserFactory(Factory):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = User

    name = LazyFunction(fake.name)
    email = Sequence(lambda n: f"emailteste{n}@email.com")
    password = get_password_hash("pass123")
    role = LazyFunction(lambda: Faker().enum(UserRoles))


def get_user_mock_with_password(
    role=UserRoles.COMERCIAL,
    password="pass123",
    activated_at: datetime | None = datetime.now(),
):
    user = UserFactory(
        role=role,
        password=get_password_hash(password),
        activated_at=activated_at,
    )
    user_with_pass = UserMockWithPassword.model_validate(user)
    user_with_pass.clean_password = password
    return user_with_pass


def insert_user_mock(
    user: UserMockWithPassword, db: Session
) -> UserMockWithPassword:
    password = user.clean_password
    db_user = User.model_validate(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user_mock = UserMockWithPassword.model_validate(db_user)
    user_mock.clean_password = password
    return user_mock
