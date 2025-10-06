from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from ..db import Order, User, Master, Service, AsyncDB
from ..shemas import OrderCreateSchema, OrderResponse 


orders_router = APIRouter(prefix="/orders", tags=["orders"])


@orders_router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreateSchema,
    session: AsyncSession = Depends(AsyncDB.get_session)
):
    
    user = await session.scalar(select(User).where(User.tg_id == data.user_tg_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {data.user_tg_id} not found"
        )

    master = await session.scalar(select(Master).where(Master.tg_id == data.master_tg_id))
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Master with id {data.master_tg_id} not found"
        )

    service = None
    if data.service_id is not None:
        service = await session.scalar(select(Service).where(Service.id == data.service_id))
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service with id {data.service_id} not found"
            )

    order = Order(
        user_id=data.user_tg_id,
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