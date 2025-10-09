from aiogram.fsm.state import State, StatesGroup


class ServiceCreate(StatesGroup):
    title = State()
    description = State()
    price = State()


class ServiceUpdate(StatesGroup):
    choosing_field = State()
    new_value = State()