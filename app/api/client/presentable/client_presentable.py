from pydantic import UUID4
from sqlmodel import Field

from app.api.countries.presentable.country_presentable import (
    CountryPresentable,
)
from app.domain.entities.client_entity import ClientEntity


class ClientPresentable(ClientEntity):
    id: UUID4 = Field()

    country: CountryPresentable = Field()
