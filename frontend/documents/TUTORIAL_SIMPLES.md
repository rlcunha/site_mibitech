# Tutorial Simples: MibiTech

Este é um guia simplificado para configurar e executar o projeto MibiTech localmente.

## Estrutura do Projeto

O projeto MibiTech é dividido em duas partes principais:

1. **Backend (Django)**: API REST que fornece dados para o frontend
2. **Frontend (JavaScript)**: Interface do usuário que consome a API

## Configuração Rápida

### Pré-requisitos

- Python 3.9+
- Node.js 18+
- Git
- Docker e Docker Compose (opcional)

### Usando Scripts de Configuração

Para facilitar a configuração, use os scripts fornecidos:

**No Windows:**
```
local_dev_setup.bat
```

**No Linux/Mac:**
```
chmod +x local_dev_setup.sh
./local_dev_setup.sh
```

### Configuração Manual

Se preferir configurar manualmente:

#### Backend (Django)

1. Navegue até a pasta do backend:
   ```
   cd backend
   ```

2. Crie um ambiente virtual Python:
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Execute as migrações do banco de dados:
   ```
   python manage.py migrate
   ```

5. Inicie o servidor:
   ```
   python manage.py runserver
   ```

O backend estará disponível em: http://localhost:8000/api/

#### Frontend (JavaScript)

1. Navegue até a pasta do frontend:
   ```
   cd frontend
   ```

2. Instale as dependências:
   ```
   npm install
   ```

3. Inicie o servidor:
   ```
   node server.js
   ```

O frontend estará disponível em: http://localhost:3000

## Usando Docker

Se preferir usar Docker:

1. Construa e inicie os contêineres:
   ```
   # Windows
   deploy.bat --build --up

   # Linux/Mac
   ./deploy.sh --build --up
   ```

2. Acesse a aplicação:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/

## Páginas Disponíveis

- **Home**: http://localhost:3000/
- **Sobre**: http://localhost:3000/sobre.html
- **Portfólio**: http://localhost:3000/portfolio.html
- **Blog**: http://localhost:3000/blog.html
- **Contato**: http://localhost:3000/contato.html

## Desenvolvimento

### Fluxo de Trabalho Básico

1. Faça alterações no código
2. Teste localmente
3. Commit e push para o GitHub (veja `criar_repositorio_github.md`)
4. Deploy para o servidor (veja `VPS_DEPLOYMENT.md`)

### Comandos Úteis

**Reiniciar serviços Docker:**
```
# Windows
deploy.bat --restart

# Linux/Mac
./deploy.sh --restart
```

**Ver logs:**
```
# Windows
deploy.bat --logs

# Linux/Mac
./deploy.sh --logs
```

## Solução de Problemas

### Problemas Comuns

1. **Portas já em uso**:
   - Verifique se outro processo está usando as portas 3000 ou 8000
   - Encerre o processo ou altere as portas nos arquivos de configuração

2. **Erro de conexão com a API**:
   - Verifique se o backend está rodando
   - Verifique se as URLs da API estão corretas

3. **Erros de dependência**:
   - Atualize as dependências:
     ```
     # Backend
     pip install -r requirements.txt

     # Frontend
     npm install
     ```

## Documentação Adicional

Para informações mais detalhadas, consulte:

- `README.md`: Visão geral do projeto
- `LOCAL_DEVELOPMENT.md`: Guia detalhado de desenvolvimento local
- `VPS_DEPLOYMENT.md`: Instruções para deploy em servidor VPS
- `criar_repositorio_github.md`: Como configurar o repositório no GitHub

## Suporte

Se encontrar problemas não cobertos neste guia, consulte a documentação completa ou abra uma issue no repositório do GitHub.