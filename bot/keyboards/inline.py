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


def order_master_service_kb(username: str, master_tg_id: int, service_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text='Списатися з майстром', url=f'https://t.me/{username}')
    builder.button(text='Зробити замовлення', callback_data=f'ordering_master_{master_tg_id}_{service_id}')

    builder.adjust(1)
    return builder.as_markup()


def suggest_create_service():
    builder = InlineKeyboardBuilder()

    builder.button(text='Створити Послугу', callback_data='create_service_master')

    builder.adjust(1)
    return builder.as_markup()


def view_order_kb(servic_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text='Переглянути', callback_data=f'check_new_order_{servic_id}')

    return builder.as_markup()


def text_user_kb(tg_id: int, phone: str, username: str | None):
    builder = InlineKeyboardBuilder()
    if username is None:
        builder.button(text='Посилланя Для iPhone', url=f'https://t.me/@id{tg_id}')
        builder.button(text='Посилланя Для Andriod', url=f'tg://openmessage?user_id={tg_id}')
        builder.button(text='Посилання через Номер', url=f'https://t.me/{phone}')
    else:
        builder.button(text='Написати замовнику', url=f'https://t.me/{username}')

    builder.adjust(1)

    return builder.as_markup()


def order_choice_action_kb(order_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text='Прийняти', callback_data=f'select_action_confirmed_{order_id}')
    builder.button(text='Відхилити', callback_data=f'select_action_cancelled_{order_id}')

    builder.adjust(2)

    return builder.as_markup()


def chose_to_delete_service_for_master_kb(services: list[dict]):
    builder = InlineKeyboardBuilder()

    for service in services:
        builder.button(
            text=f"{service.get('title')}",
            callback_data=f"start_delete_service_master_{service.get('id')}",
        )

    builder.adjust(1)
    return builder.as_markup()


def delete_service_kb(service_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Так',
        callback_data=f'final_delete_service_{service_id}'
    )
    builder.button(
        text='Ні',
        callback_data=f'no_delete_service'
    )

    builder.adjust(1)
    
    return builder.as_markup()


def check_master_services_kb(service_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Видалити',
        callback_data=f'start_delete_service_master_{service_id}'
    )
    builder.button(
        text='Змінити',
        callback_data=f'edit_service_{service_id}'
    )

    builder.adjust(1)

    return builder.as_markup()