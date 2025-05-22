# backend/app/api/v1/endpoints/users_admin.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from typing import Any, List

from fastapi import APIRouter,Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import user as crud_user
from app.db.models.user import User as UserModel
from app.schemas.user import UserCreate, UserRead, UserUpdate


# =======================================================================================================
# --- Rotas ---                                                                                     #####
# =======================================================================================================

router = APIRouter()

# =======================================================================================================
# --- Endpoints (Administração de Usuários) ---                                                     #####
# =======================================================================================================

@router.get("/", response_model=List[UserRead], status_code=status.HTTP_200_OK)
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0, description="Número de registros a pular para paginação"),
    limit: int = Query(100, ge=1, le=200, description="Número máximo de registros a retornar"),
    current_admin: UserModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Recupera uma lista de usuários.
    Acessível apenas por superusuários.
    """
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_by_admin_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_admin: UserModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Cria um novo usuário no sistema.
    Acessível apenas por superusuários. Permite definir todos os campos, incluindo is_active e is_superuser.
    """
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O usuário com este email já existe no sistema.",
        )
    new_user = crud_user.create_user_by_admin(db=db, user=user_in)
    return new_user


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def read_user_by_id_admin(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: UserModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Obtém um usuário específico pelo ID.
    Acessível apenas por superusuários.
    """
    user = crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="O usuário com este ID não foi encontrado no sistema.",
        )
    return user


@router.put("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_user_by_admin_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_admin: UserModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Atualiza um usuário existente pelo ID.
    Acessível apenas por superusuários. Permite atualizar todos os campos editáveis,
    incluindo is_active, is_superuser e, opcionalmente, a senha.
    """
    user = crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="O usuário com este ID não foi encontrado no sistema.",
        )

    if user_in.email and user_in.email != user.email:
        existing_user_with_new_email = crud_user.get_user_by_email(db, email=user_in.email)
        if existing_user_with_new_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O novo email fornecido já está registrado por outro usuário.",
            )

    updated_user = crud_user.update_user(db=db, db_user=user, user_in=user_in)
    return updated_user


@router.delete("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def delete_user_by_admin_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_admin: UserModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Deleta um usuário específico pelo ID.
    Acessível apenas por superusuários.
    Não permite que um superusuário delete a si mesmo através deste endpoint.
    """
    if current_admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superusuários não podem deletar a si mesmos através deste endpoint. Use /auth/me.",
        )

    user_to_delete = crud_user.get_user(db, user_id=user_id)
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="O usuário com este ID não foi encontrado no sistema para deleção.",
        )

    deleted_user = crud_user.delete_user(db=db, db_user=user_to_delete)
    return deleted_user