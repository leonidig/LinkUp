from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states import MasterCreate
from ..keyboards import (main_kb,
                         chose_specialization_kb,
                         main_kb, register_kb,
                         suggest_create_service,
                         exit_from_register_master_kb
                        )
from ..utils import BackendClient, check_user, check_master


masters_register_router = Router(name='Masters Router')



@masters_register_router.callback_query(F.data == 'exit_from_register_master')
async def exit_registering(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.reply('Ви повернулися в головне меню', reply_markup=main_kb(exists_user=True))


@masters_register_router.message(F.text == "Створити Профіль Майстера")
async def create_master_profile(message: Message):
    user_id = message.from_user.id
    exists_user = await check_user(user_id)
    exists_master = await check_master(user_id)

    if not exists_user:
        await message.answer("Для того щоб створити профіль майстра, спершу пройди реєстрацію", reply_markup=register_kb())
    elif exists_master:
        await message.reply("Ти вже створив профіль майстра")
    else:
        await message.reply('Якщо ти зайшов сюди випадково - натисни на кнопку `Вийти`', reply_markup=exit_from_register_master_kb())
        await message.answer("Обери спеціальність", reply_markup=chose_specialization_kb())


@masters_register_router.callback_query(F.data.startswith('spec_'))
async def enter_specialization(callback: CallbackQuery, state: FSMContext):
    spec = callback.data.split('spec_')[1]
    await state.update_data(specialization=spec)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text(f'Обрана спеціальність - {spec}')
    await callback.message.reply("Скільки в тебе досвіду (в роках)?")
    await state.set_state(MasterCreate.experience_years)


@masters_register_router.message(MasterCreate.experience_years)
async def enter_experience_years(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply("❌ Введи, будь ласка, число років досвіду (тільки цифри).")
        return
    experience = int(message.text)
    if experience < 1:
        await message.reply("❌ Досвід не може бути менше 1 року.")
    elif experience > 70:
        await message.reply("❌ Досвід не може бути більше 70 років.")
    else:
        await state.update_data(experience_years=experience)
        await message.reply("✅ Прийнято! Введи або адресу своєї точки\nАбо райони у які ти можеш приїхати\nАбо наприклад онлайн по всьому світу: ")
        await state.set_state(MasterCreate.location)


@masters_register_router.message(MasterCreate.location)
async def enter_location(message: Message, state: FSMContext):
    location = message.text.strip()
    if len(location) < 10:
        await message.reply("❌ Адреса або райони занадто короткі. Мінімум 10 символів.")
    elif len(location) > 155:
        await message.reply("❌ Адреса або райони занадто довгі. Максимум 155 символів.")
    else:
        await state.update_data(location=location)
        await message.reply("✅ Прийнято! Введи реферальний бонус у відсотках:")
        await state.set_state(MasterCreate.ref_bonus)


@masters_register_router.message(MasterCreate.ref_bonus)
async def enter_ref_bonus(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply("❌ Введи, будь ласка, число від 0 до 100.")
        return
    ref_bonus = int(message.text)
    if ref_bonus < 0:
        await message.reply("❌ Мінімальний бонус = 0%")
    elif ref_bonus > 100:
        await message.reply("❌ Максимальний бонус = 100%")
    else:
        await state.update_data(ref_bonus=ref_bonus)
        await message.reply("✅ Прийнято! Введи свій розклад:")
        await state.set_state(MasterCreate.schedule)


@masters_register_router.message(MasterCreate.schedule)
async def enter_schedule(message: Message, state: FSMContext):
    schedule = message.text.strip()
    if len(schedule) < 5:
        await message.reply("❌ Розклад занадто короткий. Мінімум 5 символів.")
    elif len(schedule) > 255:
        await message.reply("❌ Розклад занадто довгий. Максимум 255 символів.")
    else:
        await state.update_data(schedule=schedule)
        await message.reply("✅ Прийнято! Тепер додай опис для профіля (мінімум 55 символів):")
        await state.set_state(MasterCreate.description)


@masters_register_router.message(MasterCreate.description)
async def enter_description(message: Message, state: FSMContext):
    description = message.text.strip()
    if len(description) < 55:
        await message.reply("❌ Опис занадто короткий. Мінімум 55 символів.")
    elif len(description) > 1055:
        await message.reply("❌ Опис занадто довгий. Максимум 1055 символів.")
    else:
        await state.update_data(description=description, tg_id=message.from_user.id)
        data = await state.get_data()
        status, response = await BackendClient.post('/masters/', data)

        if status == 201:
            await message.reply("✅ Ти зареєстрований!", reply_markup=main_kb(exists_user=True, exists_master=True))
            await message.reply("Також можеш вже додати свої послуги натиснувши на кнопку нижче", reply_markup=suggest_create_service())
        await state.clear()
