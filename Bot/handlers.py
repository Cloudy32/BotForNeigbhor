import asyncio
from aiogram import types, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
import Bot.markups as kb

router=Router() #Роутер для удаленного доступа в другой библиотеке

"""Консоль команды старт"""
@router.message(CommandStart())
async def cmd_start (message: Message):
    await message.answer ("👋Добро пожаловать в бота по поиску сожителей. Он предназначен для того,"
                          "что бы найти себе хорошего соседа к которому можно подселиться или снимать квартиру вместе."
                          " Наш бот подберет вам лучшего соседа исходя из вашего города и характеристик,"
                          " но сначала надо зарегистрироваться. Для этого нажмите кнопку под этим сообщением (Регистрация)."
                          " В случае если нужна помощь, нажмите на кнопку (Помощь) или введите команду /help. "
                          "Если хотите связаться с администрацией "
                          "нажмите (Админ).", reply_markup=kb.start_menu)









@router.message(Command('help')) #Команда по вызову меню помощи. Нуждается в доработке
async def cmd_help(message: Message):
    await message.answer("Меню помощи")

@router.callback_query(F.data == 'registration') #Команда по вызову системы регистрации. Нуждается в доработке
async def registration(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Меню регистрации')

@router.callback_query(F.data == 'help') #Команда по вызову меню помощи. Нуждается в доработке
async def help_menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Меню помощи')

@router.callback_query(F.data == 'administrator') #Команда по вызову администратора. Нуждается в доработке
async def call_admin(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Контакты администратора: @Dayyaog')