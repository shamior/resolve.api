import uuid

from pydantic import UUID4
from sqlmodel import Field, SQLModel

from app.models.with_date_model import WithDateModel, WithDatePresentable


class ServiceStatusBase(SQLModel):
    name: str = Field()
    color: str = Field(default="#cccccc")


class ServiceStatus(ServiceStatusBase, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)


class ServiceStatusPresentable(ServiceStatusBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
