from typing import Literal

from pydantic import BaseSettings

class Settings(BaseSettings):

    REDIS_HOST: str
    REDIS_PORT: str

    ALORITHM: str
    SECRET_KEY: str

    # Тут ещё надо указать данные от гугл почты для рассылки

    MODE: Literal['DEV', 'TEST', 'PROD'] # Провеям что входит в одно из значений
    LOG_LEVEL: Literal['INFO', 'DEBUG']

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    DB_TEST_HOST: str
    DB_TEST_PORT: int
    DB_TEST_USER: str
    DB_TEST_PASS: str
    DB_TEST_NAME: str

    @property
    def DATABASE_TEST_URL(self):
        return f"postgresql+asyncpg://{self.DB_TEST_USER}:{self.DB_TEST_PASS}@{self.DB_TEST_HOST}:{self.DB_TEST_PORT}/{self.DB_TEST_NAME}"



    # SECRET_KEY: str # JWT # bash: openssl rand -base64 32
    # ALGORITHM: str  # JWT


    class Config:
        env_file = ".env"




settings = Settings()