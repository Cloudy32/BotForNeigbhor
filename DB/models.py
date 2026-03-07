"""Модели таблиц"""

from sqlalchemy import BigInteger, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    gender: Mapped[str] = mapped_column(String(10))
    age: Mapped[int] = mapped_column(Integer())
    name: Mapped[str] = mapped_column(String(15))
    city: Mapped[str] = mapped_column(String(30))
    phoneNumber: Mapped[str] = mapped_column(String(15))
    description: Mapped[str] = mapped_column(String(250))
    desired_gender: Mapped[str] = mapped_column()
    photo: Mapped[str] = mapped_column()

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


