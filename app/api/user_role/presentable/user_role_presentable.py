from sqlmodel import SQLModel

from app.domain.entities.user_role_entity import RoleType


class UserRolePresentable(SQLModel):
    role_type: RoleType
