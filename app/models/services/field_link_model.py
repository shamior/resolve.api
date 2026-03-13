from pydantic import UUID4
from sqlmodel import Field, SQLModel

from app.models.with_date_model import WithDateModel


class FieldLinkBase(SQLModel):
    pass


class FieldLink(FieldLinkBase, WithDateModel, table=True):
    service_type_id: UUID4 = Field(
        foreign_key="servicetype.id", primary_key=True
    )
    field_type_id: UUID4 = Field(
        foreign_key="servicefieldtype.id", primary_key=True
    )
