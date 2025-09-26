from fastapi import APIRouter, status, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..db import AsyncDB, User
from ..shemas import UserSchema
from ..utils import check_user_exists


users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(
                data: UserSchema,
                session = Depends(AsyncDB.get_session)
            ):
    user = User(**data.model_dump())
    session.add(user)
    return 'Created!'


@users_router.get("/check-exists/{tg_id}")
async def check_exists(tg_id: int,
                       session = Depends(AsyncDB.get_session)
                    ):
    return await check_user_exists(tg_id, session)


@users_router.get('/master/{tg_id}')
async def get_master(tg_id: int, session = Depends(AsyncDB.get_session)):
    user = await session.scalar(
        select(User)
        .options(selectinload(User.master))
        .where(User.tg_id == tg_id)
    )
    return user.master