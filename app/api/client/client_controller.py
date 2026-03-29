from fastapi import APIRouter
from pydantic import UUID4

from app.api.client.dto.read_clients_filters_dto import ReadClientFiltersDep
from app.api.client.presentable.client_presentable_with_docs import (
    ClientPresentableWithDocuments,
)
from app.api.document.presentable.document_presentable import (
    DocumentPresentable,
)
from app.domain.helpers.pagination import Pagination, PaginationParams
from app.domain.usecases.client.read_clients_usecase import (
    ReadClientsUseCaseDep,
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


# @client_router.get(
#     "/{client_id}/",
#     response_model=ClientPresentableWithDocuments,
# )
# async def read_client_by_id(
#     client_id: UUID4,
#     read_client_by_id_usecase: ReadClientByIdUseCaseDep,
# ):
#     client = read_documents_by_client_id_usecase.execute(client_id)
#     return documents


@client_router.get(
    "",
    response_model=Pagination[ClientPresentableWithDocuments],
)
async def read_clients_paginated(
    pagination: PaginationParams,
    filters: ReadClientFiltersDep,
    read_clients_usecase: ReadClientsUseCaseDep,
):
    clients_paginated = read_clients_usecase.execute(pagination, filters)
    return clients_paginated
