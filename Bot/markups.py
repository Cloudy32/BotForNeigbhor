from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start_menu = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Создать анкету', callback_data='registration')],
                     [InlineKeyboardButton(text='Помощь', callback_data='help')],
                     [InlineKeyboardButton(text='Админ', callback_data='administrator')]])


get_number = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True,)]], resize_keyboard=True
)