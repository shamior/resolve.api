import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.payment.payment_model import Payment


class AccordanceBase(SQLModel):
    promised_to: datetime = Field()
    notes: str = Field()


class Accordance(AccordanceBase, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    payment: "Payment" = Relationship(back_populates="accordance")


class AccordancePresentable(AccordanceBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
