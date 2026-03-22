from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile
from pydantic import UUID4

from app.api.document.dto.document_update_dto import DocumentUpdate
from app.api.document.presentable.document_presentable import (
    DocumentPresentable,
)
from app.domain.usecases.document.create_document_usecase import (
    CreateDocumentUseCaseDep,
)
from app.domain.usecases.document.read_document_by_id_usecase import (
    ReadDocumentByIdUseCaseDep,
)
from app.domain.usecases.document.update_document_usecase import (
    UpdateDocumentUseCaseDep,
)

document_router = APIRouter(prefix="/documents", tags=["documents"])


@document_router.get(
    "/{document_id}",
    response_model=DocumentPresentable,
)
async def read_document_by_id(
    document_id: UUID4,
    read_document_by_id_usecase: ReadDocumentByIdUseCaseDep,
):
    document = read_document_by_id_usecase.execute(document_id)
    return document


@document_router.post(
    "/",
    response_model=DocumentPresentable,
    status_code=HTTPStatus.CREATED,
)
async def create_document(
    create_document_usecase: CreateDocumentUseCaseDep,
    file: Annotated[UploadFile, File()],
    name: Annotated[str, Form()],
    client_id: Annotated[UUID4, Form()],
):
    file_content = await file.read()
    print(file.content_type)
    document = create_document_usecase.execute(
        name,
        client_id,
        file_content,
    )
    return document


@document_router.patch(
    "/{document_id}",
    response_model=DocumentPresentable,
)
async def update_document_by_id(
    document_id: UUID4,
    document_data: DocumentUpdate,
    update_document_usecase: UpdateDocumentUseCaseDep,
):
    document = update_document_usecase.execute(document_id, document_data)
    return document
