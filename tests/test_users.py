from sqlmodel import Session, select

from app.models.user_model import User, UserRoles


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


def test_user_repository_find_many_should_return_many_users(db: Session):
    users = db.exec(select(User)).all()
    assert len(users) == 0
