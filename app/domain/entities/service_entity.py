from datetime import datetime

from pydantic import UUID4
from sqlmodel import Field, SQLModel
from typing_extensions import Optional


class ServiceEntity(SQLModel):
    started_at: datetime = Field(default_factory=datetime.now)
    finished_at: Optional[datetime] = Field(default=None)

    client_id: UUID4 = Field(foreign_key="client.id")
    service_status_id: UUID4 = Field(foreign_key="servicestatus.id")
    executor_id: UUID4 = Field(foreign_key="user.id")
    comercial_id: UUID4 = Field(foreign_key="user.id")
    service_type_id: UUID4 = Field(foreign_key="servicetype.id")
