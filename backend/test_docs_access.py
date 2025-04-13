#!/usr/bin/env python
"""
Script para testar o acesso às rotas de documentação da API.

Este script verifica se as rotas de documentação da API estão acessíveis
e ajuda a diagnosticar problemas de configuração do Traefik.
"""

import requests
import sys
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_docs_access")

def test_endpoint(url, description):
    """Testa um endpoint específico e retorna o resultado."""
    logger.info(f"Testando {description}: {url}")
    try:
        response = requests.get(url, timeout=10)
        status = response.status_code
        logger.info(f"Status: {status}")
        
        if status == 200:
            logger.info(f"✅ {description} está acessível!")
            return True
        else:
            logger.error(f"❌ {description} retornou status {status}")
            logger.info(f"Headers da resposta: {dict(response.headers)}")
            return False
    except Exception as e:
        logger.error(f"❌ Erro ao acessar {description}: {str(e)}")
        return False

def main():
    """Função principal que testa todos os endpoints de documentação."""
    logger.info("Iniciando testes de acesso à documentação da API")
    
    # Configuração de base URLs para teste
    base_urls = [
        "http://localhost:8000",
        "http://apirest.mibitech.com.br",
    ]
    
    # Endpoints a serem testados
    endpoints = [
        "/api/v1/docs",
        "/api/v1/redoc",
        "/api/v1/openapi.json",
        "/api/v1/status",
        "/api/v1/diagnostics",
        "/api/v1/diagnostics/traefik",
    ]
    
    success = True
    
    # Testa cada combinação de base URL e endpoint
    for base_url in base_urls:
        logger.info(f"\nTestando base URL: {base_url}")
        
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            result = test_endpoint(url, f"Endpoint {endpoint}")
            success = success and result
        
        logger.info("-----------------------------------")
    
    # Verifica se todos os testes foram bem-sucedidos
    if success:
        logger.info("✅ Todos os endpoints de documentação estão acessíveis!")
        return 0
    else:
        logger.error("❌ Alguns endpoints de documentação não estão acessíveis.")
        logger.info("""\nSugestões de solução:
1. Verifique se o serviço FastAPI está em execução
2. Verifique a configuração do Traefik no docker-compose.yml
3. Verifique se o cabeçalho X-Forwarded-Prefix está configurado corretamente
4. Verifique os logs do FastAPI e do Traefik para mais detalhes""")
        return 1

if __name__ == "__main__":
    sys.exit(main())