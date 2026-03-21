from sqlmodel import Session, select

from app.infra.database.models import User
from tests.mocks.user_factory import UserFactory


def test_event(db: Session, mock_db_time):
    with mock_db_time(model=User) as time:
        UserFactory(db)[0]

        user_retrieved = db.exec(select(User)).first()
        assert user_retrieved is not None
        assert user_retrieved.created_at == time
