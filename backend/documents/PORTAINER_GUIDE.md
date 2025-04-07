# Guia de Implantação com Portainer

Este documento explica como implantar o backend da MibiTech usando o Portainer.

## Construindo a Imagem Docker

Antes de implantar o backend com o Portainer, você precisa construir a imagem Docker:

### Windows
```bash
build_image.bat
```

### Linux/macOS
```bash
chmod +x build_image.sh
./build_image.sh
```

Alternativamente, você pode construir a imagem manualmente:
```bash
docker build -t mibitech-backend:latest -f Dockerfile .
```

## O que é Portainer?

Portainer é uma interface web para gerenciar contêineres Docker. Ele permite que você gerencie contêineres, imagens, redes e volumes sem precisar usar a linha de comando.

## Arquivos de Configuração

Dois arquivos de configuração estão disponíveis para uso com o Portainer:

1. **docker-compose.yml**: Configuração básica para uso com o Portainer
2. **portainer-stack.yml**: Configuração específica para o Portainer com a opção restart: always

## Como Implantar usando o Portainer

### Método 1: Usando o Editor de Stack do Portainer

1. Acesse a interface web do Portainer
2. Navegue até "Stacks" no menu lateral
3. Clique em "Add stack"
4. Dê um nome para o stack (ex: "mibitech-backend")
5. Na seção "Web editor", cole o conteúdo do arquivo `docker-compose.yml` ou `portainer-stack.yml`
6. Clique em "Deploy the stack"

### Método 2: Fazendo Upload do Arquivo

1. Acesse a interface web do Portainer
2. Navegue até "Stacks" no menu lateral
3. Clique em "Add stack"
4. Dê um nome para o stack (ex: "mibitech-backend")
5. Na seção "Upload", selecione o arquivo `docker-compose.yml` ou `portainer-stack.yml`
6. Clique em "Deploy the stack"

## Verificando a Implantação

Após a implantação, você pode verificar se o serviço está funcionando acessando:

- API Backend: http://seu-servidor:8000
- Documentação da API: http://seu-servidor:8000/api/docs

## Solução de Problemas

Se o contêiner não iniciar corretamente, você pode verificar os logs no Portainer:

1. Navegue até "Containers" no menu lateral
2. Encontre o contêiner do backend na lista
3. Clique no ícone de logs (ícone de documento) para ver os logs do contêiner

## Variáveis de Ambiente

As variáveis de ambiente configuradas são:

- `DATABASE_URL`: URL de conexão com o banco de dados PostgreSQL existente
- `APP_HOST`: Host onde a aplicação será executada (0.0.0.0 para acessar de qualquer lugar)
- `APP_PORT`: Porta onde a aplicação será executada (8000)
- `ENVIRONMENT`: Ambiente de execução (development, production, etc.)
- `CORS_ORIGINS`: Origens permitidas para CORS (Cross-Origin Resource Sharing)