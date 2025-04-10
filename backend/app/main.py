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

# Adiciona rotas alternativas para documentação
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.responses import HTMLResponse

@app.get("/api/v1/docs", include_in_schema=False)
async def get_alternative_docs():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/api/v1/docs/swagger-ui-bundle.js",
        swagger_css_url="/api/v1/docs/swagger-ui.css",
    )

@app.get("/api/v1/redoc", include_in_schema=False)
async def get_alternative_redoc():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="/api/v1/docs/redoc.standalone.js",
    )

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
    # Registra início da requisição
    logger.info(f"Requisição iniciada: {request.method} {request.url.path}")
    
    # Processa a requisição
    response = await call_next(request)
    
    # Calcula duração
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    
    # Registra conclusão
    logger.info(
        f"Requisição concluída: {request.method} {request.url.path} "
        f"(Status: {response.status_code}, Tempo: {process_time:.2f}ms)"
    )
    
    return response

# Registra manipuladores de erro
register_error_handlers(app)

# Inclui rotas
app.include_router(social_media.router, prefix="/api/v1/social-media", tags=["social-media"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])
# app.include_router(contact.router, prefix="/api", tags=["contact"])
app.include_router(mensagem_router)
app.include_router(nossocontato_router)

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