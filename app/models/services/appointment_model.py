import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.services.service_model import Service


class AppointmentStatus(str, Enum):
    SCHEDULED = "Agendado"
    FINISHED = "Concluído"


class AppointmentBase(SQLModel):
    status: AppointmentStatus = Field(default=AppointmentStatus.SCHEDULED)
    scheduled_to: datetime = Field()
    site: str = Field()  # TODO: make a table
    service_id: UUID4 = Field(foreign_key="service.id")


class Appointment(AppointmentBase, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    service: "Service" = Relationship(back_populates="appointments")


class AppointmentPresentable(AppointmentBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
