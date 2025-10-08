from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..utils import check_master, BackendClient
from ..utils.decorators import master_only
from ..states import ServiceCreate


create_service_router = Router()



@create_service_router.message(F.text == 'Створити Послугу')
@create_service_router.callback_query(F.data == 'create_service_master')
@master_only
async def create_service(target: Message | CallbackQuery,
                         state: FSMContext
                        ):
    if isinstance(target, Message):
        await target.reply('Введи заголовок для послуги: ')
    else:
        await target.message.reply('Введи заголовок для послуги: ')

    await state.set_state(ServiceCreate.title)


@create_service_router.message(ServiceCreate.title)
async def enter_description(message: Message,
                           state: FSMContext
                        ):
    title = message.text
    if len(title) < 20:
        await message.reply('❌ Заголовок не може бути коротше 20 символів')
    elif len(title) > 122:
        await message.reply('❌ Заголовок не може бути довше ніж 122 символа')
    else:
        await state.update_data(title=message.text)
        await message.reply('Введіть опис для я послуги: ')
        await state.set_state(ServiceCreate.description)


@create_service_router.message(ServiceCreate.description)
async def enter_price(message: Message,
                      state: FSMContext
                      ):
    description = message.text

    if len(description) < 55:
        await message.reply('❌ Опис не може бути коротше ніж 20 символів')
    elif len(description) > 1055:
        await message.reply('❌ Опис не може бути довше ніж 1055 символів')
    else:
        await state.update_data(description=description)
        await message.reply('Введіть ціну послуги (в грн): ')
        await state.set_state(ServiceCreate.price)


@create_service_router.message(ServiceCreate.price)
async def save_service_data(message: Message,
                            state: FSMContext
                            ):
    
    if not message.text.isdigit():
        await message.reply('❌ Введи число')
    else:
        price = int(message.text)

        if price < 1:
            await message.reply('❌ Введи корректну ціну послуги')
        elif price > 9999999:
            await message.reply('❌ Введи меньшу ціну ніж 9999999')
        else:
            await state.update_data(price=price)
            await state.update_data(master_id=message.from_user.id)
            data = await state.get_data()
            status, response = await BackendClient.post('/services', data)
            if status == 201:
                await message.reply('Створено!')

            else:
                await message.reply(f'=> {response}')

            await state.clear()