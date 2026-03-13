import uuid
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.services.service_field_type_model import ServiceFieldType
    from app.models.services.service_model import Service


class ServiceFieldBase(SQLModel):
    value: str = Field()
    field_type_id: UUID4 = Field(foreign_key="servicefieldtype.id")
    service_id: UUID4 = Field(foreign_key="service.id")


class ServiceField(ServiceFieldBase, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    service: "Service" = Relationship(back_populates="service_fields")
    field_type: "ServiceFieldType" = Relationship(
        back_populates="service_fields"
    )


class ServiceFieldPresentable(ServiceFieldBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
