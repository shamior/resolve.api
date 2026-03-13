from pydantic import UUID4
from sqlmodel import Field, SQLModel


class ServiceNotesEntity(SQLModel):
    content: str = Field()
    service_id: UUID4 = Field(foreign_key="service.id")
    issuer_id: UUID4 = Field(foreign_key="user.id")
