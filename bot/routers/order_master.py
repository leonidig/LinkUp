from aiogram import Router, F
from aiogram.types import CallbackQuery

from ..utils import BackendClient


order_master_router = Router()


@order_master_router.callback_query(F.data.startswith('order_'))
async def order_master(callback: CallbackQuery):
    master_tg_id = callback.data.split('_')[1]
    status, data = await BackendClient.get(f'/masters/{master_tg_id}')
    await callback.message.reply(f'{data}')