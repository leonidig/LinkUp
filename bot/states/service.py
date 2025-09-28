from aiogram.fsm.state import State, StatesGroup


class ServiceCreate(StatesGroup):
    title = State()
    description = State()
    price = State()