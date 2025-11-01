from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove


from ..utils import BackendClient
from ..keyboards import (actions_with_services_kb,
                         suggest_create_service,
                         chose_to_delete_service_for_master_kb,
                         delete_service_kb,
                         master_services_kb,
                         chose_field_for_update_kb,
                         main_kb
                        )
from . import build_master_detail_kb
from ..utils.decorators import master_only
from ..states import ServiceUpdate


services_actions_router = Router()


@services_actions_router.message(F.text == 'Дії З Послугами')
@master_only
async def actions_with_services(message: Message):
    status, response = await BackendClient.get(f'/services/count-master-services/{message.from_user.id}')
    if response < 1:
        await message.reply('В тебе немає створених послуг\nСтворити їх ти можеш по кнопці нижче',
                            reply_markup=suggest_create_service()
                            )
    else:
        await message.reply('Ти війшов у розділ дій зі своїми сервісами',
                            reply_markup=actions_with_services_kb()
                            )

@services_actions_router.message(F.text == 'Мої Послуги')
@master_only
async def services_catalog_for_master(message: Message):
    status, response = await BackendClient.get(f'/services/by-master/{message.from_user.id}')
    if len(response) == 0:
        await message.reply('Список пуст')
    else:
        await message.reply('Ось список твоїх послуг', reply_markup=master_services_kb(response))



@services_actions_router.message(F.text == 'Видалити Послугу')
@master_only
async def delete_service_master(message: Message):
    status, response = await BackendClient.get(f'/services/by-master/{message.from_user.id}')
    await message.reply('Ось список сервісів, нажми на той який хочеш видалити', reply_markup=
                        chose_to_delete_service_for_master_kb(services=response))
    


@services_actions_router.callback_query(F.data.startswith('start_delete_service_master_'))
async def start_delete_service_for_master(callback: CallbackQuery):
    await callback.answer()
    service_id = callback.data.split('_')[4]
    status, service = await BackendClient.get(f'/services/{service_id}')
    if status == 404:
        await callback.answer('Послугу не знайдено')
    else:
        await callback.message.reply(f'Ти впевнений що хочеш видалити послугу - {service.get('title')}', 
                                     reply_markup=delete_service_kb(service.get('id'))
                                    )
        

@services_actions_router.callback_query(F.data == 'no_delete_service')
async def no_delete_service(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()  
    await callback.message.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id - 1
        )
    await callback.message.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id - 2
        )
    await callback.message.answer('Видалення відхилено ✔️')



@services_actions_router.callback_query(F.data.startswith('final_delete_service_'))
async def delete_service(callback: CallbackQuery):
     service_id = callback.data.split('_')[3]
     await callback.answer()
     status = await BackendClient.delete(f'/services/{service_id}')
     if status == 204:
        _, response = await BackendClient.get(f'/orders/have/{callback.from_user.id}')
        orders = response.get('has_orders')
        await callback.message.reply('Послугу видалено!', reply_markup=main_kb(
            exists_user=True,
            exists_master=True,
            exists_order=orders
            ))


# update

@services_actions_router.callback_query(F.data.startswith('edit_service_'))
async def start_update(callback: CallbackQuery,
                       state: FSMContext):
    service_id = callback.data.split('_')[2]
    await state.update_data(service_id=service_id)
    await callback.message.reply('Обери поле яке ти хочеш змінити',
                                 reply_markup=chose_field_for_update_kb()
                                )
    await state.set_state(ServiceUpdate.choosing_field)



@services_actions_router.message(ServiceUpdate.choosing_field)
async def choose_field(message: Message, state: FSMContext):
    text = message.text
    field_map = {
        'Назва': 'title',
        'Опис': 'description',
        'Ціна': 'price',
        'Вийти З Меню Зміни Послуги': 'leave'
    }

    if text == 'Вийти З Меню Зміни Послуги':
        await state.clear()
        await message.answer(
            "🔄 Повертаюсь у меню вибору послуги...",
            reply_markup=actions_with_services_kb()
        )

        status, response = await BackendClient.get(f'/services/by-master/{message.from_user.id}')
        if not response or len(response) == 0:
            await message.reply('У тебе немає створених послуг.')
        else:
            await message.answer(
                'Ось список твоїх послуг, обери ту, яку хочеш змінити 👇',
                reply_markup=master_services_kb(response)
            )
        return 1


    elif text not in field_map:
        await message.reply('Обери поле з клавіатури')
    else:
        await state.update_data(field=field_map[text])
        await message.reply(f'Введи нове значення для поля `{text}`')
        await state.set_state(ServiceUpdate.new_value)


@services_actions_router.message(ServiceUpdate.new_value)
async def enter_new_value(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get('field')
    service_id = int(data.get('service_id'))
    new_value = message.text.strip()

    is_valid = True

    if field == 'title':
        if len(new_value) < 20:
            await message.answer("❗ Назва має бути не коротше 20 символів.")
            is_valid = False
        elif len(new_value) > 122:
            await message.answer("❗ Назва не може перевищувати 122 символів.")
            is_valid = False

    elif field == 'description':
        if len(new_value) < 55:
            await message.answer("❗ Опис має бути не коротше 55 символів.")
            is_valid = False
        elif len(new_value) > 1055:
            await message.answer("❗ Опис не може перевищувати 1055 символів.")
            is_valid = False

    elif field == 'price':
        if not new_value.replace('.', '', 1).isdigit():
            await message.answer("❗ Введи коректну ціну (число).")
            is_valid = False
        else:
            new_value = float(new_value)
            if new_value < 0:
                await message.answer("❗ Ціна не може бути від’ємною.")
                is_valid = False

    if is_valid:
        payload = {field: new_value}
        status = await BackendClient.put(f'/services/{service_id}', data=payload)

        if status == 200:
            await message.answer("✅ Дані успішно оновлено!", reply_markup=actions_with_services_kb())
        else:
            await message.answer(f"❌ Помилка при оновленні ({status})")

        await state.clear()


@services_actions_router.message(F.text == 'Вийти З Меню Зміни Послуги')
async def leave_from_edit_service(message: Message, state: FSMContext):
    await state.clear()
    await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id - 1
        )
    await message.answer(
        "🔄 Повертаюсь у меню вибору послуги...",
        reply_markup=ReplyKeyboardRemove()
    )
    
    status, response = await BackendClient.get(f'/services/by-master/{message.from_user.id}')
    
    if not response or len(response) == 0:
        await message.reply('У тебе немає створених послуг.')
    else:
        await message.answer(
            'Ось список твоїх послуг, обери ту, яку хочеш змінити 👇',
            reply_markup=master_services_kb(response)
        )

