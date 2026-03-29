from typing import Annotated

from fastapi import Depends

from app.api.client.dto.read_clients_filters_dto import ReadClientFilters
from app.domain.helpers.pagination import (
    Pagination,
    PaginationParams,
    get_offset,
    get_total_pages,
)
from app.domain.repositories.client_repository import (
    ClientRepositoryDep,
    ClientRepositoryFindManyFilters,
)


class ReadClientsUseCase:
    def __init__(self, client_repository: ClientRepositoryDep):
        self.client_repository = client_repository

    def execute(
        self,
        pagination: PaginationParams,
        filters: ReadClientFilters,
    ):
        clients, count = self.client_repository.find_many(
            ClientRepositoryFindManyFilters(
                limit=pagination.per_page,
                offset=get_offset(pagination),
                name_phone_or_email=filters.name_email_or_phone_contains,
            ),
        )
        return Pagination(
            data=clients,
            page=pagination.page,
            per_page=pagination.per_page,
            total=count,
            total_pages=get_total_pages(count, pagination.per_page),
        )


ReadClientsUseCaseDep = Annotated[ReadClientsUseCase, Depends()]
