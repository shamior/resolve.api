from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from jwt import DecodeError, ExpiredSignatureError, decode

from app.api.auth.dto.auth_form_dto import OAuth2Form
from app.api.auth.dto.auth_refresh_dto import RefreshDTO
from app.api.auth.presentable.token_presentable import TokenWithUser
from app.api.user.presentable.user_presentable import UserPresentable
from app.domain.config.env_config.settings import settings
from app.domain.helpers.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.domain.repositories.user_repository import UserRepository

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token", response_model=TokenWithUser)
async def login_for_access_token(
    form_data: OAuth2Form, user_repository: UserRepository
):
    user = user_repository.find_by_email(email=form_data.username)

    unauthorized = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Email ou senha incorreta",
    )

    if not user:
        raise unauthorized

    if not verify_password(form_data.password, user.password):
        raise unauthorized

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return TokenWithUser(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserPresentable.model_validate(user),
    )


@auth_router.post("/refresh_token", response_model=TokenWithUser)
async def refresh_access_token(
    body: RefreshDTO, user_repository: UserRepository
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            body.refresh_token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
        )
        subject_email = payload.get("sub")
        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    new_access_token = create_access_token({"sub": subject_email})
    new_refresh_token = create_refresh_token({"sub": subject_email})
    user = user_repository.find_by_email(email=subject_email)

    if not user:
        raise credentials_exception

    return TokenWithUser(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        user=UserPresentable.model_validate(user),
    )
