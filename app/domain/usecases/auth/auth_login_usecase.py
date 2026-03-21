from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException

from app.api.auth.presentable.token_presentable import TokenWithUser
from app.api.user.presentable.user_presentable import UserPresentable
from app.domain.helpers.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.domain.repositories.user_repository import UserRepositoryDep


class AuthLoginUseCase:
    def __init__(self, user_repository: UserRepositoryDep):
        self.user_repository = user_repository
        self.error = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Email ou senha incorreta",
        )

    def fetch_user(self, email: str):
        user = self.user_repository.find_by_email(email=email)

        if not user:
            raise self.error
        return user

    def execute(self, email: str, password: str):
        user = self.fetch_user(email=email)

        if not verify_password(password, user.password):
            raise self.error

        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email})

        return TokenWithUser(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserPresentable.model_validate(user),
        )


AuthLoginUseCaseDep = Annotated[AuthLoginUseCase, Depends()]
