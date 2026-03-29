from datetime import date
from enum import Enum
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class LoggedInAs(str, Enum):
    NOT_LOGGED_IN = "Nenhum Login"
    THUNDERBIRD = "Thunderbird"


class ClientEntity(SQLModel):
    name: str = Field()
    phone: str = Field()
    country_code: Optional[str] = Field(
        default=None,
        foreign_key="country.code",
    )
    birthdate: date = Field()
    email: EmailStr = Field()
    passport: str = Field()
    logged_in_as: LoggedInAs = Field(default=LoggedInAs.NOT_LOGGED_IN)
