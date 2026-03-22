from datetime import datetime
from typing import Annotated

from fastapi import Depends
from pydantic import UUID4
from sqlmodel import select

from app.infra.database.database import Database
from app.infra.database.models import Document


class DocumentsRepository:
    def __init__(self, db: Database):
        self.db = db

    def find_documents_by_client_id(self, client_id: UUID4) -> list[Document]:
        query = select(Document).where(Document.client_id == client_id)
        documents = self.db.exec(query).all()
        return list(documents)

    def find_document_by_id(self, document_id: UUID4) -> Document | None:
        query = select(Document).where(Document.id == document_id)
        document = self.db.exec(query).first()
        return document

    def create_document(self, document: Document) -> Document:
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def update_document(self, document: Document) -> Document:
        document.updated_at = datetime.now()
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document


DocumentsRepositoryDep = Annotated[DocumentsRepository, Depends()]
