from datetime import date

from pydantic import BaseModel, EmailStr


class SMechanics(BaseModel):
    'Pydantic схема'

    first_name: str
    last_name: str
    middle_name: str | None = None
    phone: str
    email: EmailStr
    date_reg: date
    role: str
    password: str

    class Config: # нужно чтобы pydantic распознал схему алхимии (Мог обращаться к классам)
        orm_mode = True


class SMechanicsInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str | None = None

    class Config: # нужно чтобы pydantic распознал схему алхимии (Мог обращаться к классам)
        orm_mode = True