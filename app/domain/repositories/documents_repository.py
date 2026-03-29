from datetime import datetime
from enum import Enum
from typing import Annotated, Sequence

from fastapi import Depends
from pydantic import UUID4
from sqlmodel import col, select

from app.infra.database.database import Database
from app.infra.database.models import Document


class DocumentQueryType(Enum):
    NOT_DELETED = "NOT_DELETED"
    ALL = "ALL"


class DocumentsRepository:
    def __init__(self, db: Database):
        self.db = db

    def find_by_client_id(
        self,
        client_id: UUID4,
        fetch_type: DocumentQueryType = DocumentQueryType.NOT_DELETED,
    ) -> Sequence[Document]:
        query = select(Document).where(Document.client_id == client_id)

        if fetch_type == DocumentQueryType.NOT_DELETED:
            query = query.where(col(Document.deleted_at).is_(None))

        documents = self.db.exec(query).all()
        return documents

    def find_by_id(self, document_id: UUID4) -> Document | None:
        query = select(Document).where(Document.id == document_id)
        document = self.db.exec(query).first()
        return document

    def create(self, document: Document) -> Document:
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def update(self, document: Document) -> Document:
        document.updated_at = datetime.now()
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def delete(self, document: Document) -> Document:
        document.deleted_at = datetime.now()
        document.updated_at = datetime.now()
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document


DocumentsRepositoryDep = Annotated[DocumentsRepository, Depends()]
