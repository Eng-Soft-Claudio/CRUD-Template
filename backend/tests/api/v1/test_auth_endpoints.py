# tests/api/v1/test_auth_endpoints.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.orm import Session
from _pytest.capture import CaptureFixture

from app.core.config import settings
from app.schemas.user import UserCreate
from app.crud import user as crud_user
from app.core import security

# =======================================================================================================
# --- Testes para Endpoints de Autenticação ---                                                      #####
# =======================================================================================================

def test_read_root(client: TestClient) -> None:
    """Testa o endpoint raiz '/'."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert settings.PROJECT_NAME in response.json()["message"]


def test_health_check(client: TestClient) -> None:
    """Testa o endpoint de health check '/health'."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_new_user(client: TestClient, db_session: Session) -> None:
    """
    Testa o endpoint de registro de novo usuário (/api/v1/auth/register).
    Verifica:
    - Registro bem-sucedido com dados válidos.
    - Resposta correta (status 201, dados do usuário).
    - Usuário é realmente criado no banco de dados.
    - Tentativa de registro com e-mail duplicado resulta em erro 400.
    """
    # Cenário 1: Registro bem-sucedido
    user_data = {
        "email": "testregister@example.com",
        "password": "aSecurePassword123",
        "full_name": "Test Register User"
    }
    response = client.post(f"{settings.API_V1_STR}/auth/register", json=user_data)

    assert response.status_code == 201, f"Status code should be 201. Response: {response.text}"
    created_user_data = response.json()
    assert created_user_data["email"] == user_data["email"]
    assert created_user_data["full_name"] == user_data["full_name"]
    assert "id" in created_user_data
    assert "hashed_password" not in created_user_data 

    # Verifica no banco se o usuário foi realmente criado
    db_user = crud_user.get_user_by_email(db_session, email=user_data["email"])
    assert db_user is not None
    assert db_user.email == user_data["email"]
    assert db_user.full_name == user_data["full_name"]
    assert db_user.is_active is True 

    # Cenário 2: Tentativa de registro com e-mail duplicado
    response_duplicate = client.post(f"{settings.API_V1_STR}/auth/register", json=user_data)
    assert response_duplicate.status_code == 400, \
        f"Status code for duplicate email should be 400. Response: {response_duplicate.text}"
    error_data = response_duplicate.json()
    assert "detail" in error_data
    assert "already exists" in error_data["detail"].lower()


def test_login_for_access_token(client: TestClient, db_session: Session) -> None:
    """
    Testa o endpoint de login (/api/v1/auth/login).
    Verifica:
    - Login bem-sucedido com credenciais válidas.
    - Resposta contém access_token e token_type.
    - Falha no login com e-mail incorreto.
    - Falha no login com senha incorreta.
    - Falha no login para usuário inativo.
    """
    base_user_email = "testlogin@example.com"
    base_user_password = "loginPassword123"

    # Cria um usuário para testar o login
    user_in_db = UserCreate(email=base_user_email, password=base_user_password, full_name="Test Login User")
    crud_user.create_user(db=db_session, user=user_in_db)

    # Cenário 1: Login bem-sucedido
    login_data = {"username": base_user_email, "password": base_user_password} 
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data) 

    assert response.status_code == 200, f"Status code should be 200. Response: {response.text}"
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Cenário 2: E-mail incorreto
    login_data_wrong_email = {"username": "wrong@example.com", "password": base_user_password}
    response_wrong_email = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data_wrong_email)
    assert response_wrong_email.status_code == 401, \
        f"Status code for wrong email should be 401. Response: {response_wrong_email.text}"

    # Cenário 3: Senha incorreta
    login_data_wrong_password = {"username": base_user_email, "password": "wrongPassword"}
    response_wrong_password = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data_wrong_password)
    assert response_wrong_password.status_code == 401, \
        f"Status code for wrong password should be 401. Response: {response_wrong_password.text}"

    # Cenário 4: Usuário inativo
    user_from_db = crud_user.get_user_by_email(db=db_session, email=base_user_email)
    assert user_from_db is not None
    user_from_db.is_active = False
    db_session.add(user_from_db)
    db_session.commit()
    db_session.refresh(user_from_db)

    response_inactive = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response_inactive.status_code == 400, \
        f"Status code for inactive user login should be 400. Response: {response_inactive.text}"


def get_valid_token_headers(client: TestClient, db: Session, email: str, password: str) -> Dict[str, str]:
    """Gera e retorna cabeçalhos de autorização com um token válido."""
    login_data = {"username": email, "password": password}
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    response.raise_for_status()
    tokens = response.json()
    access_token = tokens["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def test_read_users_me(client: TestClient, db_session: Session) -> None:
    """
    Testa o endpoint /me para obter o usuário atual.
    Verifica:
    - Acesso bem-sucedido com token válido de usuário ativo.
    - Falha de acesso sem token (401).
    - Falha de acesso com token inválido (401).
    - Falha de acesso com token de usuário inativo (cobre get_current_active_user).
    """
    user_email = "testme@example.com"
    user_password = "mePassword123"
    user_full_name = "Test Me User"

    # Cria um usuário ativo
    user_in_create = UserCreate(email=user_email, password=user_password, full_name=user_full_name, is_active=True)
    created_user = crud_user.create_user(db=db_session, user=user_in_create)

    # Cenário 1: Acesso bem-sucedido com token válido
    headers = get_valid_token_headers(client, db_session, user_email, user_password)
    response = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert response.status_code == 200, f"Status code should be 200. Response: {response.text}"
    current_user_data = response.json()
    assert current_user_data["email"] == user_email
    assert current_user_data["full_name"] == user_full_name
    assert current_user_data["id"] == created_user.id

    # Cenário 2: Falha de acesso sem token
    response_no_token = client.get(f"{settings.API_V1_STR}/auth/me")
    assert response_no_token.status_code == 401, \
        f"Status code without token should be 401. Response: {response_no_token.text}"

    # Cenário 3: Falha de acesso com token inválido
    invalid_headers = {"Authorization": "Bearer aninvalidtoken"}
    response_invalid_token = client.get(f"{settings.API_V1_STR}/auth/me", headers=invalid_headers)
    assert response_invalid_token.status_code == 401, \
        f"Status code with invalid token should be 401. Response: {response_invalid_token.text}"

    # Cenário 4: Falha de acesso com token de usuário inativo
    created_user_model = crud_user.get_user_by_email(db_session, email=user_email)
    assert created_user_model is not None
    created_user_model.is_active = False
    db_session.add(created_user_model)
    db_session.commit()
    response_inactive_user = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert response_inactive_user.status_code == 400, \
        f"Status code with token of inactive user should be 400. Response: {response_inactive_user.text}"
    

def test_read_current_superuser_as_superuser(client: TestClient, db_session: Session) -> None:
    """
    Testa o acesso ao endpoint de superusuário por um superusuário ativo.
    """
    superuser_email = "superuser@example.com"
    superuser_password = "superPassword123"
    
    # Cria um superusuário ativo
    user_in_create = UserCreate(
        email=superuser_email,
        password=superuser_password,
        full_name="Super User Test",
        is_active=True,
        is_superuser=True
    )
    crud_user.create_user(db=db_session, user=user_in_create)

    headers = get_valid_token_headers(client, db_session, superuser_email, superuser_password)
    response = client.get(f"{settings.API_V1_STR}/auth/me/superuser", headers=headers)
    
    assert response.status_code == 200, \
        f"Superuser should access superuser endpoint. Response: {response.text}"
    returned_user = response.json()
    assert returned_user["email"] == superuser_email
    assert returned_user["is_superuser"] is True


def test_read_current_superuser_as_normal_user(client: TestClient, db_session: Session) -> None:
    """
    Testa a falha de acesso ao endpoint de superusuário por um usuário normal ativo.
    """
    normal_user_email = "normaluser_for_superuser_test@example.com"
    normal_user_password = "normalPassword123"

    # Cria um usuário normal ativo
    user_in_create = UserCreate(
        email=normal_user_email,
        password=normal_user_password,
        full_name="Normal User Test",
        is_active=True,
        is_superuser=False
    )
    crud_user.create_user(db=db_session, user=user_in_create)

    headers = get_valid_token_headers(client, db_session, normal_user_email, normal_user_password)
    response = client.get(f"{settings.API_V1_STR}/auth/me/superuser", headers=headers)
    
    assert response.status_code == 403, \
        f"Normal user should get 403 on superuser endpoint. Response: {response.text}"
    error_data = response.json()
    assert "detail" in error_data
    assert "doesn't have enough privileges" in error_data["detail"]


def test_read_current_superuser_as_inactive_superuser(client: TestClient, db_session: Session) -> None:
    """
    Testa a falha de acesso ao endpoint de superusuário por um superusuário inativo.
    A dependência get_current_active_user (que get_current_active_superuser usa)
    deve barrar o acesso antes mesmo da verificação de superusuário.
    """
    inactive_superuser_email = "inactivesuper@example.com"
    inactive_superuser_password = "inactiveSuperPass"

    user_in_create = UserCreate(
        email=inactive_superuser_email,
        password=inactive_superuser_password,
        full_name="Inactive Super User",
        is_active=False,
        is_superuser=True
    )
    crud_user.create_user(db=db_session, user=user_in_create)
    
    temp_active_email = "temp_active_for_inactive_test@example.com"
    crud_user.create_user(db=db_session, user=UserCreate(email=temp_active_email, password=inactive_superuser_password, is_active=True, is_superuser=True))
    
    user_to_make_inactive = crud_user.get_user_by_email(db_session, temp_active_email)
    assert user_to_make_inactive is not None
    
    headers = get_valid_token_headers(client, db_session, temp_active_email, inactive_superuser_password) # Obtém token enquanto ativo

    user_to_make_inactive.is_active = False 
    db_session.add(user_to_make_inactive)
    db_session.commit()

    response = client.get(f"{settings.API_V1_STR}/auth/me/superuser", headers=headers)
    
    assert response.status_code == 400, \
        f"Inactive superuser should get 400. Response: {response.text}"
    error_data = response.json()
    assert "detail" in error_data
    assert "Inactive user" in error_data["detail"]


def test_token_data_validation_error_in_get_current_user(client: TestClient):
    """
    Força um ValidationError ao criar TokenData dentro de get_current_user.
    O 'sub' do token é uma string, mas não é um email válido para Pydantic EmailStr.
    """
    payload_invalid_email_format: Dict[str, Any] = {
        "sub": "plainstringnotaschemaemail",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload_invalid_email_format, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_get_current_user_with_invalid_sub_format(client: TestClient, db_session: Session) -> None:
    """Testa get_current_user com um 'sub' no token que não é um e-mail válido."""
    invalid_sub_payload: Dict[str, Any] = {
        "sub": "not-an-email",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    invalid_sub_token = jwt.encode(invalid_sub_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    headers = {"Authorization": f"Bearer {invalid_sub_token}"}

    response = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert response.status_code == 401


def test_get_current_user_with_token_missing_sub_claim(client: TestClient) -> None:
    """
    Testa get_current_user com um token JWT que é válido mas não contém a claim 'sub'.
    Isso deve acionar a credentials_exception quando token_email_from_payload é None.
    """
    exp_time_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    payload_missing_sub: Dict[str, Any] = {
        "user_id": 123, # Alguma outra claim
        "exp": datetime.now(timezone.utc) + timedelta(minutes=exp_time_minutes)
    }
    token_missing_sub = jwt.encode(payload_missing_sub, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    headers = {"Authorization": f"Bearer {token_missing_sub}"}

    response = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_get_current_user_with_valid_token_for_nonexistent_user(client: TestClient, db_session: Session) -> None:
    """
    Testa get_current_user com um token JWT válido, mas para um email
    que não existe mais no banco de dados.
    Isso deve cobrir o 'if user is None: raise credentials_exception'.
    """
    non_existent_email = "iamnotinthedb@example.com"
    exp_time_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    payload: Dict[str, Any] = {
        "sub": non_existent_email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=exp_time_minutes)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    
    assert response.status_code == 401 
    assert "Could not validate credentials" in response.json()["detail"]

def test_update_user_me_full_name(client: TestClient, db_session: Session) -> None:
    """Testa a atualização do full_name do usuário autenticado."""
    user_email = "updateprofile@example.com"
    user_password = "profilePassword123"
    user_full_name_initial = "Initial Profile Name"
    crud_user.create_user(db_session, UserCreate(email=user_email, password=user_password, full_name=user_full_name_initial))
    
    headers = get_valid_token_headers(client, db_session, user_email, user_password)
    
    new_full_name = "Updated Profile Name"
    update_payload = {"full_name": new_full_name}
    
    response = client.patch(f"{settings.API_V1_STR}/auth/me", headers=headers, json=update_payload)
    
    assert response.status_code == 200, response.text
    updated_user_data = response.json()
    assert updated_user_data["email"] == user_email 
    assert updated_user_data["full_name"] == new_full_name
    assert updated_user_data["is_active"] is True 


def test_update_user_me_email(client: TestClient, db_session: Session) -> None:
    """Testa a atualização do email do usuário autenticado."""
    user_email_initial = "updateemail_initial@example.com"
    user_password = "emailPassword123"
    crud_user.create_user(db_session, UserCreate(email=user_email_initial, password=user_password, full_name="Email User"))
    
    headers = get_valid_token_headers(client, db_session, user_email_initial, user_password)
    
    user_email_new = "updateemail_new@example.com"
    update_payload = {"email": user_email_new}
    
    response = client.patch(f"{settings.API_V1_STR}/auth/me", headers=headers, json=update_payload)
    
    assert response.status_code == 200, response.text
    updated_user_data = response.json()
    assert updated_user_data["email"] == user_email_new
    
    new_login_headers = get_valid_token_headers(client, db_session, user_email_new, user_password)
    response_me_new_email = client.get(f"{settings.API_V1_STR}/auth/me", headers=new_login_headers)
    assert response_me_new_email.status_code == 200


def test_update_user_me_email_conflict(client: TestClient, db_session: Session) -> None:
    """Testa a tentativa de atualizar o email para um já existente por outro usuário."""
    user1_email = "user1_conflict@example.com"
    user1_password = "password1"
    crud_user.create_user(db_session, UserCreate(email=user1_email, password=user1_password, full_name="User One"))

    user2_email = "user2_tryingtoconflict@example.com"
    user2_password = "password2"
    crud_user.create_user(db_session, UserCreate(email=user2_email, password=user2_password, full_name="User Two"))

    headers_user2 = get_valid_token_headers(client, db_session, user2_email, user2_password)
    
    update_payload = {"email": user1_email}
    response = client.patch(f"{settings.API_V1_STR}/auth/me", headers=headers_user2, json=update_payload)
    
    assert response.status_code == 400, response.text
    assert "Email already registered" in response.json()["detail"]


def test_update_user_me_cannot_change_status(client: TestClient, db_session: Session) -> None:
    """Testa que o usuário não pode mudar is_active ou is_superuser via PATCH /me."""
    user_email = "statuschange@example.com"
    user_password = "statusPassword123"
    crud_user.create_user(db_session, UserCreate(email=user_email, password=user_password, is_active=True, is_superuser=False))
    
    headers = get_valid_token_headers(client, db_session, user_email, user_password)
    
    update_payload: Dict[str, Any] = { 
        "is_active": False,         
        "is_superuser": True,       
        "full_name": "New Name"     
    }
    response = client.patch(f"{settings.API_V1_STR}/auth/me", headers=headers, json=update_payload)
    
    assert response.status_code == 200, response.text
    updated_data = response.json()
    assert updated_data["full_name"] == "New Name"
    assert updated_data["is_active"] is True    
    assert updated_data["is_superuser"] is False


def test_update_current_user_password_success(client: TestClient, db_session: Session) -> None:
    """Testa a mudança de senha bem-sucedida do usuário autenticado."""
    user_email = "changepass@example.com"
    old_password = "oldPassword123"
    new_password = "newSecurePassword456"

    crud_user.create_user(db_session, UserCreate(email=user_email, password=old_password))
    headers = get_valid_token_headers(client, db_session, user_email, old_password)

    password_change_data = {
        "current_password": old_password,
        "new_password": new_password,
        "new_password_confirm": new_password
    }
    response = client.put(
        f"{settings.API_V1_STR}/auth/me/password", headers=headers, json=password_change_data
    )
    assert response.status_code == 204, response.text

    login_with_new_pass_data = {"username": user_email, "password": new_password}
    response_login_new = client.post(
        f"{settings.API_V1_STR}/auth/login", data=login_with_new_pass_data
    )
    assert response_login_new.status_code == 200, response_login_new.text

    login_with_old_pass_data = {"username": user_email, "password": old_password}
    response_login_old = client.post(
        f"{settings.API_V1_STR}/auth/login", data=login_with_old_pass_data
    )
    assert response_login_old.status_code == 401, response_login_old.text


def test_update_current_user_password_wrong_current_password(client: TestClient, db_session: Session) -> None:
    """Testa a falha na mudança de senha quando a senha atual fornecida está incorreta."""
    user_email = "wrongcurrpass@example.com"
    correct_current_password = "correctPassword"
    new_password = "newPassword"
    crud_user.create_user(db_session, UserCreate(email=user_email, password=correct_current_password))
    headers = get_valid_token_headers(client, db_session, user_email, correct_current_password)

    password_change_data = {
        "current_password": "thisIsTheWrongCurrentPassword",
        "new_password": new_password,
        "new_password_confirm": new_password
    }
    response = client.put(
        f"{settings.API_V1_STR}/auth/me/password", headers=headers, json=password_change_data
    )
    assert response.status_code == 400, response.text
    assert "Incorrect current password" in response.json()["detail"]


def test_update_current_user_password_new_passwords_mismatch(client: TestClient, db_session: Session) -> None:
    """Testa a falha na mudança de senha quando a nova senha e a confirmação não correspondem."""
    user_email = "passmismatch@example.com"
    current_password = "currentPassword"
    crud_user.create_user(db_session, UserCreate(email=user_email, password=current_password))
    headers = get_valid_token_headers(client, db_session, user_email, current_password)

    password_change_data = {
        "current_password": current_password,
        "new_password": "newPassword1",
        "new_password_confirm": "newPassword2" 
    }
    response = client.put(
        f"{settings.API_V1_STR}/auth/me/password", headers=headers, json=password_change_data
    )
    assert response.status_code == 422, response.text 
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "value_error"
    assert "As senhas não correspondem" in error_detail["msg"]


def test_update_current_user_password_new_same_as_old(client: TestClient, db_session: Session) -> None:
    """Testa a falha na mudança de senha quando a nova senha é igual à senha antiga."""
    user_email = "pass_same_as_old@example.com"
    current_password = "samePassword123"
    crud_user.create_user(db_session, UserCreate(email=user_email, password=current_password))
    headers = get_valid_token_headers(client, db_session, user_email, current_password)

    password_change_data = {
        "current_password": current_password,
        "new_password": current_password, 
        "new_password_confirm": current_password
    }
    response = client.put(
        f"{settings.API_V1_STR}/auth/me/password", headers=headers, json=password_change_data
    )
    assert response.status_code == 400, response.text
    assert "New password cannot be the same" in response.json()["detail"]


def test_delete_user_me_success(client: TestClient, db_session: Session) -> None:
    """Testa a deleção bem-sucedida da conta do usuário autenticado."""
    user_email = "delete_my_account@example.com"
    user_password = "deleteMePassword123"

    user_to_delete = crud_user.create_user(
        db_session, UserCreate(email=user_email, password=user_password)
    )
    user_id_before_delete = user_to_delete.id

    headers = get_valid_token_headers(client, db_session, user_email, user_password)

    response_delete = client.delete(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert response_delete.status_code == 204, \
        f"Status code should be 204 No Content. Response: {response_delete.content}" 

    user_in_db_after_delete = crud_user.get_user(db_session, user_id=user_id_before_delete)
    assert user_in_db_after_delete is None, "User should no longer exist in DB after deletion."

    response_me_after_delete = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert response_me_after_delete.status_code == 401, \
        "Accessing /me with token of deleted user should result in 401 (user not found)."
    
    login_data_deleted_user = {"username": user_email, "password": user_password}
    response_login_deleted = client.post(
        f"{settings.API_V1_STR}/auth/login", data=login_data_deleted_user
    )
    assert response_login_deleted.status_code == 401, \
        "Login attempt for a deleted user should result in 401."


def test_delete_user_me_no_token(client: TestClient) -> None:
    """Testa a falha ao tentar deletar sem um token de autenticação."""
    response = client.delete(f"{settings.API_V1_STR}/auth/me")
    assert response.status_code == 401, \
        "Attempting to delete /me without a token should result in 401."


def test_delete_user_me_invalid_token(client: TestClient) -> None:
    """Testa a falha ao tentar deletar com um token inválido."""
    headers = {"Authorization": "Bearer aninvalidtoken"}
    response = client.delete(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert response.status_code == 401, \
        "Attempting to delete /me with an invalid token should result in 401."
    

def test_request_password_recovery_user_exists(
    client: TestClient,
    db_session: Session,
    capsys: CaptureFixture[str] 
) -> None:
    """Testa a solicitação de recuperação de senha para um usuário existente."""
    user_email = "recovermyP4ssw0rd@example.com"
    user_password = "oldPassword123"
    crud_user.create_user(db_session, UserCreate(email=user_email, password=user_password))

    recovery_payload = {"email": user_email}
    response = client.post(f"{settings.API_V1_STR}/auth/password-recovery", json=recovery_payload)

    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Se um usuário com este email existir, um link de recuperação foi enviado."}
    
    captured = capsys.readouterr()
    assert "SIMULAÇÃO DE ENVIO DE E-MAIL" in captured.out
    assert f"Para: {user_email}" in captured.out
    assert "Use o seguinte token para resetar sua senha" in captured.out


def test_request_password_recovery_user_does_not_exist(
    client: TestClient,
    db_session: Session,
    capsys: CaptureFixture[str] 
) -> None:
    """
    Testa a solicitação de recuperação de senha para um e-mail não existente.
    Deve retornar a mesma mensagem genérica para não revelar a existência do usuário.
    """
    non_existent_email = "idonotexist@example.com"
    recovery_payload = {"email": non_existent_email}
    response = client.post(f"{settings.API_V1_STR}/auth/password-recovery", json=recovery_payload)

    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Se um usuário com este email existir, um link de recuperação foi enviado."}
    
    captured = capsys.readouterr()
    assert "SIMULAÇÃO DE ENVIO DE E-MAIL" not in captured.out 


def test_reset_user_password_success(
    client: TestClient,
    db_session: Session,
    capsys: CaptureFixture[str] 
) -> None:
    """Testa o reset de senha bem-sucedido com um token válido."""
    user_email = "resetthispassword@example.com"
    old_password = "oldPassword"
    new_password = "aBrandNewPassword123"

    _ = crud_user.create_user(db_session, UserCreate(email=user_email, password=old_password))
    
    reset_token = security.create_password_reset_token(email=user_email)

    reset_form_data = {
        "token": reset_token,
        "new_password": new_password,
        "new_password_confirm": new_password
    }
    response = client.post(f"{settings.API_V1_STR}/auth/reset-password/", json=reset_form_data)
    assert response.status_code == 204, response.content 

    login_data = {"username": user_email, "password": new_password}
    response_login = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response_login.status_code == 200, response_login.text
    assert "access_token" in response_login.json()

    login_data_old_pass = {"username": user_email, "password": old_password}
    response_login_old = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data_old_pass)
    assert response_login_old.status_code == 401, response_login_old.text

    captured = capsys.readouterr()
    assert "Sua senha foi alterada com sucesso." in captured.out
    assert f"Para: {user_email}" in captured.out


def test_reset_user_password_invalid_token(client: TestClient, db_session: Session) -> None:
    """Testa a falha no reset de senha com um token inválido ou expirado."""
    new_password = "newPasswordAttempt"
    reset_form_data_invalid_token = {
        "token": "this.is.an.invalid.token",
        "new_password": new_password,
        "new_password_confirm": new_password
    }
    response = client.post(f"{settings.API_V1_STR}/auth/reset-password/", json=reset_form_data_invalid_token)
    assert response.status_code == 400, response.text
    assert "Token de recuperação de senha inválido ou expirado" in response.json()["detail"]

    user_email_for_expired_token = "expiredtokenuser@example.com"
    _ = crud_user.create_user(db_session, UserCreate(email=user_email_for_expired_token, password="password"))
    
    expired_like_token_payload: Dict[str, Any] = {
        "sub": user_email_for_expired_token,
        "type": "not_password_reset",
        "exp": datetime.now(timezone.utc) - timedelta(hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS + 1)
    }
    expired_token = jwt.encode(expired_like_token_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    reset_form_data_expired_token = {
        "token": expired_token,
        "new_password": new_password,
        "new_password_confirm": new_password
    }
    response_expired = client.post(f"{settings.API_V1_STR}/auth/reset-password/", json=reset_form_data_expired_token)
    assert response_expired.status_code == 400, response_expired.text
    assert "Token de recuperação de senha inválido ou expirado" in response_expired.json()["detail"]


def test_reset_user_password_user_not_found_with_valid_token_logic(client: TestClient, db_session: Session) -> None:
    """
    Testa o cenário onde um token de reset é válido, mas o usuário
    (identificado pelo email no token) não existe mais no banco.
    Isso é um caso de borda, pois o token só deveria ser gerado para usuários existentes.
    """
    email_in_valid_token = "user_that_will_be_deleted@example.com"
    new_password = "newPasswordIfUserExisted"

    reset_token = security.create_password_reset_token(email=email_in_valid_token)

    reset_form_data = {
        "token": reset_token,
        "new_password": new_password,
        "new_password_confirm": new_password
    }
    response = client.post(f"{settings.API_V1_STR}/auth/reset-password/", json=reset_form_data)
    assert response.status_code == 404, response.text 
    assert "Usuário não encontrado" in response.json()["detail"]


def test_reset_user_password_inactive_user(client: TestClient, db_session: Session) -> None:
    """Testa o reset de senha para um usuário que está inativo."""
    user_email = "inactive_reset@example.com"
    old_password = "oldPassword"
    new_password = "newPasswordForInactive"

    user_db = crud_user.create_user(db_session, UserCreate(email=user_email, password=old_password))
    user_db.is_active = False
    db_session.add(user_db)
    db_session.commit()
    db_session.refresh(user_db)
    
    reset_token = security.create_password_reset_token(email=user_email)
    reset_form_data = {
        "token": reset_token,
        "new_password": new_password,
        "new_password_confirm": new_password
    }
    response = client.post(f"{settings.API_V1_STR}/auth/reset-password/", json=reset_form_data)
    assert response.status_code == 400, response.text
    assert "Usuário inativo" in response.json()["detail"]


def test_reset_user_password_passwords_mismatch(client: TestClient, db_session: Session) -> None:
    """Testa a falha no reset de senha quando a nova senha e a confirmação não correspondem."""
    user_email = "reset_mismatch@example.com"
    crud_user.create_user(db_session, UserCreate(email=user_email, password="password"))
    reset_token = security.create_password_reset_token(email=user_email)

    reset_form_data = {
        "token": reset_token,
        "new_password": "newPassword1",
        "new_password_confirm": "newPassword2Different" 
    }
    response = client.post(f"{settings.API_V1_STR}/auth/reset-password/", json=reset_form_data)
    assert response.status_code == 422, response.text 
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "value_error"
    assert "As senhas não correspondem" in error_detail["msg"]