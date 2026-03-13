from pydantic import UUID4, EmailStr
from sqlmodel import Field, SQLModel

from app.domain.entities.user_entity import UserRoles


class UserPresentable(SQLModel):
    id: UUID4 = Field()
    name: str = Field()
    email: EmailStr = Field(unique=True)
    role: UserRoles = Field()
