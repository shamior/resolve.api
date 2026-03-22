from pydantic import UUID4, BaseModel, Field


class DocumentPresentable(BaseModel):
    id: UUID4 = Field()
    name: str = Field()
    client_id: UUID4 = Field()
