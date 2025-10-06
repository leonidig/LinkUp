from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ..utils import BackendClient
from ..keyboards import master_services_kb, order_master_service_kb


order_master_router = Router()


@order_master_router.callback_query(F.data.startswith('make_order_'))
async def order_master(callback: CallbackQuery, state: FSMContext):
    master_tg_id = callback.data.split('_')[2]
    await state.update_data(master_tg_id = master_tg_id)
    status, response = await BackendClient.get(f'/services/by-master/{master_tg_id}')
    if not response:
        await callback.message.reply('У Майстра Немає Послуг')
    else:
        await callback.message.reply(f'Ось Список Послуг Цього майстра', reply_markup=master_services_kb(services=response))


@order_master_router.callback_query(F.data.startswith('service_info_'))
async def get_service_info(callback: CallbackQuery):
    service_id = int(callback.data.split('_')[2])
    status, response = await BackendClient.get(f'/services/{service_id}')

    created_at = response["created_at"]
    date = datetime.fromisoformat(created_at).strftime("%Y-%m-%d %H:%M")
    text = f"""
<b>💼 {response['title']}</b>

📄 <b>Опис:</b>
<blockquote>{response['description']}</blockquote>

💰 <b>Ціна:</b> <blockquote>{response['price']}грн </blockquote>  

🗓 <b>Створено:</b> <blockquote>{date}</blockquote>

Щоб замовити цю послугу — натисни кнопку <b>'Замовити'</b>.
"""
    status, master = await BackendClient.get(f'/services/get-master-by-service/{response.get("id")}')
    username = master.get('username')
    master_tg_id = master.get('tg_id')

    await callback.message.reply(
        text=text,
        parse_mode="HTML",
        reply_markup=order_master_service_kb(username=username, master_tg_id=master_tg_id)
    )
