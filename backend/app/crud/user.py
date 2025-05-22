# app/crud/user.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session

from app.db.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

# =======================================================================================================
# --- CRUD ---                                                                                      #####
# =======================================================================================================

def get_user_by_email(db: Session, email: str) -> Optional[UserModel]: 
    """
    Busca um usuário pelo seu endereço de e-mail.
    """
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_user(db: Session, user_id: int) -> Optional[UserModel]: 
    """
    Busca um usuário pelo seu ID.
    """
    return db.query(UserModel).filter(UserModel.id == user_id).first()

# =======================================================================================================
# --- CRUD (Superuser) ---                                                                          #####
# =======================================================================================================

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserModel]:
    """
    Busca todos os usuários com paginação.
    Acessível apenas por superusuários.
    """
    return db.query(UserModel).offset(skip).limit(limit).all()

def create_user_by_admin(db: Session, user: UserCreate) -> UserModel: 
    """
    Cria um novo usuário no banco de dados (ação de administrador).
    Permite definir is_active e is_superuser.
    """
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# =======================================================================================================
# --- CRUD (Usuário Comum / Superuser) ---                                                          #####
# =======================================================================================================

def create_user(db: Session, user: UserCreate) -> UserModel:
    """
    Cria um novo usuário no banco de dados.
    """
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        is_active=user.is_active if user.is_active is not None else True,
        is_superuser=user.is_superuser if user.is_superuser is not None else False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(
    db: Session,
    db_user: UserModel, 
    user_in: Union[UserUpdate, Dict[str, Any]]
) -> UserModel:
    """
    Atualiza um usuário no banco de dados.
    Se user_in for UserUpdate, pode ser um usuário atualizando o próprio perfil.
    Se user_in for Dict (usado por admin), pode atualizar is_active, is_superuser.
    """
    if isinstance(user_in, dict):
        update_data = user_in
    else:
        update_data = user_in.model_dump(exclude_unset=True)

    if update_data.get("password"): 
        hashed_password = get_password_hash(update_data["password"])
        db_user.hashed_password = hashed_password
        if "password" in update_data : del update_data["password"] 

    for field, value in update_data.items():
        if hasattr(db_user, field): 
            if value is not None or (field in ["full_name"] and isinstance(user_in, UserUpdate)):
                 setattr(db_user, field, value)


    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: UserModel) -> UserModel:
    """
    Deleta um usuário do banco de dados.
    """
    db.delete(db_user)
    db.commit()
    return db_user 