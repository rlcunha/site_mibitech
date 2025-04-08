#!/usr/bin/env python
"""
Script para testar o endpoint mensagem da API.

Este script faz requisições para o endpoint de mensagens
para verificar seu funcionamento correto.
"""
import os
import sys
import requests
import logging
from typing import Dict, Any, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_mensagem")

# Configuração
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def make_request(endpoint: str, method: str = "POST", data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Faz uma requisição HTTP para o endpoint cli-mensagem.
    """
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        else:
            logger.error(f"Método {method} não suportado")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição: {str(e)}")
        return None

def test_create_valid_message() -> bool:
    """
    Testa a criação de uma mensagem válida.
    """
    logger.info("Testando criação de mensagem válida...")
    
    message_data = {
        "snome": "João Silva",
        "semail": "joao@exemplo.com",
        "stelefone": "11999999999",
        "sassunto": "Dúvida sobre produto",
        "smensagem": "Gostaria de mais informações sobre o produto X"
    }
    
    response = make_request("/api/v1/mensagem/", data=message_data)
    
    if not response:
        return False
        
    if all(key in response for key in message_data.keys()):
        logger.info("✓ Mensagem criada com sucesso")
        return True
        
    logger.error("✗ Falha ao criar mensagem")
    return False

def test_required_fields() -> bool:
    """
    Testa a validação de campos obrigatórios.
    """
    logger.info("Testando campos obrigatórios...")
    
    # Testa sem nenhum campo
    response = make_request("/api/v1/mensagem/", data={})
    
    if response is None:  # Esperamos um erro 422
        logger.info("✓ Validação de campos obrigatórios funcionando")
        return True
        
    logger.error("✗ Validação de campos obrigatórios falhou")
    return False

def test_field_validation() -> bool:
    """
    Testa a validação de formatos dos campos.
    """
    logger.info("Testando validação de formatos...")
    
    invalid_data = {
        "snome": "A",  # Muito curto
        "semail": "email-invalido",
        "stelefone": "123",  # Inválido
        "sassunto": "A" * 31,  # Muito longo
        "smensagem": "A" * 401  # Muito longo
    }
    
    response = make_request("/api/v1/mensagem/", data=invalid_data)
    
    if response is None:  # Esperamos um erro 422
        logger.info("✓ Validação de formatos funcionando")
        return True
        
    logger.error("✗ Validação de formatos falhou")
    return False

def main() -> int:
    """
    Função principal que executa todos os testes.
    """
    logger.info("Iniciando testes do endpoint mensagem...")
    
    tests = [
        test_create_valid_message,
        test_required_fields,
        test_field_validation
    ]
    
    success_count = 0
    for test in tests:
        if test():
            success_count += 1
    
    logger.info(f"Resultado: {success_count}/{len(tests)} testes passaram")
    
    return 0 if success_count == len(tests) else 1

if __name__ == "__main__":
    sys.exit(main())