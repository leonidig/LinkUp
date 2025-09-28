import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from .keyboards import main_kb
from .routers import (users_register_router,
                      masters_register_router,
                      masters_catalog_router,
                      order_master_router,
                       create_service_router
                    )
from .utils import BackendClient


load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    tg_id = message.from_user.id
    status_code, user_data = await BackendClient.get(f'/users/check-exists/{tg_id}')
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=main_kb(exists_user=user_data)
    )


async def start() -> None:
    dp.include_routers(
        users_register_router,
        masters_register_router,
        masters_catalog_router,
        order_master_router,
        create_service_router
    )
    await dp.start_polling(bot)