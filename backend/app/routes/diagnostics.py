"""Rotas de diagnóstico para depuração do ambiente Docker.

Este módulo fornece endpoints para verificar a configuração do ambiente
e ajudar na depuração de problemas em produção.
"""

from fastapi import APIRouter, Request
import os
import socket
import logging
import platform
import sys

router = APIRouter()
logger = logging.getLogger("api.diagnostics")

@router.get("/")
async def get_diagnostics(request: Request):
    """Retorna informações de diagnóstico sobre o ambiente."""
    logger.info(f"[DOCKER-DEBUG] Acessando endpoint de diagnóstico")
    
    # Informações do sistema
    system_info = {
        "python_version": sys.version,
        "platform": platform.platform(),
        "hostname": socket.gethostname(),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "app_host": os.getenv("APP_HOST", "127.0.0.1"),
        "app_port": os.getenv("APP_PORT", "8000"),
    }
    
    # Informações da requisição
    request_info = {
        "method": request.method,
        "url": str(request.url),
        "base_url": str(request.base_url),
        "headers": dict(request.headers),
        "client": {
            "host": request.client.host if request.client else "N/A",
            "port": request.client.port if request.client else "N/A"
        }
    }
    
    # Informações de rede
    network_info = {}
    try:
        # Tenta obter todas as interfaces de rede
        hostname = socket.gethostname()
        network_info["hostname"] = hostname
        network_info["ip"] = socket.gethostbyname(hostname)
        
        # Tenta resolver o nome do host da API
        api_host = "apirest.mibitech.com.br"
        try:
            network_info["api_host_ip"] = socket.gethostbyname(api_host)
            network_info["api_host_resolved"] = True
        except socket.gaierror:
            network_info["api_host_resolved"] = False
    except Exception as e:
        network_info["error"] = str(e)
    
    # Variáveis de ambiente relevantes
    env_vars = {}
    for key in os.environ:
        if any(x in key.lower() for x in ["app", "host", "port", "env", "database", "cors", "proxy", "forward"]):
            env_vars[key] = os.environ[key]
    
    # Informações de proxy/Traefik
    proxy_info = {}
    for header, value in request.headers.items():
        if any(x in header.lower() for x in ["forwarded", "proxy", "origin", "referer", "host"]):
            proxy_info[header] = value
    
    return {
        "system": system_info,
        "request": request_info,
        "network": network_info,
        "environment": env_vars,
        "proxy": proxy_info
    }

@router.get("/routes")
async def get_routes_info(request: Request):
    """Retorna informações sobre as rotas configuradas na aplicação."""
    from fastapi import FastAPI
    app = request.app
    
    routes_info = []
    for route in app.routes:
        route_info = {
            "path": getattr(route, "path", "N/A"),
            "name": getattr(route, "name", "N/A"),
            "methods": getattr(route, "methods", []),
            "endpoint": str(getattr(route, "endpoint", "N/A")),
        }
        routes_info.append(route_info)
    
    return {
        "base_url": str(request.base_url),
        "routes": routes_info
    }

@router.get("/traefik")
async def get_traefik_info(request: Request):
    """Retorna informações específicas sobre a configuração do Traefik."""
    logger.info(f"[DOCKER-DEBUG] Verificando configuração do Traefik")
    
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
        "x_forwarded_for": request.headers.get("x-forwarded-for", "N/A"),
        "host": request.headers.get("host", "N/A"),
    }
    
    # Tenta construir URLs de documentação com base nos cabeçalhos
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
    
    return {
        "traefik_headers": traefik_info,
        "all_proxy_headers": proxy_headers,
        "docs_urls": docs_urls,
        "request_url": str(request.url),
        "base_url": base_url,
    }