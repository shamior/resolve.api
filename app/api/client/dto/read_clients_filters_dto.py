from typing import Annotated, Optional

from fastapi import Depends, Query
from pydantic import BaseModel

from app.domain.entities.client_entity import LoggedInAs


class ReadClientFilters(BaseModel):
    name_email_or_phone_contains: str = Query(default="")
    logged_in_as: Optional[LoggedInAs] = Query(default=None)


ReadClientFiltersDep = Annotated[ReadClientFilters, Depends()]
