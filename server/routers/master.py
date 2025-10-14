from fastapi import APIRouter, Query, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..db import AsyncDB, Master, User, Order
from ..db.models.order import OrderStatus
from ..shemas import MasterCreateSchema, MasterResponse
from ..utils import check_master_exists, check_master_exists_exception, check_user_exists_exception


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


# @masters_router.delete(
#                 "/{tg_id}",
#                 summary="Delete Master Profile",
#                 description="Delete master profile by Telegram ID",
#                 status_code=status.HTTP_204_NO_CONTENT)
# async def delete_master(tg_id: int, session = Depends(AsyncDB.get_session)):
#     master = await check_master_exists(tg_id, session)
#     if master:
#         await session.delete(master)
#         return {'detail': 'Deleted'}


@masters_router.put('/rate/{master_tg_id}')
async def rate_master(master_tg_id: int,
                      user_tg_id: int,
                      emoji: str,
                      rating: int | None = Query(None, ge=1, le=10),
                      session = Depends(AsyncDB.get_session)
                    ):
    user = await check_user_exists_exception(user_tg_id, session)
    master = await check_master_exists_exception(master_tg_id, session)
    
    if user and master:
        orders = await session.scalar(select(Order).where(Order.master_id == master_tg_id,
                                                        Order.user_id == user_tg_id,
                                                        Order.status.in_([OrderStatus.completed])
                                                        ))
    
        if not orders:
            raise HTTPException(
                detail='У вас немає завершених завдань з цим майстром',
                status_code=status.HTTP_403_FORBIDDEN
            )
    
    if emoji not in ['👍🏻', '👎🏻']:
        raise HTTPException(
            detail='Обери корректне емоджи',
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )

    if emoji == '👎🏻':
        master.bad_grades += 1

    elif emoji == '👍🏻':
        master.good_grades += 1

    if rating:
        total_votes = master.good_grades + master.bad_grades
        master.rating = round(((master.rating * (total_votes - 1)) + rating) / total_votes, 2)

        

    await session.flush()
    await session.refresh(master)

    return {
        "message": f"Ви оцінили майстра {emoji}",
        "rating": master.rating,
        "good": master.good_grades,
        "bad": master.bad_grades
    }