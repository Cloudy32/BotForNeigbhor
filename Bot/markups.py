from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start_menu = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Создать анкету', callback_data='registration')],
                     [InlineKeyboardButton(text='Админ', callback_data='administrator')]])

menu = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Просмотреть анкету', callback_data='vive_list')],
                     [InlineKeyboardButton(text='Редактировать анкету', callback_data='edit_list')]]
)


get_number = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True,)]], resize_keyboard=True
)

get_gender = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Мужской')], [KeyboardButton(text='Женский')]], resize_keyboard=True
)

gender_for_match = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Мужской')], [KeyboardButton(text='Женский')],[KeyboardButton(text='Неважно')]],
    resize_keyboard=True
)