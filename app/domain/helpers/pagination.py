from collections.abc import Sequence
from math import ceil
from typing import Annotated, Generic, TypeVar

from fastapi import Depends, Query
from pydantic import BaseModel

T = TypeVar("T")


class Pagination(BaseModel, Generic[T]):
    data: Sequence[T]
    page: int
    per_page: int
    total: int
    total_pages: int


class PaginationQueryParams(BaseModel):
    page: int = Query(1, gt=0)
    per_page: int = Query(15, gt=0)


def get_offset(pagination: PaginationQueryParams):
    return (pagination.page - 1) * pagination.per_page


def get_total_pages(total: int, per_page: int):
    return ceil(total / per_page)


PaginationParams = Annotated[PaginationQueryParams, Depends()]
