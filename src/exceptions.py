# Файл для прописывания ошибок

from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь уже существует'
)

IncorrectEmailOrPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверная почта или пароль'
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен истёк'
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен отсутствует'
)


IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Некорректный формат токена'
)

UserIsNotPresentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Без комментариев, в целях безопасности>'
)

CannotBeRecord = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Ошибка записи'
)


CannotReplacePassword = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Вы ввели неверный старый пароль'
)

