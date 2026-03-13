from datetime import datetime

from sqlmodel import Field, SQLModel


class ReceiptEntity(SQLModel):
    payed_at: datetime = Field()
    path: str = Field()
