from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from ..utils import BackendClient
from ..keyboards import (actions_with_services_kb,
                         suggest_create_service,
                         chose_to_delete_service_for_master_kb,
                         delete_service_kb
                        )
from . import build_master_detail_kb
from ..utils.decorators import master_only


services_actions_router = Router()


@services_actions_router.message(F.text == 'Дії З Послугами')
@master_only
async def actions_with_services(message: Message):
    status, response = await BackendClient.get(f'/services/count-master-services/{message.from_user.id}')
    if response < 1:
        await message.reply('В тебе немає створених послуг\nСтворити їх ти можеш по кнопці нижче',
                            reply_markup=suggest_create_service()
                            )
    else:
        await message.reply('Ти війшов у розділ дій зі своїми сервісами',
                            reply_markup=actions_with_services_kb()
                            )

@services_actions_router.message(F.text == 'Мої Послуги')
@master_only
async def services_catalog_for_master(message: Message):
    status, response = await BackendClient.get(f'/services/by-master/{message.from_user.id}')
    await message.reply('Done', reply_markup=build_master_detail_kb(master_id=message.from_user.id))



@services_actions_router.message(F.text == 'Видалити Послугу')
@master_only
async def delete_service_master(message: Message):
    status, response = await BackendClient.get(f'/services/by-master/{message.from_user.id}')
    await message.reply('Ось список сервісів, нажми на той який хочеш видалити', reply_markup=
                        chose_to_delete_service_for_master_kb(services=response))
    


@services_actions_router.callback_query(F.data.startswith('start_delete_service_master_'))
async def start_delete_service_for_master(callback: CallbackQuery):
    service_id = callback.data.split('_')[4]
    status, service = await BackendClient.get(f'/services/{service_id}')
    if status == 404:
        await callback.answer('Послугу не знайдено')
    else:
        await callback.message.reply(f'Ти впевнений що хочеш видалити послугу - {service.get('title')}', 
                                     reply_markup=delete_service_kb(service.get('id'))
                                    )


@services_actions_router.callback_query(F.data.startswith('final_delete_service_'))
async def delete_service(callback: CallbackQuery):
     service_id = callback.data.split('_')[3]
     print(service_id)
     status = await BackendClient.delete(f'/services/{service_id}')
     if status == 204:
        await callback.message.reply('Послугу видалено!')