from http import HTTPStatus

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.api.auth.presentable.token_presentable import TokenWithUser
from app.domain.config.env_config.settings import Settings
from app.domain.entities.user_role_entity import RoleType
from app.infra.database.models import Client
from tests.mocks.client_factory import ClientFactory

fake = Faker()


@pytest.fixture
def new_client(db: Session):
    return ClientFactory(db, create_file=True)[0]


def test_anyone_should_read_document(
    settings_with_path: Settings,
    new_client: Client,
    app_client: TestClient,
    token_all_roles: TokenWithUser,
):
    response = app_client.get(
        f"/documents/{new_client.documents[0].id}",
        headers={"Authorization": f"Bearer {token_all_roles.access_token}"},
    )
    assert response.status_code == HTTPStatus.OK


def test_anyone_should_visualize_document(
    settings_with_path: Settings,
    new_client: Client,
    app_client: TestClient,
    token_all_roles: TokenWithUser,
):
    response = app_client.get(
        f"/documents/{new_client.documents[0].id}/visualize",
        headers={"Authorization": f"Bearer {token_all_roles.access_token}"},
    )
    assert response.status_code == HTTPStatus.OK


def test_admin_executor_should_update_document(
    settings_with_path: Settings,
    new_client: Client,
    app_client: TestClient,
    token_all_roles: TokenWithUser,
):
    response = app_client.patch(
        f"/documents/{new_client.documents[0].id}",
        headers={"Authorization": f"Bearer {token_all_roles.access_token}"},
        json={"name": "top.pdf"},
    )
    user_roles = [role.role_type for role in token_all_roles.user.roles]
    if (
        RoleType.ADMIN.value in user_roles
        or RoleType.EXECUTOR.value in user_roles
    ):
        assert response.status_code == HTTPStatus.OK
        assert response.json()["name"] == "top.pdf"
    else:
        assert response.status_code == HTTPStatus.FORBIDDEN


def test_admin_executor_should_deleted_document(
    settings_with_path: Settings,
    new_client: Client,
    app_client: TestClient,
    token_all_roles: TokenWithUser,
):
    response = app_client.delete(
        f"/documents/{new_client.documents[0].id}",
        headers={"Authorization": f"Bearer {token_all_roles.access_token}"},
    )
    user_roles = [role.role_type for role in token_all_roles.user.roles]
    if (
        RoleType.ADMIN.value in user_roles
        or RoleType.EXECUTOR.value in user_roles
    ):
        assert response.status_code == HTTPStatus.OK
    else:
        assert response.status_code == HTTPStatus.FORBIDDEN


def test_admin_executor_should_created_document(
    settings_with_path: Settings,
    new_client: Client,
    app_client: TestClient,
    token_all_roles: TokenWithUser,
):
    response = app_client.post(
        "/documents",
        headers={"Authorization": f"Bearer {token_all_roles.access_token}"},
        data={"client_id": str(new_client.id)},
        files={"file": ("top.pdf", fake.binary(), "application/pdf")},
    )
    user_roles = [role.role_type for role in token_all_roles.user.roles]
    if (
        RoleType.ADMIN.value in user_roles
        or RoleType.EXECUTOR.value in user_roles
    ):
        assert response.status_code == HTTPStatus.CREATED
    else:
        assert response.status_code == HTTPStatus.FORBIDDEN
