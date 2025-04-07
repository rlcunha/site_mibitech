# Guia para Executar o Docker Compose com Traefik (Integração com Infraestrutura Existente)

Este guia explica como executar o arquivo `docker-compose.yml` do projeto site_mibitech, que utiliza o Traefik existente no servidor como proxy reverso, integrando-se com outros sites WordPress.

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
- Porto 80 (HTTP)
- Porto 443 (HTTPS)

### 2. Usando os Scripts de Deploy (Recomendado)

O projeto inclui scripts de deploy que facilitam o uso do Docker Compose:

#### No Windows:

```bash
# Construir e iniciar todos os contêineres
deploy.bat --build --up

# OU para construir e iniciar contêineres específicos
deploy.bat --frontend --build --up
deploy.bat --backend --build --up
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

## Integração com Infraestrutura Existente

Esta configuração foi projetada para integrar-se com a infraestrutura Traefik existente no servidor:

1. **Rede Docker compartilhada**: Os serviços usam a rede Docker existente chamada `network_public`
2. **Traefik existente**: Utiliza o Traefik já em execução no servidor, sem necessidade de iniciar uma nova instância
3. **Certificados SSL**: Aproveita o resolvedor de certificados Let's Encrypt já configurado
4. **Compatibilidade com Swarm**: Configurado para funcionar com Docker Swarm, que já está em uso no servidor

## Verificando a Instalação

Após iniciar os contêineres, você pode acessar:

- Frontend: https://site.mibitech.com.br/
- Backend API: https://site.mibitech.com.br/api/
- Admin do Django: https://site.mibitech.com.br/admin/

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
netstat -ano | findstr :80
netstat -ano | findstr :443

# Linux/Mac
lsof -i :80
lsof -i :443
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
```

## Integração com Docker Swarm

Esta configuração está preparada para ser implantada em um ambiente Docker Swarm:

1. **Configuração de deploy**: Inclui configurações específicas para o Swarm, como `replicas` e `constraints`
2. **Redes externas**: Utiliza a rede `network_public` existente no Swarm
3. **Compatibilidade com stack**: Pode ser implantado usando o comando `docker stack deploy`

### Implantação no Swarm

Para implantar no ambiente Swarm:

```bash
# Verificar se o Swarm está ativo
docker node ls

# Implantar o stack
docker stack deploy -c docker-compose.yml mibitech
```

### Verificando o Status no Swarm

Para verificar o status dos serviços no Swarm:

```bash
# Listar todos os serviços
docker service ls

# Ver logs de um serviço específico
docker service logs mibitech_frontend
docker service logs mibitech_backend

# Escalar um serviço
docker service scale mibitech_frontend=2
```

## Conclusão

Seguindo estes passos, você conseguirá executar o projeto site_mibitech integrado à infraestrutura Traefik existente no servidor, compartilhando recursos com outros sites WordPress e aproveitando a configuração de SSL já existente.

## Sobre o Traefik

O Traefik é um proxy reverso e balanceador de carga moderno que facilita a implantação de microsserviços. Algumas vantagens do Traefik:

1. **Descoberta de serviço automática**: O Traefik detecta automaticamente seus serviços e cria as rotas apropriadas.
2. **Suporte a SSL/TLS**: Facilita a configuração de HTTPS com Let's Encrypt.
3. **Dashboard web**: Interface visual para monitorar seus serviços.
4. **Configuração dinâmica**: Não é necessário reiniciar para aplicar alterações de configuração.

Para mais informações, consulte a [documentação oficial do Traefik](https://doc.traefik.io/).