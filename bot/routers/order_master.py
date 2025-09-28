from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ..utils import BackendClient
from ..keyboards import master_services_kb


order_master_router = Router()


@order_master_router.callback_query(F.data.startswith('order_'))
async def order_master(callback: CallbackQuery, state: FSMContext):
    master_tg_id = callback.data.split('_')[1]
    await state.update_data(master_tg_id = master_tg_id)
    status, response = await BackendClient.get(f'/services/by_master/{master_tg_id}')
    if not response:
        await callback.message.reply('У Майстра Немає Послуг')
    else:
        await callback.message.reply(f'Ось Список Послуг Цього майстра', reply_markup=master_services_kb(services=response))


@order_master_router.callback_query(F.data.startswith('service_info_'))
async def get_service_info(callback: CallbackQuery):
    service_id = int(callback.data.split('_')[2])
    status, response = await BackendClient.get(f'/services/{service_id}')
    await callback.message.reply(f'{response}')