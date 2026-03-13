from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.repass_entity import RepassEntity


class RepassPresentable(RepassEntity):
    id: UUID4 = Field()
