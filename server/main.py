from fastapi import FastAPI, APIRouter

from .routers import test_router


app = FastAPI()


api_router = APIRouter(prefix='/api')
api_router.include_router(test_router)
app.include_router(api_router)