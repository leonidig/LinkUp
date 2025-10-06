from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


create_order_router = Router()


@create_order_router.callback_query(F.data.startswith('ordering_master_'))
async def order_master(callback: CallbackQuery, state: FSMContext):
    master_id = callback.data.split('_')[2]
    await callback.message.reply(f'{master_id}')