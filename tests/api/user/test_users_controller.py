import random
import uuid
from datetime import datetime
from http import HTTPStatus

from faker import Faker
from fastapi.testclient import TestClient

from app.api.auth.presentable.token_presentable import TokenWithUser
from app.domain.entities.user_role_entity import RoleType
from app.infra.database.database import Database
from tests.mocks.user_factory import UserFactory, UserMockWithPassword


def test_admin_should_read_users(
    token_admin: TokenWithUser,
    app_client: TestClient,
):
    response = app_client.get(
        "/users",
        headers={"Authorization": f"Bearer {token_admin.access_token}"},
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data["page"] == 1
    assert data["total"] > 0
    assert len(data["data"]) > 0


def test_read_users_paginated(
    token_admin: TokenWithUser,
    app_client: TestClient,
    db: Database,
):
    batch_size = 102  # 103 com o admin numero primo, bacana
    UserFactory(
        db,
        batch_size=batch_size,
        activated_at=datetime.now(),
    )

    page = 2
    per_page = 17

    response = app_client.get(
        "/users",
        headers={"Authorization": f"Bearer {token_admin.access_token}"},
        params={"page": page, "per_page": per_page},
    )
    users_paginated = response.json()
    assert response.status_code == HTTPStatus.OK
    assert users_paginated["page"] == page
    assert users_paginated["total"] > 0
    assert len(users_paginated["data"]) == per_page


def test_read_users_filters_name(
    token_admin: TokenWithUser,
    app_client: TestClient,
    db: Database,
):
    batch_size = 102  # 103 com o admin numero primo, bacana
    total_users = batch_size + 1
    UserFactory(
        db,
        batch_size=batch_size,
        activated_at=datetime.now(),
    )

    name_contains = "1"
    response_name = app_client.get(
        "/users",
        headers={"Authorization": f"Bearer {token_admin.access_token}"},
        params={"name_or_email_contains": name_contains},
    )
    users_name_test1 = response_name.json()
    assert response_name.status_code == HTTPStatus.OK
    assert users_name_test1["total"] < total_users
    assert len(users_name_test1["data"]) > 0
    assert all(
        (name_contains in user["name"] or name_contains in user["email"])
        for user in users_name_test1["data"]
    )


def test_read_users_filters_role(
    token_admin: TokenWithUser,
    app_client: TestClient,
    db: Database,
):
    available_roles = list(RoleType)
    roles = random.sample(
        available_roles,
        k=random.randint(1, len(available_roles)),
    )
    batch_size = 102  # 103 com o admin numero primo, bacana
    UserFactory(
        db,
        batch_size=batch_size,
        activated_at=datetime.now(),
    )

    response_name = app_client.get(
        "/users",
        headers={"Authorization": f"Bearer {token_admin.access_token}"},
        params={"roles_in": [role.value for role in roles]},
    )
    users = response_name.json()
    assert response_name.status_code == HTTPStatus.OK
    assert len(users["data"]) > 0
    assert all(
        any(
            role.value in [r["role_type"] for r in user["roles"]]
            for role in roles
        )
        for user in users["data"]
    )


def test_comercial_should_not_read_users(
    token_comercial: TokenWithUser,
    app_client: TestClient,
):
    response = app_client.get(
        "/users",
        headers={"Authorization": f"Bearer {token_comercial.access_token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_executor_should_not_read_users(
    token_executor: TokenWithUser,
    app_client: TestClient,
):
    response = app_client.get(
        "/users",
        headers={"Authorization": f"Bearer {token_executor.access_token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_financeiro_should_not_read_users(
    token_financeiro: TokenWithUser,
    app_client: TestClient,
):
    response = app_client.get(
        "/users",
        headers={"Authorization": f"Bearer {token_financeiro.access_token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_admin_should_create_users(
    token_admin: TokenWithUser,
    app_client: TestClient,
):
    fake = Faker()
    email = fake.email()
    roles_available = [r.value for r in list(RoleType)]
    roles = random.sample(
        roles_available,
        random.randint(1, len(roles_available)),
    )
    name = fake.name()
    response = app_client.post(
        "/users",
        headers={"Authorization": f"Bearer {token_admin.access_token}"},
        json={
            "email": email,
            "roles_to_assign": roles,
            "name": name,
        },
    )
    user = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert user["email"] == email
    assert all(role["role_type"] in roles_available for role in user["roles"])
    assert user["name"] == name
    assert "id" in user


def test_create_users_email_should_be_unique(
    token_admin: TokenWithUser,
    app_client: TestClient,
):
    fake = Faker()
    email = fake.email()
    roles_available = [r.value for r in list(RoleType)]
    roles = random.sample(
        roles_available,
        random.randint(1, len(roles_available)),
    )
    name = fake.name()
    first_response = app_client.post(
        "/users",
        headers={"Authorization": f"Bearer {token_admin.access_token}"},
        json={
            "email": email,
            "roles_to_assign": roles,
            "name": name,
        },
    )
    name = fake.name()
    second_response = app_client.post(
        "/users",
        headers={"Authorization": f"Bearer {token_admin.access_token}"},
        json={
            "email": email,
            "roles_to_assign": roles,
            "name": name,
        },
    )

    assert first_response.status_code == HTTPStatus.CREATED
    assert second_response.status_code == HTTPStatus.CONFLICT
    assert second_response.json()["detail"] == f"O email {email} já existe"


def test_comercial_should_not_create_users(
    token_comercial: TokenWithUser,
    app_client: TestClient,
):
    response = app_client.post(
        "/users",
        headers={"Authorization": f"Bearer {token_comercial.access_token}"},
        json={
            "email": "emailtest@test.com",
            "roles_to_assign": [RoleType.COMERCIAL],
            "name": "testzinho da silva",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_executor_should_not_create_users(
    token_executor: TokenWithUser,
    app_client: TestClient,
):
    response = app_client.post(
        "/users",
        headers={"Authorization": f"Bearer {token_executor.access_token}"},
        json={
            "email": "emailtest@test.com",
            "roles_to_assign": [RoleType.COMERCIAL],
            "name": "testzinho da silva",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_financeiro_should_not_create_users(
    token_financeiro: TokenWithUser,
    app_client: TestClient,
):
    response = app_client.post(
        "/users",
        headers={"Authorization": f"Bearer {token_financeiro.access_token}"},
        json={
            "email": "emailtest@test.com",
            "roles_to_assign": [RoleType.COMERCIAL],
            "name": "testzinho da silva",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_anyone_should_activate_user(
    app_client: TestClient,
    user_not_activated: UserMockWithPassword,
):
    response = app_client.patch(
        f"/users/{user_not_activated.id}/activate",
        json={"password": "senha123"},
    )
    user = response.json()
    assert response.status_code == HTTPStatus.OK
    assert user["email"] == user_not_activated.email
    assert user["name"] == user_not_activated.name
    assert "id" in user


def test_activate_user_shoud_have_valid_user_id(
    app_client: TestClient,
):
    response = app_client.patch(
        f"/users/{uuid.uuid4()}/activate",
        json={"password": "senha123"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Código do usuário não encontrado"


def test_activate_user_should_not_activate_activated_user(
    app_client: TestClient,
    user_comercial: UserMockWithPassword,
):
    response = app_client.patch(
        f"/users/{user_comercial.id}/activate",
        json={"password": "senha123"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()["detail"] == "O usuário já está ativado"


def test_read_comercials(
    app_client: TestClient,
    token_admin: TokenWithUser,
    db: Database,
):
    batch_size = 50
    UserFactory(
        db,
        batch_size=batch_size,
        activated_at=datetime.now(),
    )
    UserFactory(
        db,
        batch_size=batch_size,
        activated_at=datetime.now(),
        roles=[RoleType.COMERCIAL],
    )
    response = app_client.get(
        "/users/comercials",
        headers={"Authorization": f"Bearer {token_admin.access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    users = response.json()
    assert users["total"] >= batch_size
    assert all(
        {"role_type": RoleType.COMERCIAL.value} in user["roles"]
        for user in users["data"]
    )


def test_read_user_activation(
    app_client: TestClient,
    user_comercial: UserMockWithPassword,
):
    response = app_client.get(f"/users/{user_comercial.id}/activation")
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data["activated_at"] is not None


def test_read_user_activation_with_wrong_id(
    app_client: TestClient,
    user_comercial: UserMockWithPassword,
):
    response = app_client.get(f"/users/{uuid.uuid4()}/activation")
    assert response.status_code == HTTPStatus.NOT_FOUND
