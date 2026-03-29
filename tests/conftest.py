import gettext
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import pycountry
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from app.api.auth.presentable.token_presentable import TokenWithUser
from app.api.user.presentable.user_presentable import UserPresentable
from app.domain.config.env_config.settings import Settings
from app.domain.config.env_config.settings import settings as env_settings
from app.domain.entities.user_role_entity import RoleType
from app.domain.helpers.security import (
    create_access_token,
    create_refresh_token,
)
from app.infra.database.database import get_session
from app.infra.database.models import Country
from app.main import app
from tests.mocks.user_factory import UserFactory, UserMockWithPassword


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


@pytest.fixture
def db_with_countries(db: Session):
    pt = gettext.translation(
        "iso3166-1",
        pycountry.LOCALES_DIR,
        languages=["pt"],
    )
    pt.install()
    countries = [
        Country(
            name=_(country.name),  # type: ignore
            code=country.alpha_3,
        )
        for country in pycountry.countries
    ]
    db.add_all(countries)
    db.commit()
    return db


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
    return env_settings


@pytest.fixture
def settings_with_path(tmp_path: Path, settings: Settings):
    old_storage_dir = settings.STORAGE_DIR
    settings.STORAGE_DIR = tmp_path.as_posix()
    yield settings
    settings.STORAGE_DIR = old_storage_dir


@pytest.fixture
def user_comercial(db: Session):
    user = UserFactory(db, roles=[RoleType.COMERCIAL])
    return user[0]


@pytest.fixture
def user_executor(db: Session):
    user = UserFactory(db, roles=[RoleType.EXECUTOR])
    return user[0]


@pytest.fixture
def user_financeiro(db: Session):
    user = UserFactory(db, roles=[RoleType.FINANCEIRO])
    return user[0]


@pytest.fixture
def user_admin(db: Session):
    user = UserFactory(db, roles=[RoleType.ADMIN])
    return user[0]


@pytest.fixture(
    params=[
        "user_admin",
        "user_comercial",
        "user_executor",
        "user_financeiro",
    ],
)
def user_all_roles(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def token_comercial(user_comercial: UserMockWithPassword):
    access_token = create_access_token({"sub": user_comercial.email})
    refresh_token = create_refresh_token({"sub": user_comercial.email})
    return TokenWithUser(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserPresentable.model_validate(user_comercial),
    )


@pytest.fixture
def token_executor(user_executor: UserMockWithPassword):
    access_token = create_access_token({"sub": user_executor.email})
    refresh_token = create_refresh_token({"sub": user_executor.email})
    return TokenWithUser(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserPresentable.model_validate(user_executor),
    )


@pytest.fixture
def token_financeiro(user_financeiro: UserMockWithPassword):
    access_token = create_access_token({"sub": user_financeiro.email})
    refresh_token = create_refresh_token({"sub": user_financeiro.email})
    return TokenWithUser(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserPresentable.model_validate(user_financeiro),
    )


@pytest.fixture
def token_admin(user_admin: UserMockWithPassword):
    access_token = create_access_token({"sub": user_admin.email})
    refresh_token = create_refresh_token({"sub": user_admin.email})
    return TokenWithUser(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserPresentable.model_validate(user_admin),
    )


@pytest.fixture(
    params=[
        "token_admin",
        "token_comercial",
        "token_executor",
        "token_financeiro",
    ],
)
def token_all_roles(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def user_not_activated(db: Session):
    user = UserFactory(db, activated_at=None)
    return user[0]
