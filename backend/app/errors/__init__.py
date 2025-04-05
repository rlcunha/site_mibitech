"""
Framework de tratamento de erros para gerenciamento consistente de exceções.

Fornece:
- Classes base de erro
- Manipuladores de erro
- Utilitários de exceção HTTP
- Formatação de resposta de erro
"""
from typing import Any, Dict, Optional, List, Type
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
import logging
import traceback
import json
import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("api.errors")

class BaseAPIError(Exception):
    """
    Classe base para todos os erros de API.
    
    Esta classe estende Exception e fornece funcionalidade adicional
    para formatação consistente de erros em respostas HTTP.
    """
    
    def __init__(
        self,
        message: str = "Ocorreu um erro",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None,
        log_error: bool = True
    ):
        """
        Inicializa uma nova instância de erro de API.
        
        Args:
            message: Mensagem de erro legível
            status_code: Código de status HTTP
            details: Detalhes adicionais do erro
            log_error: Se deve registrar o erro no log
        """
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.timestamp = datetime.datetime.now().isoformat()
        
        # Registra o erro se solicitado
        if log_error:
            logger.error(
                f"API Error: {message} (Code: {status_code})",
                extra={"details": self.details}
            )
            
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o erro para formato de dicionário para resposta.
        
        Returns:
            Dicionário formatado com informações de erro
        """
        return {
            "error": {
                "message": self.message,
                "code": self.status_code,
                "timestamp": self.timestamp,
                "details": self.details
            }
        }

class ValidationError(BaseAPIError):
    """
    Erro específico para falhas de validação de dados.
    
    Usado quando os dados de entrada não atendem aos requisitos.
    """
    
    def __init__(
        self,
        message: str = "Erro de validação",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa um erro de validação.
        
        Args:
            message: Mensagem de erro
            details: Detalhes da validação falha
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )

class DatabaseError(BaseAPIError):
    """
    Erro específico para problemas relacionados ao banco de dados.
    
    Usado para capturar e formatar erros de banco de dados.
    """
    
    def __init__(
        self,
        message: str = "Erro de banco de dados",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa um erro de banco de dados.
        
        Args:
            message: Mensagem de erro
            details: Detalhes do erro de banco de dados
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )

class NotFoundError(BaseAPIError):
    """
    Erro específico para recursos não encontrados.
    
    Usado quando um recurso solicitado não existe.
    """
    
    def __init__(
        self,
        message: str = "Recurso não encontrado",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa um erro de recurso não encontrado.
        
        Args:
            message: Mensagem de erro
            details: Detalhes sobre o recurso não encontrado
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )

class AuthenticationError(BaseAPIError):
    """
    Erro específico para falhas de autenticação.
    
    Usado quando há problemas com credenciais ou tokens.
    """
    
    def __init__(
        self,
        message: str = "Falha na autenticação",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa um erro de autenticação.
        
        Args:
            message: Mensagem de erro
            details: Detalhes sobre a falha de autenticação
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )

class APIErrorHandler:
    """
    Manipulador central de erros para a aplicação.
    
    Fornece métodos para processar diferentes tipos de exceções
    e convertê-las em respostas HTTP apropriadas.
    """
    
    @staticmethod
    def handle_exception(exc: Exception) -> JSONResponse:
        """
        Manipula exceções e retorna respostas HTTP apropriadas.
        
        Este método centraliza o tratamento de erros, garantindo
        consistência nas respostas de erro da API.
        
        Args:
            exc: A exceção a ser tratada
            
        Returns:
            JSONResponse formatada com detalhes do erro
        """
        # Registra o stack trace para erros não tratados
        if not isinstance(exc, (BaseAPIError, HTTPException)):
            logger.error(
                f"Unhandled exception: {str(exc)}",
                exc_info=True,
                extra={"traceback": traceback.format_exc()}
            )
        
        # Trata erros específicos da API
        if isinstance(exc, BaseAPIError):
            return JSONResponse(
                status_code=exc.status_code,
                content=exc.to_dict()
            )
        # Trata exceções HTTP do FastAPI
        elif isinstance(exc, HTTPException):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": {
                        "message": exc.detail,
                        "code": exc.status_code,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                }
            )
            
        # Erro 500 padrão para exceções não tratadas
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "message": "Erro interno do servidor",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "timestamp": datetime.datetime.now().isoformat()
                }
            }
        )
    
    @staticmethod
    async def log_request_info(request: Request, exc: Exception) -> None:
        """
        Registra informações da requisição quando ocorre um erro.
        
        Útil para depuração, captura detalhes da requisição que causou o erro.
        
        Args:
            request: Objeto de requisição FastAPI
            exc: A exceção que ocorreu
        """
        # Extrai informações úteis da requisição
        client_host = request.client.host if request.client else "unknown"
        method = request.method
        url = str(request.url)
        headers = dict(request.headers)
        
        # Remove informações sensíveis
        if "authorization" in headers:
            headers["authorization"] = "[REDACTED]"
        
        # Registra informações da requisição
        logger.error(
            f"Error processing request: {method} {url} from {client_host}",
            extra={
                "request_info": {
                    "method": method,
                    "url": url,
                    "client_ip": client_host,
                    "headers": headers
                },
                "error": str(exc)
            }
        )

def register_error_handlers(app):
    """
    Registra manipuladores de erro com a aplicação FastAPI.
    
    Esta função configura a aplicação para usar nosso sistema
    personalizado de tratamento de erros para vários tipos de exceções.
    
    Args:
        app: Instância da aplicação FastAPI
    """
    # Registra manipuladores para tipos específicos de erro
    app.add_exception_handler(
        BaseAPIError,
        lambda request, exc: APIErrorHandler.handle_exception(exc)
    )
    app.add_exception_handler(
        HTTPException,
        lambda request, exc: APIErrorHandler.handle_exception(exc)
    )
    app.add_exception_handler(
        Exception,
        lambda request, exc: APIErrorHandler.handle_exception(exc)
    )
    
    # Middleware para logging de erros
    @app.middleware("http")
    async def error_logging_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            await APIErrorHandler.log_request_info(request, exc)
            raise  # Re-lança a exceção para ser tratada pelos manipuladores