from datetime import datetime
from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class LoggedInAs(str, Enum):
    NOT_LOGGED_IN = "Nenhum Login"
    THUNDERBIRD = "Thunderbird"


class ClientEntity(SQLModel):
    name: str = Field()
    phone: str = Field()
    citizenship: str = Field()  # TODO: deixar de ser string
    birthdate: datetime = Field()
    email: EmailStr = Field()
    passport: str = Field()
    logged_in_as: LoggedInAs = Field(default=LoggedInAs.NOT_LOGGED_IN)
