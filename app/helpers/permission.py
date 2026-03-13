from enum import Enum
from http import HTTPStatus
from typing import List

from fastapi import HTTPException

from app.helpers.security import CurrentUser
from app.models.user_model import User, UserRoles


def user_permissions(action: Actions) -> List[UserRoles]:
    if action == Actions.READ:
        return [UserRoles.ADMIN]
    return [UserRoles.ADMIN]


def comercial_permissions(action: Actions) -> List[UserRoles]:
    if action == Actions.READ:
        return [UserRoles.ADMIN, UserRoles.EXECUTOR]
    return [UserRoles.ADMIN]


class Actions(str, Enum):
    READ = "READ"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class Subjects(str, Enum):
    USERS = "USERS"
    COMERCIALS = "COMERCIALS"


def subject_mapper(subject: Subjects):
    mapper = {
        Subjects.USERS: user_permissions,
        Subjects.COMERCIALS: comercial_permissions,
    }

    return mapper[subject]


class PermissionChecker:
    def __init__(self, subject: Subjects, action: Actions) -> None:
        self.subject = subject
        self.action = action

    def __call__(self, current_user: CurrentUser) -> User:
        allowed_roles = subject_mapper(self.subject)(self.action)
        allowed = self.permission_checker(
            user_roles=[current_user.role], allowed_roles=allowed_roles
        )
        if not allowed:
            raise HTTPException(
                HTTPStatus.FORBIDDEN,
                detail=f"Não é permitido usuário executar \
                    {self.action} em {self.subject}",
            )
        return User.model_validate(current_user)

    @staticmethod
    def permission_checker(
        user_roles: List[UserRoles], allowed_roles: List[UserRoles]
    ) -> bool:
        for user_role in user_roles:
            if user_role in allowed_roles:
                return True
        return False
