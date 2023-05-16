import asyncio
from typing import List

from fastapi import APIRouter, Query
from datetime import date, datetime

from pydantic import parse_obj_as

from src.mechanics.dao import MechanicsDAO

from src.mechanics.schemas import SMechanicsInfo

from fastapi_cache.decorator import cache

router = APIRouter(
    prefix='/mechanics', # Который будет перед всеми эндпоинтами
    tags=['Персонал'], # Название этого роутера для объединения роутеров в группу в документации
)

@router.get('/free', description='Получение всех свободных механиков на дату') #
async def get_free_mechanics_on_date(date_from: date = Query(..., description=f"Например, {datetime.now().date()}")) -> List[SMechanicsInfo]:
    return await MechanicsDAO.get_free_mechanics(date_from)



@router.get('/{id}', description='Поиск конкретного механика')
async def get_mechanics(id: int) -> SMechanicsInfo:
    user = await MechanicsDAO.find_by_id(id)
    return user

@router.get('', description='Посмотреть всех механиков')
@cache(expire=300) # Храним в кэше 300 секунд
async def get_all_mechanics(): # Используем альтернативный вариант валидации
    await asyncio.sleep(3)  # Для имитации долгого запроса
    result = await MechanicsDAO.find_all()
    result_json = parse_obj_as(list[SMechanicsInfo], result) # Альтернативный вариант валидации
    return result_json


