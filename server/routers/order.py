from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import Order, User, Master, Service, AsyncDB
from ..shemas import OrderCreateSchema, OrderResponse
from ..utils.check_exists_with_excexption import (
    check_master_exists_exception,
    check_service_exsists_exception,
    check_user_exists_exception,
    check_order_exists_exception
)


orders_router = APIRouter(prefix="/orders", tags=["orders"])


@orders_router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
                        data: OrderCreateSchema,
                        session: AsyncSession = Depends(AsyncDB.get_session)
                    ):
    user_exists = await check_user_exists_exception(data.user_tg_id, session)
    master_exists = await check_master_exists_exception(data.master_tg_id, session)
    service_exists = await check_service_exsists_exception(data.service_id, session)

    order = Order(user_id=data.user_tg_id,
        master_id=data.master_tg_id,
        service_id=data.service_id,
        description=data.description,
        price=data.price,
        scheduled_at=data.scheduled_at,
        deadline=data.deadline
    )

    session.add(order)
    await session.flush()
    await session.refresh(order)

    return order


@orders_router.get('/{order_id}', response_model=OrderResponse)
async def get_order_info(order_id: int,
                         session = Depends(AsyncDB.get_session) 
                        ):
    order = await check_order_exists_exception(order_id, session)
    return order