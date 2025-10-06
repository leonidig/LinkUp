from aiogram.utils.keyboard import InlineKeyboardBuilder


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
    "Репетитор",
]


def chose_specialization_kb():
    builder = InlineKeyboardBuilder()

    for spec in specializations:
        builder.button(text=spec, callback_data=f"spec_{spec}")

    builder.adjust(2)
    return builder.as_markup()


def select_master_by_specialization_kb():
    builder = InlineKeyboardBuilder()

    for spec in specializations:
        builder.button(text=spec, callback_data=f"select_spec_{spec}")

    builder.adjust(2)
    return builder.as_markup()


def register_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Зареєструватися", callback_data="register")

    return builder.as_markup()


def master_services_kb(services: list[dict]):
    builder = InlineKeyboardBuilder()

    for service in services:
        builder.button(
            text=f"{service.get('title')}",
            callback_data=f"service_info_{service.get('id')}",
        )

    builder.adjust(1)
    return builder.as_markup()


def order_master_service_kb(username: str, master_tg_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text='Списатися з майстром', url=f'https://t.me/{username}')
    builder.button(text='Зробити замовлення', callback_data=f'ordering_master_{master_tg_id}')

    builder.adjust(1)
    return builder.as_markup()