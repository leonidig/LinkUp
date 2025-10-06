from aiogram.fsm.state import State, StatesGroup


class CreateOrder(StatesGroup):
    scheduled_at = State()
    description = State()
    price = State()