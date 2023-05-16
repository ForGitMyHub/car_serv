import asyncio
from datetime import date, datetime
from typing import List

from fastapi import APIRouter, Request, Depends, Query
from pydantic import parse_obj_as

from src.auth.dependencies import get_current_user
from src.clients.models import Clients
from src.exceptions import CannotBeRecord
from src.records.dao import RecordsDAO
from src.records.schemas import SRecords

from fastapi_cache.decorator import cache

router = APIRouter(
    prefix='/records', # Который будет перед всеми эндпоинтами
    tags=['Записи на обслуживание'], # Название этого роутера для объединения роутеров в группу в документации
)

@router.get('', description='Запрос на получение всех записей клиента') #
@cache(expire=60) # Храним в кэше 60 секунд
async def get_records(user: Clients = Depends(get_current_user)) -> List[SRecords]:
    # print(user, type(user), user.id) #
    await asyncio.sleep(3) # Для имитации долгого запроса
    records = await RecordsDAO.find_all(client_id=user.id)
    return records


@router.post('', description='Добавить запись на обслуживание')
async def add_records(mechanic_id: int, car_id: int,
                      date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
                      user: Clients = Depends(get_current_user)): # Запрос на добавление записи
    new_records = await RecordsDAO.add(user.id, car_id, mechanic_id, date_from)
    if not new_records:
        raise CannotBeRecord
    return new_records


@router.delete('/{record_id}', name='Удалить', description='Удалить запись', status_code=204 )
async def delete_records(record_id: int, user: Clients = Depends(get_current_user)): # Запрос на удаление записи
    '''DELETE FROM bookings
       WHERE id = 1 AND user_id = 2'''
    await RecordsDAO.delete(id=record_id, clients_id=user)
    return {'message': 'success'}


