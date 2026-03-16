from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from app.api.user.dto.user_activate_dto import UserActivate
from app.api.user.dto.user_create_dto import UserCreate
from app.api.user.dto.user_read_params_dto import (
    ReadUsersQueryParams,
    RolesIn,
)
from app.api.user.presentable.user_activation_presentable import (
    UserActivationPresentable,
)
from app.api.user.presentable.user_presentable import UserPresentable
from app.domain.entities.user_entity import UserRoles
from app.domain.helpers.pagination import (
    Pagination,
    PaginationParams,
    get_offset,
    get_total_pages,
)
from app.domain.helpers.permission import Actions, PermissionChecker, Subjects
from app.domain.helpers.security import get_password_hash
from app.domain.repositories.user_repository import (
    UserRepository,
    UserRepositoryFindManyFilters,
)
from app.infra.database.models import User

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get(
    "/",
    response_model=Pagination[UserPresentable],
    dependencies=[
        Depends(PermissionChecker(subject=Subjects.USERS, action=Actions.READ))
    ],
)
async def read_users(
    pagination: PaginationParams,
    user_repository: UserRepository,
    filters: ReadUsersQueryParams,
    roles_in: RolesIn = [],
):
    offset = get_offset(pagination)
    users = user_repository.find_many(
        UserRepositoryFindManyFilters(
            name_or_email_contains=filters.name_or_email_contains,
            roles_in=roles_in,
            offset=offset,
            limit=pagination.per_page,
        )
    )
    total = len(
        user_repository.find_many(
            UserRepositoryFindManyFilters(
                name_or_email_contains=filters.name_or_email_contains,
                roles_in=roles_in,
            )
        )
    )
    return Pagination(
        page=pagination.page,
        per_page=pagination.per_page,
        data=users,
        total=total,
        total_pages=get_total_pages(total=total, per_page=pagination.per_page),
    )


@user_router.post(
    "/",
    response_model=UserPresentable,
    status_code=HTTPStatus.CREATED,
    dependencies=[
        Depends(
            PermissionChecker(subject=Subjects.USERS, action=Actions.CREATE)
        )
    ],
)
async def create_user(user: UserCreate, user_repository: UserRepository):
    user_validated = User.model_validate(user)
    user_validated.password = get_password_hash(user_validated.password)
    user_found = user_repository.find_by_email(user_validated.email)
    if user_found:
        raise HTTPException(
            HTTPStatus.CONFLICT, f"O email {user.email} já existe"
        )
    user_repository.create(user_validated)
    return user_validated


@user_router.patch("/{user_id}/activate", response_model=UserPresentable)
async def activate_user(
    user_id: UUID4, user_data: UserActivate, user_repository: UserRepository
):
    user = user_repository.find_by_id(user_id)
    if not user:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail="Código do usuário não encontrado"
        )

    if user.activated_at is not None:
        raise HTTPException(
            HTTPStatus.FORBIDDEN, detail="O usuário já está ativado"
        )

    user.password = get_password_hash(user_data.password)
    user.activated_at = datetime.now()
    user_repository.update(user)
    return user


@user_router.get(
    "/{user_id}/activation", response_model=UserActivationPresentable
)
async def read_user_activation(
    user_id: UUID4, user_repository: UserRepository
):
    user = user_repository.find_by_id(user_id)
    if not user:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail="Código do usuário não encontrado"
        )
    return user


@user_router.get(
    "/comercials",
    response_model=Pagination[UserPresentable],
    dependencies=[
        Depends(
            PermissionChecker(subject=Subjects.COMERCIALS, action=Actions.READ)
        )
    ],
)
async def read_comercials(
    user_repository: UserRepository,
    filters: ReadUsersQueryParams,
    pagination: PaginationParams,
):
    users = user_repository.find_many(
        UserRepositoryFindManyFilters(
            name_or_email_contains=filters.name_or_email_contains,
            roles_in=[UserRoles.COMERCIAL],
            offset=get_offset(pagination),
        )
    )
    total = len(
        user_repository.find_many(
            UserRepositoryFindManyFilters(
                name_or_email_contains=filters.name_or_email_contains,
                roles_in=[UserRoles.COMERCIAL],
                offset=get_offset(pagination),
            )
        )
    )
    return Pagination(
        data=users,
        page=pagination.page,
        per_page=pagination.per_page,
        total=total,
        total_pages=get_total_pages(total=total, per_page=pagination.per_page),
    )
