from src.database import Base # наши метаданные
from sqlalchemy import Column, Integer, String, JSON, SMALLINT, UUID, Date, Boolean, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB


class Mechanics(Base):
    __tablename__ = 'mechanics'

    id = Column(SMALLINT, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String)
    phone = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    date_reg = Column(Date, nullable=False)
    role = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    hashed_password = Column(String, nullable=False)
    __table_args__ = (
        CheckConstraint(role.in_(['admin', 'mechanic']), name='chk_mechanics_role'),  # Делаем валидацию на стороне базы
    )