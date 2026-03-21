import pytest
from sqlmodel import Session

from app.domain.entities.user_role_entity import RoleType
from app.domain.repositories.user_repository import (
    UserRepository,
    UserRepositoryDep,
    UserRepositoryFindManyFilters,
)
from app.infra.database.database import Database
from app.infra.database.models import User
from tests.mocks.user_factory import UserFactory


@pytest.fixture
def user_repository(db: Session):
    return UserRepository(db)


def test_user_repository_find_many_should_return_many_users(
    user_repository: UserRepository,
    db: Database,
):
    batch_size = 20
    UserFactory(db, batch_size=batch_size)
    users_db = user_repository.find_many(
        UserRepositoryFindManyFilters(fetch_only_active=False),
    )
    assert len(users_db) == batch_size


role_parameters = [
    [RoleType.COMERCIAL, RoleType.EXECUTOR],
    [
        RoleType.EXECUTOR,
        RoleType.FINANCEIRO,
        RoleType.ADMIN,
        RoleType.COMERCIAL,
    ],
]


@pytest.mark.parametrize("roles", role_parameters)
def test_user_repository_create_user_with_roles(
    user_repository: UserRepositoryDep,
    roles: list[RoleType],
):
    user = User(
        email="test@example.com",
        name="Test User",
    )
    role_quantity = len(roles)
    user_with_roles = user_repository.create_user_with_roles(user, roles)
    assert len(user_with_roles.roles) == role_quantity
    assert all(role.role_type in roles for role in user_with_roles.roles)
