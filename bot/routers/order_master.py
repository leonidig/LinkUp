from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from ..utils import BackendClient, format_order_response
from ..keyboards import (master_services_kb,
                         order_master_service_kb,
                         check_master_services_kb,
                         choose_orders_by_status_kb,
                         orders_kb,
                         register_kb
                        )


order_master_router = Router()


@order_master_router.callback_query(F.data.startswith('make_order_'))
async def order_master(callback: CallbackQuery, state: FSMContext):
    master_tg_id = callback.data.split('_')[2]
    author = callback.message.from_user.id
    await state.update_data(master_tg_id = master_tg_id)
    status, response = await BackendClient.get(f'/services/by-master/{master_tg_id}')
    
    if not response:
        await callback.message.reply('У Майстра Немає Послуг')
    
    else:
        if master_tg_id != author:
            await callback.message.reply(f'Ось Список Послуг Цього майстра', reply_markup=master_services_kb(services=response))
        else:
            await callback.message.reply(f'Ось ващі послуги', reply_markup=master_services_kb(services=response))


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

Щоб замовити цю послугу - натисни кнопку <b>'Замовити'</b>.
"""
    status, master = await BackendClient.get(f'/services/get-master-by-service/{response.get("id")}')
    username = master.get('username')
    master_tg_id = master.get('tg_id')

    if master.get('tg_id') == callback.from_user.id:
        await callback.message.reply(
            text=text,
            parse_mode='HTML',
            reply_markup=check_master_services_kb(service_id)
        )
    else:
        await callback.message.reply(
            text=text,
            parse_mode="HTML",
            reply_markup=order_master_service_kb(username=username, master_tg_id=master_tg_id, service_id=response.get('id'))
        )


@order_master_router.message(F.text == 'Мої Замовлення')
async def orders_list(message: Message):
    tg_id = message.from_user.id
    status, response = await BackendClient.get(f'/orders/have/{tg_id}')

    if status == 404:
        await message.reply(
            "Для того щоб продивитись список замовлень - потрібно пройти регістрацію",
            reply_markup=register_kb()
        )
    elif response.get('has_orders') == False:
        await message.reply('В тебе немає замовлень')
    else:
        await message.reply('Обери статус замовлення', reply_markup=choose_orders_by_status_kb())



@order_master_router.callback_query(F.data.startswith('selected_status'))
async def choice_status(callback: CallbackQuery):
    await callback.answer()

    selected_status = callback.data.split('_')[2]
    status, response = await BackendClient.get(f'/orders/filtered/{callback.from_user.id}', params={'status': selected_status})

    if status == 404:
        await callback.message.reply('У вас немає замовлень по цьому фільтру')
    else:
        await callback.message.reply('Ось список замовлень', reply_markup=orders_kb(response))



@order_master_router.callback_query(F.data.startswith('order_info_'))
async def get_order_info(callback: CallbackQuery):
    await callback.answer()
    
    status, response = await BackendClient.get(f'/orders/{callback.data.split('_')[2]}')
    order = format_order_response(response)
    await callback.message.reply(f'{order}')