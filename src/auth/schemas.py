from datetime import date

from pydantic import BaseModel, EmailStr


class SAuth(BaseModel):
    phone: str
    password: str


    class Config: # нужно чтобы pydantic распознал схему алхимии (Мог обращаться к классам)
        orm_mode = True