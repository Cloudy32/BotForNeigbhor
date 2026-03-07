from aiogram.fsm.state import StatesGroup, State

class Reg(StatesGroup):
    gender = State()
    age = State()
    name = State()
    city = State()
    phone = State()
    description = State()
    desired_gender = State()
    photo = State()