from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import UUID4

from app.domain.repositories.user_repository import UserRepositoryDep
from app.infra.database.models import User


class ReadUserActivationUseCase:
    def __init__(self, user_repository: UserRepositoryDep) -> None:
        self.user_repository = user_repository

    def execute(self, user_id: UUID4) -> User:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(
                HTTPStatus.NOT_FOUND,
                detail="Código do usuário não encontrado",
            )
        return user


ReadUserActivationUseCaseDep = Annotated[ReadUserActivationUseCase, Depends()]
