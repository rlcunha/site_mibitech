@echo off
REM Script para iniciar o ambiente Docker do backend MibiTech
REM Este script inicia os contêineres Docker e testa a API

echo ===================================================
echo INICIANDO AMBIENTE DOCKER PARA BACKEND MIBITECH
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

echo [INFO] Verificando se há contêineres antigos...
docker-compose down 2>nul

echo [INFO] Construindo e iniciando os contêineres...
docker-compose up -d --build

if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Falha ao iniciar os contêineres Docker.
    exit /b 1
)

echo [INFO] Contêineres iniciados com sucesso!
echo.
echo [INFO] Serviços disponíveis:
echo  - API Backend: http://localhost:8000
echo  - API Docs: http://localhost:8000/api/docs
echo  - PgAdmin: http://localhost:5050
echo.

echo [INFO] Aguardando serviços inicializarem...
timeout /t 10 /nobreak >nul

echo [INFO] Verificando status dos contêineres:
docker-compose ps

echo.
echo [INFO] Testando a API...
echo.

REM Verifica se o Python está instalado
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [AVISO] Python não encontrado. Pulando teste automatizado.
    echo [INFO] Você pode testar manualmente acessando http://localhost:8000/api/status
) else (
    REM Instala o requests se necessário
    pip show requests >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo [INFO] Instalando pacote requests...
        pip install requests
    )
    
    REM Executa o script de teste
    python test_api.py
)

echo.
echo ===================================================
echo AMBIENTE DOCKER INICIADO COM SUCESSO!
echo ===================================================
echo.
echo Para visualizar logs: docker-compose logs -f
echo Para parar os serviços: docker-compose down
echo.