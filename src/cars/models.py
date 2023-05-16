from src.database import Base # наши метаданные
from sqlalchemy import Column, Integer, String, JSON, SMALLINT, UUID, Date, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB


class Cars(Base):
    __tablename__ = 'cars'

    id = Column(SMALLINT, primary_key=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    number = Column(String, nullable=False)
    vin = Column(String, nullable=False)
    client_id = Column(ForeignKey('clients.id'), nullable=False)
    description = Column(JSONB, nullable=False)
    photo_link = Column(JSONB, nullable=False)
