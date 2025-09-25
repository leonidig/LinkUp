from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from ..states import MasterCreate
from ..keyboards import chose_specialization_kb
from ..utils import BackendClient, check_user


masters_router = Router(name='Masters Router')


 

@masters_router.callback_query(F.data.startswith('spec_'))
async def enter_specialization(callback: CallbackQuery,
                               state: FSMContext
                               ):
    spec = callback.data.split('spec_')[1]
    await state.update_data(specialization=spec)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text(f'Обрана спеціальність - {spec}')
    await callback.message.reply('Додай Опис Для Профіля ( просто розкажи базову інформацію для ознаймлення): ')
    await state.set_state(MasterCreate.description)


@masters_router.message(MasterCreate.description)
async def enter_description(message: Message, 
                            state: FSMContext
                            ):
    description = message.text
    await state.update_data(description = description)
    await message.reply('Cкільки в тебе досвіду ( в роках ): ')
    await state.set_state(MasterCreate.experience_years)


@masters_router.message(MasterCreate.experience_years)
async def enter_experience_years(message: Message, 
                                 state: FSMContext
                                 ):
    experience = int(message.text)
    await state.update_data(experience_years=experience)
    await message.reply('Введи або адресу своєї точки\nАбо райони у які ти можеш приїхати')
    await state.set_state(MasterCreate.location)


@masters_router.message(MasterCreate.location)
async def enter_location(message: Message,
                         state: FSMContext
                         ):
    location = message.text
    await state.update_data(location=location)
    await message.reply('Введи свій розклад: ')
    await state.set_state(MasterCreate.schedule)


@masters_router.message(MasterCreate.schedule)
async def enter_schedule(message: Message,
                         state: FSMContext
                        ):
    await state.update_data(schedule=message.text)
    data = await state.get_data()
    status = BackendClient.post('/masters/', data=data)
    if status == 201:
        await message.reply('Ти зареєстрований')

    await message.reply(f'Data -> \n{data}')