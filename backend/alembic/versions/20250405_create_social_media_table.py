"""create social media table

Revision ID: 20250405_create_social_media
Revises: 
Create Date: 2025-04-05 10:37:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, DateTime
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '20250405_create_social_media'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    Cria a tabela social_media e insere dados iniciais.
    
    Esta migração:
    1. Cria a tabela com todos os campos necessários
    2. Adiciona índices e restrições
    3. Insere dados iniciais de exemplo
    """
    # Cria a tabela
    op.create_table(
        'social_media',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('url', sa.String(255), nullable=False),
        sa.Column('icon', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, 
                 server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(), nullable=False,
                 server_default=sa.func.current_timestamp(),
                 server_onupdate=sa.func.current_timestamp()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Adiciona índice para melhorar performance de buscas
    op.create_index(
        'ix_social_media_name', 
        'social_media', 
        ['name'], 
        unique=True
    )
    
    # Define a tabela para inserção de dados
    social_media_table = table(
        'social_media',
        column('name', String),
        column('url', String),
        column('icon', String),
        column('created_at', DateTime),
        column('updated_at', DateTime)
    )
    
    # Insere dados iniciais
    current_time = datetime.utcnow()
    op.bulk_insert(
        social_media_table,
        [
            {
                'name': 'Facebook', 
                'url': 'https://facebook.com/mibitech', 
                'icon': 'facebook',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'name': 'Instagram', 
                'url': 'https://instagram.com/mibitech', 
                'icon': 'instagram',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'name': 'Twitter', 
                'url': 'https://twitter.com/mibitech', 
                'icon': 'twitter',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'name': 'LinkedIn', 
                'url': 'https://linkedin.com/company/mibitech', 
                'icon': 'linkedin',
                'created_at': current_time,
                'updated_at': current_time
            }
        ]
    )


def downgrade():
    """
    Reverte as alterações feitas no upgrade.
    
    Remove a tabela social_media e todos os seus dados.
    """
    op.drop_index('ix_social_media_name', 'social_media')
    op.drop_table('social_media')