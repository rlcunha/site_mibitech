"""
Script para testar a conexão com o banco de dados PostgreSQL.

Este script tenta estabelecer uma conexão com o banco de dados
configurado e executa uma consulta simples para verificar se
a conexão está funcionando corretamente.
"""
import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_db_connection")

def test_connection():
    """
    Testa a conexão com o banco de dados PostgreSQL.
    
    Tenta estabelecer uma conexão com o banco de dados usando
    as configurações do ambiente e executa uma consulta simples
    para verificar se a conexão está funcionando.
    
    Returns:
        bool: True se a conexão for bem-sucedida, False caso contrário
    """
    try:
        # Carrega variáveis de ambiente
        load_dotenv()
        
        # Obtém a URL de conexão do ambiente ou usa o valor padrão
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mibitech")
        
        logger.info(f"Tentando conectar ao banco de dados: {DATABASE_URL}")
        
        # Cria engine de conexão
        engine = create_engine(DATABASE_URL)
        
        # Tenta conectar e executar uma consulta simples
        with engine.connect() as connection:
            logger.info("Conexão estabelecida com sucesso!")
            
            # Executa uma consulta simples para verificar a conexão
            result = connection.execute(text("SELECT 1 AS test"))
            row = result.fetchone()
            
            if row and row[0] == 1:
                logger.info("Consulta de teste executada com sucesso!")
                
                # Verifica se a tabela social_media existe
                try:
                    result = connection.execute(text("SELECT COUNT(*) FROM social_media"))
                    count = result.scalar()
                    logger.info(f"Tabela social_media encontrada com {count} registros")
                except SQLAlchemyError:
                    logger.warning("Tabela social_media não encontrada. As migrações foram executadas?")
                
                return True
            else:
                logger.error("Falha na consulta de teste!")
                return False
                
    except SQLAlchemyError as e:
        logger.error(f"Erro de conexão com o banco de dados: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return False

def main():
    """Função principal."""
    logger.info("Iniciando teste de conexão com o banco de dados...")
    
    success = test_connection()
    
    if success:
        logger.info("Teste de conexão concluído com sucesso!")
        return 0
    else:
        logger.error("Teste de conexão falhou!")
        return 1

if __name__ == "__main__":
    sys.exit(main())