from src.cars.models import Cars
from src.dao.base import BaseDAO
from src.database import async_session_maker, engine
from src.exceptions import CannotBeRecord
from src.mechanics.models import Mechanics
from src.records.models import Records
from sqlalchemy import select, and_, func, insert

from sqlalchemy.exc import SQLAlchemyError # Базовая ошибка алхимии

from src.logger import logger


class RecordsDAO(BaseDAO):
    model = Records

    @classmethod
    async def add(cls, id, car_id, mechanic_id, date_from):

        # WITH rec AS (
        #     SELECT mechanic_id
        #     FROM records
        #     WHERE date_record = '2023-05-06'
        # )
        #
        # SELECT COUNT(rec.mechanic_id)
        # FROM mechanics
        # LEFT JOIN rec ON mechanics."id" = rec.mechanic_id
        # WHERE "role" = 'mechanic' AND mechanics."id" = 7
        # GROUP BY mechanics."id"
        try:
            sub_query = select(Records.mechanic_id).where(Records.date_record == date_from).cte('sub_query') # WITH rec

            query = select(func.count(sub_query.c.mechanic_id)).select_from(Mechanics).join( # Запрос который скажет нам сколько запсей у механика в выбранный день
                sub_query, sub_query.c.mechanic_id == Mechanics.id, isouter=True
            ).where(and_(Mechanics.role == 'mechanic', Mechanics.id == mechanic_id)
                    ).group_by(Mechanics.id)


             # SELECT COUNT("id") AS counter -- Проверка наличия конкретного автомобиля у данного собственника
             # FROM cars
             # WHERE "id" = 1 AND client_id = 'b746cecd-2672-459a-8ab1-c415a5ccd0b0'
             # GROUP BY "id"

            query_for_car = select(func.count(Cars.id).label('cars_status')
                                              ).where(and_(Cars.id == car_id,
                                                           Cars.client_id == id
                                                           )).group_by(Cars.id)

            async with async_session_maker() as session:
                print(query.compile(engine, compile_kwargs={'literal_binds': True}))  # Чтобы увидеть сырой запрос
                result = await session.execute(query)
                mechanic_status: int = result.scalar() # У свободного механика вернётся < 2

                cars_result = await session.execute(query_for_car)
                cars_status: int = cars_result.scalar() # Если у клиента есть автомобиль с id = car_id, то нам вернётся 1

                if mechanic_status >= 2: # Механик занят
                    raise CannotBeRecord # При попытке записаться на того механика у которого 2 записи в выбранный день
                else:
                    if cars_status != 1: # Если вернётся значение отличное от 1, значит, автомобиля либо не существует, либо он принадлежит другому клиенту
                        raise CannotBeRecord # Не даём делать запись на чужую машину
                    else:
                        add_records = insert(Records).values(
                            mechanic_id=mechanic_id,
                            client_id=id,
                            car_id=car_id,
                            date_record=date_from
                        ).returning(Records) # Вернём строку с записью

                        new_record = await session.execute(add_records)
                        await session.commit()
                        return new_record.scalar() # Можем использовать скаляр, т.к. передаём модель целиком
                    # // исправить, видео 1.8.3

        except (SQLAlchemyError, Exception) as e: # Ловим ВСЕ ошибки и далее обрабатываем их в зависимости от их типа
            if isinstance(e, SQLAlchemyError):
                msg = "Database EXC: Cannot add record"

            elif isinstance(e, Exception):
                msg = "Unknown EXC: Cannot add record"
            data ={'id': id, 'car_id': car_id, 'mechanic_id': mechanic_id, 'date_from': date_from}
            logger.error(msg, extra=data, exc_info=True) # Добавляем сообщение об ошибке в логи и переданные данные // exc_info=True чтобы ошибка отобразилась прям в логе (может быть слишком длинной)
            # logger.critical(msg, extra=data, exc_info=True) # задали другой уровень ошибки








