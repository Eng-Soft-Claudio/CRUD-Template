# backend/tests/api/v1/test_users_admin_endpoints.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from typing import Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.user import UserCreate, UserUpdate
from app.crud import user as crud_user
from tests.utils.user import create_random_user, random_email, random_lower_string
from app.db.models.user import User as UserModel
from app.core import security 


# =======================================================================================================
# --- Testes para Endpoints de Administração de Usuários ---                                        #####
# =======================================================================================================

# =======================================================================================================
# --- Testes para GET /api/v1/users/ ---                                                            #####
# =======================================================================================================

def test_read_users_as_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa a leitura de múltiplos usuários por um superusuário.
    Cria alguns usuários para garantir que há dados a serem retornados.
    """
    create_random_user(db_session)
    create_random_user(db_session)
    create_random_user(db_session)

    response = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    assert response.status_code == 200
    all_users = response.json()
    assert len(all_users) >= 3
    for user_data in all_users:
        assert "email" in user_data
        assert "id" in user_data
        assert "hashed_password" not in user_data


def test_read_users_pagination_as_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa a paginação na leitura de usuários por um superusuário.
    """
    for _ in range(15):
        create_random_user(db_session)

    response_limit = client.get(f"{settings.API_V1_STR}/users/?limit=5", headers=superuser_token_headers)
    assert response_limit.status_code == 200
    limited_users = response_limit.json()
    assert len(limited_users) == 5

    response_skip_limit = client.get(f"{settings.API_V1_STR}/users/?skip=5&limit=5", headers=superuser_token_headers)
    assert response_skip_limit.status_code == 200
    skipped_users = response_skip_limit.json()
    assert len(skipped_users) == 5
    if limited_users and skipped_users:
        assert limited_users[0]["id"] != skipped_users[0]["id"]

    response_skip_too_much = client.get(f"{settings.API_V1_STR}/users/?skip=100", headers=superuser_token_headers)
    assert response_skip_too_much.status_code == 200
    assert len(response_skip_too_much.json()) == 0


def test_read_users_as_normal_user_forbidden(
    client: TestClient, normal_user_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa que um usuário normal não pode listar todos os usuários.
    """
    response = client.get(f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers)
    assert response.status_code == 403
    assert "doesn't have enough privileges" in response.json()["detail"].lower()


def test_read_users_unauthenticated(client: TestClient, db_session: Session) -> None:
    """
    Testa que um usuário não autenticado não pode listar todos os usuários.
    """
    response = client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == 401

# =======================================================================================================
# --- Testes para GET /api/v1/users/{user_id} ---                                                   #####
# =======================================================================================================

def test_read_user_by_id_as_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa a leitura de um usuário específico por ID por um superusuário.
    """
    user_to_find: UserModel = create_random_user(db_session)
    assert user_to_find.id is not None
    response = client.get(f"{settings.API_V1_STR}/users/{user_to_find.id}", headers=superuser_token_headers)
    assert response.status_code == 200
    found_user_data = response.json()
    assert found_user_data["email"] == user_to_find.email
    assert found_user_data["id"] == user_to_find.id
    assert found_user_data["full_name"] == user_to_find.full_name
    assert "hashed_password" not in found_user_data


def test_read_user_by_id_not_found_as_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa a leitura de um ID de usuário não existente por um superusuário.
    """
    non_existent_id = 99999
    response = client.get(f"{settings.API_V1_STR}/users/{non_existent_id}", headers=superuser_token_headers)
    assert response.status_code == 404
    assert "não foi encontrado" in response.json()["detail"]


def test_read_user_by_id_as_normal_user_forbidden(
    client: TestClient, normal_user_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa que um usuário normal não pode obter outro usuário por ID.
    """
    another_user: UserModel = create_random_user(db_session)
    assert another_user.id is not None
    response = client.get(f"{settings.API_V1_STR}/users/{another_user.id}", headers=normal_user_token_headers)
    assert response.status_code == 403
    assert "doesn't have enough privileges" in response.json()["detail"].lower()


def test_read_user_by_id_unauthenticated(client: TestClient, db_session: Session) -> None:
    """
    Testa que um usuário não autenticado não pode obter usuário por ID.
    """
    user_to_find: UserModel = create_random_user(db_session)
    assert user_to_find.id is not None
    response = client.get(f"{settings.API_V1_STR}/users/{user_to_find.id}")
    assert response.status_code == 401


# =======================================================================================================
# --- Testes para POST /api/v1/users/ ---                                                           #####
# =======================================================================================================

def test_create_user_by_admin_as_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa a criação de um novo usuário por um superusuário, definindo is_superuser.
    """
    email = random_email()
    password = random_lower_string(10)
    full_name = "AdminCreated Superuser"
    user_data_in = UserCreate(
        email=email,
        password=password,
        full_name=full_name,
        is_active=True,
        is_superuser=True, # Testando a criação de outro superuser
    )
    response = client.post(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=user_data_in.model_dump())
    assert response.status_code == 201
    created_user_data = response.json()
    assert created_user_data["email"] == email
    assert created_user_data["full_name"] == full_name
    assert created_user_data["is_active"] is True
    assert created_user_data["is_superuser"] is True # Verifica se o flag foi setado

    db_user: UserModel | None = crud_user.get_user_by_email(db_session, email=email)
    assert db_user is not None
    assert db_user.is_superuser is True


def test_create_user_by_admin_existing_email_as_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa a tentativa de criar um usuário com email já existente por um superusuário.
    """
    existing_user: UserModel = create_random_user(db_session)
    password = random_lower_string(10)
    user_data_in = UserCreate(
        email=existing_user.email,
        password=password,
        full_name="Duplicate Email User",
    )
    response = client.post(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=user_data_in.model_dump())
    assert response.status_code == 400
    assert "já existe" in response.json()["detail"]


def test_create_user_by_admin_as_normal_user_forbidden(
    client: TestClient, normal_user_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa que um usuário normal não pode criar usuários via endpoint de admin.
    """
    email = random_email()
    password = random_lower_string(10)
    user_data_in = UserCreate(email=email, password=password)
    response = client.post(f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers, json=user_data_in.model_dump())
    assert response.status_code == 403


# =======================================================================================================
# --- Testes para PUT /api/v1/users/{user_id} ---                                                   #####
# =======================================================================================================

def test_update_user_by_admin_as_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa a atualização de um usuário por um superusuário, incluindo status e senha.
    """
    user_to_update: UserModel = create_random_user(db_session, is_active=True, is_superuser=False)
    assert user_to_update.id is not None

    new_full_name = "Updated Name by Admin"
    new_email = random_email()
    update_payload_schema = UserUpdate(
        full_name=new_full_name,
        email=new_email,
        is_active=False,
        is_superuser=True,
    )
    response_no_pass = client.put(
        f"{settings.API_V1_STR}/users/{user_to_update.id}", headers=superuser_token_headers, json=update_payload_schema.model_dump(exclude_unset=True)
    )
    assert response_no_pass.status_code == 200
    updated_user_data = response_no_pass.json()
    assert updated_user_data["email"] == new_email
    assert updated_user_data["full_name"] == new_full_name
    assert updated_user_data["is_active"] is False
    assert updated_user_data["is_superuser"] is True

    new_password = random_lower_string(12)
    update_payload_with_pass_schema = UserUpdate(
        password=new_password
    )
    response_with_pass = client.put(
        f"{settings.API_V1_STR}/users/{user_to_update.id}", headers=superuser_token_headers, json=update_payload_with_pass_schema.model_dump(exclude_unset=True)
    )
    assert response_with_pass.status_code == 200
    db_user_pass_updated: UserModel | None = crud_user.get_user(db_session, user_id=user_to_update.id)
    assert db_user_pass_updated is not None
    assert security.verify_password(new_password, db_user_pass_updated.hashed_password)
    assert db_user_pass_updated.email == new_email # Verifica se o email não foi revertido


def test_update_user_by_admin_email_conflict_as_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa a falha ao atualizar email de um usuário para um email que já existe por outro usuário.
    """
    user1: UserModel = create_random_user(db_session)
    user2: UserModel = create_random_user(db_session)
    assert user1.id is not None and user2.id is not None
    update_data = UserUpdate(email=user1.email)

    response = client.put(
        f"{settings.API_V1_STR}/users/{user2.id}", headers=superuser_token_headers, json=update_data.model_dump(exclude_unset=True)
    )
    assert response.status_code == 400
    assert "novo email fornecido já está registrado" in response.json()["detail"]


def test_update_user_by_admin_not_found_as_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa a atualização de um ID de usuário não existente por um superusuário.
    """
    non_existent_id = 999999
    update_data = UserUpdate(full_name="Any Name")
    response = client.put(
        f"{settings.API_V1_STR}/users/{non_existent_id}", headers=superuser_token_headers, json=update_data.model_dump(exclude_unset=True)
    )
    assert response.status_code == 404


def test_update_user_by_admin_as_normal_user_forbidden(
    client: TestClient, normal_user_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa que um usuário normal não pode atualizar outros usuários.
    """
    user_to_update: UserModel = create_random_user(db_session)
    assert user_to_update.id is not None
    update_data = UserUpdate(full_name="New Name by Normal User")
    response = client.put(
        f"{settings.API_V1_STR}/users/{user_to_update.id}", headers=normal_user_token_headers, json=update_data.model_dump(exclude_unset=True)
    )
    assert response.status_code == 403


# =======================================================================================================
# --- Testes para DELETE /api/v1/users/{user_id} ---                                                #####
# =======================================================================================================

def test_delete_user_by_admin_as_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa a deleção de um usuário por um superusuário.
    """
    user_to_delete: UserModel = create_random_user(db_session)
    user_id_to_delete = user_to_delete.id
    assert user_id_to_delete is not None

    response = client.delete(
        f"{settings.API_V1_STR}/users/{user_id_to_delete}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    deleted_user_data = response.json()
    assert deleted_user_data["id"] == user_id_to_delete
    assert deleted_user_data["email"] == user_to_delete.email

    user_in_db: UserModel | None = crud_user.get_user(db_session, user_id=user_id_to_delete)
    assert user_in_db is None


def test_delete_own_superuser_account_by_admin_endpoint_forbidden(
    client: TestClient, db_session: Session, superuser_token_headers: Dict[str, str] # Usa a fixture global
) -> None:
    """
    Testa que um superusuário não pode deletar a si mesmo via /users/{id} usando seu próprio token.
    """
    # Obtém o ID do superusuário da fixture (o usuário logado com superuser_token_headers)
    response_me = client.get(f"{settings.API_V1_STR}/auth/me", headers=superuser_token_headers)
    current_superuser_id = response_me.json()["id"]

    response = client.delete(
        f"{settings.API_V1_STR}/users/{current_superuser_id}", headers=superuser_token_headers
    )
    assert response.status_code == 403
    assert "não podem deletar a si mesmos" in response.json()["detail"]


def test_delete_user_by_admin_not_found_as_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa a deleção de um ID de usuário não existente por um superusuário.
    """
    non_existent_id = 998877
    response = client.delete(
        f"{settings.API_V1_STR}/users/{non_existent_id}", headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_delete_user_by_admin_as_normal_user_forbidden(
    client: TestClient, normal_user_token_headers: Dict[str, str], db_session: Session
) -> None:
    """
    Testa que um usuário normal não pode deletar outros usuários.
    """
    user_to_delete: UserModel = create_random_user(db_session)
    assert user_to_delete.id is not None
    response = client.delete(
        f"{settings.API_V1_STR}/users/{user_to_delete.id}", headers=normal_user_token_headers
    )
    assert response.status_code == 403