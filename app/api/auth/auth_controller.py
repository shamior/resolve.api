from fastapi import APIRouter

from app.api.auth.dto.auth_form_dto import OAuth2Form
from app.api.auth.dto.auth_refresh_dto import RefreshDTO
from app.api.auth.presentable.token_presentable import TokenWithUser
from app.domain.usecases.auth.auth_login_usecase import AuthLoginUseCaseDep
from app.domain.usecases.auth.auth_refresh_token_usecase import (
    AuthRefreshTokenUseCaseDep,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token", response_model=TokenWithUser)
async def login_for_access_token(
    form_data: OAuth2Form,
    login_usecase: AuthLoginUseCaseDep,
):
    token_with_user = login_usecase.execute(
        email=form_data.username,
        password=form_data.password,
    )

    return token_with_user


@auth_router.post("/refresh_token", response_model=TokenWithUser)
async def refresh_access_token(
    body: RefreshDTO,
    refresh_token_usecase: AuthRefreshTokenUseCaseDep,
):
    token = refresh_token_usecase.execute(body.refresh_token)
    return token
