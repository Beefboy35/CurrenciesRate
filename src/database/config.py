from pydantic_settings import BaseSettings

from src.database.settings import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings(DB_HOST=DB_HOST, DB_PORT=DB_PORT, DB_USER=DB_USER,DB_PASS=DB_PASS, DB_NAME=DB_NAME)
