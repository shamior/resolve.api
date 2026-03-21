from enum import Enum

from sqlmodel import Field, SQLModel


class RoleType(str, Enum):
    COMERCIAL = "Comercial"
    EXECUTOR = "Executor"
    FINANCEIRO = "Financeiro"
    ADMIN = "Administrador"


class UserRoleEntity(SQLModel):
    role_type: RoleType = Field(..., description="Tipo de cargo do usuário")
