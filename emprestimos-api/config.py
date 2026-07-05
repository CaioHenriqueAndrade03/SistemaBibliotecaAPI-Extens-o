from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://emprestimos:emprestimos@db_emprestimos:5432/emprestimos"
    catalogo_api_url: str = "http://catalogo-api:8000"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
