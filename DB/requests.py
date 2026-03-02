"""Файл запросов к БД"""
from pydantic import with_config

from DB.models import User, async_session
from sqlalchemy import select, insert

async def set_user(tg_id: int, data_set):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(data_set)
            await session.commit()


async def get_data(tg_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))

        user = result.scalar_one_or_none()
        return user

async def deleting_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            await session.delete(user)
            await session.commit()

