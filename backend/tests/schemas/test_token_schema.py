# tests/schemas/test_token_schema.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from pydantic import ValidationError
import pytest

from app.schemas.token import TokenData # Ou de onde você importa TokenData nos seus testes

# =======================================================================================================
# --- Teste ---                                                                                     #####
# =======================================================================================================

def test_tokendata_email_validation():
    """Testa se TokenData levanta ValidationError para um email inválido."""
    with pytest.raises(ValidationError):
        TokenData(email="not-an-email") # Deve levantar ValidationError

    # Teste com um email válido para garantir que funciona
    try:
        valid_td = TokenData(email="valid@example.com")
        assert valid_td.email == "valid@example.com"
    except ValidationError:
        pytest.fail("TokenData não deveria levantar ValidationError para um email válido.")

    # Teste com None (que é permitido pelo schema Optional[str])
    try:
        none_td = TokenData(email=None)
        assert none_td.email is None
    except ValidationError:
        pytest.fail("TokenData não deveria levantar ValidationError para email=None.")