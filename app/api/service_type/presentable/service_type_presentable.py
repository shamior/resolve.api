from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.service_type_entity import ServiceTypeEntity


class ServiceTypePresentable(ServiceTypeEntity):
    id: UUID4 = Field()
