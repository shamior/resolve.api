import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel
from typing_extensions import Optional

from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.payment.payment_model import Payment


class JudicialNotificationBase(SQLModel):
    lawyer_notified_at: Optional[datetime] = Field(default=None)
    client_notified_at: Optional[datetime] = Field(default=None)
    payment_id: UUID4 = Field(foreign_key="payment.id")


class JudicialNotification(
    JudicialNotificationBase, WithDateModel, table=True
):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    payment: "Payment" = Relationship(back_populates="notification")


class JudicialNotificationPresentable(
    JudicialNotificationBase, WithDatePresentable
):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
