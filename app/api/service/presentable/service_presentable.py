from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.service_entity import ServiceEntity


class ServicePresentable(ServiceEntity):
    id: UUID4 = Field()
