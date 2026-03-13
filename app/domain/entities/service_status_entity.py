from sqlmodel import Field, SQLModel


class ServiceStatusEntity(SQLModel):
    name: str = Field()
    color: str = Field(default="#cccccc")
