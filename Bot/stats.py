from aiogram.fsm.state import StatesGroup, State

class Reg(StatesGroup):
    meal = State()
    age = State()
    name = State()
    phone = State()
    description = State()
    photo = State()
