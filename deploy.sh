#!/bin/bash

# MibiTech Deployment Script
# This script helps deploy the MibiTech application using Docker

# Exit on error
set -e

# Check if Docker Compose is installed
check_docker_compose() {
    # Check for docker-compose command (older versions)
    if command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE="docker-compose"
        return 0
    fi
    
    # Check for docker compose command (newer versions)
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE="docker compose"
        return 0
    fi
    
    echo "Error: Docker Compose not found."
    echo "Please install Docker Compose using one of the following methods:"
    echo ""
    echo "For Ubuntu/Debian:"
    echo "  sudo apt update"
    echo "  sudo apt install docker-compose-plugin"
    echo ""
    echo "For newer Docker versions:"
    echo "  The compose plugin should be included with Docker Desktop or Docker Engine."
    echo ""
    echo "For manual installation:"
    echo "  sudo curl -L \"https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose"
    echo "  sudo chmod +x /usr/local/bin/docker-compose"
    echo ""
    return 1
}

# Display help message
show_help() {
    echo "MibiTech Deployment Script"
    echo "Usage: ./deploy.sh [OPTION]"
    echo "Options:"
    echo "  -h, --help       Display this help message"
    echo "  -b, --build      Build all Docker images"
    echo "  -u, --up         Start all containers"
    echo "  -d, --down       Stop all containers"
    echo "  -r, --restart    Restart all containers"
    echo "  -l, --logs       View logs from all containers"
    echo "  --frontend       Only affect frontend container"
    echo "  --backend        Only affect backend container"
    echo "  --traefik        Only affect traefik container"
    echo "  --nginx          Only affect nginx container (deprecated)"
}

# Build Docker images
build_images() {
    # Check if Docker Compose is installed
    check_docker_compose || return 1
    
    echo "Building Docker images..."
    if [ "$1" == "frontend" ]; then
        $DOCKER_COMPOSE build frontend
    elif [ "$1" == "backend" ]; then
        $DOCKER_COMPOSE build backend
    elif [ "$1" == "traefik" ]; then
        $DOCKER_COMPOSE build traefik
    elif [ "$1" == "nginx" ]; then
        echo "Warning: Nginx is deprecated, using Traefik instead"
        $DOCKER_COMPOSE build nginx
    else
        docker-compose build
    fi
    echo "Build completed."
}

# Start containers
start_containers() {
    # Check if Docker Compose is installed
    check_docker_compose || return 1
    
    echo "Starting containers..."
    if [ "$1" == "frontend" ]; then
        $DOCKER_COMPOSE up -d frontend
    elif [ "$1" == "backend" ]; then
        $DOCKER_COMPOSE up -d backend
    elif [ "$1" == "traefik" ]; then
        $DOCKER_COMPOSE up -d traefik
    elif [ "$1" == "nginx" ]; then
        echo "Warning: Nginx is deprecated, using Traefik instead"
        $DOCKER_COMPOSE up -d nginx
    else
        docker-compose up -d
    fi
    echo "Containers started."
}

# Stop containers
stop_containers() {
    # Check if Docker Compose is installed
    check_docker_compose || return 1
    
    echo "Stopping containers..."
    if [ "$1" == "frontend" ]; then
        $DOCKER_COMPOSE stop frontend
        $DOCKER_COMPOSE rm -f frontend
    elif [ "$1" == "backend" ]; then
        $DOCKER_COMPOSE stop backend
        $DOCKER_COMPOSE rm -f backend
    elif [ "$1" == "traefik" ]; then
        $DOCKER_COMPOSE stop traefik
        $DOCKER_COMPOSE rm -f traefik
    elif [ "$1" == "nginx" ]; then
        echo "Warning: Nginx is deprecated, using Traefik instead"
        $DOCKER_COMPOSE stop nginx
        $DOCKER_COMPOSE rm -f nginx
    else
        docker-compose down
    fi
    echo "Containers stopped."
}

# Restart containers
restart_containers() {
    # Check if Docker Compose is installed
    check_docker_compose || return 1
    
    echo "Restarting containers..."
    if [ "$1" == "frontend" ]; then
        $DOCKER_COMPOSE restart frontend
    elif [ "$1" == "backend" ]; then
        $DOCKER_COMPOSE restart backend
    elif [ "$1" == "traefik" ]; then
        $DOCKER_COMPOSE restart traefik
    elif [ "$1" == "nginx" ]; then
        echo "Warning: Nginx is deprecated, using Traefik instead"
        $DOCKER_COMPOSE restart nginx
    else
        docker-compose restart
    fi
    echo "Containers restarted."
}

# View logs
view_logs() {
    # Check if Docker Compose is installed
    check_docker_compose || return 1
    
    echo "Viewing logs..."
    if [ "$1" == "frontend" ]; then
        $DOCKER_COMPOSE logs -f frontend
    elif [ "$1" == "backend" ]; then
        $DOCKER_COMPOSE logs -f backend
    elif [ "$1" == "traefik" ]; then
        $DOCKER_COMPOSE logs -f traefik
    elif [ "$1" == "nginx" ]; then
        echo "Warning: Nginx is deprecated, using Traefik instead"
        $DOCKER_COMPOSE logs -f nginx
    else
        docker-compose logs -f
    fi
}

# Parse command line arguments
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

SERVICE=""

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -b|--build)
            build_images "$SERVICE"
            ;;
        -u|--up)
            start_containers "$SERVICE"
            ;;
        -d|--down)
            stop_containers "$SERVICE"
            ;;
        -r|--restart)
            restart_containers "$SERVICE"
            ;;
        -l|--logs)
            view_logs "$SERVICE"
            ;;
        --frontend)
            SERVICE="frontend"
            ;;
        --backend)
            SERVICE="backend"
            ;;
        --traefik)
            SERVICE="traefik"
            ;;
        --nginx)
            echo "Warning: Nginx is deprecated, using Traefik instead"
            SERVICE="nginx"
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
    shift
done

exit 0