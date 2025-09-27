from aiogram import Router, F
from aiogram.types import Message

from ..utils import check_user
from ..keyboards import register_kb


masters_catalog_router = Router()


@masters_catalog_router.message(F.text == 'Знайти майстра')
async def masters_catalog(message: Message):
    status, exists = await check_user(message.from_user.id)
    if not exists:
        await message.reply('Для того щоб продивитись список майстрів - потрібно пройти регістрацію', reply_markup=register_kb())