from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from Bot.markups import like_dislike
from DB.requests import *
import Bot.markups as kb
from stats import Reg

router=Router() #Роутер для удаленного доступа в другой библиотеке



async def users(callback: CallbackQuery):
    data = await get_another_user(callback.from_user.id)

    if data is None:
        await callback.answer('')
        await callback.message.answer("Других анкет нет")
    else:
        photo = data.photo
        await callback.answer('')
        await callback.message.answer_photo(photo=photo, caption=f'Имя: {data.name}, '
                                     f'возраст: {data.age}, пол: {data.meal}\n\n'
                                     f'Город: {data.city}, номер телефона: {data.phoneNumber}\n\n'
                                     f'Предпочтительный пол: {data.desired_gender}\n\nОписание: {data.description}',
                                            reply_markup=like_dislike)

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
   1. Сделать проверки на честность +
   2. Добавить финальную клавиатуру +
   3. Сделать просмотр и редактирование анкеты + """

@router.callback_query(F.data == 'registration')
async def registration(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Для начала выбери свой пол (Мужской/Женский)', reply_markup=kb.get_gender)
    await state.set_state(Reg.meal)

@router.message(Reg.meal)
async def meal(message: Message, state: FSMContext):
    if message.text == 'Мужской' or message.text == 'Женский':
        await state.update_data(meal=message.text)
        await message.answer('Введите ваш возраст! (цифрами)', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Reg.age)
    else:
        await message.answer('Выбери пол из двух возможных вариантов')

@router.message(Reg.age)
async def age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=int(message.text))
        await message.answer('Введите ваше Имя!')
        await state.set_state(Reg.name)
    else:
        await message.answer('Пожалуйста введите возраст цифрами!')

@router.message(Reg.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await message.answer('Напишите ваш город!')
    await state.set_state(Reg.city)

@router.message(Reg.city)
async def name(message: Message, state: FSMContext):
    await state.update_data(city=message.text.capitalize())
    await message.answer('Поделитесь номером телефона по кнопке ниже!',reply_markup=kb.get_number)
    await state.set_state(Reg.phone)

@router.message(Reg.phone, F.contact)
async def phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer('Напишите краткое описание о себе(не больше 250 символов)',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Reg.description)

@router.message(Reg.phone)
async def phone(message: Message):
    await message.answer('Отправьте контакт по кнопке ниже!!!!')

@router.message(Reg.description)
async def description(message: Message, state: FSMContext):
    if len(message.text) <= 250:
        await state.update_data(description=message.text)
        await message.answer('выберите пол соседа(Мужской, Женский, Неважно)', reply_markup=kb.gender_for_match)
        await state.set_state(Reg.desired_gender)
    else:
        await message.answer('Введите описание не более 250 символов')

@router.message(Reg.desired_gender)
async def desired_gender(message: Message, state: FSMContext):
    if message.text == 'Мужской' or message.text == 'Женский' or message.text == 'Неважно':
        await state.update_data(desired_gender=message.text)
        await message.answer('Последний шаг, отправьте свое фото', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Reg.photo)
    else:
        await message.answer('Выберите вариант из трех предложенных')

@router.message(Reg.photo, F.photo)
async def photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    await message.answer_photo(photo=message.photo[-1].file_id,caption=f'Ваша анкета создана!\n\nИмя: {data["name"]}, '
                         f'возраст: {data["age"]}, пол: {data["meal"]}\n\n'
                         f'Город: {data["city"]}, номер телефона: {data["phone"]}\n\n'
                         f'Предпочтительный пол: {data["desired_gender"]}\n\nОписание: {data["description"]}',
                               reply_markup=kb.menu)

    data_set = User(
        tg_id = message.from_user.id,
        meal = data.get('meal'),
        age=data.get('age'),
        name=data.get('name'),
        city=data.get('city'),
        phoneNumber=data.get('phone'),
        description=data.get('description'),
        desired_gender=data.get('desired_gender'),
        photo=data.get('photo')
    )

    await set_user(message.from_user.id, data_set)
    await state.clear()

@router.message(Reg.photo)
async def photo(message: Message):
    await message.answer('Отправьте пожалуйста фотографию')

"""Конец блока с меню регистрации!"""

"""Блок вспомогательных команд"""
"""Команда вывода своей анкеты"""

@router.message(Command('view_the_questionnaire'))
async def view_the_questionnaire(message: Message):
    data = await get_data(message.from_user.id)
    if data is None:
        await message.answer("Вы еще не создали анкету, для начала создайте анкету")
    else:
        photo_id = data.photo
        await message.answer_photo(photo=photo_id,caption=f'Ваша анкета! \n\nИмя: {data.name}, '
                             f'возраст: {data.age}, пол: {data.meal}\n\n'
                             f'Город: {data.city}, номер телефона: {data.phoneNumber}\n\n'
                             f'Предпочтительный пол: {data.desired_gender}\n\nОписание: {data.description}')


"""Команда пересоздания анкеты"""

@router.message(Command('create_the_questionnaire_again'))
async def questionnaire_again(message: Message, state: FSMContext):
    await deleting_user(message.from_user.id)
    await message.answer('Для начала выбери свой пол (Мужской/Женский)', reply_markup=kb.get_gender)
    await state.set_state(Reg.meal)

@router.callback_query(F.data == 'edit_list')
async def questionnaire_again(callback: CallbackQuery ,state: FSMContext):
    await deleting_user(callback.from_user.id)
    await callback.answer('')
    await callback.message.answer('Для начала выбери свой пол (Мужской/Женский)', reply_markup=kb.get_gender)
    await state.set_state(Reg.meal)


"""Команда по удалению анкеты"""

@router.message(Command('del_user'))
async def del_user(message: Message):
    await deleting_user(message.from_user.id)
    await message.answer('Ваша анкета удалена')

@router.callback_query(F.data == 'delet_list')
async def del_user(callback: CallbackQuery):
    await deleting_user(callback.from_user.id)
    await callback.answer('')
    await callback.message.answer('Ваша анкета удалена')

"""Блок с кодом демонстрации других анкет!/Подбором анкет по метчу"""

@router.callback_query(F.data == 'vive_lists')
async def viwe_lists(callback: CallbackQuery):
    await users(callback)


@router.callback_query(F.data == 'dislike')
async def next_user(callback: CallbackQuery):
    await users(callback)

@router.callback_query(F.data == 'like') #Нуждается в доработке жесткой, я хз как это реализовать
async def user_next(callback: CallbackQuery):
    await users(callback)


@router.callback_query(F.data == 'administrator')
async def call_admin(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Контакты администратора: @Dayyaog')