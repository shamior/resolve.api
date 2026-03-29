import pytest
from sqlmodel import Session

from app.domain.repositories.country_repository import CountryRepository


@pytest.fixture
def country_repository(db_with_countries: Session):
    return CountryRepository(db_with_countries)


def test_find_by_code(country_repository: CountryRepository):
    country = country_repository.find_by_code("BRA")
    assert country is not None
    assert country.name == "Brasil"
    assert country.code == "BRA"


def test_find_many(country_repository: CountryRepository):
    country_amount = 249
    countries = country_repository.find_many()
    assert len(countries) == country_amount
