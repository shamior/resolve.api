from typing import Annotated

from fastapi import Depends
from sqlmodel import col, select

from app.domain.entities.user_role_entity import RoleType
from app.infra.database.database import Database
from app.infra.database.models import UserRole


class UserRoleRepository:
    def __init__(self, db: Database):
        self.db = db

    def find_role_by_type(self, role_type: RoleType):
        select_clause = select(UserRole).filter(
            col(UserRole.role_type) == role_type,
        )
        role = self.db.exec(select_clause).first()
        return role

    def create_role(self, role_type: RoleType):
        role = UserRole(role_type=role_type)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def find_or_create_role(self, role_type: RoleType):
        role = self.find_role_by_type(role_type)
        if not role:
            role = self.create_role(role_type)
        return role

    def find_many_or_create(self, roles: list[RoleType]):
        roles_found: list[UserRole] = []
        for role_type in roles:
            role = self.find_or_create_role(role_type)
            roles_found.append(role)
        return roles_found


UserRoleRepositoryDep = Annotated[UserRoleRepository, Depends()]
