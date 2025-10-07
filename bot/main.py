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
                      create_service_router,
                      create_order_router,
                      check_new_order_router,
                      select_action_order_router
                    )
from .utils import BackendClient, check_user, check_master


load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    tg_id = message.from_user.id
    exists_user, exists_master = check_user(tg_id), check_master(tg_id)

    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=main_kb(exists_user, exists_master)
    )


async def start() -> None:
    dp.include_routers(
        users_register_router,
        masters_register_router,
        masters_catalog_router,
        order_master_router,
        create_service_router,
        create_order_router,
        check_new_order_router,
        select_action_order_router
    )
    await dp.start_polling(bot)