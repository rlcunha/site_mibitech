"""
Script de inicialização do banco de dados.

Este script executa migrações do Alembic e inicializa dados
necessários para o funcionamento da aplicação.
"""
import os
import logging
from alembic.config import Config
from alembic import command
from app.models.social_media import SocialMedia
from app.services.database import SessionLocal
from app.helpers import StringProcessor

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("init_db")

def run_migrations():
    """
    Executa migrações do banco de dados usando Alembic.
    
    Aplica todas as migrações pendentes para atualizar o esquema
    do banco de dados para a versão mais recente.
    """
    try:
        logger.info("Iniciando migrações do banco de dados...")
        
        # Configura o Alembic
        alembic_cfg = Config("alembic.ini")
        
        # Executa as migrações
        command.upgrade(alembic_cfg, "head")
        
        logger.info("Migrações concluídas com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao executar migrações: {str(e)}", exc_info=True)
        return False

def seed_data():
    """
    Inicializa dados necessários no banco de dados.
    
    Verifica se já existem dados e, caso contrário, insere
    dados iniciais para o funcionamento da aplicação.
    """
    logger.info("Verificando necessidade de seed de dados...")
    
    # Inicializa sessão do banco de dados
    db = SessionLocal()
    
    try:
        # Verifica se já existem dados de mídia social
        if not db.query(SocialMedia).first():
            logger.info("Inserindo dados iniciais de mídias sociais...")
            
            # Validador para URLs
            string_processor = StringProcessor()
            
            # Dados iniciais
            social_media = [
                SocialMedia(
                    name="Facebook",
                    url="https://facebook.com/mibitech",
                    icon="facebook"
                ),
                SocialMedia(
                    name="Instagram",
                    url="https://instagram.com/mibitech",
                    icon="instagram"
                ),
                SocialMedia(
                    name="LinkedIn",
                    url="https://linkedin.com/company/mibitech",
                    icon="linkedin"
                ),
                SocialMedia(
                    name="GitHub",
                    url="https://github.com/mibitech",
                    icon="github"
                )
            ]
            
            # Valida URLs antes de inserir
            for sm in social_media:
                if not string_processor.validate_url(sm.url):
                    logger.warning(f"URL inválida ignorada: {sm.url}")
                    continue
                    
                db.add(sm)
                
            # Salva no banco de dados
            db.commit()
            logger.info("Dados iniciais inseridos com sucesso")
        else:
            logger.info("Dados já existem, seed não necessário")
            
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao inserir dados iniciais: {str(e)}", exc_info=True)
    finally:
        db.close()

def init_db():
    """
    Inicializa o banco de dados completo.
    
    Executa migrações e seed de dados em sequência.
    """
    logger.info("Iniciando setup do banco de dados...")
    
    # Executa migrações
    if run_migrations():
        # Se migrações foram bem-sucedidas, executa seed
        seed_data()
    else:
        logger.error("Setup do banco de dados falhou devido a erros nas migrações")
        
    logger.info("Processo de inicialização do banco de dados concluído")

if __name__ == "__main__":
    init_db()