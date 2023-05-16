from fastapi import APIRouter


router = APIRouter(
    prefix='/clients', # Который будет перед всеми эндпоинтами
    tags=['Клиенты'], # Название этого роутера для объединения роутеров в группу в документации
)

