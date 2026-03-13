from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class WithDatePresentable(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class WithDateModel(WithDatePresentable):
    deleted_at: Optional[datetime] = Field(default=None)
