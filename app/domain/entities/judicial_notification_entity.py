from datetime import datetime

from pydantic import UUID4
from sqlmodel import Field, SQLModel
from typing_extensions import Optional


class JudicialNotificationEntity(SQLModel):
    lawyer_notified_at: Optional[datetime] = Field(default=None)
    client_notified_at: Optional[datetime] = Field(default=None)
    payment_id: Optional[UUID4] = Field(default=None, foreign_key="payment.id")
