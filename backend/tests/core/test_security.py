# tests/core/test_security.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    get_subject_from_token,
    verify_password,
)
from jose import jwt
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from typing import Dict, Any 

# =======================================================================================================
# --- Testes ---                                                                                    #####
# =======================================================================================================

def test_password_hashing_and_verification():
    """
    Testa a geração de hash de senha e a verificação da senha.
    Verifica se:
    - O hash é diferente da senha original.
    - A senha correta é verificada com sucesso.
    - Uma senha incorreta falha na verificação.
    """
    password = "a_plain_password"
    hashed_password = get_password_hash(password)
    assert hashed_password != password, "Hashed password should not be the same as plain password"
    assert verify_password(password, hashed_password), "Verification of correct password should succeed"
    assert not verify_password("wrong_password", hashed_password), "Verification of wrong password should fail"

def test_create_and_decode_access_token():
    """
    Testa a criação de um token de acesso JWT e sua decodificação.
    Verifica se:
    - Um token é gerado.
    - O token pode ser decodificado com sucesso.
    - O payload decodificado contém os dados esperados (subject, claims customizadas, expiração).
    - Tokens com tempo de expiração curto também funcionam.
    """
    payload_data = {"sub": "testuser@example.com", "custom_claim": "custom_value"}
    token = create_access_token(data=payload_data)
    assert token is not None
    assert isinstance(token, str)
    decoded_payload = decode_token(token)
    assert decoded_payload is not None
    assert decoded_payload.get("sub") == payload_data["sub"]
    assert decoded_payload.get("custom_claim") == payload_data["custom_claim"]
    assert "exp" in decoded_payload
    short_expires_delta = timedelta(seconds=1)
    short_lived_token = create_access_token(data=payload_data, expires_delta=short_expires_delta)
    decoded_short_lived_payload = decode_token(short_lived_token)
    assert decoded_short_lived_payload is not None

def test_create_and_decode_refresh_token() -> None:
    """
    Testa a criação de um refresh token JWT e sua decodificação.
    Verifica se:
    - Um token é gerado (usando a lógica de refresh token).
    - O token pode ser decodificado com sucesso.
    - O payload decodificado contém o subject esperado e uma expiração.
    """
    payload_data: Dict[str, Any] = {"sub": "refresh_user@example.com"}
    token = create_refresh_token(data=payload_data)

    assert token is not None
    assert isinstance(token, str)

    decoded_payload = decode_token(token)
    assert decoded_payload is not None, "Refresh token should be decodable"
    assert decoded_payload.get("sub") == payload_data["sub"], "Subject in refresh token mismatch"
    assert "exp" in decoded_payload, "Expiration claim 'exp' should be in refresh token"

    short_expires_delta = timedelta(seconds=1)
    short_lived_token = create_refresh_token(data=payload_data, expires_delta=short_expires_delta)
    decoded_short_lived_payload = decode_token(short_lived_token)
    assert decoded_short_lived_payload is not None, "Short-lived refresh token should be decodable"

def test_decode_and_get_subject_invalid_cases() -> None:
    """
    Testa a decodificação de tokens JWT inválidos e a extração de subject.
    Verifica se:
    - Um token com formato incorreto retorna None para decode_token e get_subject_from_token.
    - Um token assinado com uma chave secreta errada retorna None para ambos.
    - Um token válido mas sem a claim 'sub' retorna None para get_subject_from_token.
    - Um token válido mas com 'sub' de tipo incorreto (ex: int) retorna None para get_subject_from_token.
    """
    # 1. Token com formato inválido
    invalid_format_token = "this.is.not.a.valid.jwt"
    assert decode_token(invalid_format_token) is None, "Token with invalid format should not be decodable"
    assert get_subject_from_token(invalid_format_token) is None, "Subject from invalid format token should be None"

    # 2. Token com assinatura errada
    exp_time_minutes = (settings.ACCESS_TOKEN_EXPIRE_MINUTES if settings.ACCESS_TOKEN_EXPIRE_MINUTES else 30)
    payload_data_ok: Dict[str, Any] = { 
        "sub": "testuser@example.com",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=exp_time_minutes)
    }
    wrong_secret_key = "not-" + settings.SECRET_KEY
    
    tampered_token = jwt.encode(payload_data_ok, wrong_secret_key, algorithm=settings.ALGORITHM)
    assert decode_token(tampered_token) is None, "Token with wrong signature should not be decodable"
    assert get_subject_from_token(tampered_token) is None, "Subject from tampered token should be None"

    # 3. Token válido, mas payload não contém 'sub'
    payload_no_sub: Dict[str, Any] = { 
        "another_claim": "value",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=exp_time_minutes)
    }
    token_no_sub = jwt.encode(payload_no_sub, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    decoded_no_sub = decode_token(token_no_sub)
    assert decoded_no_sub is not None
    assert decoded_no_sub.get("another_claim") == "value"
    assert get_subject_from_token(token_no_sub) is None, "Subject from token without 'sub' claim should be None"

    # 4. Token válido, 'sub' não é uma string
    payload_sub_not_string: Dict[str, Any] = { 
        "sub": 12345,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=exp_time_minutes)
    }
    token_sub_not_string = jwt.encode(payload_sub_not_string, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    decoded_sub_not_string = decode_token(token_sub_not_string)
    assert decoded_sub_not_string is None, "Token with non-string 'sub' should fail decoding (return None)"
    assert get_subject_from_token(token_sub_not_string) is None, "Subject from token with non-string 'sub' (which failed decoding) should be None"