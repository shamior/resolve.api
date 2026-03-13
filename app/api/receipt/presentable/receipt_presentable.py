from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.receipt_entity import ReceiptEntity


class ReceiptPresentable(ReceiptEntity):
    id: UUID4 = Field()
