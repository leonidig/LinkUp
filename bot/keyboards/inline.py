from aiogram.utils.keyboard import InlineKeyboardBuilder


def chose_specialization_kb():
    builder = InlineKeyboardBuilder()

    specializations = [
        "Розробник",
        "Будівельник",
        "Дизайнер",
        "Фотограф",
        "Водій",
        "Копірайтер",
        "Майстер по ремонту",
        "Майстер краси",
        "Різноробочий",
        "Репетитор"
    ]

    for spec in specializations:
        builder.button(text=spec, callback_data=f"spec_{spec}")

    builder.adjust(2)
    return builder.as_markup()


def register_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text='Зареєструватись', callback_data='register')

    return builder.as_markup()