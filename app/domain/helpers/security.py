from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlmodel import col, select

from app.domain.config.env_config.settings import settings
from app.infra.database.database import Database
from app.infra.database.models import User

hasher = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return hasher.verify(plain_password, hashed_password)


def get_password_hash(password):
    return hasher.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(
    db: Database,
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get("sub")

        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    user = db.exec(
        select(User)
        .where(User.email == subject_email)
        .where(col(User.activated_at).is_not(None))
    ).one_or_none()

    if not user:
        raise credentials_exception

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
