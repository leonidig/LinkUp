from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from ..utils import BackendClient
from ..keyboards import text_user_kb


check_new_order_router = Router()


@check_new_order_router.callback_query(F.data.startswith('check_new_order_'))
async def check_new_order(callback: CallbackQuery):
    order_id = callback.data.split('_')[3]
    status, response = await BackendClient.get(f'/orders/{order_id}')
    status, user = await BackendClient.get(f'/users/{response.get('user_id')}')

    print('*' * 80)
    print(user)
    await callback.message.reply(f'{response}')
    await callback.message.reply('По кнопкам нижче ти можешь зв`язатися з замовником\nДекілька кнопок на той випадок якшо у людини немає юзернейма, або не відкрит номер телефону',
                                 reply_markup=text_user_kb(tg_id=user.get('tg_id'), username=user.get('username'), phone=user.get('phone'))
                                )