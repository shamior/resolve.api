from fastapi import APIRouter
from pydantic import UUID4

from app.api.document.presentable.document_presentable import (
    DocumentPresentable,
)
from app.domain.usecases.client.read_documents_by_client_id_usecase import (
    ReadDocumentsByClientIdUseCaseDep,
)

client_router = APIRouter(prefix="/clients", tags=["clients"])


@client_router.get(
    "/{client_id}/documents",
    response_model=list[DocumentPresentable],
)
async def read_documents_by_client_id(
    client_id: UUID4,
    read_documents_by_client_id_usecase: ReadDocumentsByClientIdUseCaseDep,
):
    documents = read_documents_by_client_id_usecase.execute(client_id)
    return documents
