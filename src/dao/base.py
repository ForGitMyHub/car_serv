from sqlalchemy import select, insert, delete, update

from src.database import async_session_maker, engine


class BaseDAO:
    model = None # В дочерних классах будем переназначать модель

    @classmethod
    async def data_update(cls, id, **kwargs): # Изменение данных
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == id).values(**kwargs)
            await session.execute(query) # исполняем запрос
            await session.commit() # фиксируем все изменения

    @classmethod
    async def find_by_id(cls, model_id: int): # Поиск по id
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id) # Во всех наших моделях есть поле id, поэтому, можем указать имя явно
            result = await session.execute(query)
            return result.scalar_one_or_none() # Вернётся либо один объект, либо ничего


    @classmethod
    async def find_one_or_none(cls, **kwargs): # Запрос SELECT * FROM model WHERE **kwargs (Но одна запись, или ничего)
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none() # Вернётся либо один объект, либо ничего


    @classmethod
    async def find_all(cls, **kwargs):  # Запрос SELECT * FROM model WHERE **kwargs
        async with async_session_maker() as session:
            query = select(cls.model.__table__).filter_by(**kwargs)
            result = await session.execute(query)
            return result.mappings().all()
            #return result.scalars().all()  # Конвертация в JSON // исправить



    @classmethod
    async def add(cls, **kwargs): # INSERT INTO VALUES
        async with async_session_maker() as session:
            query = insert(cls.model).values(**kwargs)
            await session.execute(query) # исполняем запрос
            await session.commit() # фиксируем все изменения


    @classmethod
    async def delete(cls, **kwargs):  # DELETE FROM
        async with async_session_maker() as session:  # используем асинхронный контекстный менеджер
            query = delete(cls.model).filter_by(**kwargs)

            print(query.compile(engine, compile_kwargs={'literal_binds': True})) # Чтобы увидеть сырой запрос

            await session.execute(query) # исполняем запрос
            await session.commit() # фиксируем все изменения