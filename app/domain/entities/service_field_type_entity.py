from sqlmodel import Field, SQLModel


class ServiceFieldTypeEntity(SQLModel):
    name: str = Field()
    field_type: str = Field()
    accepted_values: str = Field()  # TODO: ARRAY DE STRINGS
