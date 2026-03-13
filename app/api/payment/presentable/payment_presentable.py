from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.payment_entity import PaymentEntity


class PaymentPresentable(PaymentEntity):
    id: UUID4 = Field()
