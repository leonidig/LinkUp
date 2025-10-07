from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from ..utils import BackendClient


check_new_order_router = Router()


@check_new_order_router.callback_query(F.data.startswith('check_new_order_'))
async def check_new_order(callback: CallbackQuery):
    order_id = callback.data.split('_')[3]
    status, response = await BackendClient.get(f'/orders/{order_id}')
    await callback.message.reply(response)