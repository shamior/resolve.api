from collections.abc import Sequence
from datetime import datetime
from typing import Annotated

from fastapi import Depends
from pydantic import UUID4, BaseModel, Field
from sqlmodel import col, func, or_, select

from app.domain.entities.user_role_entity import RoleType
from app.domain.repositories.user_role_repository import UserRoleRepository
from app.infra.database.database import Database
from app.infra.database.models import User, UserRole


class UserRepositoryFindManyFilters(BaseModel):
    name_or_email_contains: str = Field(default="")
    offset: int = Field(default=0, ge=0)
    limit: int | None = Field(default=None, ge=1)
    roles_in: list[RoleType] | None = Field(default=None)
    fetch_only_not_deleted: bool = Field(default=True)
    fetch_only_active: bool = Field(default=True)


class UserRepository:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.role_repo = UserRoleRepository(db)

    @staticmethod
    def __get_select_clause(
        fetch_only_not_deleted=True,
        fetch_only_active=True,
    ):
        select_clause = select(User)
        if fetch_only_not_deleted:
            select_clause = select_clause.where(col(User.deleted_at).is_(None))
        if fetch_only_active:
            select_clause = select_clause.where(
                col(User.activated_at).is_not(None),
            )
        return select_clause

    def find_many(
        self,
        filters: UserRepositoryFindManyFilters,
    ) -> tuple[Sequence[User], int]:
        query = self.__get_select_clause(
            filters.fetch_only_not_deleted,
            filters.fetch_only_active,
        )
        if filters.name_or_email_contains:
            query = query.where(
                or_(
                    col(User.name).contains(filters.name_or_email_contains),
                    col(User.email).contains(filters.name_or_email_contains),
                ),
            )
        if filters.roles_in:
            query = query.where(
                col(User.roles).any(
                    col(UserRole.role_type).in_(filters.roles_in),
                ),
            )
        count_query = select(func.count()).select_from(query.subquery())
        if filters.offset:
            query = query.offset(filters.offset)
        if filters.limit:
            query = query.limit(filters.limit)
        with self.db.begin_nested():
            users = self.db.exec(query).all()
            count = self.db.exec(count_query).one()
        return users, count

    def find_by_email(
        self,
        email: str,
        fetch_only_not_deleted=False,
        fetch_only_active=False,
    ) -> User | None:
        return self.db.exec(
            self.__get_select_clause(
                fetch_only_not_deleted,
                fetch_only_active,
            ).where(User.email == email),
        ).first()

    def find_by_id(self, id: UUID4) -> User | None:
        return self.db.exec(
            self.__get_select_clause(
                fetch_only_active=False,
                fetch_only_not_deleted=False,
            ).where(User.id == id),
        ).first()

    def create(self, user: User) -> User:
        user.updated_at = datetime.now()
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def create_user_with_roles(
        self,
        user: User,
        roles: list[RoleType],
    ) -> User:
        user.roles = self.role_repo.find_many_or_create(roles)
        return self.create(user)

    def update(self, user: User) -> User:
        user.updated_at = datetime.now()
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


UserRepositoryDep = Annotated[UserRepository, Depends()]
