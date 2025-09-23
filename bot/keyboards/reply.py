from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_kb():
    builder = ReplyKeyboardBuilder()

    builder.button(text='Зареєструватися')

    builder.adjust(1)
    return builder.as_markup()


def name_kb(name: str):
    builder = ReplyKeyboardBuilder()

    builder.button(text=name)
    
    return builder.as_markup()


def contact_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Відправити", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )