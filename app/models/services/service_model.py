from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from app.models.services.service_type_model import ServiceType
from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.client_model import Client
    from app.models.payment.payment_model import Payment
    from app.models.services.appointment_model import Appointment
    from app.models.services.service_field_model import ServiceField
    from app.models.services.service_notes_model import ServiceNotes
    from app.models.services.service_status_model import ServiceStatus
    from app.models.user_model import User


class ServiceBase(SQLModel):
    started_at: datetime = Field(default_factory=datetime.now)
    finished_at: datetime | None = Field(default=None)

    client_id: UUID4 = Field(foreign_key="client.id")
    service_status_id: UUID4 = Field(foreign_key="servicestatus.id")
    executor_id: UUID4 = Field(foreign_key="user.id")
    comercial_id: UUID4 = Field(foreign_key="user.id")
    service_type_id: UUID4 = Field(foreign_key="servicetype.id")


class Service(ServiceBase, WithDateModel, table=True):
    id: Optional[int] = Field(primary_key=True)

    executor: "User" = Relationship(
        back_populates="services_as_executor",
        sa_relationship_kwargs={"foreign_keys": "Service.executor_id"},
    )
    comercial: "User" = Relationship(
        back_populates="services_as_executor",
        sa_relationship_kwargs={"foreign_keys": "Service.comercial_id"},
    )

    status: ServiceStatus = Relationship()
    client: "Client" = Relationship(back_populates="services")
    service_type: "ServiceType" = Relationship(back_populates="services")

    appointments: List["Appointment"] = Relationship(back_populates="service")
    payments: List["Payment"] = Relationship(back_populates="service")
    service_notes: List["ServiceNotes"] = Relationship(
        back_populates="service"
    )
    service_fields: List["ServiceField"] = Relationship(
        back_populates="service"
    )


class ServicePresentable(ServiceBase, WithDatePresentable):
    id: int = Field(primary_key=True)
