from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from DB.requests import *
import Bot.markups as kb
from stats import Reg

router=Router() #Роутер для удаленного доступа в другой библиотеке

"""Консоль команды старт"""
@router.message(CommandStart())
async def cmd_start (message: Message):
    await message.answer ("👋Добро пожаловать в бота по поиску сожителей. Он предназначен для того,"
                          "что бы найти себе хорошего соседа к которому можно подселиться или снимать квартиру вместе."
                          " Наш бот подберет вам лучшего соседа исходя из вашего города и характеристик,"
                          " но сначала нужно создать анкету. Для этого нажмите кнопку (Создать анкету)."
                          " Если хотите связаться с администрацией нажмите (Админ).", reply_markup=kb.start_menu)

"""Начало блока с меню регистрации!"""

"""Блок в доработке. Для завершения блока нужно:
   1. Сделать проверки на честность
   2. Добавить финальную клавиатуру
   3. Сделать просмотр и редактирование анкеты"""

@router.callback_query(F.data == 'registration')
async def registration(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Для начала выбери свой пол (Мужской/Женский)')
    await state.set_state(Reg.meal)

@router.message(Reg.meal)
async def meal(message: Message, state: FSMContext):
    await state.update_data(meal=message.text)
    await message.answer('Введите ваш возраст!')
    await state.set_state(Reg.age)

@router.message(Reg.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите ваше Имя!')
    await state.set_state(Reg.name)

@router.message(Reg.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Напишите ваш город!')
    await state.set_state(Reg.city)

@router.message(Reg.city)
async def name(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer('Поделитесь номером телефона по кнопке ниже!',reply_markup=kb.get_number)
    await state.set_state(Reg.phone)

@router.message(Reg.phone, F.contact)
async def phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer('Напишите краткое описание о себе(не больше 150 символов)',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Reg.description)

@router.message(Reg.phone)
async def phone(message: Message):
    await message.answer('Отправьте контакт по кнопке ниже!!!!')

@router.message(Reg.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Последний шаг, отправьте свое фото')
    await state.set_state(Reg.photo)

@router.message(Reg.photo, F.photo)
async def photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    await message.answer_photo(photo=message.photo[-1].file_id,caption=f'Ваша анкета создана!\n\nИмя: {data["name"]}, '
                         f'возраст: {data["age"]}, пол: {data["meal"]}\n\n'
                         f'Город: {data["city"]}, номер телефона: {data["phone"]}\n\n'
                         f'Описание: {data["description"]}')

    data_set = User(
        tg_id = message.from_user.id,
        meal = data.get('meal'),
        age=data.get('age'),
        name=data.get('name'),
        city=data.get('city'),
        phoneNumber=data.get('phone'),
        description=data.get('description'),
        photo=data.get('photo')
    )

    await set_user(message.from_user.id, data_set)
    await state.clear()

@router.message(Reg.photo)
async def photo(message: Message):
    await message.answer('Отправьте пожалуйста фотографию')

"""Конец блока с меню регистрации!"""

"""Блок с кодом демонстрации других анкет!/Подбором анкет по метчу"""

@router.callback_query(F.data == 'administrator')
async def call_admin(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Контакты администратора: @Dayyaog')