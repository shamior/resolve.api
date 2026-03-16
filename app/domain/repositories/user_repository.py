from datetime import datetime
from typing import Annotated, Optional, Sequence

from fastapi import Depends
from pydantic import UUID4, BaseModel, Field
from sqlmodel import col, or_, select

from app.domain.entities.user_entity import UserRoles
from app.infra.database.database import Database
from app.infra.database.models import User


class UserRepositoryFindManyFilters(BaseModel):
    name_or_email_contains: str = Field(default="")
    offset: int = Field(default=0, ge=0)
    limit: Optional[int] = Field(default=None, ge=1)
    roles_in: Optional[list[UserRoles]] = Field(default=None)
    fetch_only_not_deleted: bool = Field(default=True)
    fetch_only_active: bool = Field(default=True)


class UserRepositoryFactory:
    def __init__(self, db: Database) -> None:
        self.db = db

    @staticmethod
    def __get_select_clause(
        fetch_only_not_deleted=True, fetch_only_active=True
    ):
        select_clause = select(User)
        if fetch_only_not_deleted:
            select_clause = select_clause.where(col(User.deleted_at).is_(None))
        if fetch_only_active:
            select_clause = select_clause.where(
                col(User.activated_at).is_not(None)
            )
        return select_clause

    def find_many(
        self, filters: UserRepositoryFindManyFilters
    ) -> Sequence[User]:
        query = self.__get_select_clause(
            filters.fetch_only_not_deleted, filters.fetch_only_active
        )
        if filters.name_or_email_contains:
            query = query.where(
                or_(
                    col(User.name).contains(filters.name_or_email_contains),
                    col(User.email).contains(filters.name_or_email_contains),
                )
            )
        if filters.roles_in:
            query = query.where(col(User.role).in_(filters.roles_in))
        if filters.offset:
            query = query.offset(filters.offset)
        if filters.limit:
            query = query.limit(filters.limit)
        users = self.db.exec(query).all()
        return users

    def find_by_email(
        self, email: str, fetch_only_not_deleted=False, fetch_only_active=False
    ) -> User | None:
        user = self.db.exec(
            self.__get_select_clause(
                fetch_only_not_deleted, fetch_only_active
            ).where(User.email == email)
        ).one_or_none()
        return user

    def find_by_id(self, id: UUID4) -> User | None:
        user = self.db.exec(
            self.__get_select_clause(
                fetch_only_active=False, fetch_only_not_deleted=False
            ).where(User.id == id)
        ).one_or_none()
        return user

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User) -> User:
        user.updated_at = datetime.now()
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


UserRepository = Annotated[UserRepositoryFactory, Depends()]
