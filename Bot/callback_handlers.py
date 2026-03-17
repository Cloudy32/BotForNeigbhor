from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers import users
from DB.requests import *
import Bot.markups as kb
from stats import Reg

callback_router = Router() # Callback роутер для удаленного доступа в другой библиотеке

"""Хендлер для старта регистрации"""
@callback_router.callback_query(F.data == 'registration')
async def registration(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Для начала выбери свой пол (Мужской/Женский)', reply_markup=kb.get_gender)
    await state.set_state(Reg.gender)

"""Команда пересоздания анкеты"""
@callback_router.callback_query(F.data == 'edit_list')
async def questionnaire_again(callback: CallbackQuery ,state: FSMContext):
    await deleting_user(callback.from_user.id)
    await callback.answer('')
    await callback.message.answer('Для начала выбери свой пол (Мужской/Женский)', reply_markup=kb.get_gender)
    await state.set_state(Reg.gender)

"""Команда по удалению анкеты"""
@callback_router.callback_query(F.data == 'delet_list')
async def del_user(callback: CallbackQuery):
    await deleting_user(callback.from_user.id)
    await callback.answer('')
    await callback.message.answer('Ваша анкета удалена')

"""Блок с кодом демонстрации других анкет!/Подбором анкет по метчу"""
@callback_router.callback_query(F.data == 'vive_lists')
async def viwe_lists(callback: CallbackQuery):
    await users(callback)

@callback_router.callback_query(F.data == 'dislike')
async def next_user(callback: CallbackQuery):
    await users(callback)

@callback_router.callback_query(F.data == 'like')
async def user_next(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer("Пользователю отправлено ваше предложение о совместном проживании!")
    data = await users(callback)
    liked_user_id2 = int(data)
    if data:
        chat_id = liked_user_id2
        second_user_data = await get_data(callback.from_user.id)
        photo = second_user_data.photo
        await callback.bot.send_photo(chat_id=chat_id, photo=photo, caption=f'Анкета человека которому вы понравились \n\n'
                             f'Имя: {second_user_data.name}\n\n' 
                             f'возраст: {second_user_data.age}, пол: {second_user_data.gender}\n\n'
                             f'Город: {second_user_data.city}\n\n' 
                             f'Предпочтительный пол: {second_user_data.desired_gender}\n\n'
                             f'Описание: {second_user_data.description}\n\n'
                             f'id для связи:@{second_user_data.username}')

"""Вызов админа"""
@callback_router.callback_query(F.data == 'administrator')
async def call_admin(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Контакты администратора: @Dayyaog')