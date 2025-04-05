#!/bin/bash
# Script para iniciar o ambiente Docker do backend MibiTech
# Este script inicia os contêineres Docker e testa a API

echo "==================================================="
echo "INICIANDO AMBIENTE DOCKER PARA BACKEND MIBITECH"
echo "==================================================="

# Verifica se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "[ERRO] Docker não encontrado. Por favor, instale o Docker."
    exit 1
fi

# Verifica se o Docker está rodando
if ! docker info &> /dev/null; then
    echo "[ERRO] Docker não está rodando. Por favor, inicie o serviço Docker."
    exit 1
fi

# Verifica se o Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "[ERRO] Docker Compose não encontrado. Por favor, instale o Docker Compose."
    exit 1
fi

echo "[INFO] Verificando se há contêineres antigos..."
docker-compose down 2>/dev/null

echo "[INFO] Construindo e iniciando os contêineres..."
docker-compose up -d --build

if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao iniciar os contêineres Docker."
    exit 1
fi

echo "[INFO] Contêineres iniciados com sucesso!"
echo
echo "[INFO] Serviços disponíveis:"
echo " - API Backend: http://localhost:8000"
echo " - API Docs: http://localhost:8000/api/docs"
echo " - PgAdmin: http://localhost:5050"
echo

echo "[INFO] Aguardando serviços inicializarem..."
sleep 10

echo "[INFO] Verificando status dos contêineres:"
docker-compose ps

echo
echo "[INFO] Testando a API..."
echo

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[AVISO] Python não encontrado. Pulando teste automatizado."
    echo "[INFO] Você pode testar manualmente acessando http://localhost:8000/api/status"
else
    # Verifica se o módulo requests está instalado
    if ! python3 -c "import requests" &> /dev/null; then
        echo "[INFO] Instalando pacote requests..."
        pip3 install requests || pip install requests
    fi
    
    # Torna o script de teste executável
    chmod +x test_api.py
    
    # Executa o script de teste
    python3 test_api.py || python test_api.py
fi

echo
echo "==================================================="
echo "AMBIENTE DOCKER INICIADO COM SUCESSO!"
echo "==================================================="
echo
echo "Para visualizar logs: docker-compose logs -f"
echo "Para parar os serviços: docker-compose down"
echo