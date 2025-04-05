"""
Script simples para testar a conexão com o banco de dados PostgreSQL.

Este script tenta estabelecer uma conexão direta com o banco de dados
PostgreSQL usando a biblioteca psycopg2.
"""
import os
import sys
import logging
import psycopg2
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("simple_db_test")

def test_connection():
    """
    Testa a conexão com o banco de dados PostgreSQL.
    
    Returns:
        bool: True se a conexão for bem-sucedida, False caso contrário
    """
    try:
        # Carrega variáveis de ambiente
        load_dotenv()
        
        # Obtém parâmetros de conexão do ambiente ou usa valores padrão
        db_host = os.getenv("DB_HOST", "server.mibitech.com.br")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB", "postgres")
        db_user = os.getenv("POSTGRES_USER", "postgres")
        db_password = os.getenv("POSTGRES_PASSWORD", "Mfcd62!!Mfcd62!!")
        
        # Constrói string de conexão
        conn_string = f"host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"
        
        logger.info(f"Tentando conectar ao banco de dados: {db_host}:{db_port}/{db_name}")
        
        # Tenta estabelecer conexão
        conn = psycopg2.connect(conn_string)
        
        logger.info("Conexão estabelecida com sucesso!")
        
        # Cria um cursor e executa uma consulta simples
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        
        # Obtém o resultado
        db_version = cursor.fetchone()
        logger.info(f"Versão do PostgreSQL: {db_version[0]}")
        
        # Verifica se a tabela social_media existe
        try:
            cursor.execute("SELECT COUNT(*) FROM social_media;")
            count = cursor.fetchone()[0]
            logger.info(f"Tabela social_media encontrada com {count} registros")
        except psycopg2.errors.UndefinedTable:
            logger.warning("Tabela social_media não encontrada. As migrações foram executadas?")
        
        # Fecha cursor e conexão
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.OperationalError as e:
        logger.error(f"Erro de conexão com o banco de dados: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return False

def main():
    """Função principal."""
    logger.info("Iniciando teste simples de conexão com o banco de dados...")
    
    success = test_connection()
    
    if success:
        logger.info("Teste de conexão concluído com sucesso!")
        return 0
    else:
        logger.error("Teste de conexão falhou!")
        return 1

if __name__ == "__main__":
    sys.exit(main())