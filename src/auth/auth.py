from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from src.exceptions import UserAlreadyExistsException, CannotReplacePassword
from src.clients.dao import ClientsDAO
from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password) -> bool: # Проверяем переданый пароль, соответствует ли он захэшированному паролю в БД
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str: # Хэшируем пароль
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str: # Создаём токен который будем отдавать клиенту
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=45) # Срок жизни токена по умолчанию
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALORITHM) # Кодируем файл
    return encoded_jwt

    print({'user': 'first_user'}) # исправить (убрать перед заливом в гит)
    print(type(ClientsDAO))
    # {'user': 'first_user', "exp": datetime.datetime(дата)


async def registration(dao, user_data):
    existing_user = await dao.find_one_or_none(phone=user_data.phone)
    if existing_user:  # Если сотрудник уже зарегистрирован
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)  # хэшируем пароль
    data = dict(user_data)
    data.pop('password')
    data['hashed_password'] = hashed_password
    print(data)
    await dao.add(**data)

async def authenticate_user(model_dao, phone: str, password: str):
    user = await model_dao.find_one_or_none(phone=phone)

    if not (user and verify_password(password, user.hashed_password)):
        return None

    return user

async def replace_old_password(old_password, new_password, curretnt_user, response):
    if verify_password(old_password, curretnt_user.hashed_password): # Если введённый пользователем старый пароль совпадает с тем что в базе, разрешаем изменение
        new_password = get_password_hash(new_password) # Захешировали новый пароль
        await ClientsDAO.data_update(curretnt_user.id, hashed_password=new_password)
        response.delete_cookie('car_service_token')  # Удаляем куки
        return {'message': 'Вы изменили пароль'}
    else:
        raise CannotReplacePassword


