\"""
Middlewares personalizados para a aplicação FastAPI.

Este módulo contém middlewares adicionais para lidar com requisições HTTP.
"""

import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import traceback

# Configuração de logging
logger = logging.getLogger("api.middleware")

class InvalidRequestMiddleware(BaseHTTPMiddleware):
    """
    Middleware para capturar e registrar detalhes sobre requisições HTTP inválidas.
    
    Este middleware tenta capturar requisições malformadas antes que elas causem
    erros no processamento normal da aplicação.
    """
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Processa a requisição e captura detalhes sobre requisições inválidas.
        
        Args:
            request: Objeto de requisição
            call_next: Próxima função na cadeia de middleware
            
        Returns:
            Resposta da requisição
        """
        try:
            # Tenta processar a requisição normalmente
            response = await call_next(request)
            return response
            
        except Exception as e:
            # Captura e registra detalhes sobre a exceção
            logger.error(f"[INVALID-REQUEST] Exceção capturada: {str(e)}")

            # Registra informações detalhadas sobre a requisição
            try:
                logger.error(f"[INVALID-REQUEST] Método: {request.method}")

                logger.error(f"[INVALID-REQUEST] URL: {request.url}")

                logger.error(f"[INVALID-REQUEST] Headers: {dict(request.headers)}")

                logger.error(f"[INVALID-REQUEST] Client: {request.client.host}:{request.client.port if request.client else 'N/A'}")

                
                # Tenta capturar o corpo da requisição
                try:
                    body = await request.body()

                    if body:

                        try:

                            body_text = body.decode('utf-8')

                            logger.error(f"[INVALID-REQUEST] Corpo: {body_text[:1000]}" + 

                                       ("..." if len(body_text) > 1000 else ""))

                        except UnicodeDecodeError:

                            logger.error(f"[INVALID-REQUEST] Corpo (binário): {len(body)} bytes")

                except Exception as body_error:

                    logger.error(f"[INVALID-REQUEST] Erro ao capturar corpo: {str(body_error)}")

            except Exception as info_error:

                logger.error(f"[INVALID-REQUEST] Erro ao capturar informações da requisição: {str(info_error)}")

            
            # Registra a stack trace completa
            logger.error(f"[INVALID-REQUEST] Stack trace: {traceback.format_exc()}")

            
            # Propaga a exceção para ser tratada pelos manipuladores de erro da aplicação
            raise e