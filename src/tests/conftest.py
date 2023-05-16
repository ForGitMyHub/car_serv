# Файл конфигурации наших тестов

# Чтобы запустить тест - в корне cmd -> pytest -v (-v для информативности + -s для того чтобы увидеть print())
# Можем указать путь до теста конкретного, чтобы запустить только его

# pip install httpx для тестирования эндпоинтов

import asyncio
import json
from datetime import datetime

from sqlalchemy import insert

from src.config import settings

from src.clients.models import Clients  # нужно для того чтобы Base увидел таблицу
from src.mechanics.models import Mechanics  # нужно для того чтобы Base увидел таблицу
from src.cars.models import Cars  # нужно для того чтобы Base увидел таблицу
from src.records.models import Records  # нужно для того чтобы Base увидел таблицу

from src.database import Base, async_session_maker, engine
import pytest

# Импорты связанные с httpx
from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.main import app as fastapi_app


# аргумент autouse=True нужен при написании фикстуры для ее автоматического использования во всех тестах
@pytest.fixture(scope="session", autouse=True) # фикстура это функция, которая подготавливает определённую среду для тестирования. Например, подъём или наполнение БД,
async def prepare_database():
    assert settings.MODE == 'TEST' # Должны убедиться что работаем с тестовой БД

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # Удаление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.create_all) # Добавление всех заданных нами таблиц из БД
        # Не используем alembic для создания БД

    def open_mock_json(model: str): # Импортируем данные для тестовой БД
        with open(f'src/tests/mock_{model}.json', encoding='utf-8') as file:
            return json.load(file)

    clients = open_mock_json('clients')
    cars = open_mock_json('cars')
    mechanics = open_mock_json('mechanics')
    records = open_mock_json('records')

    for client in clients:
        # SQLAlchemy не принимает дату в текстовом формате, поэтому форматируем к datetime
        client["date_reg"] = datetime.strptime(client["date_reg"], "%Y-%m-%d")

    for mechanic in mechanics:
        # SQLAlchemy не принимает дату в текстовом формате, поэтому форматируем к datetime
        mechanic["date_reg"] = datetime.strptime(mechanic["date_reg"], "%Y-%m-%d")

    for record in records:
        # SQLAlchemy не принимает дату в текстовом формате, поэтому форматируем к datetime
        record["date_record"] = datetime.strptime(record["date_record"], "%Y-%m-%d")


    async with async_session_maker() as session: # Будем добавлять данные в БД
        # Важно учитывать порядок PK и FK
        add_clients = insert(Clients).values(clients)
        add_mechanics = insert(Mechanics).values(mechanics)
        add_cars = insert(Cars).values(cars)
        add_records = insert(Records).values(records)

        await session.execute(add_clients)
        await session.execute(add_cars)
        await session.execute(add_mechanics)
        await session.execute(add_records)

        await session.commit() # Коммитим изменения

# Взято из документации к pytest-asyncio https://pytest-asyncio.readthedocs.io/en/latest/reference/fixtures.html#event-loop
# Создаем новый event loop для прогона тестов
@pytest.fixture(scope="session") # scope="session" - означает что фикстура запускается 1 раз на весь прогон всех тестов
def event_loop():
    '''Create an instance of the default event loop for each tect case'''
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function') # scope='function' - нам отдаётся чистый клиент (без записей в куках)
async def ac(): # Async Client
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac: # Импортируем наше приложение, что позволяет прогонять тесты без запуска uvicorn
        yield ac # Для каждой функции будет создан заново


@pytest.fixture(scope='session') # Используем данную фикстуру для проверки эндпоинтов с аутентификацией
async def authenticated_ac(): # Async Client
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac: # Импортируем наше приложение, что позволяет прогонять тесты без запуска uvicorn
        await ac.post("/auth/login", json={
            "phone": '434398',
            "password": "string"
        })
        assert ac.cookies['car_service_token'] # Проверяем наличие нашей куки
        yield ac # Для каждой функции будет создан заново


# Фикстура с сессиями (Нам не понадобится, т.к. внутри наших эндпоинтов сессия уже генерируется)
# @pytest.fixture(scope="function") # Для каждой функции отдельная сессия
# async def session():
#     async with async_session_maker() as session:
#         yield session