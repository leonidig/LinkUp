from aiogram import Router, F
from aiogram.types import Message


masters_catalog_router = Router()


@masters_catalog_router.message(F.text == 'Знайти майстра')
async def masters_catalog(message: Message):
    await message.reply('Some')