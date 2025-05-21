# app/schemas/token.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from typing import Optional
from pydantic import BaseModel, EmailStr

# =======================================================================================================
# --- Token Base e Data ---                                                                         #####
# =======================================================================================================

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
