from sqlalchemy import select
from fastapi import Depends, status, HTTPException

from ..db import AsyncDB, Service


async def get_service_by_id(service_id: int, session):
    service = await session.scalar(select(Service).where(Service.id == service_id))
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Сервіс з ID {service_id} не знайдено'
        )
    else:
        return service