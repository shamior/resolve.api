from datetime import date

from sqlmodel import Field, SQLModel


class AccordanceEntity(SQLModel):
    promised_to: date = Field()
    notes: str = Field()
