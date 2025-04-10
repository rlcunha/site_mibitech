#!/bin/bash

# Não espera pelo serviço postgres, pois estamos usando um banco de dados externo
echo "Conectando ao banco de dados externo..."
# Initialize database
python init_db.py

echo "Iniciando servidor FASTAPI..."
# Start FastAPI server
uvicorn app.main:app --host $APP_HOST --port $APP_PORT --reload