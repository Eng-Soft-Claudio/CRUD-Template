# app/db/base_class.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from sqlalchemy.orm import DeclarativeBase, declared_attr
from typing import Any

# =======================================================================================================
# --- Instância ---                                                                                 #####
# =======================================================================================================
class Base(DeclarativeBase):
    """
    Classe base para os modelos SQLAlchemy.
    Automaticamente define o nome da tabela como o nome da classe em minúsculas.
    """
    id: Any
    __name__: str

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()