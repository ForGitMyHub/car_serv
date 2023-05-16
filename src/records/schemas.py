from datetime import date

from pydantic import BaseModel, EmailStr, UUID4


class SRecords(BaseModel):
    'Pydantic схема'

    id: int
    mechanic_id: int
    client_id: UUID4
    car_id: int
    date_record: date

    class Config: # нужно чтобы pydantic распознал схему алхимии (Мог обращаться к классам)
        orm_mode = True