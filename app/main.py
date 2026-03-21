from fastapi import FastAPI

from app.api.auth.auth_controller import auth_router
from app.api.service.service_controller import service_router
from app.api.user.users_controller import user_router

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield


app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(service_router)
