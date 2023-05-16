from src.database import Base # наши метаданные
from sqlalchemy import Column, Integer, String, JSON, SMALLINT, UUID, Date
from sqlalchemy.dialects.postgresql import JSONB

import uuid


class Clients(Base):
    __tablename__ = 'clients'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4(), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String)
    phone = Column(String, nullable=False, unique=True) # Столбец должен быть уникальным
    email = Column(String, nullable=False)
    date_reg = Column(Date, nullable=False)
    hashed_password = Column(String, nullable=False)