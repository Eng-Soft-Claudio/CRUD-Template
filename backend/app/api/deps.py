# app/api/deps.py

# ====================================================================================
# --- Importações ---                                                            =====
# ====================================================================================

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core import security
from app.core.config import settings
from app.db.models.user import User as UserModel 
from app.schemas.token import TokenData
from app.crud import user as crud_user 

# ====================================================================================
# --- Autenticação ---                                                           =====
# ====================================================================================

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login" #
)

# ====================================================================================
# --- Funções ---                                                                =====
# ====================================================================================

def get_db() -> Generator[Session, None, None]: # pragma: no cover
    """
    Dependência para obter uma sessão do banco de dados por request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_token(token)
        if payload is None:
            raise credentials_exception
        
        token_email_from_payload = payload.get("sub")
        if token_email_from_payload is None:
            raise credentials_exception
        
        token_data = TokenData(email=token_email_from_payload)

    except (JWTError, ValidationError):
        raise credentials_exception

    if token_data.email is None: 
        raise credentials_exception # pragma: no cover

    user = crud_user.get_user_by_email(db, email=token_data.email)
    
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """
    Dependência para obter o usuário atual que também está ativo.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: UserModel = Depends(get_current_active_user),
) -> UserModel:
    """
    Dependência para obter o usuário atual que é ativo e superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user