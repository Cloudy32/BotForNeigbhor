from aiogram import Bot, Dispatcher
from handlers import  router
import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from DB.database import async_main

load_dotenv(find_dotenv())

bot=Bot(os.getenv('TOKEN'))
dp = Dispatcher()

async def main():
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        print("Бот запущен...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен...')