from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.domain.entities.user_role_entity import RoleType


class UserCreate(SQLModel):
    email: EmailStr = Field(unique=True)
    roles_to_assign: list[RoleType] = Field(min_items=1)
    name: str = Field()
