"""
Ambiente de execução do Alembic.

Este módulo configura o ambiente para execução de migrações,
incluindo detecção de modelos e configuração de conexão.
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
import logging

# Adiciona diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuração de logging
logger = logging.getLogger("alembic.env")

# Importa todos os modelos para autogerar migrações
# Importante: Todos os novos modelos devem ser importados aqui
from app.models.base import Base
from app.models.social_media import SocialMedia
# Adicione novos modelos aqui quando criados

# Obtém configuração do Alembic
config = context.config

# Configura logging a partir do arquivo de configuração
fileConfig(config.config_file_name)

# Define os metadados alvo para as migrações
target_metadata = Base.metadata

# Outras variáveis de configuração
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # Sobrescreve a URL do banco de dados se definida como variável de ambiente
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Opções de configuração para as migrações
config_opts = {
    "compare_type": True,      # Compara tipos de colunas
    "compare_server_default": True,  # Compara valores padrão
    "include_schemas": True,   # Inclui esquemas
    "render_as_batch": True,   # Renderiza como batch (útil para SQLite)
}

def run_migrations_offline():
    """
    Executa migrações em modo 'offline'.
    
    Útil para gerar SQL sem conectar ao banco de dados.
    """
    url = config.get_main_option("sqlalchemy.url")
    logger.info(f"Executando migrações offline com URL: {url}")
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        **config_opts
    )

    with context.begin_transaction():
        context.run_migrations()
    
    logger.info("Migrações offline concluídas")

def run_migrations_online():
    """
    Executa migrações em modo 'online'.
    
    Conecta ao banco de dados e aplica as migrações diretamente.
    """
    # Obtém configuração da seção do alembic.ini
    section = config.get_section(config.config_ini_section)
    logger.info(f"Executando migrações online com URL: {section.get('sqlalchemy.url')}")
    
    # Cria engine de conexão
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Configura contexto com a conexão
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            **config_opts
        )

        # Executa migrações dentro de uma transação
        with context.begin_transaction():
            context.run_migrations()
    
    logger.info("Migrações online concluídas")

# Executa o modo apropriado com base na configuração
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()