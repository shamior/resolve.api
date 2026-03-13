from typing import Annotated, Generic, Sequence, TypeVar

from fastapi import Depends, Query
from pydantic import BaseModel
from sqlmodel import Field

T = TypeVar("T")


class Pagination(BaseModel, Generic[T]):
    data: Sequence[T] = Field()
    page: int = Field()
    per_page: int = Field()
    total: int = Field()


class QueryParams(BaseModel):
    page: int = Query(1, gt=0)
    per_page: int = Query(10, gt=0)


PaginationParams = Annotated[QueryParams, Depends()]
