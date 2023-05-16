from fastapi import APIRouter, Response, Depends

from src.auth.auth import authenticate_user, create_access_token, registration, \
    replace_old_password
from src.auth.dependencies import get_current_user
from src.auth.schemas import SAuth
from src.clients.models import Clients
from src.clients.schemas import SClients, SClientsInfo
from src.clients.dao import ClientsDAO
from src.exceptions import IncorrectEmailOrPassword, CannotReplacePassword
from src.mechanics.dao import MechanicsDAO
from src.mechanics.models import Mechanics
from src.mechanics.schemas import SMechanics

router = APIRouter(
    prefix='/auth', # Который будет перед всеми эндпоинтами
    tags=['Работа с аутентификацией'], # Название этого роутера для объединения роутеров в группу в документации
)


############################### Вход ################################

@router.post('/login', name='Вход') # Будем передавать данные для создания JWT, поэтому, post
async def login_user(response: Response, user_data: SAuth): # Response - для работы с ответом, чтобы передать токен JWT
    'Вход в систему'
    user = await authenticate_user(ClientsDAO, user_data.phone, user_data.password) # DAO в котором ведём поиск
    if not user:
        raise IncorrectEmailOrPassword
    access_token = create_access_token({'sub': str(user.id), 'role': 'client'})  # всегда приводим к str чтобы избежать ошибок
    response.set_cookie('car_service_token', access_token, httponly=True) # Засетим наши куки под именем 'car_service_token' // httponly для безопасности

    # Тут же добавляем рефреш токен
    return access_token, user #  // только для демонстрации, не отправлять в прод



@router.post('/login_employees', name='Вход персонала', description='Вход в систему для персонала') # Будем передавать данные для создания JWT, поэтому, post
async def login_user(response: Response, user_data: SAuth): # Response - для работы с ответом, чтобы передать токен JWT
    user = await authenticate_user(MechanicsDAO, user_data.phone, user_data.password) # DAO в котором ведём поиск
    if not user:
        raise IncorrectEmailOrPassword
    access_token = create_access_token({'sub': str(user.id), 'role': 'employee'}) # всегда приводим к str чтобы избежать ошибок
    response.set_cookie('car_service_token', access_token, httponly=True) # Засетим наши куки под именем 'car_service_token' // httponly для безопасности

    # Тут же добавляем рефреш токен

    return access_token, user #  // только для демонстрации, не отправлять в прод

############################ Другое ###########################


@router.post('/logout', name="Выход", description='Эндоинт выхода из системы') #
async def logout(response: Response):
    response.delete_cookie('car_service_token') # Удаляем куки
    return {'status': 'Пользователь вышел из системы'}


@router.get('/me', description='"Обо мне"') # Информация "обо мне"
async def info_user_me(curretnt_user: Clients = Depends(get_current_user)) -> SClientsInfo: # Снова применяем зависимости Depends
    return curretnt_user # Возвращаем без пароля

################################################################



############################ Замена пароля ############################

@router.patch('/replace_password', name='Замена пароля пользователя') #
async def replace_password(old_password: str, new_password: str, response: Response, curretnt_user: Clients = Depends(get_current_user)):
    'Замена пароля' # Альтернативный способ описания энпоинта в swagger
    return await replace_old_password(old_password, new_password, curretnt_user, response)


@router.patch('/replace_password_employee', name='Замена пароля персонала') #
async def replace_password(old_password: str, new_password: str, response: Response, curretnt_user: Mechanics = Depends(get_current_user)):
    'Замена пароля (Для персонала)'
    return await replace_old_password(old_password, new_password, curretnt_user, response)

#####################################################################

############################ Регистрация ############################

@router.post('/register_clients') #
async def register_user(user_data: SClients):
    'Регистрация'
    await registration(ClientsDAO, user_data)


@router.post('/register_employees') #
async def register_user(user_data: SMechanics):
    'Регистрация персонала (По дефолту статус активности False)'
    await registration(MechanicsDAO, user_data)
#####################################################################



