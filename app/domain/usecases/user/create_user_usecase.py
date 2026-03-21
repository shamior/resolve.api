from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException

from app.api.user.dto.user_create_dto import UserCreate
from app.domain.helpers.security import get_password_hash
from app.domain.repositories.user_repository import UserRepositoryDep
from app.infra.database.models import User


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepositoryDep) -> None:
        self.user_repository = user_repository

    def execute(self, user: UserCreate) -> User:
        user_validated = User.model_validate(user)
        user_validated.password = get_password_hash(user_validated.password)

        user_found = self.user_repository.find_by_email(user_validated.email)
        if user_found:
            raise HTTPException(
                HTTPStatus.CONFLICT,
                f"O email {user.email} já existe",
            )

        return self.user_repository.create_user_with_roles(
            user_validated,
            user.roles_to_assign,
        )


CreateUserUseCaseDep = Annotated[CreateUserUseCase, Depends()]
