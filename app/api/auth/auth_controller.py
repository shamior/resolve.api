from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlmodel import col, select

from app.api.auth.dto.auth_form_dto import OAuth2Form
from app.api.auth.presentable.token_presentable import TokenWithUser
from app.api.user.presentable.user_presentable import UserPresentable
from app.domain.helpers.security import (
    CurrentUser,
    create_access_token,
    verify_password,
)
from app.infra.database.database import Database
from app.infra.database.models import User

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token", response_model=TokenWithUser)
def login_for_access_token(form_data: OAuth2Form, db: Database):
    user = db.exec(
        select(User)
        .where(User.email == form_data.username)
        .where(col(User.activated_at).is_not(None))
    ).one_or_none()

    unauthorized = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Email ou senha incorreta",
    )

    if not user:
        raise unauthorized

    if not verify_password(form_data.password, user.password):
        raise unauthorized

    access_token = create_access_token(data={"sub": user.email})

    return TokenWithUser(
        access_token=access_token,
        token_type="bearer",
        user=UserPresentable.model_validate(user),
    )


@auth_router.post("/refresh_token", response_model=TokenWithUser)
async def refresh_access_token(user: CurrentUser):
    new_access_token = create_access_token(data={"sub": user.email})

    return TokenWithUser(
        access_token=new_access_token,
        token_type="bearer",
        user=UserPresentable.model_validate(user),
    )
