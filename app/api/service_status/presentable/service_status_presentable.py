from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.service_status_entity import ServiceStatusEntity


class ServiceStatusPresentable(ServiceStatusEntity):
    id: UUID4 = Field()
