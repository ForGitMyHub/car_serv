from celery import Celery

from src.config import settings

celery_app = Celery(
    'app_tasks', # Название
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', # исправить вынести в .env
    include=['src.tasks.tasks'] # Путь где храним задачи
)

# исправить // проблема с celery что он может забить оперативную память, надо придумать что с этим сделать