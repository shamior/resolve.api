from http import HTTPStatus

from starlette.testclient import TestClient

from app.api.auth.presentable.token_presentable import TokenWithUser


def test_country_all_access(
    app_client: TestClient,
    token_all_roles: TokenWithUser,
):
    response = app_client.get(
        "/countries",
        headers={"Authorization": f"Bearer {token_all_roles.access_token}"},
    )
    assert response.status_code == HTTPStatus.OK


def test_country_access_unauthorized(
    app_client: TestClient,
):
    response = app_client.get("/countries")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
