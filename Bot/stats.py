from aiogram.fsm.state import StatesGroup, State

class Reg(StatesGroup):
    gender = State()
    age = State()
    name = State()
    city = State()
    description = State()
    desired_gender = State()
    photo = State()