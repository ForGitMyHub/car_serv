from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.config import settings

# Выбираем БД в зависимости от MODE
if settings.MODE == 'TEST':
    URL = settings.DATABASE_TEST_URL
    DATABASE_PARAMS = {'poolclass': NullPool} # Параметр для работы с тестовой БД
else:
    URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(URL, **DATABASE_PARAMS)  # Подключение к БД // точка входа sqlalchemy в наше приложение // echo - подробное логгирование

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) # создаём сессию (временное соединение) для работы с БД // expire_on_commit - исчезать после транзакции

class Base(DeclarativeBase): # аналог MetaData() // в дальнейшем будет видоизменяться в классах // используется для моделей создания таблицы и миграций
    pass

async def get_async_session() -> AsyncGenerator[AsyncSession, None]: # Получаем сессию // исправить используется только для вебсокета
    async with async_session_maker() as session:
        yield session