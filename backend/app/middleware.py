"""
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
    
    def __init__(self, app):
        super().__init__(app)
        logger.info(f"[DOCKER-DEBUG] Middleware InvalidRequestMiddleware inicializado")
        # Registra informações do ambiente
        import os
        import socket
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            logger.info(f"[DOCKER-DEBUG] Hostname: {hostname}")
            logger.info(f"[DOCKER-DEBUG] IP: {ip_address}")
            logger.info(f"[DOCKER-DEBUG] Ambiente: {os.getenv('ENVIRONMENT', 'development')}")
            logger.info(f"[DOCKER-DEBUG] APP_HOST: {os.getenv('APP_HOST', '127.0.0.1')}")
            logger.info(f"[DOCKER-DEBUG] APP_PORT: {os.getenv('APP_PORT', '8000')}")
        except Exception as e:
            logger.error(f"[DOCKER-DEBUG] Erro ao obter informações do sistema: {str(e)}")
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Processa a requisição e captura detalhes sobre requisições inválidas.
        
        Args:
            request: Objeto de requisição
            call_next: Próxima função na cadeia de middleware
            
        Returns:
            Resposta da requisição
        """
        # Log adicional para ambiente Docker
        if '/api/v1/docs' in request.url.path or '/api/v1/redoc' in request.url.path or '/api/v1/openapi.json' in request.url.path:
            logger.info(f"[DOCKER-DEBUG] Tentativa de acesso à documentação via middleware: {request.url.path}")
            logger.info(f"[DOCKER-DEBUG] URL completa: {request.url}")
            logger.info(f"[DOCKER-DEBUG] Headers de proxy: {[h for h in request.headers.items() if 'forwarded' in h[0].lower() or 'proxy' in h[0].lower()]}")
            
            # Verifica se há cabeçalhos de proxy que podem estar afetando o roteamento
            x_forwarded_host = request.headers.get('x-forwarded-host')
            x_forwarded_proto = request.headers.get('x-forwarded-proto')
            x_forwarded_prefix = request.headers.get('x-forwarded-prefix')
            
            if x_forwarded_host:
                logger.info(f"[DOCKER-DEBUG] X-Forwarded-Host detectado: {x_forwarded_host}")
            if x_forwarded_proto:
                logger.info(f"[DOCKER-DEBUG] X-Forwarded-Proto detectado: {x_forwarded_proto}")
            if x_forwarded_prefix:
                logger.info(f"[DOCKER-DEBUG] X-Forwarded-Prefix detectado: {x_forwarded_prefix}")
                logger.warning(f"[DOCKER-DEBUG] Prefixo encaminhado pode estar afetando o roteamento da documentação!")
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