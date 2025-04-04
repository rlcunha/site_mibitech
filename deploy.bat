@echo off
REM MibiTech Deployment Script for Windows
REM This script helps deploy the MibiTech application using Docker

setlocal enabledelayedexpansion

REM Display help message
:show_help
if "%~1"=="" (
    echo MibiTech Deployment Script for Windows
    echo Usage: deploy.bat [OPTION]
    echo Options:
    echo   -h, --help       Display this help message
    echo   -b, --build      Build all Docker images
    echo   -u, --up         Start all containers
    echo   -d, --down       Stop all containers
    echo   -r, --restart    Restart all containers
    echo   -l, --logs       View logs from all containers
    echo   --frontend       Only affect frontend container
    echo   --backend        Only affect backend container
    echo   --nginx          Only affect nginx container
    exit /b 0
)

REM Initialize variables
set SERVICE=

REM Parse command line arguments
:parse_args
if "%~1"=="" goto :end_parse_args

if "%~1"=="-h" goto :show_help
if "%~1"=="--help" goto :show_help

if "%~1"=="--frontend" (
    set SERVICE=frontend
    shift
    goto :parse_args
)
if "%~1"=="--backend" (
    set SERVICE=backend
    shift
    goto :parse_args
)
if "%~1"=="--nginx" (
    set SERVICE=nginx
    shift
    goto :parse_args
)

if "%~1"=="-b" (
    call :build_images %SERVICE%
    shift
    goto :parse_args
)
if "%~1"=="--build" (
    call :build_images %SERVICE%
    shift
    goto :parse_args
)

if "%~1"=="-u" (
    call :start_containers %SERVICE%
    shift
    goto :parse_args
)
if "%~1"=="--up" (
    call :start_containers %SERVICE%
    shift
    goto :parse_args
)

if "%~1"=="-d" (
    call :stop_containers %SERVICE%
    shift
    goto :parse_args
)
if "%~1"=="--down" (
    call :stop_containers %SERVICE%
    shift
    goto :parse_args
)

if "%~1"=="-r" (
    call :restart_containers %SERVICE%
    shift
    goto :parse_args
)
if "%~1"=="--restart" (
    call :restart_containers %SERVICE%
    shift
    goto :parse_args
)

if "%~1"=="-l" (
    call :view_logs %SERVICE%
    shift
    goto :parse_args
)
if "%~1"=="--logs" (
    call :view_logs %SERVICE%
    shift
    goto :parse_args
)

echo Unknown option: %~1
call :show_help
exit /b 1

:end_parse_args
exit /b 0

REM Build Docker images
:build_images
echo Building Docker images...
if "%~1"=="frontend" (
    docker-compose build frontend
) else if "%~1"=="backend" (
    docker-compose build backend
) else if "%~1"=="nginx" (
    docker-compose build nginx
) else (
    docker-compose build
)
echo Build completed.
exit /b 0

REM Start containers
:start_containers
echo Starting containers...
if "%~1"=="frontend" (
    docker-compose up -d frontend
) else if "%~1"=="backend" (
    docker-compose up -d backend
) else if "%~1"=="nginx" (
    docker-compose up -d nginx
) else (
    docker-compose up -d
)
echo Containers started.
exit /b 0

REM Stop containers
:stop_containers
echo Stopping containers...
if "%~1"=="frontend" (
    docker-compose stop frontend
    docker-compose rm -f frontend
) else if "%~1"=="backend" (
    docker-compose stop backend
    docker-compose rm -f backend
) else if "%~1"=="nginx" (
    docker-compose stop nginx
    docker-compose rm -f nginx
) else (
    docker-compose down
)
echo Containers stopped.
exit /b 0

REM Restart containers
:restart_containers
echo Restarting containers...
if "%~1"=="frontend" (
    docker-compose restart frontend
) else if "%~1"=="backend" (
    docker-compose restart backend
) else if "%~1"=="nginx" (
    docker-compose restart nginx
) else (
    docker-compose restart
)
echo Containers restarted.
exit /b 0

REM View logs
:view_logs
echo Viewing logs...
if "%~1"=="frontend" (
    docker-compose logs -f frontend
) else if "%~1"=="backend" (
    docker-compose logs -f backend
) else if "%~1"=="nginx" (
    docker-compose logs -f nginx
) else (
    docker-compose logs -f
)
exit /b 0