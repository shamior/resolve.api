import pytest

from app.domain.entities.user_role_entity import RoleType
from app.domain.repositories.user_role_repository import UserRoleRepository
from app.infra.database.database import Database


@pytest.fixture
def user_role_repo(db: Database):
    return UserRoleRepository(db)


@pytest.mark.parametrize("role_type", RoleType)
def test_find_or_create_role(
    user_role_repo: UserRoleRepository,
    role_type: RoleType,
):
    created = user_role_repo.find_or_create_role(role_type)
    assert created is not None
    assert created.role_type == role_type

    found = user_role_repo.find_role_by_type(role_type)
    assert found is not None
    assert found.role_type == role_type


role_parameters = [
    (RoleType.COMERCIAL, RoleType.EXECUTOR),
    (
        RoleType.EXECUTOR,
        RoleType.FINANCEIRO,
        RoleType.FINANCEIRO,
        RoleType.ADMIN,
        RoleType.COMERCIAL,
    ),
]


@pytest.mark.parametrize("roles", role_parameters)
def test_find_many_or_create(
    user_role_repo: UserRoleRepository,
    roles: list[RoleType],
):
    first_role = roles[0]
    created_first = user_role_repo.find_many_or_create([first_role])
    assert len(created_first) == 1
    assert created_first[0].role_type == first_role

    role_len = len(roles)
    created_roles = user_role_repo.find_many_or_create(roles)
    assert len(created_roles) == role_len
    for role_type in roles:
        found = user_role_repo.find_role_by_type(role_type)
        assert found is not None
        assert found.role_type == role_type
