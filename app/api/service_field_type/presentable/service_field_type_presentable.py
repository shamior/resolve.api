from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.service_field_type_entity import (
    ServiceFieldTypeEntity,
)


class ServiceFieldTypePresentable(ServiceFieldTypeEntity):
    id: UUID4 = Field()
