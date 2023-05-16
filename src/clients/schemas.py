from datetime import date

from pydantic import BaseModel, EmailStr


class SClientsInfo(BaseModel): # Возврат данных без пароля
    first_name: str
    last_name: str
    middle_name: str | None = None
    phone: str
    email: EmailStr
    date_reg: date



    class Config: # нужно чтобы pydantic распознал схему алхимии (Мог обращаться к классам)
        orm_mode = True


class SClients(SClientsInfo):

    password: str


    class Config: # нужно чтобы pydantic распознал схему алхимии (Мог обращаться к классам)
        orm_mode = True


