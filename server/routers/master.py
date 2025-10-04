from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..db import AsyncDB, Master, User
from ..shemas import MasterCreateSchema, MasterResponse
from ..utils import check_master_exists


masters_router = APIRouter(prefix='/masters', tags=['Master'])


@masters_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_master(
    data: MasterCreateSchema,
    session = Depends(AsyncDB.get_session)
):
    user = await session.scalar(select(User).where(User.tg_id == data.user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {data.user_id} not found"
        )
    
    master = await check_master_exists(data.user_id, session)
    if master:
        raise HTTPException(
            detail='Ви не можете створити більше 1го профіля майстра',
            status_code=status.HTTP_409_CONFLICT
        )
    
    master = Master(**data.model_dump(), user=user)
    session.add(master)
    await session.flush()
    await session.refresh(master)
    return master


@masters_router.get("/check-exists/{tg_id}")
async def check_exists(tg_id: int,
                   session = Depends(AsyncDB.get_session)
                    ):
    return await check_master_exists(tg_id, session)


@masters_router.get("/by-specialization/{spec}", response_model=list[MasterResponse])
async def masters_by_spec(spec: str, session = Depends(AsyncDB.get_session)):
    allowed_specs = [
        "Розробник", "Будівельник", "Дизайнер", "Фотограф", "Водій",
        "Копірайтер", "Майстер по ремонту", "Майстер краси", "Різноробочий", "Репетитор"
    ]
    spec_clean = spec.strip()
    if spec_clean not in allowed_specs:
        raise HTTPException(status_code=422, detail=f"Спеціалізація {spec_clean} не допустима")

    masters = await session.scalars(select(Master).where(Master.specialization == spec_clean))
    return masters.all()



@masters_router.get('/{master_tg_id}', response_model=MasterResponse)
async def master_info(master_tg_id: int, session = Depends(AsyncDB.get_session)):
    master = await session.scalar(
        select(Master)
        .where(Master.user.has(User.tg_id == master_tg_id))
        .options(selectinload(Master.user))
    )
    if not master:
        raise HTTPException(status_code=404, detail="Майстра не знайдено")
    return master