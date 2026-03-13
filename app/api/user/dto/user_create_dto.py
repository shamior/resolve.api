from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.domain.entities.user_entity import UserRoles


class UserCreate(SQLModel):
    email: EmailStr = Field(unique=True)
    role: UserRoles = Field()
    name: str = Field()
