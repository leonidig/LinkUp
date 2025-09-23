from os import getenv

from aiogram import Router, F
from aiogram.types import Message, ReactionTypeEmoji
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from dotenv import load_dotenv

from ..keyboards import contact_keyboard, name_kb
from ..states import UserRegistration
from ..utils import BackendClient


load_dotenv()

users_router = Router(name='Users Router')
BACKEND_URL = getenv('BACKEND_URL')

@users_router.message(F.text == 'Зареєструватися')
async def start_register(message: Message):
    await message.reply('Для звʼязку і безпеки нам потрібно запросити ваш номер', reply_markup=contact_keyboard())


@users_router.message(F.contact)
async def get_number(message: Message, state: FSMContext):
    contact = message.contact
    if contact.user_id == message.from_user.id:
        await message.react([ReactionTypeEmoji(emoji="👍")])
        await message.reply(f"Дякуємо!\nВведіть своє імʼя", reply_markup=name_kb(message.from_user.first_name))
        await state.update_data(number=contact.phone_number)
        await state.set_state(UserRegistration.name)
    else:
        await message.reply("Будь ласка, надішліть свій власний номер ☝️")


@users_router.message(UserRegistration.name)
async def enter_name(message: Message, state: FSMContext):
    await message.react([ReactionTypeEmoji(emoji="👍")])
    context = await state.get_data()
    data = {
        'tg_id': message.from_user.id,
        'username': message.from_user.username,
        'phone': context.get('number'),
        'name': message.text
    }
    await state.clear()

    status = await BackendClient.post("/users/", data)
    if status == 201:
        await message.reply("Done!")
    else:
        await message.reply("Error")