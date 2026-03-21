import random
import uuid
from datetime import datetime
from typing import Optional

from factory.base import Factory
from factory.declarations import LazyFunction, Sequence
from faker import Faker
from pydantic import UUID4
from sqlmodel import Field, Session

from app.domain.entities.user_entity import UserEntity
from app.domain.entities.user_role_entity import RoleType
from app.domain.entities.with_date_entity import WithDateModel
from app.domain.helpers.security import get_password_hash
from app.domain.repositories.user_repository import (
    UserRepository,
)
from app.infra.database.models import User, UserRole

fake = Faker()


class UserMockWithPassword(UserEntity, WithDateModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    clean_password: str = Field(default="")
    roles: list[UserRole]


clean_password = fake.password()
computed_password = get_password_hash(clean_password)


class UserFactory:
    def __new__(
        cls,
        db: Session,
        roles: Optional[list[RoleType]] = None,
        name: str | None = None,
        email: str | None = None,
        password=clean_password,
        activated_at: datetime | None = datetime.now(),
        batch_size: int = 1,
    ):
        user_repo = UserRepository(db)
        clean_password = password
        password = get_password_hash(clean_password)
        kwargs = {
            "name": name,
            "email": email,
            "password": password,
            "activated_at": activated_at,
        }
        not_none_kwargs = {
            key: value for key, value in kwargs.items() if value is not None
        }
        users_from_factory = cls.UserInsideFactory.create_batch(
            batch_size,
            **not_none_kwargs,
        )
        users_validated = [
            User.model_validate(user) for user in users_from_factory
        ]
        users: list[UserMockWithPassword] = []
        for user in users_validated:
            created_user = user_repo.create_user_with_roles(
                user,
                cls.roles_or_sample(roles),
            )
            user_mock = UserMockWithPassword.model_validate(created_user)
            user_mock.clean_password = clean_password
            users.append(user_mock)
        return users

    @staticmethod
    def roles_or_sample(
        roles: Optional[list[RoleType]] = None,
    ) -> list[RoleType]:
        if roles is not None:
            return roles
        return random.sample(
            list(RoleType),
            random.randint(1, len(RoleType)),
        )

    class UserInsideFactory(Factory):
        class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
            model = User

        name = LazyFunction(fake.name)
        email = Sequence(lambda n: f"emailteste{n}@email.com")
        password = computed_password
