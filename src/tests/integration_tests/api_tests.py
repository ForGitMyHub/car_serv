from httpx import AsyncClient
import pytest

# def tests_abc(): # Тестовый тест
#     assert 1 == 1

@pytest.mark.parametrize("first_name, last_name, middle_name, phone, email, date_reg, password,status_code", [
                         ("string","string","string","string","user@example.com","2023-05-12","string", 200),
                         ("string","string","string","string","user@example.com","2023-05-12","string", 409), # Проверяем, может ли пользователь второй раз зарегистрироваться, второй раз должна быть 409 ошибка (Сами её прописали в эндпоинте)
                         ("string","string","string","st345ring","userexample.com","2023-05-12","string", 422) # Должны не пройти валидацию по email

                          ])
async def tests_register_user(first_name, # Тест на проверку регистрации
                              last_name,
                              middle_name,
                              phone,
                              email,
                              date_reg,
                              password,
                              status_code,
                              ac: AsyncClient):
    response = await ac.post('/auth/register_clients', json={
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "phone": phone,
        "email": email,
        "date_reg": date_reg,
        "password": password
    }) # для post используем json, для get - params (лучше подробнее заглянуть в ac)

    assert response.status_code == status_code # Во втором прогоне ждём 409 код, а в первом - 200


@pytest.mark.parametrize("phone,password,status_code", [
    ("434398", "string", 200),
    ("20230630", "string", 200)
])
async def tests_login_user(phone, password, status_code, ac: AsyncClient): # Тест функции логина (если используем данные из предыдущего теста - важно соблюдать порядок функций, т.к. тесты работают последовательно, а при перезапуске бд очищается)
    response = await ac.post('/auth/login', json={
        "phone": phone,
        "password": password # Не hashed_password
    })
    assert response.status_code == status_code



