from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class AppointmentStatus(str, Enum):
    SCHEDULED = "Agendado"
    FINISHED = "Concluído"


class AppointmentEntity(SQLModel):
    status: AppointmentStatus = Field(default=AppointmentStatus.SCHEDULED)
    scheduled_to: datetime = Field()
    site: str = Field()  # TODO: make a table
    service_id: Optional[int] = Field(default=None, foreign_key="service.id")
