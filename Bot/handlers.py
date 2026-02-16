import asyncio
from aiogram import types, F, Router
from aiogram.filters import Command, CommandStart

router=Router()

@router.message(CommandStart())
async def cmd_start (message: types.Message):
    await message.answer ("👋Привет")