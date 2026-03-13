import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List

from pydantic import UUID4, EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.services.service_model import Service


class LoggedInAs(str, Enum):
    NOT_LOGGED_IN = "Nenhum Login"
    THUNDERBIRD = "Thunderbird"


class ClientBase(SQLModel):
    name: str = Field()
    phone: str = Field()
    citizenship: str = Field()  # TODO: deixar de ser string
    birthdate: datetime = Field()
    email: EmailStr = Field()
    passport: str = Field()
    logged_in_as: LoggedInAs = Field(default=LoggedInAs.NOT_LOGGED_IN)


class Client(ClientBase, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    services: List["Service"] = Relationship(back_populates="client")
    documents: List["Document"] = Relationship(back_populates="client")


class ClientPresentable(ClientBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)


###########################################################################################
class DocumentBase(SQLModel):
    name: str = Field()
    path: str = Field()
    client_id: UUID4 = Field(foreign_key="client.id")


class Document(DocumentBase, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    client: "Client" = Relationship(back_populates="documents")


class DocumentPresentable(DocumentBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
