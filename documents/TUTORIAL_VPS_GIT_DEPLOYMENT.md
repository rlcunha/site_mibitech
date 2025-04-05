# Tutorial: Baixando e Instalando o site_mibitech em uma VPS através do Git

Este tutorial explica como baixar o repositório site_mibitech do GitHub e instalá-lo em um servidor VPS.

## Pré-requisitos

- Um servidor VPS com pelo menos 1GB de RAM e 20GB de armazenamento
- Acesso SSH ao servidor VPS
- Conhecimento básico de linha de comando Linux
- O repositório site_mibitech hospedado no GitHub

## Passo 1: Conectar-se ao Servidor VPS

1. Abra um terminal e conecte-se ao seu servidor VPS usando SSH:
   ```bash
   ssh usuario@ip-do-seu-servidor
   ```
   Substitua `usuario` pelo seu nome de usuário no servidor e `ip-do-seu-servidor` pelo endereço IP do seu VPS.

2. Após conectar, atualize os pacotes do sistema:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

## Passo 2: Instalar o Git

1. Instale o Git no servidor:
   ```bash
   sudo apt install git -y
   ```

2. Verifique se o Git foi instalado corretamente:
   ```bash
   git --version
   ```

## Passo 3: Instalar Docker e Docker Compose

O projeto site_mibitech utiliza Docker para facilitar a implantação. Vamos instalar o Docker e o Docker Compose:

1. Instale o Docker usando o script oficial:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

2. Instale o Docker Compose:
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. Adicione seu usuário ao grupo Docker para executar comandos sem sudo:
   ```bash
   sudo usermod -aG docker $USER
   ```

4. Aplique as alterações de grupo (ou faça logout e login novamente):
   ```bash
   newgrp docker
   ```

5. Verifique se o Docker e o Docker Compose foram instalados corretamente:
   ```bash
   docker --version
   docker-compose --version
   ```

## Passo 4: Clonar o Repositório do GitHub

1. Crie um diretório para a aplicação:
   ```bash
   sudo mkdir -p /var/www
   sudo chown $USER:$USER /var/www
   cd /var/www
   ```

2. Clone o repositório do GitHub:
   ```bash
   git clone https://github.com/seu-usuario/site_mibitech.git
   ```
   Substitua `seu-usuario` pelo nome de usuário do GitHub onde o repositório está hospedado.

3. Entre no diretório do projeto:
   ```bash
   cd site_mibitech
   ```

## Passo 5: Configurar o Ambiente

1. Crie um arquivo `.env` para as variáveis de ambiente:
   ```bash
   touch .env
   ```

2. Edite o arquivo `.env` com suas configurações:
   ```bash
   nano .env
   ```

3. Adicione as seguintes variáveis (ajuste conforme necessário):
   ```
   DEBUG=False
   ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com,seu-ip-vps
   SECRET_KEY=sua-chave-secreta
   ```
   Substitua `seu-dominio.com` pelo seu domínio real, `seu-ip-vps` pelo IP do seu servidor e gere uma chave secreta segura.

## Passo 6: Implantar a Aplicação

1. Torne o script de implantação executável:
   ```bash
   chmod +x deploy.sh
   ```

2. Execute o script de implantação para construir e iniciar os contêineres:
   ```bash
   ./deploy.sh --build --up
   ```

3. Verifique se os contêineres estão em execução:
   ```bash
   docker-compose ps
   ```
   Todos os contêineres devem estar no estado "Up".

## Passo 7: Configurar o Firewall

1. Configure o firewall para permitir tráfego HTTP e HTTPS:
   ```bash
   sudo ufw allow OpenSSH
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. Verifique o status do firewall:
   ```bash
   sudo ufw status
   ```

## Passo 8: Configurar o Domínio e SSL (Opcional)

Se você tiver um domínio, siga estes passos para configurá-lo com SSL:

1. Configure os registros DNS no seu provedor de domínio:
   - Adicione um registro A apontando para o IP do seu VPS
   - Adicione um registro CNAME para o subdomínio www

2. Atualize a configuração do Nginx:
   ```bash
   nano nginx/nginx.conf
   ```
   Atualize a diretiva `server_name` com seu domínio:
   ```
   server_name seu-dominio.com www.seu-dominio.com;
   ```

3. Reconstrua e reinicie o contêiner Nginx:
   ```bash
   ./deploy.sh --nginx --build --restart
   ```

4. Instale o Certbot para obter certificados SSL:
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   ```

5. Obtenha o certificado SSL:
   ```bash
   sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
   ```
   Siga as instruções na tela para concluir a configuração SSL.

## Passo 9: Atualizar a Aplicação

Quando houver atualizações no repositório, você pode atualizar facilmente a aplicação:

1. Navegue até o diretório do projeto:
   ```bash
   cd /var/www/site_mibitech
   ```

2. Puxe as alterações mais recentes do GitHub:
   ```bash
   git pull origin main
   ```
   Se o branch principal for "master" em vez de "main", use `git pull origin master`.

3. Reconstrua e reinicie os contêineres:
   ```bash
   ./deploy.sh --build --restart
   ```

## Solução de Problemas

### Contêiner falha ao iniciar

1. Verifique os logs:
   ```bash
   ./deploy.sh --logs
   ```

2. Verifique as variáveis de ambiente no arquivo `.env`.

3. Certifique-se de que as portas não estão sendo usadas por outros serviços.

### Não é possível conectar-se à aplicação

1. Verifique se os contêineres estão em execução:
   ```bash
   docker-compose ps
   ```

2. Verifique as configurações do firewall:
   ```bash
   sudo ufw status
   ```

3. Certifique-se de que as portas corretas estão expostas no arquivo `docker-compose.yml`.

### Problemas com certificado SSL

1. Verifique se as configurações DNS foram propagadas:
   ```bash
   nslookup seu-dominio.com
   ```

2. Verifique os certificados do Certbot:
   ```bash
   sudo certbot certificates
   ```

3. Tente renovar manualmente o certificado:
   ```bash
   sudo certbot renew --dry-run
   ```

## Comandos Úteis

### Reiniciar Serviços

Para reiniciar serviços específicos:
```bash
./deploy.sh --frontend --restart
./deploy.sh --backend --restart
./deploy.sh --nginx --restart
```

Para reiniciar todos os serviços:
```bash
./deploy.sh --restart
```

### Verificar Status dos Contêineres

```bash
docker-compose ps
docker stats
```

### Acessar o Shell de um Contêiner

```bash
docker-compose exec frontend sh
docker-compose exec backend bash
docker-compose exec nginx sh
```

## Conclusão

Agora você tem o site_mibitech implantado em seu servidor VPS, baixado diretamente do GitHub. A aplicação está configurada para ser facilmente atualizada quando houver mudanças no repositório.

Para mais informações sobre o desenvolvimento local, consulte o arquivo `LOCAL_DEVELOPMENT.md`.