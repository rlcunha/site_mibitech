@echo off
REM Script para construir a imagem Docker para o backend

echo ===================================================
echo CONSTRUINDO IMAGEM DOCKER PARA BACKEND MIBITECH
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

REM Constrói a imagem Docker
echo [INFO] Construindo a imagem Docker...
docker build -t mibitech-backend:latest -f Dockerfile .

if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Falha ao construir a imagem Docker.
    exit /b 1
)

echo [INFO] Imagem Docker construída com sucesso!
echo.
echo [INFO] Detalhes da imagem:
docker images | findstr mibitech-backend

echo.
echo ===================================================
echo IMAGEM DOCKER CONSTRUÍDA COM SUCESSO!
echo ===================================================
echo.
echo Para executar a imagem: docker run -p 8000:8000 mibitech-backend:latest
echo.