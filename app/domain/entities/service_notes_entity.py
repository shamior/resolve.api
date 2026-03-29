from typing import Optional

from pydantic import UUID4
from sqlmodel import Field, SQLModel


class ServiceNotesEntity(SQLModel):
    content: str = Field()
    service_id: Optional[int] = Field(foreign_key="service.id")
    issuer_id: Optional[UUID4] = Field(foreign_key="user.id")
