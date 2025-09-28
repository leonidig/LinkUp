from os import getenv

from aiogram import Router, F
from aiogram.types import Message, ReactionTypeEmoji, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from dotenv import load_dotenv

from ..keyboards import contact_keyboard, name_kb, main_kb
from ..states import UserRegistration
from ..utils import BackendClient, check_user


load_dotenv()

users_register_router = Router(name='Users Router')
BACKEND_URL = getenv('BACKEND_URL')


@users_register_router.message(F.text == 'Зареєструватися')
@users_register_router.callback_query(F.data == 'register')
async def start_register(update: Message | CallbackQuery):
    user_id = update.from_user.id

    status, exists = await check_user(user_id)

    if not exists:
        text = 'Для звʼязку і безпеки нам потрібно запросити ваш номер'
        if isinstance(update, Message):
            await update.reply(text, reply_markup=contact_keyboard())
        else:
            await update.message.reply(text, reply_markup=contact_keyboard())
    else:
        text = 'Ти вже завреєстрований'
        if isinstance(update, Message):
            await update.reply(text)
        else:
            await update.message.reply(text)


@users_register_router.message(F.contact)
async def get_number(message: Message, state: FSMContext):
    contact = message.contact
    status, exists = await check_user(message.from_user.id)
    if exists:
        await message.reply('Ти вже зареєстрований\nНе треба відправляти свій контакт')
    elif contact.user_id == message.from_user.id:
        await message.react([ReactionTypeEmoji(emoji="👍")])
        await message.reply(f"Дякуємо!\nВведіть своє імʼя", reply_markup=name_kb(message.from_user.first_name))
        await state.update_data(number=contact.phone_number)
        await state.set_state(UserRegistration.name)
    else:
        await message.reply("Будь ласка, надішліть свій власний номер ☝️")


@users_register_router.message(UserRegistration.name)
async def enter_name(message: Message, state: FSMContext):
    if len(message.text.strip()) < 2:
        await message.reply("❗️ Занадто коротке імʼя, введіть ще раз")
    await message.react([ReactionTypeEmoji(emoji="👍")])
    context = await state.get_data()
    data = {
        "tg_id": message.from_user.id,
        "username": message.from_user.username,
        "phone": context.get('number'),
        "name": message.text
    }
    await state.clear()
    status, response = await BackendClient.post("/users/", data)
    if status == 201:
        await message.reply("Ти пройшов реїстрацію!", reply_markup=main_kb(exists_user=True, exists_master=False))
    else:
        await message.reply("Помилка", response)