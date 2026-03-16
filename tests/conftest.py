import json
from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from app.api.auth.presentable.token_presentable import TokenWithUser
from app.domain.config.env_config.settings import Settings
from app.domain.entities.user_entity import UserRoles
from app.infra.database.database import get_session
from app.main import app
from tests.mocks.user_mock import (
    UserMockWithPassword,
    get_user_mock_with_password,
    insert_user_mock,
)


@pytest.fixture
def app_client(db):
    def override_db():
        return db

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = override_db
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=datetime.now()):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time

    event.listen(model, "before_insert", fake_time_hook)
    yield time

    event.remove(model, "before_insert", fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def settings():
    settings = Settings()  # pyright: ignore[reportCallIssue]
    return settings


@pytest.fixture
def user_comercial(db: Session):
    user = get_user_mock_with_password(UserRoles.COMERCIAL)
    user = insert_user_mock(user, db)
    return user


@pytest.fixture
def user_executor(db: Session):
    user = get_user_mock_with_password(UserRoles.EXECUTOR)
    user = insert_user_mock(user, db)
    return user


@pytest.fixture
def user_financeiro(db: Session):
    user = get_user_mock_with_password(UserRoles.FINANCEIRO)
    user = insert_user_mock(user, db)
    return user


@pytest.fixture
def user_admin(db: Session):
    user = get_user_mock_with_password(UserRoles.ADMIN)
    user = insert_user_mock(user, db)
    return user


@pytest.fixture
def token_comercial(
    user_comercial: UserMockWithPassword, app_client: TestClient
):
    response = app_client.post(
        "/auth/token",
        data={
            "username": user_comercial.email,
            "password": user_comercial.clean_password,
        },
    )
    return TokenWithUser.model_validate_json(json.dumps(response.json()))


@pytest.fixture
def token_executor(
    user_executor: UserMockWithPassword, app_client: TestClient
):
    response = app_client.post(
        "/auth/token",
        data={
            "username": user_executor.email,
            "password": user_executor.clean_password,
        },
    )
    return TokenWithUser.model_validate_json(json.dumps(response.json()))


@pytest.fixture
def token_financeiro(
    user_financeiro: UserMockWithPassword, app_client: TestClient
):
    response = app_client.post(
        "/auth/token",
        data={
            "username": user_financeiro.email,
            "password": user_financeiro.clean_password,
        },
    )
    return TokenWithUser.model_validate_json(json.dumps(response.json()))


@pytest.fixture
def token_admin(user_admin: UserMockWithPassword, app_client: TestClient):
    response = app_client.post(
        "/auth/token",
        data={
            "username": user_admin.email,
            "password": user_admin.clean_password,
        },
    )
    return TokenWithUser.model_validate_json(json.dumps(response.json()))


@pytest.fixture
def user_not_activated(db: Session):
    user = get_user_mock_with_password(activated_at=None)
    user = insert_user_mock(user, db)
    return user
