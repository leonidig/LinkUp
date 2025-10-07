from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from ..utils import BackendClient, format_order_response
from ..keyboards import text_user_kb, order_choice_action_kb


check_new_order_router = Router()


@check_new_order_router.callback_query(F.data.startswith('check_new_order_'))
async def check_new_order(callback: CallbackQuery):
    order_id = callback.data.split('_')[3]
    status, response = await BackendClient.get(f'/orders/{order_id}')
    status, user = await BackendClient.get(f'/users/{response.get('user_id')}')

    status, service = await BackendClient.get(f'/services/{response.get('service_id')}')
    if status == 200:

        service_name = service.get('title')

        formatted_text = format_order_response(response)
        await callback.message.reply(
            f"{formatted_text}\n💅 <b>Послуга:</b> {service_name}",
            parse_mode="HTML",
            reply_markup=order_choice_action_kb(order_id)
        )


        await callback.message.reply(
            "👇 По кнопкам нижче ти можеш зв’язатися з замовником.\n"
            "Кілька варіантів — на випадок, якщо в користувача немає юзернейму або прихований номер телефону.",
            reply_markup=text_user_kb(
                tg_id=user.get('tg_id'),
                username=user.get('username'),
                phone=user.get('phone')
            )
        )