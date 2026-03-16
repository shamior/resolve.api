import pytest
from sqlmodel import Session, select

from app.domain.entities.user_entity import UserRoles
from app.domain.repositories.user_repository import (
    UserRepositoryFactory,
    UserRepositoryFindManyFilters,
)
from app.infra.database.database import Database
from app.infra.database.models import User
from tests.mocks.user_mock import UserFactory


@pytest.fixture
def user_repository(db: Session):
    return UserRepositoryFactory(db)


def test_user_create(db: Session):
    db.add(
        User(
            name="a",
            email="email@email.com",
            password="nosa",
            role=UserRoles.ADMIN,
        )
    )
    users = db.exec(select(User)).all()
    assert len(users) == 1


def test_user_repository_find_many_should_return_many_users(
    user_repository: UserRepositoryFactory, db: Database
):
    batch_size = 20
    users = UserFactory.create_batch(20)
    db.add_all(users)
    db.commit()
    users_db = user_repository.find_many(
        UserRepositoryFindManyFilters(fetch_only_active=False)
    )
    assert len(users_db) == batch_size
