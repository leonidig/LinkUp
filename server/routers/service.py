from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from ..db import AsyncDB, Master, Service, User
from ..shemas import (ServiceSchema,
                      ServiceResponse,
                      MasterResponse,
                      ServiceUpdate  
                    )
from ..utils import (check_master_exists,
                     get_master_by_tg_id,
                     get_service_by_id,
                     get_master_services 
                    )

from ..utils.check_exists_with_excexption import check_service_exsists_exception


services_router = APIRouter(prefix='/services', tags=['Service'])


@services_router.post('/', 
                      summary='Create Service',
                      description='Create Service ( Master Profile Required )',
                      status_code=status.HTTP_201_CREATED)
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


@services_router.get("/by-master/{tg_id}",
                     summary='Master Services',
                     description='Get All Master Services By Telegram ID',
                     response_model=list[ServiceResponse])
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


@services_router.get('/{service_id}', 
                     summary='Service Info',
                     description='Get Service Info By ID',
                     response_model=ServiceResponse)
async def get_service(service_id: int,
                      session = Depends(AsyncDB.get_session)
                      ):
        service = await get_service_by_id(service_id, session)
        return service


@services_router.get('/count-master-services/{tg_id}',
                      summary='Count Master Services',
                      description='Count Master Services by Telegram ID'
                     )
async def get_master_services_count(tg_id: int,
                                    session = Depends(AsyncDB.get_session)
                                    ):
        master = await get_master_services(tg_id, session)
        if not master:
               raise HTTPException(
                      detail=f'Майстера з ID {tg_id} не знайдено',
                      status_code=status.HTTP_404_NOT_FOUND
               )
        return len(master.services)


@services_router.get('/get-master-by-service/{service_id}',
                      summary='Get Master By Service ID'
                     )
async def get_master_by_service_id(service_id: int, session=Depends(AsyncDB.get_session)):
    service = await get_service_by_id(service_id=service_id, session=session)
    master = await session.get(Master, service.master_id)

    if not master:
        raise HTTPException(status_code=404, detail="Майстер не знайдений")

    await session.refresh(master, attribute_names=["user"])
    
    return master.user


@services_router.delete('/{service_id}', 
                        summary='Delete Service By ID',
                        status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_id: int, session = Depends(AsyncDB.get_session)):
      service = await check_service_exsists_exception(service_id, session)
      if service:
            await session.delete(service)
            return {'detail': 'Послугу видалено'}


@services_router.put('/{service_id}',
                      summary='Change Service Info',
                      description='Change Service By ID ( field and data required )',
                     response_model=ServiceResponse)
async def update_service(
                    service_id: int,
                    data: ServiceUpdate,
                    session = Depends(AsyncDB.get_session)
                ):
        service = await check_service_exsists_exception(service_id, session)

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
              raise HTTPException(
                    detail='Не передано жодного поля для оновлення',
                    status_code=status.HTTP_400_BAD_REQUEST
              )
        
        await session.execute(
              update(Service).
              where(Service.id == service_id).
              values(**update_data)
        )

        updated = await session.scalar(select(Service).where(Service.id == service_id))

        return updated