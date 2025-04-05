@echo off
REM Script para executar o contêiner Docker diretamente

echo ===================================================
echo INICIANDO CONTÊINER DOCKER PARA BACKEND MIBITECH
echo ===================================================

REM Verifica se o Docker está instalado
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Docker não encontrado. Por favor, instale o Docker Desktop.
    exit /b 1
)

REM Verifica se o Docker está rodando
docker info >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Docker não está rodando. Por favor, inicie o Docker Desktop.
    exit /b 1
)

REM Para e remove o contêiner se já existir
echo [INFO] Removendo contêiner existente (se houver)...
docker stop mibitech_backend_api 2>nul
docker rm mibitech_backend_api 2>nul

REM Executa o contêiner
echo [INFO] Iniciando o contêiner...
docker run -d --name mibitech_backend_api ^
  -p 8000:8000 ^
  -e DATABASE_URL=postgresql://postgres:Mfcd62!!@server.mibitech.com.br:5432/mibitech ^
  -e APP_HOST=0.0.0.0 ^
  -e APP_PORT=8000 ^
  -e ENVIRONMENT=development ^
  -e CORS_ORIGINS=* ^
  -v %cd%:/app ^
  -w /app ^
  --restart always ^
  python:3.9-slim ^
  bash -c "pip install -r requirements.txt && python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"

if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Falha ao iniciar o contêiner Docker.
    exit /b 1
)

echo [INFO] Contêiner iniciado com sucesso!
echo.
echo [INFO] Serviço disponível:
echo  - API Backend: http://localhost:8000
echo  - API Docs: http://localhost:8000/api/docs
echo.

echo [INFO] Aguardando serviço inicializar...
timeout /t 10 /nobreak >nul

echo [INFO] Verificando status do contêiner:
docker ps -a | findstr mibitech_backend_api

echo.
echo ===================================================
echo CONTÊINER DOCKER INICIADO COM SUCESSO!
echo ===================================================
echo.
echo Para visualizar logs: docker logs -f mibitech_backend_api
echo Para parar o contêiner: docker stop mibitech_backend_api
echo.