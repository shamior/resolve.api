from typing import Annotated

from fastapi import Depends

from app.api.user.dto.user_read_params_dto import ReadUsersQueryParams, RolesIn
from app.domain.helpers.pagination import (
    Pagination,
    PaginationParams,
    get_offset,
    get_total_pages,
)
from app.domain.repositories.user_repository import (
    UserRepositoryDep,
    UserRepositoryFindManyFilters,
)


class ReadUsersUseCase:
    def __init__(self, user_repository: UserRepositoryDep) -> None:
        self.user_repository = user_repository

    def execute(
        self,
        pagination: PaginationParams,
        filters: ReadUsersQueryParams,
        roles_in: RolesIn,
    ):
        offset = get_offset(pagination)
        users, total = self.user_repository.find_many(
            UserRepositoryFindManyFilters(
                name_or_email_contains=filters.name_or_email_contains,
                roles_in=roles_in,
                offset=offset,
                limit=pagination.per_page,
            ),
        )
        return Pagination(
            page=pagination.page,
            per_page=pagination.per_page,
            data=users,
            total=total,
            total_pages=get_total_pages(
                total=total,
                per_page=pagination.per_page,
            ),
        )


ReadUsersUseCaseDep = Annotated[ReadUsersUseCase, Depends()]
