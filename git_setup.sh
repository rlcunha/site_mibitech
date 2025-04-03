#!/bin/bash

# Script para inicializar o repositório Git e fazer push para o GitHub
# Repositório: rlcunha

echo "=== Configurando o repositório Git para o projeto ==="

# Inicializar o repositório Git
git init

# Adicionar todos os arquivos ao repositório
git add .

# Fazer o commit inicial
git commit -m "Versão inicial da aplicação Django com Docker Swarm e Nginx"

# Configurar o repositório remoto (GitHub)
# Substitua 'seu-usuario' pelo seu nome de usuário do GitHub
echo "Digite seu nome de usuário do GitHub:"
read github_user

git remote add origin https://github.com/$github_user/rlcunha.git

# Configurar a branch principal como 'main'
git branch -M main

# Fazer push para o repositório remoto
echo "Fazendo push para o repositório remoto..."
git push -u origin main

echo "=== Configuração do Git concluída! ==="
echo "Repositório: https://github.com/$github_user/rlcunha"
echo ""
echo "Se você encontrou algum erro de autenticação, pode ser necessário:"
echo "1. Criar um token de acesso pessoal no GitHub (Settings > Developer settings > Personal access tokens)"
echo "2. Usar o token como senha ao fazer o push"
echo ""
echo "Ou configurar o SSH para o GitHub:"
echo "1. Gerar uma chave SSH: ssh-keygen -t ed25519 -C 'seu-email@exemplo.com'"
echo "2. Adicionar a chave ao GitHub (Settings > SSH and GPG keys)"
echo "3. Configurar o repositório remoto com SSH: git remote set-url origin git@github.com:$github_user/rlcunha.git"