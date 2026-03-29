from typing import Optional

from pydantic import UUID4
from sqlmodel import Field, SQLModel


class ServiceFieldEntity(SQLModel):
    value: str = Field()
    field_type_id: Optional[UUID4] = Field(
        default=None,
        foreign_key="servicefieldtype.id",
    )
    service_id: Optional[int] = Field(default=None, foreign_key="service.id")
