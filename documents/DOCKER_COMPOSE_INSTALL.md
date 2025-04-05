# Guia de Instalação do Docker Compose

Este guia fornece instruções detalhadas para instalar o Docker Compose em diferentes sistemas operacionais.

## Instalação no Ubuntu/Debian

### Método 1: Usando o Gerenciador de Pacotes

```bash
# Atualizar os repositórios
sudo apt update

# Instalar o plugin Docker Compose
sudo apt install docker-compose-plugin
```

### Método 2: Instalação Manual

```bash
# Baixar o Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Tornar o binário executável
sudo chmod +x /usr/local/bin/docker-compose

# Verificar a instalação
docker-compose --version
```

## Instalação no CentOS/RHEL

```bash
# Instalar o plugin Docker Compose
sudo yum install docker-compose-plugin

# OU para instalação manual
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Instalação no Docker Swarm

Se você estiver usando o Docker Swarm, o Docker Compose pode não estar disponível por padrão. Você pode instalar o Docker Compose em cada nó do Swarm ou usar o comando `docker stack deploy` com um arquivo docker-compose.yml.

### Instalação em Cada Nó

Instale o Docker Compose em cada nó do Swarm usando um dos métodos acima.

### Usando Docker Stack Deploy

Para usar o Docker Compose com Swarm, você pode converter seu arquivo docker-compose.yml para um formato compatível com Swarm:

```bash
# Converter docker-compose.yml para formato de stack
docker-compose config > docker-stack.yml

# Implantar o stack
docker stack deploy -c docker-stack.yml mibitech
```

## Verificando a Instalação

Após a instalação, verifique se o Docker Compose está funcionando corretamente:

```bash
# Para versões mais antigas
docker-compose --version

# Para versões mais recentes (Docker Compose V2)
docker compose version
```

## Solução de Problemas

### Comando não encontrado

Se você receber o erro "command not found" após a instalação:

1. Verifique se o binário está no PATH:
   ```bash
   echo $PATH
   ```

2. Crie um link simbólico para um diretório no PATH:
   ```bash
   sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
   ```

### Permissões Insuficientes

Se você receber erros de permissão:

```bash
# Certifique-se de que o usuário está no grupo docker
sudo usermod -aG docker $USER

# Faça logout e login novamente para aplicar as alterações
# Ou execute
newgrp docker
```

## Usando o Script deploy.sh Atualizado

O script `deploy.sh` foi atualizado para verificar automaticamente se o Docker Compose está instalado e fornecer instruções de instalação se necessário. Ele também suporta tanto o comando `docker-compose` (versões mais antigas) quanto o comando `docker compose` (versões mais recentes).

Para usar o script atualizado:

1. Baixe a versão mais recente do repositório:
   ```bash
   git pull origin main
   ```

2. Torne o script executável:
   ```bash
   chmod +x deploy.sh
   ```

3. Execute o script:
   ```bash
   ./deploy.sh --build --up
   ```

O script verificará automaticamente se o Docker Compose está instalado e fornecerá instruções se não estiver.