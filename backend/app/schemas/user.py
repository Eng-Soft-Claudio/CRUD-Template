# app/schemas/user.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, ValidationInfo
from typing import Optional

# =======================================================================================================
# --- Schemas de Usuário ---                                                                        #####
# =======================================================================================================

class UserBase(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = Field(default=True)
    is_superuser: Optional[bool] = Field(default=False)

class UserCreate(BaseModel): 
    """Schema para criar um novo usuário."""
    email: EmailStr 
    password: str   
    full_name: Optional[str] = None
    is_active: Optional[bool] = Field(default=True) 
    is_superuser: Optional[bool] = Field(default=False)

class UserUpdate(UserBase):
    """Schema para atualizar um usuário. Todos os campos são opcionais."""
    email: Optional[EmailStr] = None
    password: Optional[str] = None 

class UserRead(BaseModel):
    """Schema para dados de usuário retornados pela API."""
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserRead):
    hashed_password: str

class UserPasswordChange(BaseModel):
    """Schema para mudança de senha do usuário."""
    current_password: str
    new_password: str
    new_password_confirm: str

    @field_validator('new_password_confirm')
    @classmethod
    def passwords_match(cls, v: str, info: ValidationInfo) -> str:
        """Verifica se a nova senha e a confirmação correspondem."""
        if info.data and 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('As senhas não correspondem')
        return v
    
class PasswordRecoveryRequest(BaseModel):
    """Schema para solicitar a recuperação de senha."""
    email: EmailStr

class PasswordResetForm(BaseModel):
    """
    Schema para o formulário de reset (definição) de nova senha.
    Utilizado quando o usuário já tem o token de recuperação.
    """
    token: str 
    new_password: str
    new_password_confirm: str

    @field_validator('new_password_confirm')
    @classmethod
    def passwords_match(cls, v: str, info: ValidationInfo) -> str:
        """Verifica se a nova senha e a confirmação correspondem."""
        if info.data and 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('As senhas não correspondem')
        return v