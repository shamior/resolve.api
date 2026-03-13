from fastapi import APIRouter

from app.helpers.pagination import Pagination, PaginationParams
from app.helpers.security import CurrentUser
from app.models.aggregates import ServiceAggregate
from app.repositories.service_repository import ServiceRepository

service_router = APIRouter(prefix="/services", tags=["services"])


@service_router.get(
    "/",
    response_model=Pagination[ServiceAggregate],
)
async def read_paginated_services(
    service_repository: ServiceRepository,
    pagination: PaginationParams,
    current_user: CurrentUser,
):
    services = service_repository.find_many()
    return Pagination(
        page=pagination.page,
        per_page=pagination.per_page,
        data=services,
        total=len(services),
    )


@service_router.get(
    "/mine",
    response_model=Pagination[ServiceAggregate],
)
async def read_paginated_services_related_to_authenticated_user(
    service_repository: ServiceRepository,
    pagination: PaginationParams,
    current_user: CurrentUser,
):
    services = service_repository.find_related_to_user(user_id=current_user.id)
    return Pagination(
        page=pagination.page,
        per_page=pagination.per_page,
        data=services,
        total=len(services),
    )
