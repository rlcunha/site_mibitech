# MibiTech Backend API

Este é o backend da API para o website da MibiTech, construído com FastAPI e PostgreSQL.

## Funcionalidades

- Endpoints RESTful API
- Integração com banco de dados PostgreSQL
- Containerização com Docker
- Endpoint de mídias sociais (/api/social-media/)
- Webhooks para integrações (/api/webhooks/)

## Configuração Rápida com Docker

A maneira mais fácil de iniciar o backend é usando Docker Compose:

### Windows
```bash
start_docker_env.bat
```

### Linux/macOS
```bash
chmod +x start_docker_env.sh
./start_docker_env.sh
```

Estes scripts irão:
1. Iniciar todos os contêineres necessários
2. Verificar se os serviços estão funcionando
3. Executar testes básicos na API

Para mais detalhes sobre a configuração Docker, consulte [README_DOCKER.md](README_DOCKER.md).

## Configuração Manual

1. Copie .env.example para .env e configure:
   ```bash
   cp .env.example .env
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute com Docker:
   ```bash
   docker-compose up --build
   ```

4. Ou execute localmente:
   ```bash
   python init_db.py
   uvicorn app.main:app --reload
   ```

## Testando a API

Após iniciar o servidor, você pode testar a API usando o script de teste:

```bash
python test_api.py
```

Este script verifica se os principais endpoints estão funcionando corretamente.

## Documentação da API

Após iniciar o servidor, acesse a documentação da API em:
- Swagger UI: http://localhost:8000/api/docs
- Redoc: http://localhost:8000/api/redoc
- Status: http://localhost:8000/api/status

## Implantação

1. Construa a imagem Docker:
   ```bash
   docker-compose build
   ```

2. Inicie os serviços:
   ```bash
   docker-compose up -d
   ```

## Banco de Dados

A API usa PostgreSQL com as seguintes credenciais padrão:
- Banco de dados: mibitech
- Usuário: postgres
- Senha: Mfcd62!!

Os dados iniciais de mídias sociais são automaticamente inseridos na primeira execução.

## Migrações de Banco de Dados

Este projeto usa Alembic para migrações de banco de dados.

### Configuração Inicial
1. Instale o Alembic:
```bash
pip install alembic
```

2. Inicialize as migrações (já feito):
```bash
alembic init alembic
```

### Uso

Crie uma nova migração:
```bash
alembic revision --autogenerate -m "descrição das alterações"
```

Execute as migrações:
```bash
alembic upgrade head
```

Reverta migrações:
```bash
alembic downgrade -1
```

### Comandos de Migração
- `alembic current` - Mostra a revisão atual
- `alembic history` - Mostra o histórico de migrações
- `alembic upgrade head` - Aplica todas as migrações pendentes
- `alembic downgrade base` - Reverte todas as migrações

## Estrutura do Projeto

```
backend/
├── alembic/              # Configurações e migrações do Alembic
├── app/                  # Código principal da aplicação
│   ├── errors/           # Manipuladores de erro
│   ├── helpers/          # Funções auxiliares
│   ├── models/           # Modelos SQLAlchemy
│   ├── routes/           # Rotas da API
│   ├── schemas/          # Esquemas Pydantic
│   ├── services/         # Serviços e lógica de negócios
│   └── main.py           # Ponto de entrada da aplicação
├── tests/                # Testes automatizados
├── .env                  # Variáveis de ambiente (local)
├── .env.example          # Exemplo de variáveis de ambiente
├── alembic.ini           # Configuração do Alembic
├── docker-compose.yml    # Configuração do Docker Compose
├── Dockerfile            # Instruções para construir a imagem Docker
├── init_db.py            # Script de inicialização do banco de dados
├── README.md             # Este arquivo
├── README_DOCKER.md      # Documentação específica do Docker
├── requirements.txt      # Dependências do projeto
├── start_docker_env.bat  # Script para iniciar ambiente Docker (Windows)
├── start_docker_env.sh   # Script para iniciar ambiente Docker (Linux/macOS)
├── start.sh              # Script de inicialização para contêiner Docker
└── test_api.py           # Script para testar a API