from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

from app.domain.entities.user_role_entity import RoleType


class ReadUsersParams(BaseModel):
    name_or_email_contains: str = Query(default="")


ReadUsersQueryParams = Annotated[ReadUsersParams, Depends()]
RolesIn = Annotated[list[RoleType], Query()]
