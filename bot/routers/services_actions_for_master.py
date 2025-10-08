from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from ..utils import BackendClient
from ..utils.decorators import master_only


services_actions_router = Router()


@services_actions_router.message(F.text == 'Мої Послуги')
@master_only
async def services_catalog_for_master(message: Message):
    status, response = await BackendClient.get(f'/services/by-master/{message.from_user.id}')
    await message.reply(f'{response}')