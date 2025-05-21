"""create_user_table

Revision ID: 595de6c503ca
Revises: 
Create Date: 2025-05-20 13:58:34.664170

"""

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# =======================================================================================================
# --- Revisão e Identificadores ---                                                                 #####
# =======================================================================================================

revision: str = '595de6c503ca'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# =======================================================================================================
# --- Upgrade e Downgrade do Alembic ---                                                            #####
# =======================================================================================================

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_full_name'), 'user', ['full_name'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_full_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
