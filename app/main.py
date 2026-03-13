from fastapi import FastAPI

from app.routers.auth_router import auth_router
from app.routers.service_router import service_router
from app.routers.users_router import user_router

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     SQLModel.metadata.create_all(engine)
#     yield


app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(service_router)
