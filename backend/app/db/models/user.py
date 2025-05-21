# app/db/models/user.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column 

from app.db.base_class import Base 

# =======================================================================================================
# --- Classe Base de Usuário ---                                                                    #####
# =======================================================================================================
class User(Base):
    """
    Modelo de tabela para os usuários.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True) 
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
