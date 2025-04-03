# Aplicação Django com Docker Swarm e Nginx

Esta é uma aplicação Django simples "Hello World" configurada para ser implantada usando Docker Swarm e Nginx. A stack foi projetada para ser implantada via Portainer em um servidor Ubuntu 24.04.

## Estrutura do Projeto

```
.
├── app/                    # Aplicação Django
│   ├── django_app/         # Projeto Django
│   ├── Dockerfile          # Dockerfile para a aplicação Django
│   └── requirements.txt    # Dependências Python
├── nginx/                  # Configuração do Nginx
│   ├── Dockerfile          # Dockerfile para o Nginx
│   └── nginx.conf          # Arquivo de configuração do Nginx
├── traefik/                # Configuração do Traefik (referência apenas)
│   └── traefik.yml         # Arquivo de configuração do Traefik
└── docker-stack.yml        # Arquivo de stack do Docker Swarm
```

## Pré-requisitos

- Docker e Docker Swarm inicializados no Ubuntu 24.04
- Portainer instalado
- Traefik já configurado e em execução
- Rede `network_public` já criada

## Instruções de Implantação

### 1. Criar os volumes externos necessários

```bash
docker volume create django_app_data
docker volume create nginx_data
```

### 2. Construir as imagens Docker

```bash
# Na pasta raiz do projeto
docker build -t django_app:latest ./app
docker build -t nginx_app:latest ./nginx
```

### 3. Implantar a stack via Portainer

1. Faça login na sua instância do Portainer
2. Navegue até Stacks
3. Clique em "Adicionar stack"
4. Faça upload do arquivo `docker-stack.yml` ou cole seu conteúdo
5. Nomeie sua stack (ex: "django-nginx")
6. Clique em "Implantar a stack"

### 4. Acessar a aplicação

- Aplicação Django: https://appteste.mibitech.com.br
- Proxy Nginx: https://nginx-appteste.mibitech.com.br

## Configuração

### Escalando os serviços

Você pode escalar os serviços alterando o valor de `replicas` no arquivo `docker-stack.yml` ou através da interface do Portainer.

### Nomes de domínio personalizados

Para usar nomes de domínio personalizados, atualize as regras `Host` nas labels `traefik` no arquivo `docker-stack.yml`.

## Solução de Problemas

- Verifique os logs de cada serviço no Portainer
- Certifique-se de que todos os volumes foram criados corretamente
- Verifique se a rede `network_public` existe e está configurada corretamente
- Confirme que o Traefik está configurado para usar o resolver Let's Encrypt

## Considerações de Segurança

Para uso em produção:
- Substitua a chave secreta do Django
- Configure HTTPS com certificados adequados (já configurado via Traefik)
- Proteja os endpoints com autenticação quando necessário

## Subir para o GitHub

Para subir este projeto para o repositório GitHub "rlcunha", siga estas etapas:

### No Windows:

1. Instale o Git para Windows se ainda não tiver: https://git-scm.com/download/win
2. Abra o Git Bash ou o PowerShell na pasta do projeto
3. Execute os seguintes comandos:

```bash
# Inicializar o repositório Git
git init

# Adicionar todos os arquivos ao repositório
git add .

# Fazer o commit inicial
git commit -m "Versão inicial da aplicação Django com Docker Swarm e Nginx"

# Configurar o repositório remoto (substitua 'seu-usuario' pelo seu nome de usuário do GitHub)
git remote add origin https://github.com/seu-usuario/rlcunha.git

# Configurar a branch principal como 'main'
git branch -M main

# Fazer push para o repositório remoto
git push -u origin main
```

### No Linux/Mac:

1. Torne o script git_setup.sh executável:
```bash
chmod +x git_setup.sh
```

2. Execute o script:
```bash
./git_setup.sh
```

3. Siga as instruções na tela para completar o processo.

## Tutorial para Iniciantes

Se você é iniciante, consulte o arquivo `TUTORIAL_SIMPLES.md` para instruções passo a passo sobre como implantar esta aplicação em uma VPS.