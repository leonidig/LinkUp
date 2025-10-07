from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from ..states import CreateOrder
from ..utils import parse_datetime_or_none, BackendClient
from ..keyboards import view_order_kb


create_order_router = Router()


@create_order_router.callback_query(F.data.startswith('ordering_master_'))
async def order_master(callback: CallbackQuery, state: FSMContext):
    master_id, service_id = callback.data.split('_')[2], callback.data.split('_')[3]

    await state.update_data(master_tg_id=master_id, service_id=service_id)
    await state.set_state(CreateOrder.scheduled_at)
    await callback.message.reply('Введи час на який заплановано приїзд або зустріч\nФормат - 2026-10-25 17:00\nАбо введі - ні, якшо немає часу')


@create_order_router.message(CreateOrder.scheduled_at)
async def enter_scheduled_at(message: Message, state: FSMContext):
    try:
        scheduled_at = parse_datetime_or_none(message.text)
    except ValueError as e:
        await message.reply(str(e))
        return 0

    await state.update_data(scheduled_at=scheduled_at)
    await state.set_state(CreateOrder.description)
    await message.reply("Введи опис задачі для майстра")


@create_order_router.message(CreateOrder.description)
async def enter_description_for_order(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.reply('Введи дедлайн якшо він є\nЯкщо його немає - напиши ні')
    await state.set_state(CreateOrder.deadline)


@create_order_router.message(CreateOrder.deadline)
async def enter_deadline(message: Message, state: FSMContext):
    try:
        deadline = parse_datetime_or_none(message.text)
    except ValueError as e:
        await message.reply(str(e))
        return 0

    await state.update_data(deadline=deadline)
    await state.set_state(CreateOrder.price)
    await message.reply("Введи скільки ти заплатиш (в грн):")


@create_order_router.message(CreateOrder.price)
async def enter_price_for_order(message: Message, state: FSMContext):
    await state.update_data(price=int(message.text), user_tg_id=message.from_user.id)
    data = await state.get_data()

    if data.get("scheduled_at"):
        data["scheduled_at"] = data["scheduled_at"].strftime("%Y-%m-%d %H:%M")
    if data.get("deadline"):
        data["deadline"] = data["deadline"].strftime("%Y-%m-%d %H:%M")

    status, response = await BackendClient.post('/orders/', data=data)
    if status == 201:
        await message.reply('Замовлення створено!')
        from .. import bot

        await bot.send_message(
                    int(data.get('master_tg_id')),
                    'В тебе замовлення',
                    reply_markup = view_order_kb(response.get('id'))
                )
    else:
        await message.reply(f"Сталася помилка при створенні замовлення: {response}")
