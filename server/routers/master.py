from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..db import AsyncDB, Master, User
from ..shemas import MasterCreateSchema, MasterResponse
from ..utils import check_master_exists


masters_router = APIRouter(prefix='/masters', tags=['Master'])


@masters_router.post("/", 
                     summary='Create Master Profile',
                     description='Create Master Profile ( User Profile Required)',
                     status_code=status.HTTP_201_CREATED,
                     response_model=MasterResponse)
async def create_master(
    data: MasterCreateSchema,
    session = Depends(AsyncDB.get_session)
):
    user = await session.scalar(select(User).where(User.tg_id == data.tg_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {data.tg_id} not found"
        )
    
    master = await check_master_exists(data.tg_id, session)
    if master:
        raise HTTPException(
            detail='Ви не можете створити більше 1го профіля майстра',
            status_code=status.HTTP_409_CONFLICT
        )
    
    master = Master(**data.model_dump(), user=user)
    user.role = 'master'
    session.add(master)
    await session.flush()
    await session.refresh(master)
    return master


@masters_router.get("/check-exists/{tg_id}",
                    summary='Check Master Exists',
                    description='Check Master Exists By Telegram ID'
                    )
async def check_exists(tg_id: int,
                   session = Depends(AsyncDB.get_session)
                    ):
    return await check_master_exists(tg_id, session)


@masters_router.get("/by-specialization/{spec}",
                    summary='Get Masters By Spec',
                    description='Get Masters By Selected Specialization',
                    response_model=list[MasterResponse])
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



@masters_router.get('/{master_tg_id}',
                    summary='Get Master Profile Info',
                    description='Get Master Profile By Telegram ID',
                    response_model=MasterResponse)
async def master_info(master_tg_id: int, session = Depends(AsyncDB.get_session)):
    master = await session.scalar(
        select(Master)
        .where(Master.user.has(User.tg_id == master_tg_id))
        .options(selectinload(Master.user))
    )
    if not master:
        raise HTTPException(status_code=404, detail="Майстра не знайдено")
    return master


@masters_router.delete(
                "/{tg_id}",
                summary="Delete Master Profile",
                description="Delete master profile by Telegram ID",
                status_code=status.HTTP_204_NO_CONTENT)
async def delete_master(tg_id: int, session = Depends(AsyncDB.get_session)):
    master = await check_master_exists(tg_id, session)
    if master:
        await session.delete(master)
        return {'detail': 'Deleted'}