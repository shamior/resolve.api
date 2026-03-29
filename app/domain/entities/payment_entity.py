from enum import Enum
from typing import Optional

from pydantic import UUID4
from sqlmodel import Field, SQLModel


class PaymentStatus(str, Enum):
    REGISTERED = "Cadastrado"
    WAITING_FOR_PAYMENT = "Aguardando pagamento"
    LATE_PAYMENT = "Atrasado"
    ACCORDANCE = "Acordado"
    EXTRA_JUDICIAL = "Extrajudicial"
    PAID = "Pago"


class PaymentType(str, Enum):
    INSTALLMENT = "Parcela"
    UPFRONT = "Entrada"
    PAYBACK = "Devolução"


class PaymentEntity(SQLModel):
    status: PaymentStatus = Field(default=PaymentStatus.REGISTERED)
    payment_type: PaymentType = Field()
    amount: int = Field()
    receipt_id: Optional[UUID4] = Field(foreign_key="receipt.id", default=None)
    accordance_id: Optional[UUID4] = Field(
        default=None,
        foreign_key="accordance.id",
    )

    service_id: Optional[int] = Field(foreign_key="service.id")
