from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import UUID4

from app.api.user.dto.user_activate_dto import UserActivate
from app.domain.helpers.security import get_password_hash
from app.domain.repositories.user_repository import UserRepositoryDep
from app.infra.database.models import User


class ActivateUserUseCase:
    def __init__(self, user_repository: UserRepositoryDep) -> None:
        self.user_repository = user_repository

    def execute(self, user_id: UUID4, user_data: UserActivate) -> User:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(
                HTTPStatus.NOT_FOUND,
                detail="Código do usuário não encontrado",
            )

        if user.activated_at is not None:
            raise HTTPException(
                HTTPStatus.FORBIDDEN,
                detail="O usuário já está ativado",
            )

        user.password = get_password_hash(user_data.password)
        user.activated_at = datetime.now()
        self.user_repository.update(user)
        return user


ActivateUserUseCaseDep = Annotated[ActivateUserUseCase, Depends()]
