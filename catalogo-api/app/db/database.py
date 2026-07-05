from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings

# Cria o engine de conexão com o PostgreSQL
engine = create_engine(settings.database_url)

# Fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependência injetada nas rotas para obter a sessão do banco."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
