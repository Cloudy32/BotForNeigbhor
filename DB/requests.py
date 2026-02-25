"""Файл запросов к БД"""
from pydantic import with_config

from DB.models import User, async_session
from sqlalchemy import select, insert

async def set_user(tg_id,data_set):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(data_set)
            await session.commit()


