from sqlmodel import SQLModel


class DocumentUpdate(SQLModel):
    name: str
