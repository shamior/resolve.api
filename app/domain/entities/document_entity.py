from pydantic import UUID4
from sqlmodel import Field, SQLModel


class DocumentEntity(SQLModel):
    name: str = Field()
    path: str = Field(default="")
    client_id: UUID4 = Field(foreign_key="client.id")
