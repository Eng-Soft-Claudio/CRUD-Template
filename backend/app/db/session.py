# app/db/session.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings


# =======================================================================================================
# --- Motor e Seção local ---                                                                       #####
# =======================================================================================================

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# =======================================================================================================
# --- Dependência ---                                                                               #####
# =======================================================================================================

def get_db() -> Generator[Session, None, None]: # pragma: no cover
    """
    Função de dependência para obter uma sessão do banco de dados por request.
    Garante que a sessão seja fechada após o request, mesmo em caso de erro.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()