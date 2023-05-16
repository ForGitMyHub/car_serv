import asyncio
import os
from typing import List

import aiofiles
from fastapi import APIRouter, Depends, UploadFile, File, Form

from src.auth.dependencies import get_current_user
from src.cars.dao import CarsDAO
from src.cars.func import save_file
from src.cars.schemas import SCars, SCarsInfo
from src.clients.models import Clients
from src.tasks.tasks import process_pic

router = APIRouter(
    prefix='/cars', # Который будет перед всеми эндпоинтами
    tags=['Автомобили'], # Название этого роутера для объединения роутеров в группу в документации
)




@router.post("/add_car", description='Добавить машину')
async def add_car(brand:str=Form(...), model:str=Form(...),
                        number:str=Form(...), vin:str=Form(...),
                        description: list[str]=Form(...),
                        images: List[UploadFile] = File(...), # По протоколу HTTP запрещено одновременно передавать файлы и JSON // в Form можно передать аргументы-ограничения
                         user: Clients = Depends(get_current_user)):
    paths = []
    tasks = []
    base_path = './src/cars/images/' # где сохраняем фото

    # async for # исправить отсутствие async with open
    for image in images:
        file_path = base_path + image.filename
        file_content = await image.read()
        task = asyncio.create_task(save_file(file_path, file_content))
        tasks.append(task)
        paths.append(file_path) # пути к файлам

    # сохранение ссылок на изображения в базу данных
    data = {"urls": paths}
    await asyncio.gather(*tasks)

    for path in data['urls']:
        process_pic.delay(path) # Отправляем задачу обработки картинок в celery

    await CarsDAO.add(client_id=user.id,
                      photo_link=data,
                      brand=brand,
                      model=model,
                      number=number,
                      vin=vin,
                      description=description)

    return {"status": "success"}


@router.get('', description='Получаем свои машины')
async def get_cars(user: Clients = Depends(get_current_user)) -> List[SCarsInfo]:
    cars = await CarsDAO.find_all(client_id=user.id)
    return cars


@router.delete('/{cars_id}', description="Удалить машину", status_code=204) # Установили статус код в случае успеха
async def delete_records(cars_id: int, user: Clients = Depends(get_current_user)): # Запрос на удаление записи
    '''DELETE FROM bookings
       WHERE id = 1 AND user_id = 2'''
    await CarsDAO.delete(id=cars_id, clients_id=user)
    return {"status": "success"}
