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
    if exists_master:
        builder.button(text='Дії З Послугами')
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


def actions_with_services_kb():
    builder = ReplyKeyboardBuilder()

    builder.button(text='Мої Послуги')
    builder.button(text='Створити Послугу')
    builder.button(text='Видалити Послугу')
    builder.button(text='Повернутися До Меню')

    builder.adjust(1)

    return builder.as_markup()