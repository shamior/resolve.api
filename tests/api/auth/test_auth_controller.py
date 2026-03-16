from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi.testclient import TestClient
from freezegun import freeze_time

from app.api.auth.presentable.token_presentable import TokenWithUser
from app.domain.config.env_config.settings import Settings
from app.domain.helpers.security import create_refresh_token
from tests.mocks.user_mock import UserMockWithPassword


def test_get_token(
    app_client: TestClient, user_comercial: UserMockWithPassword
):
    response = app_client.post(
        "/auth/token",
        data={
            "username": user_comercial.email,
            "password": user_comercial.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_get_token_expired(
    app_client: TestClient,
    user_admin: UserMockWithPassword,
    settings: Settings,
):
    date = datetime(2026, 3, 15)

    def get_date():
        return date

    def get_expired_date():
        return date + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    with freeze_time(get_date):
        response = app_client.post(
            "/auth/token",
            data={
                "username": user_admin.email,
                "password": user_admin.clean_password,
            },
        )
        token = response.json()["access_token"]

    with freeze_time(get_expired_date):
        response = app_client.get(
            "/users", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_token_almost_expired(
    app_client: TestClient,
    user_admin: UserMockWithPassword,
    settings: Settings,
):
    date = datetime(2026, 3, 15)

    def get_date():
        return date

    def get_almost_expired_date():
        return (
            date
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            - timedelta(seconds=1)
        )

    with freeze_time(get_date):
        response = app_client.post(
            "/auth/token",
            data={
                "username": user_admin.email,
                "password": user_admin.clean_password,
            },
        )
        token = response.json()["access_token"]

    with freeze_time(get_almost_expired_date):
        response = app_client.get(
            "/users", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == HTTPStatus.OK


def test_login_with_no_email_found(
    app_client: TestClient, user_admin: UserMockWithPassword
):
    response = app_client.post(
        "/auth/token",
        data={
            "username": "thisemailwillnotbefound@email.com",
            "password": user_admin.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_login_with_wrong_password(
    app_client: TestClient, user_admin: UserMockWithPassword
):
    response = app_client.post(
        "/auth/token",
        data={
            "username": user_admin.email,
            "password": "wrongpassword123",
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_refresh_token(app_client: TestClient, token_comercial: TokenWithUser):
    response = app_client.post(
        "/auth/refresh_token",
        json={"refresh_token": token_comercial.refresh_token},
    )
    assert response.status_code == HTTPStatus.OK


def test_refresh_invalid_credentials(app_client: TestClient):
    response = app_client.post(
        "/auth/refresh_token",
        json={"refresh_token": "invalidcredential"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_refresh_without_email(app_client: TestClient):
    response = app_client.post(
        "/auth/refresh_token",
        json={"refresh_token": create_refresh_token({})},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_refresh_with_email_not_in_database(app_client: TestClient):
    response = app_client.post(
        "/auth/refresh_token",
        json={
            "refresh_token": create_refresh_token({
                "sub": "thisemailisnotindatabase@email.com"
            })
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_refresh_token_expired(
    app_client: TestClient,
    user_admin: UserMockWithPassword,
    settings: Settings,
):
    date = datetime(2026, 3, 15)

    def get_date():
        return date

    def get_expired_date():
        return date + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    with freeze_time(get_date):
        response = app_client.post(
            "/auth/token",
            data={
                "username": user_admin.email,
                "password": user_admin.clean_password,
            },
        )
        token = response.json()["refresh_token"]

    with freeze_time(get_expired_date):
        response = app_client.post(
            "/auth/refresh_token", json={"refresh_token": token}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_refresh_token_almost_expired(
    app_client: TestClient,
    user_admin: UserMockWithPassword,
    settings: Settings,
):
    date = datetime(2026, 3, 15)

    def get_date():
        return date

    def get_almost_expired_date():
        return (
            date
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            - timedelta(seconds=1)
        )

    with freeze_time(get_date):
        response = app_client.post(
            "/auth/token",
            data={
                "username": user_admin.email,
                "password": user_admin.clean_password,
            },
        )
        token = response.json()["refresh_token"]

    with freeze_time(get_almost_expired_date):
        response = app_client.post(
            "/auth/refresh_token", json={"refresh_token": token}
        )
        assert response.status_code == HTTPStatus.OK
