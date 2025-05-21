# etapa1_mvp/conftest.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

import pytest
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app 
from app.api.deps import get_db
from app.db.base_class import Base 
from app.core.config import settings

# =======================================================================================================
# --- Configurações de URL e Fixtures ---                                                           #####
# =======================================================================================================

# --- URL do banco de dados de teste ---
actual_test_db_url: str = settings.DATABASE_URL_TEST if settings.DATABASE_URL_TEST is not None else "sqlite:///:memory:"
"""
URL do banco de dados usada para os testes. Prioriza DATABASE_URL_TEST se definida,
senão utiliza um banco de dados SQLite em memória para execução rápida.
"""

# --- Engine e Session para Testes ---
if actual_test_db_url.startswith("sqlite"):
    engine_test = create_engine(
        actual_test_db_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine_test = create_engine(actual_test_db_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)
"""
Fábrica de sessões SQLAlchemy configurada para o banco de dados de teste.
As sessões não farão autocommit ou autoflush, permitindo controle transacional nos testes.
"""

# --- Fixture para criar o schema do banco de dados de teste antes dos testes ---
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Fixture de escopo de sessão para configurar o schema do banco de dados de teste.
    Cria todas as tabelas no início da sessão de teste e as remove no final,
    a menos que seja um banco SQLite em memória.
    O 'autouse=True' garante que esta fixture seja executada automaticamente para a sessão.
    """
    Base.metadata.create_all(bind=engine_test)
    yield
    if not actual_test_db_url.startswith("sqlite:///:memory:"):
        Base.metadata.drop_all(bind=engine_test)

# --- Fixture para fornecer uma sessão de banco de dados para os testes ---
@pytest.fixture(scope="function") 
def db_session() -> Generator[Session, None, None]:
    """
    Fixture de escopo de função que fornece uma sessão transacional do banco de dados de teste.
    Cria as tabelas (segurança para SQLite em memória), inicia uma transação,
    fornece a sessão ao teste e faz rollback da transação após o teste,
    garantindo isolamento e um estado limpo para o próximo teste.
    """
    Base.metadata.create_all(bind=engine_test)
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close() 

# --- Fixture para o TestClient, sobrescrevendo a dependência get_db ---
@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Fixture de escopo de função que fornece um FastAPI TestClient.
    Este client é configurado para usar o banco de dados de teste,
    sobrescrevendo a dependência 'get_db' da aplicação PARA CADA TESTE.
    Usa a fixture 'db_session' (também de escopo de função).
    """
    def override_get_db() -> Generator[Session, None, None]:
        """Sobrescreve a dependência get_db para usar a sessão de teste."""
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    del app.dependency_overrides[get_db]