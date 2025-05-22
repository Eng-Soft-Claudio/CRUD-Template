# backend/tests/conftest.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

import pytest
from typing import Generator, Dict
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.deps import get_db
from app.db.base_class import Base
from app.core.config import settings
from app.schemas.user import UserCreate, EmailStr 
from app.crud import user as crud_user

from tests.utils.user import authentication_token_from_email, random_email, random_lower_string

# =======================================================================================================
# --- Configurações de URL e Fixtures ---                                                           #####
# =======================================================================================================


actual_test_db_url: str = settings.DATABASE_URL_TEST if settings.DATABASE_URL_TEST is not None else "sqlite:///:memory:"

if actual_test_db_url.startswith("sqlite"):
    engine_test = create_engine(
        actual_test_db_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine_test = create_engine(actual_test_db_url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    if not actual_test_db_url.startswith("sqlite:///:memory:"):
        Base.metadata.drop_all(bind=engine_test)

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Fixture de escopo de função que fornece um FastAPI TestClient.
    Este client é configurado para usar o banco de dados de teste,
    sobrescrevendo a dependência 'get_db' da aplicação PARA CADA TESTE,
    usando a instância específica de db_session fornecida pela fixture.
    """
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    del app.dependency_overrides[get_db]


@pytest.fixture(scope="function")
def superuser_token_headers(client: TestClient, db_session: Session) -> Dict[str, str]:
   
    email: EmailStr = settings.FIRST_SUPERUSER_EMAIL
    password: str = settings.FIRST_SUPERUSER_PASSWORD
    
    user = crud_user.get_user_by_email(db_session, email=email)
    if not user:
        user_in_create = UserCreate(
            email=email,
            password=password,
            is_superuser=True,
            is_active=True,
            full_name="Test Superuser"
        )
        crud_user.create_user_by_admin(db_session, user=user_in_create)
    
    return authentication_token_from_email(client=client, email=email, password=password)


@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db_session: Session) -> Dict[str, str]:
    email = random_email()
    password = random_lower_string(8)
    user_in = UserCreate(email=email, password=password, is_active=True, is_superuser=False, full_name="Test Normal User")
    crud_user.create_user(db_session, user=user_in)
    return authentication_token_from_email(client=client, email=email, password=password)