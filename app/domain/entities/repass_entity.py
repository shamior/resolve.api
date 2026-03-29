from enum import Enum
from typing import Optional

from pydantic import UUID4
from sqlmodel import Field, SQLModel


class RepassStatus(str, Enum):
    REGISTERED = "Cadastrado"
    PAID = "Pago"


class RepassEntity(SQLModel):
    status: RepassStatus = Field(default=RepassStatus.REGISTERED)
    amount: int = Field()
    receipt_id: Optional[UUID4] = Field(default=None, foreign_key="receipt.id")
    payment_id: Optional[UUID4] = Field(default=None, foreign_key="payment.id")
    receiver_id: Optional[UUID4] = Field(default=None, foreign_key="user.id")
