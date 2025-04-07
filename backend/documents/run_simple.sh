#!/bin/bash
# Script para executar o docker-compose com o arquivo simplificado

echo "==================================================="
echo "INICIANDO DOCKER COMPOSE SIMPLIFICADO"
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

# Para e remove os contêineres existentes
echo "[INFO] Parando contêineres existentes..."
docker-compose -f docker-compose.simple.yml down

# Executa o docker-compose
echo "[INFO] Iniciando os contêineres..."
docker-compose -f docker-compose.simple.yml up -d

if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao iniciar os contêineres Docker."
    exit 1
fi

echo "[INFO] Contêineres iniciados com sucesso!"
echo
echo "[INFO] Serviço disponível:"
echo " - API Backend: http://localhost:8000"
echo " - API Docs: http://localhost:8000/api/docs"
echo

echo "[INFO] Aguardando serviço inicializar..."
sleep 10

echo "[INFO] Verificando status dos contêineres:"
docker-compose -f docker-compose.simple.yml ps

echo
echo "==================================================="
echo "DOCKER COMPOSE INICIADO COM SUCESSO!"
echo "==================================================="
echo
echo "Para visualizar logs: docker-compose -f docker-compose.simple.yml logs -f"
echo "Para parar os contêineres: docker-compose -f docker-compose.simple.yml down"
echo