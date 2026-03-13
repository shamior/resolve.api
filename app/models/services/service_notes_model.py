import uuid
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.services.service_model import Service
    from app.models.user_model import User


class ServiceNotesBase(SQLModel):
    content: str = Field()
    service_id: UUID4 = Field(foreign_key="service.id")
    issuer_id: UUID4 = Field(foreign_key="user.id")


class ServiceNotes(ServiceNotesBase, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    service: "Service" = Relationship(back_populates="service_notes")
    issuer: "User" = Relationship(back_populates="service_notes")


class ServiceNotesPresentable(ServiceNotesBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
