from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from ..utils import BackendClient
from ..keyboards import (actions_with_services_kb,
                         suggest_create_service,
                         delete_service_for_master_kb
                        )
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
    await message.reply(f'{response}')


@services_actions_router.message(F.text == 'Видалити Послугу')
@master_only
async def delete_service_master(message: Message):
    status, response = await BackendClient.get(f'/services/by-master/{message.from_user.id}')
    await message.reply('Ось список сервісів, нажми на той який хочеш видалити', reply_markup=
                        delete_service_for_master_kb(services=response))