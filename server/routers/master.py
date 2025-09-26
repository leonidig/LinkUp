from fastapi import APIRouter, status, Depends, HTTPException

from ..db import AsyncDB, Master, User
from ..shemas import MasterCreateSchema
from ..utils import check_master_exists


masters_router = APIRouter(prefix='/masters', tags=['Master'])


@masters_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_master(
    data: MasterCreateSchema,
    session = Depends(AsyncDB.get_session)
):
    user = await session.get(User, data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {data.user_id} not found"
        )
    
    master = Master(**data.model_dump(), user=user)
    session.add(master)
    await session.refresh(master)
    return master


@masters_router.get("/check-exists/{tg_id}")
async def check_exists(tg_id: int,
                   session = Depends(AsyncDB.get_session)
                    ):
    return await check_master_exists(tg_id, session)