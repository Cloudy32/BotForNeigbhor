from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import Bot.markups as kb
from stats import Reg

router=Router() #Роутер для удаленного доступа в другой библиотеке

"""Консоль команды старт"""
@router.message(CommandStart())
async def cmd_start (message: Message):
    await message.answer ("👋Добро пожаловать в бота по поиску сожителей. Он предназначен для того,"
                          "что бы найти себе хорошего соседа к которому можно подселиться или снимать квартиру вместе."
                          " Наш бот подберет вам лучшего соседа исходя из вашего города и характеристик,"
                          " но сначала нужно создать анкету. Для этого нажмите кнопку под этим сообщением (Создать анкету)."
                          " В случае если нужна помощь, нажмите на кнопку (Помощь) или введите команду /help. "
                          "Если хотите связаться с администрацией "
                          "нажмите (Админ).", reply_markup=kb.start_menu)


@router.message(Command('help')) #Команда по вызову меню помощи. Нуждается в доработке
async def cmd_help(message: Message):
    await message.answer("Меню помощи")

"""Начало блока с меню регистрации!"""

@router.callback_query(F.data == 'registration') #Команда по вызову системы регистрации. Нуждается в доработке
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
    await message.answer('Поделитесь номером телефона по кнопке ниже!', reply_markup=kb.get_number)
    await state.set_state(Reg.phone)

@router.message(Reg.phone, F.contact)
async def phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer('Напишите краткое описание о себе(не больше 150 символов)',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Reg.description)

@router.message(Reg.phone)
async def phone(message: Message, state: FSMContext):
    await message.answer('Отправьте контакт по кнопке ниже!!!!')

@router.message(Reg.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Последний шаг, отправьте свое фото')
    await state.set_state(Reg.photo)

@router.message(Reg.photo) #Нуждается в доработке для фотографий
async def photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.text)
    await message.answer('Ваша анкета создана!')
    await state.clear()

"""Конец блока с меню регистрации!"""

@router.callback_query(F.data == 'help') #Команда по вызову меню помощи. Нуждается в доработке
async def help_menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Меню помощи')

@router.callback_query(F.data == 'administrator') #Команда по вызову администратора. Нуждается в доработке
async def call_admin(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Контакты администратора: @Dayyaog')