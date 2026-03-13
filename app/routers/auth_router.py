from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import col, select

from app.database import SessionDep
from app.helpers.security import (
    CurrentUser,
    create_access_token,
    verify_password,
)
from app.models.user_model import User

auth_router = APIRouter(prefix="/auth", tags=["auth"])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


class Token(BaseModel):
    access_token: str
    token_type: str


@auth_router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2Form, db: SessionDep):
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

    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/refresh_token", response_model=Token)
async def refresh_access_token(user: CurrentUser):
    new_access_token = create_access_token(data={"sub": user.email})

    return Token(access_token=new_access_token, token_type="bearer")
