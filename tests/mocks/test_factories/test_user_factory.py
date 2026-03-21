import pytest
from sqlmodel import Session

from app.domain.entities.user_role_entity import RoleType
from tests.mocks.user_factory import UserFactory


@pytest.mark.parametrize(
    "roles",
    [
        [RoleType.COMERCIAL],
        [RoleType.COMERCIAL, RoleType.EXECUTOR],
    ],
)
def test_user_factory(db: Session, roles: list[RoleType]):
    user = UserFactory(db, roles=roles, batch_size=10)
    for user in user:
        assert user.name is not None
        assert user.email is not None
        assert user.activated_at is not None
        assert user.clean_password is not None
        assert len(user.roles) == len(roles)
        for role in user.roles:
            assert role.role_type in roles


def test_user_factory_random_roles(db: Session):
    user = UserFactory(db, batch_size=10)
    for user in user:
        assert len(user.roles) > 0
