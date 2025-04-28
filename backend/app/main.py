"""
Aplicação principal FastAPI.

Este módulo configura a aplicação FastAPI, incluindo middlewares,
rotas e manipuladores de erro.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
import os
from datetime import datetime

from .routes import social_media, webhooks
from .routes.mensagem.routes import router as mensagem_router
from .routes.nossocontato.routes import router as nossocontato_router
from .errors import register_error_handlers, BaseAPIError
from .helpers import DataProcessor, DateTimeProcessor

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("api.main")

# Configuração da aplicação
app = FastAPI(
    title="MibiTech Backend API",
    description="API backend para o website da MibiTech",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

# Log de configuração da aplicação no startup
logger.info(f"[DOCKER-DEBUG] Iniciando aplicação FastAPI")
logger.info(f"[DOCKER-DEBUG] Ambiente: {os.getenv('ENVIRONMENT', 'development')}")
logger.info(f"[DOCKER-DEBUG] Host: {os.getenv('APP_HOST', '127.0.0.1')}")
logger.info(f"[DOCKER-DEBUG] Porta: {os.getenv('APP_PORT', '8000')}")
logger.info(f"[DOCKER-DEBUG] docs_url: {app.docs_url}")
logger.info(f"[DOCKER-DEBUG] redoc_url: {app.redoc_url}")
logger.info(f"[DOCKER-DEBUG] openapi_url: {app.openapi_url}")

# Adiciona rotas alternativas para documentação
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.responses import HTMLResponse

@app.get("/api/v1/docs", include_in_schema=False)
async def get_alternative_docs():
    logger.info(f"[DEBUG-404] Acessando documentação Swagger UI")
    logger.info(f"[DEBUG-404] OpenAPI URL: {app.openapi_url}")
    logger.info(f"[DEBUG-404] OAuth2 Redirect URL: {app.swagger_ui_oauth2_redirect_url}")
    
    try:
        # Usando URLs absolutas do CDN para evitar problemas de roteamento
        docs = get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
        )
        logger.info(f"[DEBUG-404] Documentação Swagger UI gerada com sucesso")
        return docs
    except Exception as e:
        logger.error(f"[DEBUG-404] Erro ao gerar documentação Swagger UI: {str(e)}")
        raise e

# Endpoints para servir os arquivos estáticos da documentação Swagger
@app.get("/api/v1/docs/swagger-ui-bundle.js", include_in_schema=False)
async def swagger_ui_bundle():
    logger.info(f"[DEBUG-404] Requisição para arquivo swagger-ui-bundle.js")
    try:
        # Fallback para CDN
        return JSONResponse(
            {"redirect": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"},
            headers={"Location": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"},
            status_code=302
        )
    except Exception as e:
        logger.error(f"[DEBUG-404] Erro ao servir swagger-ui-bundle.js: {str(e)}")
        raise e

@app.get("/api/v1/docs/swagger-ui.css", include_in_schema=False)
async def swagger_ui_css():
    logger.info(f"[DEBUG-404] Requisição para arquivo swagger-ui.css")
    try:
        # Fallback para CDN
        return JSONResponse(
            {"redirect": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css"},
            headers={"Location": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css"},
            status_code=302
        )
    except Exception as e:
        logger.error(f"[DEBUG-404] Erro ao servir swagger-ui.css: {str(e)}")
        raise e

@app.get("/api/v1/docs/redoc.standalone.js", include_in_schema=False)
async def redoc_standalone():
    logger.info(f"[DEBUG-404] Requisição para arquivo redoc.standalone.js")
    try:
        # Fallback para CDN
        return JSONResponse(
            {"redirect": "https://cdn.jsdelivr.net/npm/redoc@2.0.0/bundles/redoc.standalone.js"},
            headers={"Location": "https://cdn.jsdelivr.net/npm/redoc@2.0.0/bundles/redoc.standalone.js"},
            status_code=302
        )
    except Exception as e:
        logger.error(f"[DEBUG-404] Erro ao servir redoc.standalone.js: {str(e)}")
        raise e

@app.get("/api/v1/redoc", include_in_schema=False)
async def get_alternative_redoc():
    logger.info(f"[DEBUG-404] Acessando documentação ReDoc")
    try:
        # Usando URL absoluta do CDN para evitar problemas de roteamento
        docs = get_redoc_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} - ReDoc",
            redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.0.0/bundles/redoc.standalone.js",
        )
        logger.info(f"[DEBUG-404] Documentação ReDoc gerada com sucesso")
        return docs
    except Exception as e:
        logger.error(f"[DEBUG-404] Erro ao gerar documentação ReDoc: {str(e)}")
        raise e

# Importa o middleware personalizado para requisições inválidas
from .middleware import InvalidRequestMiddleware

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://appteste.mibitech.com.br",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://apirest.mibitech.com.br:8000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Accept",
        "Authorization",
        "X-Requested-With",
        "Access-Control-Allow-Origin"
    ],
)

# Adiciona middleware para capturar requisições inválidas
app.add_middleware(InvalidRequestMiddleware)

# Middleware para logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware para registrar informações sobre cada requisição.
    
    Args:
        request: Objeto de requisição
        call_next: Próxima função na cadeia de middleware
        
    Returns:
        Resposta da requisição
    """
    start_time = time.time()
    
    try:
        # Registra informações detalhadas da requisição para debug do erro 404
        logger.info(f"[DEBUG-404] Requisição iniciada: {request.method} {request.url.path}")
        logger.info(f"[DEBUG-404] URL completa: {request.url}")
        logger.info(f"[DEBUG-404] Base URL: {request.base_url}")
        logger.info(f"[DEBUG-404] Headers: {dict(request.headers)}")
        logger.info(f"[DEBUG-404] Client host: {request.client.host if request.client else 'N/A'}")
        logger.info(f"[DEBUG-404] Client port: {request.client.port if request.client else 'N/A'}")
        
        # Log para endpoints de documentação
        if '/api/v1/docs' in request.url.path or '/api/v1/redoc' in request.url.path or '/api/v1/openapi.json' in request.url.path:
            logger.info(f"[DEBUG-404] Tentativa de acesso à documentação: {request.url.path}")
            logger.info(f"[DEBUG-404] Query params: {request.query_params}")
            logger.info(f"[DEBUG-404] Path params: {request.path_params}")
        
        # Tenta capturar o corpo da requisição para requisições não-GET
        if request.method != "GET":
            try:
                body_bytes = await request.body()
                if body_bytes:
                    try:
                        # Tenta decodificar como JSON
                        body_str = body_bytes.decode('utf-8')
                        logger.info(f"[DEBUG-404] Corpo da requisição: {body_str[:500]}" + 
                                   ("..." if len(body_str) > 500 else ""))
                    except UnicodeDecodeError:
                        # Se não for texto, registra como binário
                        logger.info(f"[DEBUG-404] Corpo da requisição (binário): {len(body_bytes)} bytes")
            except Exception as e:
                logger.warning(f"[DEBUG-404] Erro ao capturar corpo da requisição: {str(e)}")
        
        # Processa a requisição
        try:
            response = await call_next(request)
            
            # Calcula duração
            process_time = (time.time() - start_time) * 1000
            response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
            
            # Registra conclusão com informações detalhadas
            logger.info(
                f"[DEBUG-404] Requisição concluída: {request.method} {request.url.path} "
                f"(Status: {response.status_code}, Tempo: {process_time:.2f}ms)"
            )
            
            # Log adicional para respostas 404
            if response.status_code == 404:
                logger.warning(
                    f"[DEBUG-404] ERRO 404 DETECTADO: {request.method} {request.url.path} - "
                    f"Headers: {dict(request.headers)}"
                )
            
            return response
        except Exception as e:
            # Captura exceções durante o processamento da requisição
            logger.error(f"[DEBUG-404] Erro durante processamento da requisição: {str(e)}")
            raise e
            
    except Exception as e:
        # Captura exceções durante o middleware
        logger.error(f"[DEBUG-404] Erro no middleware de logging: {str(e)}")
        # Registra a stack trace para depuração
        import traceback
        logger.error(f"[DEBUG-404] Stack trace: {traceback.format_exc()}")
        
        # Se ocorrer um erro no middleware, ainda precisamos processar a requisição
        try:
            response = await call_next(request)
            return response
        except Exception as inner_e:
            logger.error(f"[DEBUG-404] Erro secundário no middleware: {str(inner_e)}")
            raise inner_e

# Registra manipuladores de erro
register_error_handlers(app)

# Importa rotas de diagnóstico
from .routes import diagnostics

# Inclui rotas
app.include_router(social_media.router, prefix="/api/v1/social-media", tags=["social-media"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])
# app.include_router(contact.router, prefix="/api", tags=["contact"])
app.include_router(mensagem_router)
app.include_router(nossocontato_router)

# Inclui rotas de diagnóstico para ambiente de produção
app.include_router(diagnostics.router, prefix="/api/v1/diagnostics", tags=["diagnostics"])

# Inclui rotas de diagnóstico específicas para documentação
from .routes import diagnostics_docs
app.include_router(diagnostics_docs.router, prefix="/api/v1/diagnostics", tags=["diagnostics"])

@app.get("/api/v1/status")
async def status():
    """
    Endpoint para verificar o status da API.
    
    Útil para health checks e monitoramento.
    
    Returns:
        Informações sobre o status atual da API
    """
    try:
        # Usa o processador de data/hora para formatar timestamp
        dt_processor = DateTimeProcessor()
        current_time = dt_processor.format_datetime(datetime.now())
        
        # Cria dados de status
        status_data = {
            "status": "ok",
            "timestamp": current_time,
            "version": app.version,
            "environment": os.getenv("ENVIRONMENT", "development")
        }
            
        return status_data
        
    except Exception as e:
        logger.error(f"Erro ao obter status: {str(e)}")
        raise BaseAPIError(
            message="Falha ao obter status",
            status_code=500,
            details={"error": str(e)}
        )

@app.get("/")
async def root():
    """
    Endpoint raiz da API.
    
    Redireciona para a documentação.
    
    Returns:
        Mensagem de boas-vindas com links úteis
    """
    return {
        "message": "Bem-vindo à API da MibiTech",
        "documentation": "/api/v1/docs",
        "status": "/api/v1/status"
    }