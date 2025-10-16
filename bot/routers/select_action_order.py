from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from ..utils import BackendClient
from ..keyboards import view_order_kb


select_action_order_router = Router()


@select_action_order_router.callback_query(F.data.startswith('select_action_'))
async def select_action(callback: CallbackQuery):
    action, order_id = callback.data.split('_')[2], callback.data.split('_')[3]

    data = {
        'tg_id': callback.from_user.id,
        'action': action
    }
    status_edit = await BackendClient.put(f'/orders/set-status/{order_id}?action={action}&tg_id={callback.from_user.id}', data=None)

    status, response = await BackendClient.get(f'/orders/{order_id}')
    user_tg_id = response.get('user_id')
    status_texts = {
            "confirmed": "Прийнято",
            "cancelled": "Відхилено"
        }

    from .. import bot

    await bot.send_message(
        user_tg_id,
        f'Майстер змінив статус замовлення\nСтатус замовлення тепер: {status_texts[action]}\nПереглянути можеш це натиснувши на кнопку `Мої Замовлення`',
    )
    if status_edit == 200:
        await callback.message.reply('Прийнято!')
    else:
        await callback.message.reply(f'Сталася помилка: {status_edit}')
