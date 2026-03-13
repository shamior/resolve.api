import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.payment.payment_model import Payment
    from app.models.payment.repass_model import Repass


class ReceiptBase(SQLModel):
    payed_at: datetime = Field()
    path: str = Field()


class Receipt(ReceiptBase, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    payment: Optional["Payment"] = Relationship(back_populates="receipt")
    repass: Optional["Repass"] = Relationship(back_populates="receipt")


class ReceiptPresentable(ReceiptBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
