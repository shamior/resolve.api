import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from pydantic import UUID4, EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.payment.repass_model import Repass
    from app.models.services.service_model import Service
    from app.models.services.service_notes_model import ServiceNotes


class UserRoles(str, Enum):
    COMERCIAL = "Comercial"
    EXECUTOR = "Executor"
    FINANCEIRO = "Financeiro"
    ADMIN = "Administrador"


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)
    role: UserRoles = Field()
    name: str = Field()


class UserCreate(UserBase):
    pass


class User(UserCreate, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    activated_at: Optional[datetime] = Field(default=None)
    password: str = Field()

    services_as_executor: List["Service"] = Relationship(
        back_populates="executor",
        sa_relationship_kwargs={"foreign_keys": "Service.executor_id"},
    )
    services_as_comercial: List["Service"] = Relationship(
        back_populates="comercial",
        sa_relationship_kwargs={"foreign_keys": "Service.comercial_id"},
    )

    repasses: List["Repass"] = Relationship(back_populates="receiver")
    service_notes: List["ServiceNotes"] = Relationship(back_populates="issuer")


class UserPresentable(UserBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)


class UserActivate(SQLModel):
    name: str = Field()
    password: str = Field()


class BasicUserPresentable(UserBase):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
