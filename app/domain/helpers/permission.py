from enum import Enum
from http import HTTPStatus

from fastapi import HTTPException

from app.domain.entities.user_role_entity import RoleType
from app.domain.helpers.security import CurrentUser
from app.infra.database.models import User

all_roles = [
    RoleType.ADMIN,
    RoleType.EXECUTOR,
    RoleType.FINANCEIRO,
    RoleType.COMERCIAL,
]

admin = [RoleType.ADMIN]
executor = [RoleType.EXECUTOR, RoleType.ADMIN]
financeiro = [RoleType.FINANCEIRO, RoleType.ADMIN]
comercial = [RoleType.COMERCIAL, RoleType.ADMIN]

executor_comercial = [RoleType.EXECUTOR, RoleType.COMERCIAL, RoleType.ADMIN]
executor_financeiro = [RoleType.EXECUTOR, RoleType.FINANCEIRO, RoleType.ADMIN]
comercial_financeiro = [
    RoleType.COMERCIAL,
    RoleType.FINANCEIRO,
    RoleType.ADMIN,
]


def user_permissions(action: Actions) -> list[RoleType]:
    if action == Actions.READ:
        return admin
    return admin


def comercial_permissions(_action: Actions) -> list[RoleType]:
    return executor


def country_permissions(_action: Actions) -> list[RoleType]:
    return all_roles


def document_permissions(action: Actions) -> list[RoleType]:
    if action == Actions.READ:
        return all_roles
    else:
        return executor


class Actions(str, Enum):
    READ = "READ"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class Subjects(str, Enum):
    USERS = "USERS"
    COMERCIALS = "COMERCIALS"
    COUNTRIES = "COUNTRIES"
    DOCUMENTS = "DOCUMENTS"


def subject_mapper(subject: Subjects):
    mapper = {
        Subjects.USERS: user_permissions,
        Subjects.COMERCIALS: comercial_permissions,
        Subjects.COUNTRIES: country_permissions,
        Subjects.DOCUMENTS: document_permissions,
    }

    return mapper[subject]


class PermissionChecker:
    def __init__(self, subject: Subjects, action: Actions) -> None:
        self.subject = subject
        self.action = action

    def __call__(self, current_user: CurrentUser) -> User:
        allowed_roles = subject_mapper(self.subject)(self.action)
        allowed = self.permission_checker(
            user_roles=[role.role_type for role in current_user.roles],
            allowed_roles=allowed_roles,
        )
        if not allowed:
            raise HTTPException(
                HTTPStatus.FORBIDDEN,
                detail=f"Não é permitido usuário executar \
                    {self.action} em {self.subject}",
            )
        return current_user

    @staticmethod
    def permission_checker(
        user_roles: list[RoleType],
        allowed_roles: list[RoleType],
    ) -> bool:
        return any(user_role in allowed_roles for user_role in user_roles)
