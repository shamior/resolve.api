import uuid
from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.payment.payment_model import Payment
    from app.models.payment.receipt_model import Receipt
    from app.models.user_model import User


class RepassStatus(str, Enum):
    REGISTERED = "Cadastrado"
    PAID = "Pago"


class RepassBase(SQLModel):
    status: RepassStatus = Field(default=RepassStatus.REGISTERED)
    amount: int = Field()
    receipt_id: Optional[UUID4] = Field(foreign_key="receipt.id")
    payment_id: UUID4 = Field(foreign_key="payment.id")
    receiver_id: UUID4 = Field(foreign_key="user.id")


class Repass(RepassBase, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    receipt: Optional["Receipt"] = Relationship(back_populates="repass")
    payment: "Payment" = Relationship(back_populates="repasses")
    receiver: "User" = Relationship(back_populates="repasses")


class RepassPresentable(RepassBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
