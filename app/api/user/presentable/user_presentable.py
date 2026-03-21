from pydantic import UUID4, EmailStr
from sqlmodel import Field, SQLModel

from app.api.user_role.presentable.user_role_presentable import (
    UserRolePresentable,
)


class UserPresentable(SQLModel):
    id: UUID4 = Field()
    name: str = Field()
    email: EmailStr = Field(unique=True)
    roles: list[UserRolePresentable]
