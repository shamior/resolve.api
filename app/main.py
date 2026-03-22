import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth.auth_controller import auth_router
from app.api.client.client_controller import client_router
from app.api.document.document_controller import document_router
from app.api.service.service_controller import service_router
from app.api.user.users_controller import user_router
from app.domain.config.env_config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(
        f"{settings.STORAGE_DIR}{settings.DOCUMENTS_DIR}",
        exist_ok=True,
    )
    os.makedirs(
        f"{settings.STORAGE_DIR}{settings.RECEIPTS_DIR}",
        exist_ok=True,
    )
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(service_router)
app.include_router(document_router)
app.include_router(client_router)
