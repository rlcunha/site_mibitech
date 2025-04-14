"""Rotas de diagnóstico específicas para a documentação da API.

Este módulo fornece endpoints para verificar a configuração da documentação
e ajudar na depuração de problemas de acesso à documentação da API.
"""

from fastapi import APIRouter, Request
import logging
import os

router = APIRouter()
logger = logging.getLogger("api.diagnostics.docs")

@router.get("/docs")
async def get_docs_diagnostics(request: Request):
    """Retorna informações de diagnóstico específicas para a documentação da API."""
    logger.info(f"[DOCS-DEBUG] Acessando endpoint de diagnóstico de documentação")
    
    # Obtém a aplicação FastAPI
    app = request.app
    
    # Informações da aplicação
    app_info = {
        "title": app.title,
        "description": app.description,
        "version": app.version,
        "docs_url": app.docs_url,
        "redoc_url": app.redoc_url,
        "openapi_url": app.openapi_url,
    }
    
    # Informações da requisição
    request_info = {
        "method": request.method,
        "url": str(request.url),
        "base_url": str(request.base_url),
        "headers": dict(request.headers),
    }
    
    # Informações de cabeçalhos de proxy
    proxy_headers = {}
    for header, value in request.headers.items():
        if any(x in header.lower() for x in ["forwarded", "proxy", "origin", "host"]):
            proxy_headers[header] = value
    
    # Verifica cabeçalhos específicos do Traefik
    traefik_info = {
        "x_forwarded_host": request.headers.get("x-forwarded-host", "N/A"),
        "x_forwarded_proto": request.headers.get("x-forwarded-proto", "N/A"),
        "x_forwarded_prefix": request.headers.get("x-forwarded-prefix", "N/A"),
        "host": request.headers.get("host", "N/A"),
    }
    
    # Constrói URLs de documentação com base nos cabeçalhos
    base_url = str(request.base_url)
    docs_urls = {
        "docs_url": f"{base_url}api/v1/docs",
        "redoc_url": f"{base_url}api/v1/redoc",
        "openapi_url": f"{base_url}api/v1/openapi.json",
    }
    
    # Se temos um X-Forwarded-Host, construímos URLs alternativas
    if traefik_info["x_forwarded_host"] != "N/A":
        proto = traefik_info["x_forwarded_proto"] if traefik_info["x_forwarded_proto"] != "N/A" else "https"
        prefix = traefik_info["x_forwarded_prefix"] if traefik_info["x_forwarded_prefix"] != "N/A" else ""
        
        alt_base = f"{proto}://{traefik_info['x_forwarded_host']}{prefix}/"
        docs_urls["alt_docs_url"] = f"{alt_base}api/v1/docs"
        docs_urls["alt_redoc_url"] = f"{alt_base}api/v1/redoc"
        docs_urls["alt_openapi_url"] = f"{alt_base}api/v1/openapi.json"
    
    # Verifica se as rotas de documentação estão registradas
    routes_info = []
    for route in app.routes:
        path = getattr(route, "path", "N/A")
        if "/api/v1/docs" in path or "/api/v1/redoc" in path or "/api/v1/openapi.json" in path:
            route_info = {
                "path": path,
                "name": getattr(route, "name", "N/A"),
                "methods": getattr(route, "methods", []),
                "endpoint": str(getattr(route, "endpoint", "N/A")),
            }
            routes_info.append(route_info)
    
    # Sugestões de solução
    suggestions = [
        "Verifique se o cabeçalho X-Forwarded-Prefix está configurado corretamente no Traefik",
        "Certifique-se de que o Traefik está roteando corretamente as requisições para /api/v1/docs",
        "Verifique se as rotas de documentação estão registradas na aplicação FastAPI",
        "Verifique se o middleware de CORS está configurado corretamente",
        "Verifique se o middleware de remoção de prefixo está configurado corretamente",
    ]
    
    return {
        "app": app_info,
        "request": request_info,
        "traefik": traefik_info,
        "proxy_headers": proxy_headers,
        "docs_urls": docs_urls,
        "docs_routes": routes_info,
        "suggestions": suggestions,
        "environment": os.getenv("ENVIRONMENT", "development"),
    }