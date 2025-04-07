#!/bin/bash
# Script para construir a imagem Docker para o backend

echo "==================================================="
echo "CONSTRUINDO IMAGEM DOCKER PARA BACKEND MIBITECH"
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

# Constrói a imagem Docker
echo "[INFO] Construindo a imagem Docker..."
docker build -t mibitech-backend:latest -f Dockerfile .

if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao construir a imagem Docker."
    exit 1
fi

echo "[INFO] Imagem Docker construída com sucesso!"
echo
echo "[INFO] Detalhes da imagem:"
docker images | grep mibitech-backend

echo
echo "==================================================="
echo "IMAGEM DOCKER CONSTRUÍDA COM SUCESSO!"
echo "==================================================="
echo
echo "Para executar a imagem: docker run -p 8000:8000 mibitech-backend:latest"
echo