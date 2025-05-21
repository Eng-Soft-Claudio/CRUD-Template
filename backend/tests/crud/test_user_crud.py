# tests/crud/test_user_crud.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from sqlalchemy.orm import Session
from typing import Dict, Any

from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import verify_password

# =======================================================================================================
# --- Testes para CRUD de Usuário ---                                                               #####
# =======================================================================================================

def test_create_user(db_session: Session) -> None:
    """
    Testa a criação de um novo usuário no banco de dados.
    Verifica se:
    - O usuário é criado com os dados corretos.
    - A senha é armazenada com hash.
    - Os valores padrão para 'is_active' e 'is_superuser' são aplicados.
    """
    user_email = "test_create@example.com"
    user_password = "testpassword123"
    user_full_name = "Test Create User"

    user_in = UserCreate(
        email=user_email,
        password=user_password,
        full_name=user_full_name
    )

    db_user = crud_user.create_user(db=db_session, user=user_in)

    assert db_user is not None, "A criação do usuário deve retornar um objeto usuário."
    assert db_user.email == user_email, "O email do usuário criado não corresponde."
    assert db_user.full_name == user_full_name, "O nome completo do usuário criado não corresponde."
    assert hasattr(db_user, "hashed_password"), "O usuário criado deve ter uma senha com hash."
    assert db_user.hashed_password != user_password, "A senha com hash não deve ser igual à senha plana."
    assert verify_password(user_password, db_user.hashed_password), "A senha plana deve ser verificável contra o hash."
    assert db_user.is_active is True, "O usuário deve ser ativo por padrão."
    assert db_user.is_superuser is False, "O usuário não deve ser superusuário por padrão."
    assert db_user.id is not None, "O usuário criado deve ter um ID atribuído pelo banco."


def test_get_user_by_email(db_session: Session) -> None:
    """
    Testa a recuperação de um usuário pelo seu endereço de e-mail.
    Verifica se:
    - Um usuário existente é retornado corretamente.
    - None é retornado para um e-mail não existente.
    """
    user_email = "get_by_email@example.com"
    user_password = "testpassword123"
    user_in_create = UserCreate(email=user_email, password=user_password)
    created_user = crud_user.create_user(db=db_session, user=user_in_create)

    retrieved_user = crud_user.get_user_by_email(db=db_session, email=user_email)
    assert retrieved_user is not None, "Deve encontrar o usuário pelo e-mail."
    assert retrieved_user.id == created_user.id, "O ID do usuário recuperado não corresponde."
    assert retrieved_user.email == user_email, "O email do usuário recuperado não corresponde."

    non_existent_user = crud_user.get_user_by_email(db=db_session, email="nonexistent@example.com")
    assert non_existent_user is None, "Não deve encontrar um usuário com e-mail não existente."


def test_get_user_by_id(db_session: Session) -> None:
    """
    Testa a recuperação de um usuário pelo seu ID.
    Verifica se:
    - Um usuário existente é retornado corretamente pelo ID.
    - None é retornado para um ID não existente.
    """
    user_email = "get_by_id@example.com"
    user_password = "testpassword123"
    user_in_create = UserCreate(email=user_email, password=user_password)
    created_user = crud_user.create_user(db=db_session, user=user_in_create)

    assert created_user.id is not None, "Usuário criado deve ter um ID."

    retrieved_user = crud_user.get_user(db=db_session, user_id=created_user.id)
    assert retrieved_user is not None, "Deve encontrar o usuário pelo ID."
    assert retrieved_user.id == created_user.id, "O ID do usuário recuperado não corresponde."
    assert retrieved_user.email == user_email, "O email do usuário recuperado não corresponde."

    non_existent_user = crud_user.get_user(db=db_session, user_id=999999)
    assert non_existent_user is None, "Não deve encontrar um usuário com ID não existente."

def test_update_user_all_fields(db_session: Session) -> None:
    """
    Testa a atualização de todos os campos permitidos de um usuário, incluindo a senha.
    """
    original_email = "update_me@example.com"
    original_password = "oldPassword123"
    original_full_name = "Original Name"
    user_to_update = crud_user.create_user(db_session, UserCreate(
        email=original_email, password=original_password, full_name=original_full_name,
        is_active=True, is_superuser=False
    ))

    new_email = "updated_email@example.com"
    new_password = "newStrongPassword456"
    new_full_name = "Updated Full Name"
    update_data = UserUpdate(
        email=new_email,
        password=new_password,
        full_name=new_full_name,
        is_active=False,
        is_superuser=True
    )

    updated_user = crud_user.update_user(db=db_session, db_user=user_to_update, user_in=update_data)

    assert updated_user is not None
    assert updated_user.id == user_to_update.id
    assert updated_user.email == new_email
    assert updated_user.full_name == new_full_name
    assert updated_user.is_active is False
    assert updated_user.is_superuser is True
    assert verify_password(new_password, updated_user.hashed_password)
    assert not verify_password(original_password, updated_user.hashed_password)


def test_update_user_partial_no_password(db_session: Session) -> None:
    """
    Testa a atualização parcial de um usuário (ex: apenas nome), sem alterar a senha.
    """
    email = "partial_update@example.com"
    password = "passwordUnchanged"
    user_to_update = crud_user.create_user(db_session, UserCreate(
        email=email, password=password, full_name="Initial Name"
    ))

    new_full_name = "Partially Updated Name"
    update_data_dict: Dict[str, Any] = {
        "full_name": new_full_name, 
        "is_active": False        
    } 

    updated_user = crud_user.update_user(db=db_session, db_user=user_to_update, user_in=update_data_dict)

    assert updated_user is not None
    assert updated_user.email == email 
    assert updated_user.full_name == new_full_name
    assert updated_user.is_active is False
    assert verify_password(password, updated_user.hashed_password)


def test_update_user_only_password(db_session: Session) -> None:
    """Testa a atualização apenas da senha de um usuário."""
    email = "password_only_update@example.com"
    original_password = "originalPassword"
    user_to_update = crud_user.create_user(db_session, UserCreate(
        email=email, password=original_password, full_name="Password User"
    ))

    new_password = "newSecurePasswordOnly"
    update_data = UserUpdate(password=new_password)

    updated_user = crud_user.update_user(db=db_session, db_user=user_to_update, user_in=update_data)

    assert updated_user is not None
    assert updated_user.email == email
    assert verify_password(new_password, updated_user.hashed_password)
    assert not verify_password(original_password, updated_user.hashed_password)


def test_update_user_with_none_values(db_session: Session) -> None:
    """
    Testa que campos não enviados (que são None no Pydantic model se não definidos)
    não sobrescrevem valores existentes para None na função de update.
    A lógica atual do crud.update_user é:
    `if hasattr(db_user, field) and value is not None: setattr(db_user, field, value)`
    Então, se passarmos `None` explicitamente para um campo que pode ser `None` no UserUpdate
    (como `full_name`), ele não deveria ser atualizado para `None`.
    Para "limpar" um campo (setar para None), precisaríamos de lógica adicional
    ou passar um valor específico como uma string vazia.
    Este teste verifica que campos 'não preenchidos' no update não mudam o valor do DB.
    """
    email = "none_values_update@example.com"
    initial_full_name = "Initial Full Name"
    user_to_update = crud_user.create_user(db_session, UserCreate(
        email=email, password="password", full_name=initial_full_name
    ))

    update_data_schema = UserUpdate() 
    updated_user = crud_user.update_user(db=db_session, db_user=user_to_update, user_in=update_data_schema)

    assert updated_user.full_name == initial_full_name, "full_name não deveria mudar para None se não enviado."
    assert updated_user.email == email, "email não deveria mudar para None se não enviado."

    update_data_dict = {"full_name": None}
    updated_user_dict = crud_user.update_user(db=db_session, db_user=user_to_update, user_in=update_data_dict)
    assert updated_user_dict.full_name == initial_full_name, \
        "full_name não deveria ser setado para None explicitamente devido à condição 'value is not None'."


def test_delete_user(db_session: Session) -> None:
    """
    Testa a exclusão de um usuário do banco de dados.
    """
    email_to_delete = "delete_me@example.com"
    user_to_delete_in_create = UserCreate(email=email_to_delete, password="password")
    user_to_delete_model = crud_user.create_user(db=db_session, user=user_to_delete_in_create) 

    assert user_to_delete_model.id is not None
    user_id_deleted = user_to_delete_model.id

    deleted_user_obj = crud_user.delete_user(db=db_session, db_user=user_to_delete_model)

    assert deleted_user_obj.id == user_id_deleted 

    user_after_delete = crud_user.get_user(db=db_session, user_id=user_id_deleted)
    assert user_after_delete is None, "Usuário não deveria ser encontrado no banco após a exclusão."

    user_by_email_after_delete = crud_user.get_user_by_email(db=db_session, email=email_to_delete)
    assert user_by_email_after_delete is None, "Usuário não deveria ser encontrado por e-mail após a exclusão."