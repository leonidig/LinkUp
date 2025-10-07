from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from ..utils import BackendClient


select_action_order_router = Router()


@select_action_order_router.callback_query(F.data.startswith('select_action_'))
async def select_action(callback: CallbackQuery):
    action, order_id = callback.data.split('_')[2], callback.data.split('_')[3]

    status = await BackendClient.put(f'/orders/set-status/{order_id}?action={action}', data=None)
    if status == 200:
        await callback.message.reply('Прийнято!')
    else:
        await callback.message.reply(f'Сталася помилка: {status}')
