from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserRoles(str, Enum):
    COMERCIAL = "Comercial"
    EXECUTOR = "Executor"
    FINANCEIRO = "Financeiro"
    ADMIN = "Administrador"


class UserEntity(SQLModel):
    email: EmailStr = Field(unique=True)
    role: UserRoles = Field()
    name: str = Field()
    activated_at: Optional[datetime] = Field(default=None)
    password: str = Field()
