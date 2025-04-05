# Docker Compose para Backend MibiTech

Este documento explica como utilizar o Docker Compose para executar o módulo de backend da MibiTech.

## Serviços Configurados

O arquivo `docker-compose.yml` configura os seguintes serviços:

1. **api**: Serviço principal do backend que roda a aplicação FastAPI
   - Expõe a API REST na porta 8000
   - Conecta-se automaticamente ao banco de dados PostgreSQL

2. **postgres**: Banco de dados PostgreSQL
   - Armazena todos os dados da aplicação
   - Expõe a porta 5432 para conexões

3. **pgadmin**: Interface web para administração do PostgreSQL (opcional)
   - Acessível na porta 5050
   - Útil para gerenciar o banco de dados visualmente

## Pré-requisitos

- Docker instalado (versão 19.03.0+)
- Docker Compose instalado (versão 1.27.0+)

## Como Executar

1. Navegue até o diretório do backend:
   ```bash
   cd backend
   ```

2. Inicie os serviços com Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Verifique se os serviços estão rodando:
   ```bash
   docker-compose ps
   ```

4. Acesse a API:
   - Documentação: http://localhost:8000/api/docs
   - Status: http://localhost:8000/api/status
   - Endpoint principal: http://localhost:8000/

5. Acesse o PgAdmin (opcional):
   - URL: http://localhost:5050
   - Email: admin@mibitech.com.br
   - Senha: Mfcd62!!

## Logs e Monitoramento

Para visualizar os logs do serviço de backend:
```bash
docker-compose logs -f api
```

Para visualizar os logs do banco de dados:
```bash
docker-compose logs -f postgres
```

## Parando os Serviços

Para parar todos os serviços:
```bash
docker-compose down
```

Para parar e remover volumes (isso apagará os dados do banco):
```bash
docker-compose down -v
```

## Reconstruindo a Imagem

Se você fizer alterações no código ou no Dockerfile, reconstrua a imagem:
```bash
docker-compose build
```

Ou para reconstruir e iniciar:
```bash
docker-compose up -d --build
```

## Variáveis de Ambiente

As principais variáveis de ambiente configuradas são:

- `DATABASE_URL`: URL de conexão com o banco de dados
- `APP_HOST`: Host onde a aplicação será executada (0.0.0.0 para acessar de qualquer lugar)
- `APP_PORT`: Porta onde a aplicação será executada (8000)
- `ENVIRONMENT`: Ambiente de execução (development, production, etc.)
- `CORS_ORIGINS`: Origens permitidas para CORS (Cross-Origin Resource Sharing)

## Volumes e Persistência

O serviço PostgreSQL utiliza um volume Docker nomeado (`mibitech_postgres_data`) para persistir os dados do banco entre reinicializações dos contêineres.

## Redes

Os serviços estão configurados para usar uma rede Docker dedicada (`mibitech_backend_network`), garantindo isolamento e comunicação segura entre os contêineres.

## Resolução de Problemas

1. **API não inicia**: Verifique os logs com `docker-compose logs api`
2. **Erro de conexão com o banco**: Verifique se o PostgreSQL está rodando com `docker-compose ps`
3. **Erro de migração**: Verifique os logs do serviço API durante a inicialização

## Segurança

Para ambientes de produção, recomenda-se:

1. Alterar todas as senhas padrão
2. Restringir as origens CORS
3. Configurar HTTPS
4. Limitar o acesso às portas expostas