from fastapi import FastAPI, APIRouter

from .routers import users_router, masters_router


app = FastAPI()


api_router = APIRouter(prefix='/api')
api_router.include_router(users_router)
api_router.include_router(masters_router)
app.include_router(api_router)