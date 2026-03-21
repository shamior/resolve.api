from http import HTTPStatus

from fastapi import APIRouter, Depends
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
from app.domain.helpers.pagination import (
    Pagination,
    PaginationParams,
)
from app.domain.helpers.permission import Actions, PermissionChecker, Subjects
from app.domain.usecases.user.activate_user_usecase import (
    ActivateUserUseCaseDep,
)
from app.domain.usecases.user.create_user_usecase import CreateUserUseCaseDep
from app.domain.usecases.user.read_comercials_usecase import (
    ReadComercialsUseCaseDep,
)
from app.domain.usecases.user.read_user_activation_usecase import (
    ReadUserActivationUseCaseDep,
)
from app.domain.usecases.user.read_users_usecase import ReadUsersUseCaseDep

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get(
    "/",
    response_model=Pagination[UserPresentable],
    dependencies=[
        Depends(
            PermissionChecker(subject=Subjects.USERS, action=Actions.READ),
        ),
    ],
)
async def read_users(
    pagination: PaginationParams,
    read_users_usecase: ReadUsersUseCaseDep,
    filters: ReadUsersQueryParams,
    roles_in: RolesIn = [],
):
    return read_users_usecase.execute(pagination, filters, roles_in)


@user_router.post(
    "/",
    response_model=UserPresentable,
    status_code=HTTPStatus.CREATED,
    dependencies=[
        Depends(
            PermissionChecker(subject=Subjects.USERS, action=Actions.CREATE),
        ),
    ],
)
async def create_user(
    user: UserCreate,
    create_user_usecase: CreateUserUseCaseDep,
):
    user_created = create_user_usecase.execute(user)
    return user_created


@user_router.patch("/{user_id}/activate", response_model=UserPresentable)
async def activate_user(
    user_id: UUID4,
    user_data: UserActivate,
    activate_user_usecase: ActivateUserUseCaseDep,
):
    user_activated = activate_user_usecase.execute(user_id, user_data)
    return user_activated


@user_router.get(
    "/{user_id}/activation",
    response_model=UserActivationPresentable,
)
async def read_user_activation(
    user_id: UUID4,
    read_user_activation_usecase: ReadUserActivationUseCaseDep,
):
    user = read_user_activation_usecase.execute(user_id)
    return user


@user_router.get(
    "/comercials",
    response_model=Pagination[UserPresentable],
    dependencies=[
        Depends(
            PermissionChecker(
                subject=Subjects.COMERCIALS,
                action=Actions.READ,
            ),
        ),
    ],
)
async def read_comercials(
    read_comercials_usecase: ReadComercialsUseCaseDep,
    filters: ReadUsersQueryParams,
    pagination: PaginationParams,
):
    comercials = read_comercials_usecase.execute(pagination, filters)
    return comercials
