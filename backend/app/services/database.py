"""
Serviços de banco de dados.

Este módulo fornece funcionalidades para conexão e interação
com o banco de dados, incluindo configuração, validação e
gerenciamento de sessões.
"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
import logging
import time
from typing import Generator, Dict, Any

from ..errors import BaseAPIError, DatabaseError
from ..helpers import DataProcessor, StringProcessor

# Configuração de logging
logger = logging.getLogger("api.database")

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da conexão com o banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Mfcd62!!Mfcd62!!@server.mibitech.com.br:5432/mibitech")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))

# Configuração do engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
    pool_timeout=DB_POOL_TIMEOUT,
    pool_pre_ping=True,  # Verifica conexões antes de usá-las
    pool_recycle=3600,   # Recicla conexões após 1 hora
    echo=os.getenv("SQL_ECHO", "false").lower() == "true"  # Log de SQL
)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para modelos
Base = declarative_base()

# Eventos de conexão para monitoramento
@event.listens_for(engine, "connect")
def receive_connect(dbapi_connection, connection_record):
    """
    Registra quando uma conexão é estabelecida.
    
    Args:
        dbapi_connection: Conexão DBAPI
        connection_record: Registro da conexão
    """
    logger.info("Conexão de banco de dados estabelecida")

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    """
    Registra quando uma conexão é retirada do pool.
    
    Args:
        dbapi_connection: Conexão DBAPI
        connection_record: Registro da conexão
        connection_proxy: Proxy da conexão
    """
    logger.debug("Conexão retirada do pool")
    connection_record.info['checkout_time'] = time.time()

@event.listens_for(engine, "checkin")
def receive_checkin(dbapi_connection, connection_record):
    """
    Registra quando uma conexão é devolvida ao pool.
    
    Args:
        dbapi_connection: Conexão DBAPI
        connection_record: Registro da conexão
    """
    checkout_time = connection_record.info.get('checkout_time')
    if checkout_time is not None:
        connection_record.info['checkout_time'] = None
        elapsed = time.time() - checkout_time
        logger.debug(f"Conexão devolvida ao pool (tempo de uso: {elapsed:.2f}s)")

class DatabaseValidator(DataProcessor):
    """
    Validador de parâmetros de conexão com banco de dados.
    
    Fornece métodos para validar strings de conexão e outros
    parâmetros relacionados ao banco de dados.
    """
    
    def __init__(self):
        """Inicializa o validador com processador de strings."""
        self.string_processor = StringProcessor()
    
    def process(self, data: str) -> str:
        """
        Processa uma string de conexão (implementação padrão).
        
        Args:
            data: String de conexão
            
        Returns:
            String de conexão processada
        """
        return data
    
    def validate(self, data: str) -> bool:
        """
        Valida o formato da URL de conexão com o banco de dados.
        
        Args:
            data: String de conexão a ser validada
            
        Returns:
            bool: True se o formato for válido, False caso contrário
        """
        # Verifica se é uma string
        if not self.string_processor.validate(data):
            return False
            
        # Verifica se começa com um dos prefixos suportados
        return data.startswith(("postgresql://", "sqlite://", "mysql://"))
    
    def validate_connection_params(self, params: Dict[str, Any]) -> bool:
        """
        Valida parâmetros de conexão.
        
        Args:
            params: Dicionário com parâmetros de conexão
            
        Returns:
            bool: True se os parâmetros forem válidos, False caso contrário
        """
        required_params = ["host", "database"]
        return all(param in params for param in required_params)

def get_db() -> Generator[Session, None, None]:
    """
    Obtém uma sessão de banco de dados do pool.
    
    Esta função é usada como dependência em endpoints FastAPI
    para fornecer uma sessão de banco de dados.
    
    Yields:
        Sessão de banco de dados
        
    Raises:
        DatabaseError: Se ocorrer um erro de conexão
    """
    try:
        # Valida string de conexão
        validator = DatabaseValidator()
        if not validator.validate(DATABASE_URL):
            logger.error(f"String de conexão inválida: {DATABASE_URL}")
            raise ValueError("String de conexão com banco de dados inválida")
            
        # Obtém sessão do pool
        db = SessionLocal()
        logger.debug("Sessão de banco de dados obtida")
        
        try:
            yield db
        finally:
            # Garante que a sessão seja fechada
            db.close()
            logger.debug("Sessão de banco de dados fechada")
            
    except SQLAlchemyError as e:
        # Erro específico de SQLAlchemy
        logger.error(f"Erro SQLAlchemy: {str(e)}")
        raise DatabaseError(
            message="Falha na conexão com o banco de dados",
            details={"error": str(e)}
        )
    except Exception as e:
        # Outros erros
        logger.error(f"Erro ao obter sessão de banco de dados: {str(e)}", exc_info=True)
        raise BaseAPIError(
            message="Falha na conexão com o banco de dados",
            status_code=500,
            details={"error": str(e)}
        )

def get_engine_stats() -> Dict[str, Any]:
    """
    Obtém estatísticas do pool de conexões.
    
    Útil para monitoramento e diagnóstico.
    
    Returns:
        Dicionário com estatísticas do pool
    """
    if not hasattr(engine, 'pool'):
        return {"error": "Pool não disponível"}
        
    pool = engine.pool
    if isinstance(pool, QueuePool):
        return {
            "size": pool.size(),
            "checkedin": pool.checkedin(),
            "overflow": pool.overflow(),
            "checkedout": pool.checkedout(),
        }
    return {"error": "Não é um QueuePool"}