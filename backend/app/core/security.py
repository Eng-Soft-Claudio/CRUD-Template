# app/core/security.py


# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Dict

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


# =======================================================================================================
# --- Configuração do Passlib para hashing de senhas ---                                            #####
# =======================================================================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
PASSWORD_RESET_TOKEN_EXPIRE_HOURS = settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS

# =======================================================================================================
# --- Funções ---                                                                                   #####
# =======================================================================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha plana corresponde à senha com hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha."""
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Cria um novo refresh token JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_password_reset_token(email: str) -> str:
    """
    Gera um token JWT específico para recuperação de senha.
    O 'sub' do token será o email. Adiciona 'type' claim.
    """
    expire = datetime.now(timezone.utc) + timedelta(hours=PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
    to_encode: Dict[str, Any] = {
        "exp": expire,
        "sub": email,
        "type": "password_reset" 
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verifica um token de recuperação de senha.
    Retorna o email (subject) se o token for válido e do tipo 'password_reset',
    caso contrário, retorna None.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") == "password_reset":
            email_sub = payload.get("sub")
            if isinstance(email_sub, str): 
                 return email_sub
        return None # pragma: no cover
    except JWTError: 
        return None

def decode_token(token: str) -> Optional[dict[str, Any]]:
    """Decodifica um token JWT e retorna o payload se válido, None caso contrário."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_subject_from_token(token: str) -> Optional[str]:
    """
    Decodifica um token JWT e extrai o 'sub' (subject, e.g., email ou user_id) do payload.
    Retorna o subject se o token for válido e o subject estiver presente, caso contrário None.
    """
    payload = decode_token(token)
    if payload:
        return payload.get("sub")
    return None