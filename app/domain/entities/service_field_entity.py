from pydantic import UUID4
from sqlmodel import Field, SQLModel


class ServiceFieldEntity(SQLModel):
    value: str = Field()
    field_type_id: UUID4 = Field(foreign_key="servicefieldtype.id")
    service_id: UUID4 = Field(foreign_key="service.id")
