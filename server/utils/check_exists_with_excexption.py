from sqlalchemy import select
from fastapi import HTTPException, status

from ..db import Master, User, Service, Order


async def check_master_exists_exception(tg_id: int, session):
    master = await session.scalar(
        select(Master)
        .join(User)
        .where(User.tg_id == tg_id)
    )
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Майстра з TG ID {tg_id} не знайдено"
        )
    return master


async def check_user_exists_exception(tg_id: int, session):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з TG ID {tg_id} не знайдено"
        )
    return user


async def check_service_exsists_exception(service_id: int,
                        session
                        ):
    service = await session.scalar(select(Service).where(Service.id == service_id))
    if not service:
        raise HTTPException(
            detail=f'Сервіс з ID {service_id} не знайдено',
            status_code=status.HTTP_404_NOT_FOUND
        )
    else:
        return service
    

async def check_order_exists_exception(order_id: int,
                                       session
                                       ):
    order = await session.get(Order, order_id)
    if not order:
        raise HTTPException(
            detail=f'Замовлення з ID {order_id} не знайдено',
            status_code=status.HTTP_404_NOT_FOUND
        )
    else:
        return order
    

async def check_user_exists_exception(tg_id: int,
                                       session
                                       ):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        raise HTTPException(
            detail=f'Користувача з телеграм ID {tg_id} не знайдено',
            status_code=status.HTTP_404_NOT_FOUND
        )
    else:
        return user