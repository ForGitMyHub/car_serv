from datetime import date


from src.dao.base import BaseDAO
from src.database import async_session_maker, engine
from src.mechanics.models import Mechanics

from sqlalchemy import select, and_, func

from src.records.models import Records


class MechanicsDAO(BaseDAO):
    model = Mechanics


    @classmethod
    async def get_free_mechanics(cls, date_from: date): # Функция поиска свободных механиков на дату, 1 механик может принимать 2 машины в день


    # SELECT "id", first_name, last_name, middle_name -- свободные механики в выбранный день
    # FROM mechanics
    # WHERE "role" = 'mechanic' AND "id" NOT IN(
            # 	SELECT mechanic_id
            # 	FROM records
            # 	WHERE date_record = '2023-05-25'
            # 	GROUP BY mechanic_id
            # 	HAVING COUNT(date_record) < 2)

        sub_query = select(Records.mechanic_id).where(Records.date_record == date_from).group_by(Records.mechanic_id).having(func.count(Records.date_record) < 2)

        query_for_free_mechanics = select(Mechanics.id, Mechanics.first_name, Mechanics.last_name, Mechanics.middle_name
                       ).where(and_(Mechanics.role == 'mechanic',
                                    Mechanics.id.notin_(sub_query
                                 )))

        async with async_session_maker() as session:


            # print(query_for_free_mechanics.compile(engine, compile_kwargs={'literal_binds': True}))  # Чтобы увидеть сырой запрос
            result = await session.execute(query_for_free_mechanics)

            return result.mappings().all()