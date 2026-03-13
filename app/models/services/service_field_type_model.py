import uuid
from typing import TYPE_CHECKING, List

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from app.models.services.field_link_model import FieldLink
from app.models.services.service_type_model import ServiceType
from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.services.service_field_model import ServiceField


class ServiceFieldTypeBase(SQLModel):
    name: str = Field()
    field_type: str = Field()
    accepted_values: str = Field()  # TODO: ARRAY DE STRINGS


class ServiceFieldType(ServiceFieldTypeBase, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    service_fields: List["ServiceField"] = Relationship(
        back_populates="field_type"
    )
    service_types: List["ServiceType"] = Relationship(
        back_populates="field_types", link_model=FieldLink
    )


class ServiceFieldTypePresentable(ServiceFieldTypeBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
