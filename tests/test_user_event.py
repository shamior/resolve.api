from sqlmodel import Session, select

from app.models.user_model import User, UserRoles


def test_event(db: Session, mock_db_time):
    with mock_db_time(model=User) as time:
        user = User(
            email="email@email.com",
            name="nice name",
            password="senha",
            role=UserRoles.ADMIN,
        )
        db.add(user)
        db.commit()

        user_retrieved = db.exec(select(User)).one_or_none()
        assert user_retrieved is not None
        assert user_retrieved.created_at == time
