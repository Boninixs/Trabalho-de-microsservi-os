"""
Esse arquivo é responsável pela configuração de conexão com o banco de dados.
Nele há a criação da engine do SQLAlchemy, a configuração da fábrica de sessões (SessionLocal) e 
a definição de uma função de dependência para fornecer sessões ao FastAPI.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db():
    """
    Fornece uma sessão de banco de dados por requisição.

    Utilizado como dependência no FastAPI.

    Yields:
        Sessão ativa do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
