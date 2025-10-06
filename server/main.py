from fastapi import FastAPI, APIRouter

from .routers import users_router, masters_router, services_router, orders_router


app = FastAPI()


api_router = APIRouter(prefix='/api')
api_router.include_router(users_router)
api_router.include_router(masters_router)
api_router.include_router(services_router)
api_router.include_router(orders_router)
app.include_router(api_router)