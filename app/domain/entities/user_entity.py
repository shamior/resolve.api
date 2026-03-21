from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserEntity(SQLModel):
    email: EmailStr = Field(unique=True)
    name: str = Field()
    activated_at: Optional[datetime] = Field(default=None)
    password: str = Field(default="")
