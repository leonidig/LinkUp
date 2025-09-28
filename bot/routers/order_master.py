from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ..utils import BackendClient


order_master_router = Router()


@order_master_router.callback_query(F.data.startswith('order_'))
async def order_master(callback: CallbackQuery, state: FSMContext):
    await state.update_data(master_tg_id = callback.data.split('_')[1])
    await callback.message.reply('')