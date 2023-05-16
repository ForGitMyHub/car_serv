# Тестируем эндпоинты, в которых необходима аутентификация

import pytest
from httpx import AsyncClient



@pytest.mark.parametrize("mechanic_id,car_id,date_from,status_code", [
   *[("1", "1", '2023-07-30', 200)]*2,
    ("1", "1", '2023-07-30', 409)
])
async def tests_add_records(mechanic_id, car_id, date_from, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/records", params={ # Используем params чтобы не было проблем с валидацией
        "mechanic_id": mechanic_id,
        "car_id": car_id,
        "date_from": date_from
    })
    assert response.status_code == status_code