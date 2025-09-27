from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_kb(exists_user: bool,
            exists_master: bool = False
            ):
    builder = ReplyKeyboardBuilder()

    if not exists_user:
        builder.button(text='Зареєструватися')
    if not exists_master and exists_user:
        builder.button(text='Створити Профіль Майстера')
    if exists_user and exists_master:
        builder.button(text='Some Btn If All')
    if exists_master or exists_user:
        builder.button(text='Знайти майстра')

    builder.adjust(1)
    return builder.as_markup()


def name_kb(name: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=name)]],
        resize_keyboard=True,
        one_time_keyboard=True 
    )


def contact_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Відправити", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )