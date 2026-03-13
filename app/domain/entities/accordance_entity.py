from datetime import datetime

from sqlmodel import Field, SQLModel


class AccordanceEntity(SQLModel):
    promised_to: datetime = Field()
    notes: str = Field()
