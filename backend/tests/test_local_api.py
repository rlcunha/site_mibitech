#!/usr/bin/env python
"""
Script para testar a API do backend localmente.

Este script faz requisições para os endpoints principais da API
rodando localmente via uvicorn.
"""
import requests
import time
import sys
import json
import warnings
import os
from typing import Dict, Any, Optional

# Suprimir avisos de SSL
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Configuração
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MAX_RETRIES = 10
RETRY_INTERVAL = 3  # segundos


def print_colored(text: str, color: str = "white") -> None:
    """
    Imprime texto colorido no terminal.
    
    Args:
        text: Texto a ser imprimido
        color: Cor do texto (red, green, yellow, blue, magenta, cyan, white)
    """
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    
    print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")


def make_request(endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Faz uma requisição HTTP para a API local.
    
    Args:
        endpoint: Endpoint da API (sem a URL base)
        method: Método HTTP (GET, POST, etc.)
        data: Dados para enviar na requisição (para POST, PUT, etc.)
        
    Returns:
        Resposta da API como dicionário ou None em caso de erro
    """
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            print_colored(f"Método {method} não suportado", "red")
            return None
            
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print_colored(f"Erro na requisição para {url}: {str(e)}", "red")
        return None


def wait_for_api() -> bool:
    """
    Aguarda a API local ficar disponível.
    
    Returns:
        True se a API estiver disponível, False caso contrário
    """
    print_colored("Verificando disponibilidade da API local...", "blue")
    
    for attempt in range(1, MAX_RETRIES + 1):
        print_colored(f"Tentativa {attempt}/{MAX_RETRIES}...", "yellow")
        
        try:
            response = requests.get(f"{API_BASE_URL}/api/v1/status", timeout=5)
            if response.status_code == 200:
                print_colored("API local está disponível!", "green")
                return True
        except requests.exceptions.RequestException:
            pass
            
        time.sleep(RETRY_INTERVAL)
    
    print_colored("API local não disponível após várias tentativas", "red")
    return False


def test_status_endpoint() -> bool:
    """
    Testa o endpoint de status da API local.
    
    Returns:
        True se o teste passar, False caso contrário
    """
    print_colored("\nTestando endpoint de status local...", "blue")
    
    response = make_request("/api/v1/status")
    if not response:
        return False
        
    if response.get("status") == "ok":
        print_colored("✓ Endpoint de status local funcionando corretamente", "green")
        print_colored(f"  Versão: {response.get('version')}", "cyan")
        print_colored(f"  Ambiente: {response.get('environment')}", "cyan")
        return True
    else:
        print_colored("✗ Endpoint de status local retornou status diferente de 'ok'", "red")
        return False


def test_docs_endpoint() -> bool:
    """
    Testa o endpoint de documentação da API local.
    
    Returns:
        True se o teste passar, False caso contrário
    """
    print_colored("\nTestando endpoint de documentação local...", "blue")
    
    response = make_request("/api/v1/docs")
    if not response:
        return False
        
    print_colored("✓ Endpoint de documentação local acessível", "green")
    return True


def main() -> int:
    """
    Função principal que executa todos os testes locais.
    
    Returns:
        Código de saída (0 para sucesso, 1 para falha)
    """
    print_colored("=" * 60, "magenta")
    print_colored("TESTE LOCAL DA API BACKEND MIBITECH", "magenta")
    print_colored("=" * 60, "magenta")
    
    if not wait_for_api():
        return 1
        
    tests = [
        test_status_endpoint,
        test_docs_endpoint
    ]
    
    success_count = 0
    for test in tests:
        if test():
            success_count += 1
    
    print_colored("\n" + "=" * 60, "magenta")
    print_colored(f"RESULTADO: {success_count}/{len(tests)} testes locais passaram", 
                 "green" if success_count == len(tests) else "red")
    print_colored("=" * 60, "magenta")
    
    return 0 if success_count == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())