from http import HTTPStatus

from jwt import decode
from starlette.testclient import TestClient

from app.domain.helpers.security import create_access_token


def test_jwt(settings):
    data = {"test": "testvalue"}
    token = create_access_token(data)

    decoded = decode(token, settings.JWT_SECRET, settings.ALGORITHM)

    assert decoded["test"] == "testvalue"
    assert "exp" in decoded


def test_jwt_with_invalid_token(app_client: TestClient):
    response = app_client.get(
        "/users",
        headers={"Authorization": "Bearer bomba"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_jwt_without_email(app_client: TestClient):
    response = app_client.get(
        "/users",
        headers={"Authorization": f"Bearer {create_access_token({})}"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_jwt_with_no_valid_email(app_client: TestClient):
    response = app_client.get(
        "/users",
        headers={
            "Authorization": f"Bearer {create_access_token({'sub': 'email'})}",
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
