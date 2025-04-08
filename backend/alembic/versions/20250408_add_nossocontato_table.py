"""Add nossocontato table

Revision ID: 20250408_add_nossocontato_table
Revises: 5890837d8efc
Create Date: 2025-04-08 10:25:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '20250408_add_nossocontato_table'
down_revision = '5890837d8efc'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('nossocontato',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('tipo', sa.String(50), nullable=False),
        sa.Column('local', sa.String(100), nullable=False),
        sa.Column('telefone', sa.String(20), nullable=False),
        sa.Column('email', sa.String(100), nullable=False)
    )

def downgrade():
    op.drop_table('nossocontato')