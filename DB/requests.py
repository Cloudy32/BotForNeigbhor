"""Файл запросов к БД"""
from pydantic import with_config

import random


from DB.models import User, async_session
from sqlalchemy import select, insert, and_

async def set_user(tg_id: int, data_set) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(data_set)
            await session.commit()


async def get_data(tg_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))

        if result:
            user = result.scalar_one_or_none()
            return user
        else:
            return None

async def deleting_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            await session.delete(user)
            await session.commit()

async def other_user(tg_id: int, city: str, desired_gender: str):
    async with async_session() as session:
        query = select(User).where(
            and_(
                User.tg_id != tg_id,
                User.city.ilike(f"%{city}%")
            )
        )

        if desired_gender and desired_gender.lower() != "Неважно":
            query = query.where(User.desired_gender == desired_gender)

        result = await session.execute(query)
        users = result.scalars().all()

        return random.choice(users)


async def get_another_user(tg_id: int):
    async with async_session() as session:
        current_user = await session.scalar(select(User).where(User.tg_id != tg_id))

        city = current_user.city
        desired_gender = current_user.desired_gender

        another_user = await other_user(tg_id=tg_id, city=city, desired_gender=desired_gender)

        return another_user





