import pytest

from src.clients.dao import ClientsDAO


# Тестируем функцию из DAO
@pytest.mark.parametrize("phone,is_present", [
    ("20230630", True),
    ("20234530630", True),
    (".....", False)
])
async def test_find_user_by_id(phone, is_present):
    user = await ClientsDAO.find_one_or_none(phone=phone)
    print('Пользователь', user)
    if is_present:
        assert user
        assert user.phone == phone
        print('Пользователь существует', user.phone)
    else:
        assert not user