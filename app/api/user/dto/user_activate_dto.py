from sqlmodel import Field, SQLModel


class UserActivate(SQLModel):
    password: str = Field()
