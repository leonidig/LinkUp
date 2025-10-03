from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..db import AsyncDB, Master, Service, User
from ..shemas import ServiceSchema, ServiceResponse
from ..utils import (check_master_exists,
                     get_master_by_tg_id,
                     get_service_by_id,
                     get_master_services 
                    )

services_router = APIRouter(prefix='/services', tags=['Service'])


@services_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_service(
    data: ServiceSchema,
    session=Depends(AsyncDB.get_session)
):
    master = await get_master_by_tg_id(data.master_id, session)
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Майстер з telegram ID {data.master_id} не знайдено'
        )
    
    service = Service(**data.model_dump(), master=master)
    session.add(service)
    await session.flush()
    await session.refresh(service)
    return service


@services_router.get("/by_master/{tg_id}", response_model=list[ServiceResponse])
async def get_services_by_master(tg_id: int,
                                 session=Depends(AsyncDB.get_session)
                                ):
            
            master = await get_master_services(tg_id, session)
            if not master:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Майстра з telegram ID {tg_id} не знайдено"
                )

            return master.services


@services_router.get('/{service_id}', response_model=ServiceResponse)
async def get_service(service_id: int,
                      session = Depends(AsyncDB.get_session)
                      ):
        service = await get_service_by_id(service_id, session)
        return service


@services_router.get('/count-master-services/{tg_id}')
async def get_master_services_count(tg_id: int,
                                    session = Depends(AsyncDB.get_session)
                                    ):
        master = await get_master_services(tg_id, session)
        if not master:
               raise HTTPException(
                      detail=f'Не знайдено',
                      status_code=status.HTTP_404_NOT_FOUND
               )
        return len(master.services)