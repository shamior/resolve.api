import pytest

from app.domain.repositories.country_repository import CountryRepository
from app.infra.database.database import Database
from app.infra.database.models import Country


@pytest.fixture
def country_repository(db: Database):
    return CountryRepository(db)


def test_find_by_code(country_repository: CountryRepository):
    country_repository.db.add(Country(code="BRA", name="Brasil"))
    country = country_repository.find_by_code("BRA")
    assert country is not None
    assert country.name == "Brasil"


def test_find_many(country_repository: CountryRepository):
    country_repository.db.add(Country(code="BRA", name="Brasil"))
    country_repository.db.add(Country(code="USA", name="United States"))
    country_amount = 2
    countries = country_repository.find_many()
    assert len(countries) == country_amount
    assert countries[0].name == "Brasil"
    assert countries[1].name == "United States"
