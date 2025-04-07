@echo off
REM Script para executar o docker-compose com o arquivo simplificado

echo ===================================================
echo INICIANDO DOCKER COMPOSE SIMPLIFICADO
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

REM Para e remove os contêineres existentes
echo [INFO] Parando contêineres existentes...
docker-compose -f docker-compose.simple.yml down

REM Executa o docker-compose
echo [INFO] Iniciando os contêineres...
docker-compose -f docker-compose.simple.yml up -d

if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Falha ao iniciar os contêineres Docker.
    exit /b 1
)

echo [INFO] Contêineres iniciados com sucesso!
echo.
echo [INFO] Serviço disponível:
echo  - API Backend: http://localhost:8000
echo  - API Docs: http://localhost:8000/api/docs
echo.

echo [INFO] Aguardando serviço inicializar...
timeout /t 10 /nobreak >nul

echo [INFO] Verificando status dos contêineres:
docker-compose -f docker-compose.simple.yml ps

echo.
echo ===================================================
echo DOCKER COMPOSE INICIADO COM SUCESSO!
echo ===================================================
echo.
echo Para visualizar logs: docker-compose -f docker-compose.simple.yml logs -f
echo Para parar os contêineres: docker-compose -f docker-compose.simple.yml down
echo.