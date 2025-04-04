# Guia para Executar o Docker Compose com Traefik (Configuração Isolada)

Este guia explica como executar o arquivo `docker-compose.yml` do projeto site_mibitech, que utiliza o Traefik como proxy reverso em uma configuração isolada que não interfere com outros sites no servidor.

## Pré-requisitos

Antes de executar o Docker Compose, certifique-se de que você tem:

1. **Docker instalado** - [Instruções de instalação do Docker](https://docs.docker.com/get-docker/)
2. **Docker Compose instalado** - [Instruções de instalação do Docker Compose](https://docs.docker.com/compose/install/)
3. **Todos os arquivos do projeto** - Certifique-se de que você tem todos os diretórios e arquivos necessários:
   - Diretório `backend/` com seu Dockerfile e código
   - Diretório `frontend/` com seu Dockerfile e código
   - Diretório `traefik/` com o arquivo de configuração `traefik.yml`
   - Arquivo `docker-compose.yml` na raiz do projeto

## Passos para Executar

### 1. Parar Serviços Locais (se necessário)

Se você estiver executando serviços localmente que usam as mesmas portas, pare-os:
- Porto 80 (HTTP - Traefik)
- Porto 443 (HTTPS - Traefik)
- Porto 8080 (Dashboard do Traefik)

### 2. Usando os Scripts de Deploy (Recomendado)

O projeto inclui scripts de deploy que facilitam o uso do Docker Compose:

#### No Windows:

```bash
# Construir e iniciar todos os contêineres
deploy.bat --build --up

# OU para construir e iniciar contêineres específicos
deploy.bat --frontend --build --up
deploy.bat --backend --build --up
deploy.bat --traefik --build --up
```

#### No Linux/Mac:

```bash
# Tornar o script executável (se necessário)
chmod +x deploy.sh

# Construir e iniciar todos os contêineres
./deploy.sh --build --up

# OU para construir e iniciar contêineres específicos
./deploy.sh --frontend --build --up
./deploy.sh --backend --build --up
./deploy.sh --traefik --build --up
```

### 3. Usando Docker Compose Diretamente

Se preferir, você pode usar os comandos do Docker Compose diretamente:

```bash
# Construir as imagens
docker-compose build

# Iniciar os contêineres em segundo plano
docker-compose up -d

# Verificar o status dos contêineres
docker-compose ps

# Ver logs
docker-compose logs -f
```

## Configuração Isolada

Esta configuração foi projetada para ser completamente independente e não interferir com outros sites ou serviços Docker que possam estar rodando no servidor:

1. **Rede Docker isolada**: Todos os serviços usam uma rede Docker dedicada chamada `mibitech-internal-network`
2. **Portas não padrão**: O Traefik usa portas não padrão para evitar conflitos:
   - Porta 8081 para HTTP (em vez da porta 80)
   - Porta 8443 para HTTPS (em vez da porta 443)
   - Porta 8082 para o Dashboard (em vez da porta 8080)
3. **Nomes de contêineres específicos**: Todos os contêineres têm o prefixo `mibitech-` para evitar conflitos de nomes
4. **Configuração Traefik isolada**: O Traefik está configurado para não expor automaticamente todos os contêineres

## Verificando a Instalação

Após iniciar os contêineres, você pode acessar:

- Frontend: http://site.mibitech.com.br:8081/
- Backend API: http://site.mibitech.com.br:8081/api/
- Admin do Django: http://site.mibitech.com.br:8081/admin/
- Dashboard do Traefik: http://localhost:8082/ (para monitoramento)

### Configurando o Host Local

Para acessar o site usando o domínio `site.mibitech.com.br` localmente, você precisa adicionar uma entrada no arquivo hosts do seu sistema:

#### No Windows:
1. Abra o Bloco de Notas como administrador
2. Abra o arquivo `C:\Windows\System32\drivers\etc\hosts`
3. Adicione a seguinte linha:
   ```
   127.0.0.1 site.mibitech.com.br
   ```
4. Salve o arquivo

#### No Linux/Mac:
1. Abra um terminal
2. Execute o comando:
   ```bash
   sudo nano /etc/hosts
   ```
3. Adicione a seguinte linha:
   ```
   127.0.0.1 site.mibitech.com.br
   ```
4. Salve o arquivo (Ctrl+O, Enter, Ctrl+X)

Após essa configuração, você poderá acessar o site usando o domínio `site.mibitech.com.br` no seu navegador.

## Parando os Contêineres

Quando terminar, você pode parar os contêineres:

#### Usando os scripts:

```bash
# Windows
deploy.bat --down

# Linux/Mac
./deploy.sh --down
```

#### Ou diretamente:

```bash
docker-compose down
```

## Solução de Problemas

### Portas em Uso

Se você receber um erro indicando que as portas já estão em uso:

```bash
# Verifique quais processos estão usando as portas
# Windows (PowerShell)
netstat -ano | findstr :8081
netstat -ano | findstr :8443
netstat -ano | findstr :8082

# Linux/Mac
lsof -i :8081
lsof -i :8443
lsof -i :8082
```

### Problemas de Permissão

Se encontrar problemas de permissão ao executar o Docker:

```bash
# No Linux, adicione seu usuário ao grupo docker
sudo usermod -aG docker $USER
# Faça logout e login novamente para aplicar as alterações
```

### Verificando Logs para Depuração

```bash
# Ver logs de todos os contêineres
docker-compose logs -f

# Ver logs de um contêiner específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
```

## Coexistência com Outros Sites

Esta configuração permite que o site MibiTech coexista com outros sites no mesmo servidor:

1. **Sem conflito de portas**: Como estamos usando portas não padrão, não haverá conflito com outros serviços que usam as portas padrão 80/443
2. **Rede isolada**: A rede Docker isolada garante que não haja interferência com outros contêineres
3. **Configuração independente**: O Traefik está configurado para gerenciar apenas os serviços deste projeto

### Configuração em Produção

Para um ambiente de produção, você pode:

1. **Usar um subdomínio**: Configure o DNS para apontar um subdomínio específico (como mibitech.seudominio.com) para o IP do servidor
2. **Configurar um proxy reverso externo**: Use o Nginx ou Apache existente no servidor para encaminhar solicitações para as portas do Traefik
3. **Configurar regras de firewall**: Certifique-se de que as portas 8081, 8443 e 8082 estão abertas no firewall

### Exemplo de Configuração Nginx para Proxy Reverso

Se você já tem o Nginx rodando no servidor para outros sites, pode adicionar esta configuração:

```nginx
server {
    listen 80;
    server_name site.mibitech.com.br;

    location / {
        proxy_pass http://localhost:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Conclusão

Seguindo estes passos, você conseguirá executar o projeto site_mibitech de forma isolada, sem interferir com outros sites ou serviços no servidor.

## Sobre o Traefik

O Traefik é um proxy reverso e balanceador de carga moderno que facilita a implantação de microsserviços. Algumas vantagens do Traefik:

1. **Descoberta de serviço automática**: O Traefik detecta automaticamente seus serviços e cria as rotas apropriadas.
2. **Suporte a SSL/TLS**: Facilita a configuração de HTTPS com Let's Encrypt.
3. **Dashboard web**: Interface visual para monitorar seus serviços.
4. **Configuração dinâmica**: Não é necessário reiniciar para aplicar alterações de configuração.

Para mais informações, consulte a [documentação oficial do Traefik](https://doc.traefik.io/).