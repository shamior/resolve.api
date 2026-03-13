from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.appointment_entity import AppointmentEntity


class AppointmentPresentable(AppointmentEntity):
    id: UUID4 = Field()
