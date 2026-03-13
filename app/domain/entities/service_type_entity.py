from sqlmodel import Field, SQLModel


class ServiceTypeEntity(SQLModel):
    name: str = Field()
    schedulable: bool = Field()
