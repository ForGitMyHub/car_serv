from datetime import datetime

from fastapi import Request, HTTPException, status, Depends
from jose import JWTError, jwt

from src.exceptions import TokenAbsentException, IncorrectTokenFormatException, TokenExpiredException, \
    IncorrectEmailOrPassword
from src.clients.dao import ClientsDAO
from src.config import settings
from src.mechanics.dao import MechanicsDAO


def get_token(request: Request):
    'Проверка наличия наших cookies'
    token = request.cookies.get('car_service_token') # Ищем название наших cookies
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)): # парсим токен // Depends - говорит нам от какой функции зависит // async def т.к. внутри используем хотя бы одну асинхронную функцию
    # print(token.cookies) # Убрать при prod
    # print(token.url)
    # print(dir(token))
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALORITHM)  # Декодируем наш токен (ранее мы его кодировали в auth.py)

    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    role_id = payload.get('role')
    user_id: str = payload.get('sub') # исправить // переписать с учётом того что у нас входят работники и клиенты
    if not user_id:
        raise TokenAbsentException

    if role_id == 'employee':
        user_id = int(user_id) # В качестве id у нас встречается как int(для персонала), так и uuid для клиентов
        modelDAO = MechanicsDAO

    elif role_id == 'client':
        modelDAO = ClientsDAO

    user = await modelDAO.find_by_id(user_id) # стоит прописать отдельный метод чтобы получать данные без пароля password
    if not user:
        raise IncorrectEmailOrPassword
    return user



