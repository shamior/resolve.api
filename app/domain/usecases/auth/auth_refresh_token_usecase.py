from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from jwt import DecodeError, ExpiredSignatureError, decode

from app.api.auth.presentable.token_presentable import TokenWithUser
from app.api.user.presentable.user_presentable import UserPresentable
from app.domain.config.env_config.settings import settings
from app.domain.helpers.security import (
    create_access_token,
    create_refresh_token,
)
from app.domain.repositories.user_repository import UserRepositoryDep


class AuthRefreshTokenUseCase:
    def __init__(
        self,
        user_repository: UserRepositoryDep,
    ):
        self.user_repository = user_repository
        self.error = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def fetch_user(self, email: str):
        user = self.user_repository.find_by_email(email=email)
        if not user:
            raise self.error
        return user

    def extract_email_from_token(self, token: str):
        try:
            payload = decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.ALGORITHM],
            )
            subject_email = payload.get("sub")
            if not subject_email:
                raise self.error

        except DecodeError:
            raise self.error

        except ExpiredSignatureError:
            raise self.error

        return subject_email

    def execute(self, refresh_token: str):
        email = self.extract_email_from_token(refresh_token)
        new_access_token = create_access_token({"sub": email})
        new_refresh_token = create_refresh_token({"sub": email})
        user = self.fetch_user(email=email)

        return TokenWithUser(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            user=UserPresentable.model_validate(user),
        )


AuthRefreshTokenUseCaseDep = Annotated[AuthRefreshTokenUseCase, Depends()]
