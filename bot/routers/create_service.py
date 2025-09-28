from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..utils import check_master, BackendClient
from ..utils.decorators import master_only
from ..states import ServiceCreate


create_service_router = Router()


@create_service_router.message(F.text == 'Створити Послугу')
@master_only
async def create_service(message: Message,
                         state: FSMContext
                        ):
    await message.reply('Введи заголовок для послуги: ')
    await state.set_state(ServiceCreate.title)


@create_service_router.message(ServiceCreate.title)
async def enter_description(message: Message,
                           state: FSMContext
                        ):
    await state.update_data(title=message.text)
    await message.reply('Введіть описдл я послуги: ')
    await state.set_state(ServiceCreate.description)


@create_service_router.message(ServiceCreate.description)
async def enter_price(message: Message,
                      state: FSMContext
                      ):
    await state.update_data(description=message.text)
    await message.reply('Введіть ціну послуги (в грн): ')
    await state.set_state(ServiceCreate.price)


@create_service_router.message(ServiceCreate.price)
async def save_service_data(message: Message,
                            state: FSMContext
                            ):
    await state.update_data(price=int(message.text))
    await state.update_data(master_id=message.from_user.id)
    data = await state.get_data()
    status, response = await BackendClient.post('/services', data)
    await message.reply(f'=> {response}')
    await state.clear()