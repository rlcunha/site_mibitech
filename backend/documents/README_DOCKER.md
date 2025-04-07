# Docker Compose para Backend MibiTech

Este documento explica como utilizar o Docker Compose para executar o módulo de backend da MibiTech.

## Serviço Configurado

O arquivo `docker-compose.yml` configura o seguinte serviço:

**api**: Serviço principal do backend que roda a aplicação FastAPI
- Expõe a API REST na porta 8000
- Conecta-se ao banco de dados PostgreSQL existente
- Usa um Dockerfile modificado para construir a imagem

## Arquivos Modificados

Para garantir o funcionamento correto do serviço sem depender de um banco de dados PostgreSQL local, foram criados os seguintes arquivos:

1. **start_modified.sh**: Versão modificada do script de inicialização que não espera por um serviço PostgreSQL local
2. **Dockerfile.modified**: Versão modificada do Dockerfile que usa o script start_modified.sh

## Pré-requisitos

- Docker instalado (versão 19.03.0+)
- Docker Compose instalado (versão 1.27.0+)
- Servidor PostgreSQL já configurado e acessível em server.mibitech.com.br

## Como Executar

1. Navegue até o diretório do backend:
   ```bash
   cd backend
   ```

2. Inicie o serviço com Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Verifique se o serviço está rodando:
   ```bash
   docker-compose ps
   ```

4. Acesse a API:
   - Documentação: http://localhost:8000/api/docs
   - Status: http://localhost:8000/api/status
   - Endpoint principal: http://localhost:8000/

## Logs e Monitoramento

Para visualizar os logs do serviço de backend:
```bash
docker-compose logs -f api
```

## Parando o Serviço

Para parar o serviço:
```bash
docker-compose down
```

## Variáveis de Ambiente

As principais variáveis de ambiente configuradas são:

- `DATABASE_URL`: URL de conexão com o banco de dados PostgreSQL existente
- `APP_HOST`: Host onde a aplicação será executada (0.0.0.0 para acessar de qualquer lugar)
- `APP_PORT`: Porta onde a aplicação será executada (8000)
- `ENVIRONMENT`: Ambiente de execução (development, production, etc.)
- `CORS_ORIGINS`: Origens permitidas para CORS (Cross-Origin Resource Sharing)

## Conexão com o Banco de Dados

O serviço se conecta a um servidor PostgreSQL existente. A conexão é configurada através da variável de ambiente `DATABASE_URL` no formato:

```
postgresql://postgres:Mfcd62!!@server.mibitech.com.br:5432/mibitech
```

Onde:
- `postgres`: usuário do banco de dados
- `Mfcd62!!`: senha do banco de dados
- `server.mibitech.com.br`: hostname do servidor PostgreSQL
- `5432`: porta do servidor PostgreSQL
- `mibitech`: nome do banco de dados

## Dockerfile Modificado

O serviço utiliza um Dockerfile modificado (`Dockerfile.modified`) para construir a imagem. As principais modificações são:

1. Usa o script `start_modified.sh` em vez do script `start.sh` original
2. O script modificado não espera por um serviço PostgreSQL local, permitindo a conexão direta com o banco de dados externo

## Resolução de Problemas

1. **API não inicia**: Verifique os logs com `docker-compose logs api`
2. **Erro de conexão com o banco**: Verifique se o servidor PostgreSQL está acessível em server.mibitech.com.br
3. **Erro de migração**: Verifique os logs do serviço API durante a inicialização

## Segurança

Para ambientes de produção, recomenda-se:

1. Alterar todas as senhas padrão
2. Restringir as origens CORS
3. Configurar HTTPS
4. Limitar o acesso às portas expostas