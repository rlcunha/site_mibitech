#!/bin/bash

# Script de implantação para a aplicação Django com Docker Swarm e Nginx
# Para uso em Ubuntu 24.04

echo "=== Iniciando implantação da aplicação Django com Docker Swarm e Nginx ==="

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se o Docker Swarm está inicializado
if ! docker info | grep -q "Swarm: active"; then
    echo "Docker Swarm não está ativo. Inicializando..."
    docker swarm init
else
    echo "Docker Swarm já está ativo."
fi

# Verificar se a rede network_public existe
if ! docker network ls | grep -q "network_public"; then
    echo "Criando rede network_public..."
    docker network create --driver=overlay --attachable network_public
else
    echo "Rede network_public já existe."
fi

# Criar volumes externos
echo "Criando volumes externos..."
docker volume create django_app_data
docker volume create nginx_data

# Construir imagens Docker
echo "Construindo imagens Docker..."
docker build -t django_app:latest ./app
docker build -t nginx_app:latest ./nginx

# Implantar a stack
echo "Implantando a stack via Docker Swarm..."
docker stack deploy -c docker-stack.yml django-app

echo "=== Implantação concluída! ==="
echo "Aplicação Django: https://appteste.mibitech.com.br"
echo "Proxy Nginx: https://nginx-appteste.mibitech.com.br"
echo ""
echo "Para verificar o status dos serviços, execute: docker service ls"
echo "Para visualizar logs, execute: docker service logs <service_name>"