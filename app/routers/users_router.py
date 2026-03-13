from datetime import datetime
from typing import Sequence

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlmodel import select

from app.database import SessionDep
from app.helpers.pagination import Pagination, PaginationParams
from app.helpers.permission import Actions, PermissionChecker, Subjects
from app.helpers.security import get_password_hash
from app.models.aggregates import UserAggregate
from app.models.user_model import (
    BasicUserPresentable,
    User,
    UserActivate,
    UserCreate,
    UserPresentable,
    UserRoles,
)
from app.repositories.user_repository import UserRepository

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get(
    "/",
    response_model=Pagination[UserPresentable],
    dependencies=[
        Depends(PermissionChecker(subject=Subjects.USERS, action=Actions.READ))
    ],
)
async def read_users(
    user_repository: UserRepository,
    pagination: PaginationParams,
):
    users = user_repository.find_many()
    return Pagination(
        page=pagination.page,
        per_page=pagination.per_page,
        data=users,
        total=len(users),
    )


@user_router.post(
    "/",
    response_model=UserAggregate,
    dependencies=[
        Depends(
            PermissionChecker(subject=Subjects.USERS, action=Actions.CREATE)
        )
    ],
)
async def create_user(user: UserCreate, db: SessionDep):
    user_validated = User.model_validate(user)
    user_validated.password = get_password_hash(user_validated.password)
    db.add(user_validated)
    db.commit()
    db.refresh(user_validated)
    return user_validated


@user_router.patch("/{user_id}/activate", response_model=UserPresentable)
async def activate_user(
    user_id: UUID4, user_data: UserActivate, db: SessionDep
):
    user = db.exec(select(User).where(User.id == user_id)).one()
    user.password = get_password_hash(user_data.password)
    user.name = user_data.name
    user.updated_at = datetime.now()
    user.activated_at = datetime.now()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@user_router.get(
    "/comercials",
    response_model=Sequence[BasicUserPresentable],
    dependencies=[
        Depends(
            PermissionChecker(subject=Subjects.COMERCIALS, action=Actions.READ)
        )
    ],
)
async def read_comercials(db: SessionDep):
    users = db.exec(select(User).where(User.role == UserRoles.COMERCIAL)).all()
    return users
