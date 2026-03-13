import uuid
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from app.models.with_date_model import WithDateModel, WithDatePresentable

if TYPE_CHECKING:
    from app.models.payment.accordance_model import Accordance
    from app.models.payment.judicial_notification_model import (
        JudicialNotification,
    )
    from app.models.payment.receipt_model import Receipt
    from app.models.payment.repass_model import Repass
    from app.models.services.service_model import Service


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


class PaymentBase(SQLModel):
    status: PaymentStatus = Field(default=PaymentStatus.REGISTERED)
    payment_type: PaymentType = Field()
    amount: int = Field()
    receipt_id: Optional[UUID4] = Field(foreign_key="receipt.id", default=None)
    accordance_id: Optional[UUID4] = Field(
        foreign_key="accordance.id", default=None
    )

    service_id: UUID4 = Field(foreign_key="service.id")


class Payment(PaymentBase, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    service: "Service" = Relationship(back_populates="payments")
    repasses: List["Repass"] = Relationship(back_populates="payment")
    receipt: Optional["Receipt"] = Relationship(back_populates="payment")
    accordance: Optional["Accordance"] = Relationship(back_populates="payment")
    notification: Optional["JudicialNotification"] = Relationship(
        back_populates="payment"
    )


class PaymentPresentable(PaymentBase, WithDatePresentable):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
