from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.document_entity import DocumentEntity


class DocumentPresentable(DocumentEntity):
    id: UUID4 = Field()
