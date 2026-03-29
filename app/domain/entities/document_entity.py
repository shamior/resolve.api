from typing import Optional

from pydantic import UUID4
from sqlmodel import Field, SQLModel


class DocumentEntity(SQLModel):
    name: str = Field()
    path: str = Field()
    mime_type: str = Field(default="application/octet-stream")
    client_id: Optional[UUID4] = Field(default=None, foreign_key="client.id")
