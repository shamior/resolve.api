from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.client_entity import ClientEntity


class ClientPresentable(ClientEntity):
    id: UUID4 = Field()
