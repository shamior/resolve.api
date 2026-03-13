import uuid
from typing import TYPE_CHECKING, List

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from app.models.services.field_link_model import FieldLink
from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.services.service_field_type_model import ServiceFieldType
    from app.models.services.service_model import Service


class ServiceTypeBase(SQLModel):
    name: str = Field()
    schedulable: bool = Field()


class ServiceType(ServiceTypeBase, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    services: List["Service"] = Relationship(back_populates="service_type")
    field_types: List["ServiceFieldType"] = Relationship(
        back_populates="service_types", link_model=FieldLink
    )


class ServiceTypePresentable(ServiceTypeBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
