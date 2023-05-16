from src.database import Base # наши метаданные
from sqlalchemy import Column, Integer, String, JSON, SMALLINT, UUID, Date, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB


class Records(Base):
    __tablename__ = 'records'

    id = Column(SMALLINT, primary_key=True, nullable=False)
    mechanic_id = Column(ForeignKey('mechanics.id'), nullable=False)
    client_id = Column(ForeignKey('clients.id'), nullable=False)
    car_id = Column(ForeignKey('cars.id'), nullable=False)
    date_record = Column(Date, nullable=False)
