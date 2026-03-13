from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.service_field_entity import ServiceFieldEntity


class ServiceFieldPresentable(ServiceFieldEntity):
    id: UUID4 = Field()
