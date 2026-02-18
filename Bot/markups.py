from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_menu = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Регистрация', callback_data='registration')],
                     [InlineKeyboardButton(text='Помощь', callback_data='help')],
                     [InlineKeyboardButton(text='Админ', callback_data='administrator')]])