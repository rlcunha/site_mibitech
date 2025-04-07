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

from .routes import social_media, webhooks, contact
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

# Configuração CORS
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
        
        # Valida usando o processador de dados
        processor = DataProcessor()
        if not processor.validate(status_data):
            raise ValueError("Dados de status inválidos")
            
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