#!/bin/bash

# MibiTech Local Development Setup Script for Linux/Mac
# This script helps set up the local development environment

# Exit on error
set -e

echo "MibiTech Local Development Setup"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed or not in PATH."
    echo "Please install Python 3.9 or later from https://www.python.org/downloads/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed or not in PATH."
    echo "Please install Node.js 18 or later from https://nodejs.org/"
    exit 1
fi

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed or not in PATH."
    echo "Please install Git from https://git-scm.com/downloads"
    exit 1
fi

echo "All required tools are installed."

# Setup Backend
echo "Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Apply migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if needed
echo "Do you want to create a superuser? (y/n)"
read -r create_superuser
if [[ "$create_superuser" =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Deactivate virtual environment
deactivate

# Return to root directory
cd ..

# Setup Frontend
echo "Setting up frontend..."
cd frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Return to root directory
cd ..

echo "Setup complete!"
echo ""
echo "To start the backend server:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "To start the frontend server:"
echo "  cd frontend"
echo "  node server.js"
echo ""
echo "Or use Docker Compose:"
echo "  ./deploy.sh --build --up"
echo ""
echo "For more information, see LOCAL_DEVELOPMENT.md"