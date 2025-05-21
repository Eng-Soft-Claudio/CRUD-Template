# app/crud/user.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from typing import Any, Dict, Optional, Union
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
    """
    if isinstance(user_in, dict):
        update_data = user_in
    else:
        update_data = user_in.model_dump(exclude_unset=True)

    if update_data.get("password"):
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        db_user.hashed_password = hashed_password 

    for field, value in update_data.items():
        if hasattr(db_user, field) and value is not None:
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