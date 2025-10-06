from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from ..states import CreateOrder

create_order_router = Router()


@create_order_router.callback_query(F.data.startswith('ordering_master_'))
async def order_master(callback: CallbackQuery, state: FSMContext):
    master_id = callback.data.split('_')[2]
    await state.update_data(master_tg_id=master_id)
    await state.set_state(CreateOrder.scheduled_at)
    await callback.message.reply('Введи час на який заплановано приїзд або зустріч\nФормат - 2026-10-25 17:00')


@create_order_router.message(CreateOrder.scheduled_at)
async def enter_scheduled_at(message: Message, state: FSMContext):
    date_str = message.text.strip()
    try:
        scheduled_at = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        await message.reply("Некоректний формат! Введи дату у форматі: 2026-10-25 17:00")

    await state.update_data(scheduled_at=scheduled_at)
    await state.set_state(CreateOrder.description)
    await message.reply(f"Введи опис задачі для майстра")


@create_order_router.message(CreateOrder.description)
async def enter_description_for_order(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CreateOrder.price)
    await message.reply('Введи скільки ти заплатиш ( в грн ): ')


@create_order_router.message(CreateOrder.price)
async def enter_price_for_order(message: Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    data = await state.get_data()
    await message.reply(f'{data}')