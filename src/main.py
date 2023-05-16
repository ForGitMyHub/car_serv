import time

from fastapi import FastAPI, Request
from src.clients.router import router as clients_router
from src.config import settings
from src.mechanics.router import router as mechanics_router
from src.cars.router import router as cars_router
from src.records.router import router as records_router
from src.auth.router import router as auth_router
from src.chat.router import router as chat_router

from src.logger import logger

############ Модули для кэшироввания ############
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
#################################################



app = FastAPI() # start main app

app.include_router(auth_router) # Роутер связанный с аутентификацией

app.include_router(clients_router) # добавили роутер
app.include_router(mechanics_router) # добавили роутер
app.include_router(cars_router) # добавили роутер
app.include_router(records_router) # добавили роутер
app.include_router(chat_router) # добавили роутер


############ Кэщирование ############
@app.on_event("startup") # startup отвечает за запуск приложения // при запуске приложения прогоняется эта функция
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# @app.on_event("shutdown")  # <-- данный декоратор прогоняет код после завершения программы
# def shutdown_event():
#     logger.info("Service exited")

######################################

################## MiddleWare ####################
# Функция которая работает с запросом и ответом и позволяет извлекать данные из одного и другого и прикреплять данные к нашему ответу, например, хэдер (Не только в FastAPI)

# MiddleWare — промежуточный слой между запросом пользователя и ответом. MiddleWare присутствует и в FastAPI, и в Flask, и в Django, и даже в других языках программирования.
# MiddleWare  может как проверять токены авторизации и перенаправлять пользователя на другую страницу, так и изменять ошибки/исключения, отправляемые пользователю

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request) # Получение ответа
    process_time = time.time() - start_time
    # response.headers["X-Process-Time"] = str(process_time)


    # При подключении Prometheus + Grafana подобный лог не требуется, там есть готовые решения
    logger.info("Request handling time", extra={ # выбрали уровель info
        "process_time": round(process_time, 4) # Время обработки запроса
    })
    return response # Теперь при запросах к эндпоинтам есть логгирование времени исполнения запроса

########################################