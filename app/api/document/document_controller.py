from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import Response
from pydantic import UUID4

from app.api.document.dto.document_update_dto import DocumentUpdate
from app.api.document.presentable.document_presentable import (
    DocumentPresentable,
)
from app.api.document.presentable.document_presentable_with_date import (
    DocumentPresentableWithDate,
)
from app.domain.helpers.permission import Actions, PermissionChecker, Subjects
from app.domain.usecases.document.create_document_usecase import (
    CreateDocumentUseCaseDep,
)
from app.domain.usecases.document.delete_document_usecase import (
    DeleteDocumentUseCaseDep,
)
from app.domain.usecases.document.export_document_usecase import (
    ExportDocumentUseCaseDep,
)
from app.domain.usecases.document.read_document_by_id_usecase import (
    ReadDocumentByIdUseCaseDep,
)
from app.domain.usecases.document.update_document_usecase import (
    UpdateDocumentUseCaseDep,
)

document_router = APIRouter(prefix="/documents", tags=["documents"])


@document_router.get(
    "/{document_id}/visualize",
    response_class=Response,
    dependencies=[
        Depends(
            PermissionChecker(
                subject=Subjects.DOCUMENTS,
                action=Actions.READ,
            ),
        ),
    ],
    responses={
        200: {
            "content": {"*/*": {}},
            "description": "Retorna o arquivo do documento para visualização",
        },
    },
)
async def export_document(
    document_id: UUID4,
    export_document_usecase: ExportDocumentUseCaseDep,
):
    document, file_content = export_document_usecase.execute(document_id)
    return Response(
        content=file_content,
        media_type=document.mime_type,
        headers={
            "Content-Disposition": f'inline; filename="{document.name}"',
        },
    )


@document_router.get(
    "/{document_id}",
    response_model=DocumentPresentableWithDate,
    dependencies=[
        Depends(
            PermissionChecker(
                subject=Subjects.DOCUMENTS,
                action=Actions.READ,
            ),
        ),
    ],
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
    dependencies=[
        Depends(
            PermissionChecker(
                subject=Subjects.DOCUMENTS,
                action=Actions.CREATE,
            ),
        ),
    ],
)
async def create_document(
    create_document_usecase: CreateDocumentUseCaseDep,
    file: Annotated[UploadFile, File()],
    client_id: Annotated[UUID4, Form()],
):
    file_content = await file.read()
    document = create_document_usecase.execute(
        file.filename,  # TODO: SANITIZEEEE
        file.content_type,
        client_id,
        file_content,
    )
    return document


@document_router.patch(
    "/{document_id}",
    response_model=DocumentPresentable,
    dependencies=[
        Depends(
            PermissionChecker(
                subject=Subjects.DOCUMENTS,
                action=Actions.UPDATE,
            ),
        ),
    ],
)
async def update_document_by_id(
    document_id: UUID4,
    document_data: DocumentUpdate,
    update_document_usecase: UpdateDocumentUseCaseDep,
):
    document = update_document_usecase.execute(
        document_id,
        document_data.name,  # TODO: SANITIZEEE
    )
    return document


@document_router.delete(
    "/{document_id}",
    response_model=DocumentPresentableWithDate,
    dependencies=[
        Depends(
            PermissionChecker(
                subject=Subjects.DOCUMENTS,
                action=Actions.DELETE,
            ),
        ),
    ],
)
async def delete_document_by_id(
    document_id: UUID4,
    delete_document_usecase: DeleteDocumentUseCaseDep,
):
    document = delete_document_usecase.execute(document_id)
    return document
