from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://biblioteca:biblioteca@db:5432/biblioteca"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
