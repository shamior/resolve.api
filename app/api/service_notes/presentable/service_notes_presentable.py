from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.service_notes_entity import ServiceNotesEntity


class ServiceNotesPresentable(ServiceNotesEntity):
    id: UUID4 = Field()
