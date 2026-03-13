from datetime import datetime
from typing import Sequence

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlmodel import select

from app.api.user.dto.user_activate_dto import UserActivate
from app.api.user.dto.user_create_dto import UserCreate
from app.api.user.presentable.user_presentable import UserPresentable
from app.domain.entities.user_entity import UserRoles
from app.domain.helpers.pagination import Pagination, PaginationParams
from app.domain.helpers.permission import Actions, PermissionChecker, Subjects
from app.domain.helpers.security import get_password_hash
from app.domain.repositories.user_repository import UserRepository
from app.infra.database.database import Database
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
    response_model=UserPresentable,
    dependencies=[
        Depends(
            PermissionChecker(subject=Subjects.USERS, action=Actions.CREATE)
        )
    ],
)
async def create_user(user: UserCreate, db: Database):
    user_validated = User.model_validate(user)
    user_validated.password = get_password_hash(user_validated.password)
    db.add(user_validated)
    db.commit()
    db.refresh(user_validated)
    return user_validated


@user_router.patch("/{user_id}/activate", response_model=UserPresentable)
async def activate_user(user_id: UUID4, user_data: UserActivate, db: Database):
    user = db.exec(select(User).where(User.id == user_id)).one()
    user.password = get_password_hash(user_data.password)
    user.updated_at = datetime.now()
    user.activated_at = datetime.now()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@user_router.get(
    "/comercials",
    response_model=Sequence[UserPresentable],
    dependencies=[
        Depends(
            PermissionChecker(subject=Subjects.COMERCIALS, action=Actions.READ)
        )
    ],
)
async def read_comercials(db: Database):
    users = db.exec(select(User).where(User.role == UserRoles.COMERCIAL)).all()
    return users
