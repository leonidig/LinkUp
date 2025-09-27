from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from ..utils import check_user, BackendClient
from ..keyboards import register_kb, select_master_by_specialization_kb

masters_catalog_router = Router()



@masters_catalog_router.message(F.text == 'Знайти майстра')
async def masters_catalog(message: Message):
    status, exists = await check_user(message.from_user.id)
    if not exists:
        await message.reply('Для того щоб продивитись список майстрів - потрібно пройти регістрацію', reply_markup=register_kb())
    else: 
        await message.reply('Обери спеціалізацію для майстра', reply_markup=select_master_by_specialization_kb())


@masters_catalog_router.callback_query(F.data.startswith("select_spec_"))
async def select_master_spec(callback: CallbackQuery):
    spec = callback.data.removeprefix("select_spec_")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(f"Ви обрали: {spec}")
    response = BackendClient.get('')