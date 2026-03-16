from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

from app.domain.entities.user_entity import UserRoles


class ReadUsersParams(BaseModel):
    name_or_email_contains: str = Query(default="")


ReadUsersQueryParams = Annotated[ReadUsersParams, Depends()]
RolesIn = Annotated[list[UserRoles], Query()]
