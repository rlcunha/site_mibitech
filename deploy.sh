#!/bin/bash

# MibiTech Deployment Script
# This script helps deploy the MibiTech application using Docker

# Exit on error
set -e

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
    echo "  --nginx          Only affect nginx container"
}

# Build Docker images
build_images() {
    echo "Building Docker images..."
    if [ "$1" == "frontend" ]; then
        docker-compose build frontend
    elif [ "$1" == "backend" ]; then
        docker-compose build backend
    elif [ "$1" == "nginx" ]; then
        docker-compose build nginx
    else
        docker-compose build
    fi
    echo "Build completed."
}

# Start containers
start_containers() {
    echo "Starting containers..."
    if [ "$1" == "frontend" ]; then
        docker-compose up -d frontend
    elif [ "$1" == "backend" ]; then
        docker-compose up -d backend
    elif [ "$1" == "nginx" ]; then
        docker-compose up -d nginx
    else
        docker-compose up -d
    fi
    echo "Containers started."
}

# Stop containers
stop_containers() {
    echo "Stopping containers..."
    if [ "$1" == "frontend" ]; then
        docker-compose stop frontend
        docker-compose rm -f frontend
    elif [ "$1" == "backend" ]; then
        docker-compose stop backend
        docker-compose rm -f backend
    elif [ "$1" == "nginx" ]; then
        docker-compose stop nginx
        docker-compose rm -f nginx
    else
        docker-compose down
    fi
    echo "Containers stopped."
}

# Restart containers
restart_containers() {
    echo "Restarting containers..."
    if [ "$1" == "frontend" ]; then
        docker-compose restart frontend
    elif [ "$1" == "backend" ]; then
        docker-compose restart backend
    elif [ "$1" == "nginx" ]; then
        docker-compose restart nginx
    else
        docker-compose restart
    fi
    echo "Containers restarted."
}

# View logs
view_logs() {
    echo "Viewing logs..."
    if [ "$1" == "frontend" ]; then
        docker-compose logs -f frontend
    elif [ "$1" == "backend" ]; then
        docker-compose logs -f backend
    elif [ "$1" == "nginx" ]; then
        docker-compose logs -f nginx
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
        --nginx)
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