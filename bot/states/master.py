from aiogram.fsm.state import State, StatesGroup


class MasterCreate(StatesGroup):
    specialization = State()
    description = State()
    experience_years = State()
    location = State()
    schedule = State()
    ref_bonus = State()