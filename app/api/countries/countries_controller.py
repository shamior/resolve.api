from fastapi import APIRouter, Depends

from app.api.countries.presentable.country_presentable import (
    CountryPresentable,
)
from app.domain.helpers.permission import Actions, PermissionChecker, Subjects
from app.domain.repositories.country_repository import CountryRepositoryDep

country_router = APIRouter(prefix="/countries", tags=["countries"])


@country_router.get(
    "",
    response_model=list[CountryPresentable],
    dependencies=[
        Depends(
            PermissionChecker(subject=Subjects.COUNTRIES, action=Actions.READ),
        ),
    ],
)
async def read_countries(country_repository: CountryRepositoryDep):
    countries = country_repository.find_many()
    return countries
