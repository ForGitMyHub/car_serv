from datetime import date

from pydantic import BaseModel, EmailStr


class SCars(BaseModel):
    # Схема для добавления автомобиля
    brand: str
    model: str
    number: str
    vin: str
    description: list[str]

    #
    class Config: # нужно чтобы pydantic распознал схему алхимии (Мог обращаться к классам)
        orm_mode = True


class SCarsInfo(BaseModel):
    id: int
    brand: str
    model: str
    number: str
    vin: str
    description: list[str]

    class Config: # нужно чтобы pydantic распознал схему алхимии (Мог обращаться к классам)
        orm_mode = True