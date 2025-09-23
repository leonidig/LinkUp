from fastapi import APIRouter, status, Depends

from ..db import AsyncDB, User
from ..shemas import UserSchema


users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(data: UserSchema, session = Depends(AsyncDB.get_session)):
    user = User(**data.model_dump())
    session.add(user)
    return 'Created!'