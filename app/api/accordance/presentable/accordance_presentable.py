from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.accordance_entity import AccordanceEntity


class AccordancePresentable(AccordanceEntity):
    id: UUID4 = Field()
