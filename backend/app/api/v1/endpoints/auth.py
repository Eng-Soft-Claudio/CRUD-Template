# app/api/v1/endpoints/auth.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session

from app.schemas.user import ( 
    UserCreate,
    UserRead,
    UserUpdate,
    UserPasswordChange,
    PasswordRecoveryRequest, 
    PasswordResetForm        
)
from app.schemas.token import Token
from app.crud.user import ( 
    get_user_by_email,
    create_user,
    update_user,
    delete_user 
)
from app.api import deps
from app.core import security
from app.core.config import settings
from app.db.models.user import User as UserModel 

# =======================================================================================================
# --- Rotas ---                                                                                     #####
# =======================================================================================================

router = APIRouter()

# =======================================================================================================
# --- Endpoints ---                                                                                 #####
# =======================================================================================================

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_new_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Cria um novo usuário.
    """
    user = get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    new_user = create_user(db=db, user=user_in)
    return new_user


@router.post("/login", response_model=Token)
def login_for_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends() 
) -> Any:
    """
    OAuth2 compatível com endpoint de token, login com email e senha.
    Retorna um access_token e um refresh_token (opcional).
    """
    user = get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    
    access_token = security.create_access_token(
        data={"sub": user.email} 
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserRead)
def read_users_me(
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtém o usuário atual.
    """
    return current_user


@router.get("/me/superuser", response_model=UserRead)
def read_current_superuser(
    current_user: UserModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Obtém o usuário atual, requerendo que seja um superusuário ativo.
    Endpoint de teste para a dependência get_current_active_superuser.
    """
    return current_user


@router.patch("/me", response_model=UserRead)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_update_data: UserUpdate, 
    current_user: UserModel = Depends(deps.get_current_active_user) 
) -> Any:
    """
    Atualiza os dados do usuário autenticado.
    Permite atualizar email, full_name, password (se enviado).
    Campos como is_active e is_superuser não devem ser atualizáveis pelo próprio usuário aqui.
    """
    if user_update_data.email and user_update_data.email != current_user.email:
        existing_user = get_user_by_email(db, email=user_update_data.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered by another user.",
            )

    update_data_for_crud = user_update_data.model_dump(exclude_unset=True)
    if "is_active" in update_data_for_crud:
        del update_data_for_crud["is_active"] 
    if "is_superuser" in update_data_for_crud:
        del update_data_for_crud["is_superuser"] 

    updated_user = update_user(db=db, db_user=current_user, user_in=update_data_for_crud)
    return updated_user


@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
def update_current_user_password(
    *,
    db: Session = Depends(deps.get_db),
    password_data: UserPasswordChange, 
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> None: 
    """
    Atualiza a senha do usuário autenticado.
    Requer a senha atual e a nova senha (com confirmação).
    """
    # 1. Verificar se a senha atual fornecida está correta
    if not security.verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password",
        )
    
    # 2. Verificar se a nova senha é diferente da antiga 
    if security.verify_password(password_data.new_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be the same as the current password.",
        )

    # 3. Gerar o hash da nova senha
    hashed_password = security.get_password_hash(password_data.new_password)
    current_user.hashed_password = hashed_password 
    
    db.add(current_user)
    db.commit()


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> None: 
    """
    Deleta a conta do usuário autenticado.
    """
    delete_user(db=db, db_user=current_user)
    return None


@router.post("/password-recovery", response_model=Dict[str, str])
async def request_password_recovery(
    recovery_data: PasswordRecoveryRequest,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Inicia o processo de recuperação de senha.
    Gera um token de recuperação se o usuário existir.
    (Simula o envio de e-mail printando o token e um link de exemplo).
    """
    user = get_user_by_email(db, email=recovery_data.email)
    if not user:
        return {"message": "Se um usuário com este email existir, um link de recuperação foi enviado."}

    password_reset_token = security.create_password_reset_token(email=user.email)
    
    reset_link = f"{settings.SERVER_HOST}{settings.API_V1_STR}/auth/reset-password-form?token={password_reset_token}" 
    
    print("---- SIMULAÇÃO DE ENVIO DE E-MAIL ----")
    print(f"Para: {user.email}")
    print(f"Assunto: Recuperação de Senha - {settings.PROJECT_NAME}")
    print(f"Use o seguinte token para resetar sua senha (ou clique no link): {password_reset_token}")
    print(f"Ou acesse o link: {reset_link}")
    print("--------------------------------------")
    
    return {"message": "Se um usuário com este email existir, um link de recuperação foi enviado."}


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_user_password(
    reset_form_data: PasswordResetForm = Body(...),
    db: Session = Depends(deps.get_db)
) -> None:
    """
    Reseta a senha do usuário usando um token de recuperação válido.
    """
    email_from_token = security.verify_password_reset_token(reset_form_data.token)
    if not email_from_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de recuperação de senha inválido ou expirado.",
        )
    
    user = get_user_by_email(db, email=email_from_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado. Token pode ser inválido.",
        )
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inativo.")
    
    hashed_password = security.get_password_hash(reset_form_data.new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()

    # Simulação de envio de e-mail de confirmação:
    print(f"---- SIMULAÇÃO DE ENVIO DE E-MAIL ----")         
    print(f"Para: {user.email}")                            
    print(f"Assunto: Sua senha foi alterada - {settings.PROJECT_NAME}")
    print(f"Sua senha foi alterada com sucesso.")              
    print("--------------------------------------") 

    return None