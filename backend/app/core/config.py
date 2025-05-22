# app/core/config.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from typing import Optional
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict 
from dotenv import load_dotenv


# =======================================================================================================
# --- Carrega Variáveis de Ambiente ---                                                             #####
# =======================================================================================================

load_dotenv()

# =======================================================================================================
# --- Configurações ---                                                                             #####
# =======================================================================================================

class Settings(BaseSettings):
    PROJECT_NAME: str = "CRUD-Template"
    API_V1_STR: str = "/api/v1"

    # Configurações do Banco de Dados
    DATABASE_URL: str = "postgresql://default_user:default_password@localhost:5432/default_db"
    DATABASE_URL_TEST: Optional[str] = None

    # Configurações para JWT 
    SECRET_KEY: str = "a_very_secret_key_that_should_be_long_and_random_and_changed"
    RECOVERY_TOKEN_SECRET_KEY: str = "a_very_secret_key_that_should_be_long_and_random_and_changed"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  

    # Configurações de tipo
    FIRST_SUPERUSER_EMAIL: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethis"

    # Configurações para Token de Recuperação de Senha
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 1
    SERVER_HOST: str = "http://localhost:8000"

    # Configurações para Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # Configurações de Ambiente
    model_config = SettingsConfigDict(
        env_file=".env",        
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'          
    )

settings = Settings()